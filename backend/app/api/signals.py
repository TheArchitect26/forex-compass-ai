from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel
from datetime import timedelta

from app.db import get_db
from app.models import Signal
from app.models import SignalOutcome, ReliabilityHistory, StrategyState, ExplainabilityAudit
from app.models import SignalScanContext
from app.config import settings
from app.config import has_real_market_provider, is_production_like, synthetic_buy_sell_blocked
from app.engines.adaptive import record_outcome
from app.engines.outcome_validation import validate_pending_outcomes
from app.utils_time import utc_now
from app.engines.reliability import classify_alignment, reliability_score
from app.engines.pipeline import run_signal_pipeline_for_pair, config_snapshot
from app.engines.strategy_profiles import profile_or_default
from app.engines.session import classify_session
from app.security import current_user

router = APIRouter()


@router.get("")
async def list_signals(db: AsyncSession = Depends(get_db), limit: int = 50):
    rows = (await db.execute(select(Signal).order_by(desc(Signal.created_at)).limit(limit))).scalars().all()
    outcomes = (await db.execute(select(SignalOutcome))).scalars().all()
    by_signal = {o.signal_id: o for o in outcomes}
    return [_serialize(s, by_signal.get(s.id)) for s in rows]


@router.get("/status")
async def status(db: AsyncSession = Depends(get_db)):
    real_provider_configured = has_real_market_provider()
    production_like = is_production_like()
    demo_only = not real_provider_configured
    data_mode = "twelve_data" if real_provider_configured else "synthetic_demo"
    live_data_ready = real_provider_configured
    execution_ready = False
    blocked_synthetic = synthetic_buy_sell_blocked() or (
        demo_only and not settings.ALLOW_SYNTHETIC_SIGNALS
    )

    stats = await _validation_stats(db)
    return {
        "scanner_ready": live_data_ready or (demo_only and not production_like),
        "live_data_ready": live_data_ready,
        "execution_ready": execution_ready,
        "demo_only": demo_only,
        "data_mode": data_mode,
        "market_data": {
            "mode": data_mode,
            "twelve_data_configured": real_provider_configured,
            "demo_only": demo_only,
        },
        "synthetic_buy_sell_blocked": blocked_synthetic,
        "auto_trade": False,
        "no_execution": True,
        "advisory_only": True,
        "pending_validation_count": stats["provider_backed"]["pending"],
        "recent_accuracy": stats["provider_backed"]["win_rate"],
        "validation": stats,
    }


@router.post("/scan")
async def scan(db: AsyncSession = Depends(get_db), _user: str = Depends(current_user)):
    """Run unified pipeline over all pairs."""
    found = []
    real_count = 0
    cached_count = 0
    synthetic_demo_count = 0
    unavailable_count = 0
    provider_failed_symbols = []
    for p in settings.PAIRS:
        sig = await run_signal_pipeline_for_pair(db, p, source="api_scan", report_unavailable=True)
        if sig:
            found.append(sig)
            if sig.get("provider_failed"):
                unavailable_count += 1
                provider_failed_symbols.append(p)
            elif sig.get("demo_only") or sig.get("data_mode") == "synthetic_demo" or sig.get("data_source") == "synthetic":
                synthetic_demo_count += 1
            elif sig.get("data_mode") == "cached" or sig.get("provider_name") == "cached_provider":
                cached_count += 1
            elif sig.get("data_source") == "real" or sig.get("provider_name") == "twelve_data":
                real_count += 1
    await db.commit()
    data_mode = _scan_data_mode(real_count, cached_count, synthetic_demo_count, unavailable_count)
    return {
        "found": len(found),
        "signals": found,
        "real_count": real_count,
        "cached_count": cached_count,
        "synthetic_demo_count": synthetic_demo_count,
        "unavailable_count": unavailable_count,
        "provider_failed_symbols": provider_failed_symbols,
        "data_mode": data_mode,
        "auto_trade": False,
        "no_execution": True,
        "advisory_only": True,
    }


