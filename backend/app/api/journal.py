from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from pydantic import BaseModel
from app.db import get_db
from app.models import JournalEntry

router = APIRouter()


class JournalIn(BaseModel):
    signal_id: int | None = None
    pair: str
    direction: str
    entry: float
    exit: float | None = None
    size: float = 0.0
    pnl: float | None = None
    result: str | None = None
    notes: str = ""
    tags: list[str] = []


@router.get("")
async def list_entries(db: AsyncSession = Depends(get_db), limit: int = 100):
    rows = (await db.execute(select(JournalEntry).order_by(desc(JournalEntry.created_at)).limit(limit))).scalars().all()
    return [{c.name: getattr(r, c.name) for c in JournalEntry.__table__.columns} for r in rows]


@router.post("")
async def add_entry(body: JournalIn, db: AsyncSession = Depends(get_db)):
    e = JournalEntry(**body.model_dump())
    db.add(e); await db.commit(); await db.refresh(e)
    return {"id": e.id}
