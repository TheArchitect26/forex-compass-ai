from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_db
from app.models import Signal
from app.engines import performance

router = APIRouter()


@router.get("")
async def overview(db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(Signal))).scalars().all()
    serialized = [{
        "pair": r.pair, "status": r.status, "pnl_pips": r.pnl_pips,
        "market_regime": r.market_regime,
    } for r in rows]
    return performance.summarize(serialized)