@router.get("/scan")
async def scan_get(db: AsyncSession = Depends(get_db), _user: str = Depends(current_user)):
    return await scan(db, _user)


def _scan_data_mode(real_count: int, cached_count: int, synthetic_demo_count: int, unavailable_count: int) -> str:
    active = sum(1 for n in [real_count, cached_count, synthetic_demo_count, unavailable_count] if n > 0)
    if active > 1:
        return "mixed"
    if real_count:
        return "live"
    if cached_count:
        return "cached"
    if synthetic_demo_count:
        return "synthetic_demo"
    if unavailable_count:
        return "unavailable"
    return "unavailable"


@router.post("/validate-outcomes")
async def validate_outcomes(db: AsyncSession = Depends(get_db), _user: str = Depends(current_user)):
    return await validate_pending_outcomes(db)


@router.get("/performance")
async def performance(db: AsyncSession = Depends(get_db), include_synthetic: bool = False, pair: str = "", timeframe: str = "", risk_level: str = "", strength: str = ""):
    outcomes = (await db.execute(select(SignalOutcome))).scalars().all()
    signals = (await db.execute(select(Signal))).scalars().all()
    by_id = {s.id: s for s in signals}
    filtered = [o for o in outcomes if (include_synthetic or (by_id.get(o.signal_id) and by_id[o.signal_id].data_source != "synthetic"))]
    if pair: filtered = [o for o in filtered if o.pair == pair]
    if timeframe: filtered = [o for o in filtered if o.timeframe == timeframe]
    if risk_level: filtered = [o for o in filtered if by_id.get(o.signal_id) and by_id[o.signal_id].risk_level == risk_level]
    if strength: filtered = [o for o in filtered if by_id.get(o.signal_id) and by_id[o.signal_id].strength == strength]
    total = len(filtered)
    trade_outcomes = [o for o in filtered if o.direction in {"BUY", "SELL"} and o.outcome in {"win", "loss", "expired", "invalidated"}]
    wins = sum(1 for o in trade_outcomes if o.outcome == "win")
    def group(key_fn):
        out = {}
        for o in filtered:
            k = key_fn(o)
            out.setdefault(k, {"n": 0, "wins": 0, "pips": 0.0})
            out[k]["n"] += 1
            out[k]["wins"] += 1 if o.outcome == "win" else 0
            out[k]["pips"] += o.result_pips
        return out
    validation = await _validation_stats(db)
    return {
        "total_signals": total,
        "buy_sell_count": sum(1 for o in filtered if o.direction in {"BUY", "SELL"}),
        "hold_count": sum(1 for o in filtered if o.direction == "HOLD"),
        "pending_outcomes": sum(1 for o in filtered if o.outcome == "pending"),
        "win_rate_excl_hold": round((wins / len(trade_outcomes) * 100), 2) if trade_outcomes else 0,
        "average_result_pips": round(sum(o.net_result_pips for o in filtered) / total, 2) if total else 0,
        "average_gross_pips": round(sum(o.gross_result_pips for o in filtered) / total, 2) if total else 0,
        "average_cost_pips": round(sum(o.estimated_cost_pips for o in filtered) / total, 2) if total else 0,
        "average_confidence": round(sum((by_id.get(o.signal_id).confidence if by_id.get(o.signal_id) else 0) for o in filtered) / total, 2) if total else 0,
        "by_pair": group(lambda o: o.pair),
        "by_timeframe": group(lambda o: o.timeframe),
        "by_risk_level": group(lambda o: by_id.get(o.signal_id).risk_level if by_id.get(o.signal_id) else "unknown"),
        "by_strength": group(lambda o: by_id.get(o.signal_id).strength if by_id.get(o.signal_id) else "unknown"),
        "by_confidence_bucket": group(lambda o: "80-100" if (by_id.get(o.signal_id).confidence if by_id.get(o.signal_id) else 0) >= 80 else "60-79" if (by_id.get(o.signal_id).confidence if by_id.get(o.signal_id) else 0) >= 60 else "0-59"),
        "latest_validated": [
            {"signal_id": o.signal_id, "pair": o.pair, "direction": o.direction, "outcome": o.outcome, "result_pips": o.net_result_pips, "gross_result_pips": o.gross_result_pips, "estimated_cost_pips": o.estimated_cost_pips, "checked_at": o.checked_at.isoformat() if o.checked_at else None}
            for o in sorted(filtered, key=lambda x: x.created_at, reverse=True)[:20]
        ],
        "validation": validation,
    }


