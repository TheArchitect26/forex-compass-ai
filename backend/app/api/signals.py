from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from pydantic import BaseModel
from datetime import datetime

from app.db import get_db
from app.models import Signal
from app.config import settings
from app.engines.signal_intelligence import analyze_pair
from app.engines.adaptive import record_outcome

router = APIRouter()


@router.get("")
async def list_signals(db: AsyncSession = Depends(get_db), limit: int = 50):
    rows = (await db.execute(select(Signal).order_by(desc(Signal.created_at)).limit(limit))).scalars().all()
    return [_serialize(s) for s in rows]


@router.post("/scan")
async def scan(db: AsyncSession = Depends(get_db)):
    """Run intelligence over all pairs, persist any qualifying signals."""
    found = []
    for p in settings.PAIRS:
        res = await analyze_pair(p)
        if res.get("signal"):
            s = res["signal"]
            row = Signal(
                pair=s["pair"], direction=s["direction"], timeframe=s["timeframe"],
                entry=s["entry"], stop_loss=s["stop_loss"], take_profit=s["take_profit"],
                risk_reward=s["risk_reward"], confidence=s["confidence"],
                market_regime=s["market_regime"], reasoning=s["reasoning"],
                explanation=s["explanation"], status="open",
            )
            db.add(row); found.append(s)
    await db.commit()
    return {"found": len(found), "signals": found}


class CloseSignal(BaseModel):
    status: str  # win | loss | expired
    pnl_pips: float | None = None


@router.post("/{signal_id}/close")
async def close(signal_id: int, body: CloseSignal, db: AsyncSession = Depends(get_db)):
    s = await db.get(Signal, signal_id)
    if not s: raise HTTPException(404, "Signal not found")
    s.status = body.status; s.pnl_pips = body.pnl_pips; s.closed_at = datetime.utcnow()
    await db.commit()
    learn = await record_outcome(db, _serialize(s))
    return {"ok": True, "learning": learn}


def _serialize(s: Signal) -> dict:
    return {
        "id": s.id, "pair": s.pair, "direction": s.direction, "timeframe": s.timeframe,
        "entry": s.entry, "stop_loss": s.stop_loss, "take_profit": s.take_profit,
        "risk_reward": s.risk_reward, "confidence": s.confidence,
        "market_regime": s.market_regime, "reasoning": s.reasoning,
        "explanation": s.explanation, "status": s.status, "pnl_pips": s.pnl_pips,
        "created_at": s.created_at.isoformat(), "closed_at": s.closed_at.isoformat() if s.closed_at else None,
    }
