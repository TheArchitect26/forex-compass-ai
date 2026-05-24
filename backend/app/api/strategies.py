from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_db
from app.models import StrategyState
from app.utils_time import utc_now
from app.engines.strategy_profiles import PROFILES, profile_or_default
from app.security import current_user

router = APIRouter()


async def _ensure_state(db: AsyncSession) -> StrategyState:
    row = (await db.execute(select(StrategyState).order_by(StrategyState.id.asc()))).scalars().first()
    if not row:
        row = StrategyState(active_profile="intraday", source="default", updated_at=utc_now())
        db.add(row)
        await db.commit()
        await db.refresh(row)
    return row


@router.get("")
async def list_strategies(db: AsyncSession = Depends(get_db)):
    row = await _ensure_state(db)
    return {"active": {**profile_or_default(row.active_profile), "source": row.source, "updated_at": row.updated_at.isoformat()}, "profiles": PROFILES}


class SelectProfile(BaseModel):
    profile: str
    source: str = "manual"


@router.post("/select")
async def select_profile(body: SelectProfile, db: AsyncSession = Depends(get_db), _user: str = Depends(current_user)):
    if body.profile not in PROFILES:
        raise HTTPException(400, "Unknown profile")
    row = await _ensure_state(db)
    row.active_profile = body.profile
    row.source = body.source if body.source in {"manual", "adaptive", "default"} else "manual"
    row.updated_at = utc_now()
    await db.commit()
    return {"active": {**profile_or_default(row.active_profile), "source": row.source, "updated_at": row.updated_at.isoformat()}}