@router.get("/validation-stats")
async def validation_stats(db: AsyncSession = Depends(get_db)):
    return await _validation_stats(db)



@router.post("/replay/run")
async def replay_run(body: dict, db: AsyncSession = Depends(get_db)):
    pair = body.get("pair", "EUR/USD")
    timeframe = body.get("timeframe", "1h")
    profile = body.get("strategy_profile", "intraday")
    fixed_regime = body.get("fixed_regime")
    # deterministic-ish replay scaffold: run pipeline repeatedly over historical span count
    # For now uses current engine deterministic synthetic/live behavior with isolated metadata
    signals = []
    sig = await run_signal_pipeline_for_pair(db, pair, source="replay")
    if sig:
        if fixed_regime:
            sig.setdefault("reasoning", {}).setdefault("regime_details", {})["replay_fixed_regime"] = fixed_regime
        signals.append(sig)
    await db.commit()
    rel = await reliability(db)
    return {"generated_signals": signals, "outcomes": [], "reliability_snapshot": rel, "drift_warnings": rel.get("drift_warnings", []), "replay_metadata": {"pair": pair, "timeframe": timeframe, "strategy_profile": profile, "engine_version": "phase8-v1"}}


@router.get("/calibration")
async def calibration(db: AsyncSession = Depends(get_db)):
    outcomes = (await db.execute(select(SignalOutcome))).scalars().all()
    signals = (await db.execute(select(Signal))).scalars().all()
    by_id = {s.id: s for s in signals}
    buckets = [(0,40),(41,55),(56,70),(71,85),(86,100)]
    out=[]
    for a,b in buckets:
        rows=[o for o in outcomes if by_id.get(o.signal_id) and a <= by_id[o.signal_id].confidence <= b and by_id[o.signal_id].direction in {"BUY","SELL"} and by_id[o.signal_id].data_source!="synthetic"]
        n=len(rows); wins=sum(1 for r in rows if r.outcome=="win")
        wr=(wins/n*100) if n else 0
        mid=(a+b)/2
        align=classify_alignment(mid, wr)
        out.append({"bucket":f"{a}-{b}","signals_count":n,"win_rate":round(wr,2),"average_net_pips":round(sum(r.net_result_pips for r in rows)/n,2) if n else 0,"alignment":align})
    return {"buckets": out}


@router.get("/reliability")
async def reliability(db: AsyncSession = Depends(get_db)):
    perf = await performance(db, include_synthetic=False)
    cal = await calibration(db)
    n = perf["total_signals"]
    win = perf["win_rate_excl_hold"]
    pips = perf["average_result_pips"]
    aligned = sum(1 for b in cal["buckets"] if b["alignment"]=="aligned")
    score, label = reliability_score(n, win, pips, aligned)
    recent = sorted([o for o in outcomes if o.outcome in {"win", "loss", "invalidated"}], key=lambda x: x.created_at, reverse=True)[:40] if (outcomes := (await db.execute(select(SignalOutcome))).scalars().all()) else []
    drift_warnings = []
    if recent:
        invalidated_rate = sum(1 for o in recent if o.outcome == "invalidated") / len(recent)
        if invalidated_rate > 0.30:
            drift_warnings.append("Increased invalidation frequency")
    if score < 45:
        drift_warnings.append("Engine reliability is currently low")
    if drift_warnings:
        score = max(0.0, score - 8)
    db.add(ReliabilityHistory(score=score, label=label, sample_size=n, win_rate=win, avg_net_pips=pips, drift_warning="; ".join(drift_warnings) if drift_warnings else None))
    await db.commit()
    return {"score": score, "label": label, "sample_size": n, "win_rate": win, "avg_net_pips": pips, "drift_warnings": drift_warnings, "adaptive_engine_status": "active"}


