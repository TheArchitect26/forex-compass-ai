from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_db
from app.models import Signal
from app.engines import adaptive, ml

router = APIRouter()


@router.get("/insights")
async def insights(db: AsyncSession = Depends(get_db)):
    return await adaptive.insights(db)


@router.post("/train")
async def train(db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(Signal))).scalars().all()
    serialized = [{
        "confidence": r.confidence, "risk_reward": r.risk_reward,
        "reasoning": r.reasoning, "status": r.status,
    } for r in rows]
    return ml.train(serialized)
