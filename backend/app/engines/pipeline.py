from __future__ import annotations
from datetime import timedelta
from sqlalchemy import select, desc
from app.config import settings
from app.config import synthetic_buy_sell_blocked
from app.models import Signal, ExplainabilityAudit, HistoricalCandle, SignalScanContext, StrategyState
from app.engines.market_data import market_data
from app.engines.signal_intelligence import analyze_pair
from app.engines.signal_discipline import apply_quality_gates, blocked_by_synthetic_policy, is_duplicate_recent
from app.engines.strategy_profiles import profile_or_default
from app.utils_time import utc_now

from app.engines.pipeline_meta import config_snapshot

async def get_active_profile(db) -> dict:
    state = (await db.execute(select(StrategyState).order_by(StrategyState.id.asc()))).scalars().first()
    return profile_or_default(state.active_profile if state else "intraday")


async def run_signal_pipeline_for_pair(db, pair: str, source: str = "api_scan") -> dict | None:
    profile = await get_active_profile(db)
    res = await analyze_pair(pair)
    if not res.get("signal"):
        return None
    s = res["signal"]
    before = s["confidence"]
    s = apply_quality_gates(s, profile["min_confidence"])
    allow_synthetic_signals = settings.ALLOW_SYNTHETIC_SIGNALS and not synthetic_buy_sell_blocked()
    if blocked_by_synthetic_policy(s, allow_synthetic_signals):
        return None

    cooldown_since = utc_now() - timedelta(minutes=profile["cooldown_minutes"])
    existing = (await db.execute(select(Signal).where(Signal.pair == s["pair"], Signal.timeframe == s["timeframe"], Signal.created_at >= cooldown_since).order_by(desc(Signal.created_at)))).scalars().first()
    if existing and is_duplicate_recent(existing.created_at, profile["cooldown_minutes"]):
        return None

    snap = config_snapshot(profile, runtime={"allow_synthetic_signals": allow_synthetic_signals, "default_slippage_pips": settings.DEFAULT_SLIPPAGE_PIPS, "default_spread_pips": settings.DEFAULT_SPREAD_PIPS})
    s.setdefault("reasoning", {})["profile"] = profile["name"]
    s["reasoning"]["config_snapshot"] = snap
    s["reasoning"]["source_path"] = source

    row = Signal(
        pair=s["pair"], direction=s["direction"], timeframe=s["timeframe"],
        entry=s["entry"], stop_loss=s["stop_loss"], take_profit=s["take_profit"],
        risk_reward=s["risk_reward"], confidence=s["confidence"], strength=s["strength"],
        risk_level=s["risk_level"], reason_summary=s["reason_summary"], indicators_used=s["indicators_used"],
        invalidation_price=s["invalidation_price"], data_source=s["data_source"], market_regime=s["market_regime"],
        reasoning=s["reasoning"], explanation=s["explanation"], status="open",
    )
    db.add(row)
    await db.flush()

    source_info = market_data.source_info(s["pair"], s["timeframe"], 200)
    provider_name = source_info.get("source") or s["data_source"]
    demo_only = s["data_source"] == "synthetic" or provider_name == "synthetic"
    data_mode = "synthetic_demo" if demo_only else "provider"
    snapshot = await _persist_signal_candle_snapshot(db, s["pair"], s["timeframe"], provider_name, demo_only)
    db.add(SignalScanContext(
        signal_id=row.id,
        symbol=s["pair"],
        interval=s["timeframe"],
        signal_timestamp=row.created_at,
        direction=s["direction"],
        confidence=s["confidence"],
        entry_price=s["entry"],
        data_mode=data_mode,
        provider_name=provider_name,
        demo_only=demo_only,
        candle_snapshot=snapshot,
    ))
    db.add(ExplainabilityAudit(
        pair=s["pair"], timeframe=s["timeframe"], regime=s["market_regime"], strategy_profile=profile["name"],
        signal_decision=s["direction"], confidence_before=before, confidence_after=s["confidence"],
        adaptive_changes=s.get("reasoning", {}).get("adaptive_weighting", {}), drift_warnings=s.get("reasoning", {}).get("risk_warnings", []),
        reasons=f"{s.get('reason_summary','')} | src={source} | versions={snap}",
    ))
    return s


async def _persist_signal_candle_snapshot(db, pair: str, timeframe: str, provider_name: str, demo_only: bool) -> dict:
    limit = 200
    df = await market_data.ohlcv(pair, timeframe, limit)
    rows = []
    for r in df.itertuples():
        ts = r.datetime.to_pydatetime() if hasattr(r.datetime, "to_pydatetime") else r.datetime
        rows.append({
            "timestamp": ts,
            "open": float(r.open),
            "high": float(r.high),
            "low": float(r.low),
            "close": float(r.close),
            "volume": float(getattr(r, "volume", 0.0) or 0.0),
        })
    if not demo_only:
        for c in rows:
            db.add(HistoricalCandle(
                pair=pair,
                timeframe=timeframe,
                timestamp=c["timestamp"],
                open=c["open"],
                high=c["high"],
                low=c["low"],
                close=c["close"],
                volume=c["volume"],
                source=provider_name,
                integrity_flags={"scan_context": True},
            ))
    return {
        "rows": len(rows),
        "first_timestamp": rows[0]["timestamp"].isoformat() if rows else None,
        "last_timestamp": rows[-1]["timestamp"].isoformat() if rows else None,
        "source": provider_name,
        "demo_only": demo_only,
    }