@router.get("/reliability-history")
async def reliability_history(db: AsyncSession = Depends(get_db), limit: int = 120):
    rows = (await db.execute(select(ReliabilityHistory).order_by(desc(ReliabilityHistory.created_at)).limit(limit))).scalars().all()
    return {"items": [{"score": r.score, "label": r.label, "sample_size": r.sample_size, "win_rate": r.win_rate, "avg_net_pips": r.avg_net_pips, "drift_warning": r.drift_warning, "created_at": r.created_at.isoformat()} for r in rows]}


@router.get("/regime-performance")
async def regime_performance(db: AsyncSession = Depends(get_db)):
    outcomes = (await db.execute(select(SignalOutcome))).scalars().all()
    signals = (await db.execute(select(Signal))).scalars().all()
    by_id = {s.id: s for s in signals}
    def agg(key_fn):
        out = {}
        for o in outcomes:
            s = by_id.get(o.signal_id)
            if not s:
                continue
            k = key_fn(s, o)
            out.setdefault(k, {"n": 0, "wins": 0, "net": 0.0})
            out[k]["n"] += 1
            out[k]["wins"] += 1 if o.outcome == "win" else 0
            out[k]["net"] += o.net_result_pips
        return out
    by_regime = agg(lambda s, o: s.market_regime)
    by_risk = agg(lambda s, o: s.risk_level)
    by_profile = agg(lambda s, o: (s.reasoning or {}).get("profile", "unknown"))
    by_session = agg(lambda s, o: classify_session(s.created_at))
    best = max(by_regime.items(), key=lambda kv: (kv[1]["net"] / max(1, kv[1]["n"])), default=("n/a", {}))[0]
    worst = min(by_regime.items(), key=lambda kv: (kv[1]["net"] / max(1, kv[1]["n"])), default=("n/a", {}))[0]
    return {"best_regime": best, "worst_regime": worst, "by_regime": by_regime, "profile_effectiveness": by_profile, "reliability_by_regime": by_regime, "by_risk_level": by_risk, "by_session": by_session}


@router.get("/validation-runs")
async def validation_runs(db: AsyncSession = Depends(get_db), limit: int = 50):
    from app.models import ValidationRun
    rows = (await db.execute(select(ValidationRun).order_by(desc(ValidationRun.started_at)).limit(limit))).scalars().all()
    return [{"id": r.id, "started_at": r.started_at.isoformat(), "completed_at": r.completed_at.isoformat() if r.completed_at else None, "status": r.status, "signals_checked": r.signals_checked, "outcomes_updated": r.outcomes_updated, "error_message": r.error_message} for r in rows]


@router.get("/{signal_id}/outcome")
async def get_outcome(signal_id: int, db: AsyncSession = Depends(get_db)):
    o = (await db.execute(select(SignalOutcome).where(SignalOutcome.signal_id == signal_id))).scalar_one_or_none()
    if not o:
        raise HTTPException(404, "Outcome not found")
    return {
        "signal_id": o.signal_id, "pair": o.pair, "timeframe": o.timeframe, "direction": o.direction,
        "entry_price": o.entry_price, "stop_loss": o.stop_loss, "take_profit": o.take_profit,
        "invalidation_price": o.invalidation_price, "outcome": o.outcome,
        "max_favorable_move": o.max_favorable_move, "max_adverse_move": o.max_adverse_move,
        "result_pips": o.result_pips, "checked_at": o.checked_at.isoformat() if o.checked_at else None,
        "created_at": o.created_at.isoformat(),
    }


