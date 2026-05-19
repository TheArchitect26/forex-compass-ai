"""Celery jobs — periodic scan, news ingestion, daily retrain."""
import asyncio
from .celery_app import celery_app
from app.db import SessionLocal
from app.models import Signal
from sqlalchemy import select
from app.config import settings
from app.engines.signal_intelligence import analyze_pair
from app.engines.notifications import notify_signal
from app.engines import ml


def _run(coro): return asyncio.get_event_loop().run_until_complete(coro) if not asyncio.iscoroutine(coro) else asyncio.run(coro)


@celery_app.task
def scan_market():
    async def _go():
        async with SessionLocal() as db:
            count = 0
            for p in settings.PAIRS:
                res = await analyze_pair(p)
                if res.get("signal"):
                    s = res["signal"]
                    db.add(Signal(
                        pair=s["pair"], direction=s["direction"], timeframe=s["timeframe"],
                        entry=s["entry"], stop_loss=s["stop_loss"], take_profit=s["take_profit"],
                        risk_reward=s["risk_reward"], confidence=s["confidence"],
                        market_regime=s["market_regime"], reasoning=s["reasoning"],
                        explanation=s["explanation"], status="open",
                    ))
                    await notify_signal(s); count += 1
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
            return ml.train([{
                "confidence": r.confidence, "risk_reward": r.risk_reward,
                "reasoning": r.reasoning, "status": r.status,
            } for r in rows])
    return asyncio.run(_go())
