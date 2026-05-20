from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.db import get_db
from app.models import VersionRegistry

router = APIRouter()


async def _ensure(db: AsyncSession):
    row = (await db.execute(select(VersionRegistry).where(VersionRegistry.active == True))).scalars().first()
    if not row:
        row = VersionRegistry()
        db.add(row)
        await db.commit()
        await db.refresh(row)
    return row


@router.get("")
async def list_versions(db: AsyncSession = Depends(get_db)):
    active = await _ensure(db)
    history = (await db.execute(select(VersionRegistry).order_by(desc(VersionRegistry.created_at)).limit(20))).scalars().all()
    return {"active": _ser(active), "history": [_ser(h) for h in history]}


class ActivateBody(BaseModel):
    engine_version: str
    weighting_version: str
    calibration_version: str
    adaptation_version: str
    discipline_version: str


@router.post("/activate")
async def activate(body: ActivateBody, db: AsyncSession = Depends(get_db)):
    current = await _ensure(db)
    current.active = False
    new = VersionRegistry(**body.model_dump(), active=True)
    db.add(new)
    await db.commit()
    return {"active": _ser(new)}


class RollbackBody(BaseModel):
    target_id: int


@router.post("/rollback")
async def rollback(body: RollbackBody, db: AsyncSession = Depends(get_db)):
    target = await db.get(VersionRegistry, body.target_id)
    if not target:
        raise HTTPException(404, "Version not found")
    cur = await _ensure(db)
    cur.active = False
    target.active = True
    await db.commit()
    return {"active": _ser(target)}


def _ser(v: VersionRegistry):
    return {
        "id": v.id,
        "engine_version": v.engine_version,
        "weighting_version": v.weighting_version,
        "calibration_version": v.calibration_version,
        "adaptation_version": v.adaptation_version,
        "discipline_version": v.discipline_version,
        "active": v.active,
        "created_at": v.created_at.isoformat(),
    }