class CloseSignal(BaseModel):
    status: str  # win | loss | expired
    pnl_pips: float | None = None


@router.post("/{signal_id}/close")
async def close(signal_id: int, body: CloseSignal, db: AsyncSession = Depends(get_db)):
    s = await db.get(Signal, signal_id)
    if not s: raise HTTPException(404, "Signal not found")
    s.status = body.status; s.pnl_pips = body.pnl_pips; s.closed_at = utc_now()
    await db.commit()
    learn = await record_outcome(db, _serialize(s))
    return {"ok": True, "learning": learn}


def _serialize(s: Signal, outcome: SignalOutcome | None = None) -> dict:
    return {
        "id": s.id, "pair": s.pair, "direction": s.direction, "timeframe": s.timeframe,
        "entry": s.entry, "stop_loss": s.stop_loss, "take_profit": s.take_profit,
        "risk_reward": s.risk_reward, "confidence": s.confidence,
        "strength": s.strength, "risk_level": s.risk_level, "reason_summary": s.reason_summary,
        "indicators_used": s.indicators_used, "invalidation_price": s.invalidation_price,
        "data_source": s.data_source,
        "outcome": outcome.outcome if outcome else "pending",
        "estimated_cost_pips": outcome.estimated_cost_pips if outcome else 0.0,
        "net_result_pips": outcome.net_result_pips if outcome else 0.0,
        "market_regime": s.market_regime, "reasoning": s.reasoning,
        "explanation": s.explanation, "status": s.status, "pnl_pips": s.pnl_pips,
        "created_at": s.created_at.isoformat(), "closed_at": s.closed_at.isoformat() if s.closed_at else None,
    }


async def _validation_stats(db: AsyncSession) -> dict:
    try:
        outcomes = (await db.execute(select(SignalOutcome))).scalars().all()
        contexts = (await db.execute(select(SignalScanContext))).scalars().all()
    except SQLAlchemyError:
        provider = {"total": 0, "validated": 0, "pending": 0, "wins": 0, "losses": 0, "win_rate": 0.0, "loss_rate": 0.0}
        demo = dict(provider)
        return {
            "provider_backed": provider,
            "synthetic_demo": demo,
            "recent_accuracy_by_symbol_interval": {},
            "auto_trade": False,
            "no_execution": True,
            "advisory_only": True,
        }
    by_signal = {c.signal_id: c for c in contexts}

    def blank():
        return {"total": 0, "validated": 0, "pending": 0, "wins": 0, "losses": 0, "win_rate": 0.0, "loss_rate": 0.0}

    provider = blank()
    demo = blank()
    by_symbol_interval: dict[str, dict] = {}

    for outcome in outcomes:
        context = by_signal.get(outcome.signal_id)
        target = demo if (context.demo_only if context else False) else provider
        key = f"{outcome.pair} {outcome.timeframe}"
        bucket = by_symbol_interval.setdefault(key, blank())
        for agg in (target, bucket):
            agg["total"] += 1
            if outcome.outcome == "pending":
                agg["pending"] += 1
            if outcome.outcome in {"win", "loss"}:
                agg["validated"] += 1
            if outcome.outcome == "win":
                agg["wins"] += 1
            if outcome.outcome == "loss":
                agg["losses"] += 1

    for agg in [provider, demo, *by_symbol_interval.values()]:
        validated = max(1, agg["validated"])
        agg["win_rate"] = round(agg["wins"] / validated * 100, 2) if agg["validated"] else 0.0
        agg["loss_rate"] = round(agg["losses"] / validated * 100, 2) if agg["validated"] else 0.0

    return {
        "provider_backed": provider,
        "synthetic_demo": demo,
        "recent_accuracy_by_symbol_interval": by_symbol_interval,
        "auto_trade": False,
        "no_execution": True,
        "advisory_only": True,
    }
