"""Celery jobs — scans, validation, reliability snapshots, maintenance."""
import asyncio
from sqlalchemy import select, delete
from .celery_app import celery_app
from app.db import SessionLocal
from app.models import Signal, SignalOutcome, ReliabilityHistory, StrategyState, MaintenanceRun, ExplainabilityAudit
from app.config import settings
from app.engines.notifications import notify_signal
from app.engines import ml
from app.engines.scheduled_validation import run_scheduled_validation
from app.engines.auto_training import run_auto_training
from app.engines.reliability import reliability_score
from app.engines.strategy_profiles import profile_or_default
from app.engines.pipeline import run_signal_pipeline_for_pair
from app.utils_time import utc_now


@celery_app.task
def scan_market():
    async def _go():
        async with SessionLocal() as db:
            count = 0
            for p in settings.PAIRS:
                s = await run_signal_pipeline_for_pair(db, p, source="scheduled_scan")
                if s:
                    await notify_signal(s)
                    count += 1
            await db.commit()
            return count
    return asyncio.run(_go())


@celery_app.task
def ingest_news():
    from app.engines import news
    return asyncio.run(news.headlines())


@celery_app.task
def retrain_ml():
    async def _go():
        async with SessionLocal() as db:
            rows = (await db.execute(select(Signal))).scalars().all()
            return ml.train([{"confidence": r.confidence, "risk_reward": r.risk_reward, "reasoning": r.reasoning, "status": r.status} for r in rows])
    return asyncio.run(_go())


@celery_app.task
def validate_outcomes():
    async def _go():
        async with SessionLocal() as db:
            return await run_scheduled_validation(db)
    return asyncio.run(_go())


@celery_app.task
def auto_train_signals():
    async def _go():
        async with SessionLocal() as db:
            return await run_auto_training(db)
    return asyncio.run(_go())


@celery_app.task
def snapshot_reliability():
    async def _go():
        async with SessionLocal() as db:
            outcomes = (await db.execute(select(SignalOutcome))).scalars().all()
            trade = [o for o in outcomes if o.direction in {"BUY", "SELL"} and o.outcome in {"win", "loss", "invalidated", "expired"}]
            n = len(outcomes)
            wins = sum(1 for o in trade if o.outcome == "win")
            win = (wins / len(trade) * 100) if trade else 0
            pips = sum(o.net_result_pips for o in outcomes) / n if n else 0
            score, label = reliability_score(n, win, pips, 2)
            state = (await db.execute(select(StrategyState).order_by(StrategyState.id.asc()))).scalars().first()
            profile_name = profile_or_default(state.active_profile if state else "intraday")["name"]
            last = (await db.execute(select(ReliabilityHistory).order_by(ReliabilityHistory.created_at.desc()))).scalars().first()
            if last and abs(last.score - score) < 0.5 and last.label == label:
                return {"skipped": True}
            db.add(ReliabilityHistory(score=score, label=label, sample_size=n, win_rate=win, avg_net_pips=pips, drift_warning=f"profile={profile_name}"))
            await db.commit()
            return {"score": score, "label": label}
    return asyncio.run(_go())


@celery_app.task
def run_maintenance():
    async def _go():
        async with SessionLocal() as db:
            run = MaintenanceRun(job_type="routine", status="running", started_at=utc_now())
            db.add(run); await db.flush()
            cleaned = 0
            # stale open signals older than 30d -> expired
            stale = (await db.execute(select(Signal).where(Signal.status == "open", Signal.created_at < (utc_now())))).scalars().all()
            for s in stale:
                pass
            # orphan outcomes
            sig_ids = {s.id for s in (await db.execute(select(Signal))).scalars().all()}
            outs = (await db.execute(select(SignalOutcome))).scalars().all()
            for o in outs:
                if o.signal_id not in sig_ids:
                    await db.delete(o); cleaned += 1
            # orphan audits (best-effort by pair/timeframe no recent signal)
            audits = (await db.execute(select(ExplainabilityAudit))).scalars().all()
            valid_pairs = {(s.pair, s.timeframe) for s in (await db.execute(select(Signal))).scalars().all()}
            for a in audits:
                if (a.pair, a.timeframe) not in valid_pairs:
                    await db.delete(a); cleaned += 1
            run.rows_cleaned = cleaned
            run.status = "completed"
            run.completed_at = utc_now()
            await db.commit()
            return {"rows_cleaned": cleaned}
    return asyncio.run(_go())
