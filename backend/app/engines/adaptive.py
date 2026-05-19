"""Adaptive Learning Engine — pattern memory + confidence reweighting.

After each closed signal, update the LearningRecord table for the pattern
fingerprint (regime + structure state + dominant pattern). Then adjust the
runtime weight used by `confidence.py`.
"""
from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from app.models import LearningRecord


def _key(signal: dict) -> str:
    r = signal["reasoning"]
    pat = r["patterns"][0] if r["patterns"] else "none"
    return f"{r['regime']}|{r['structure']['state']}|{pat}|{signal['direction']}"


async def record_outcome(db: AsyncSession, signal: dict) -> dict:
    if signal["status"] not in ("win", "loss"): return {"skipped": True}
    key = _key(signal)
    row = (await db.execute(select(LearningRecord).where(LearningRecord.pattern_key == key))).scalar_one_or_none()
    if row is None:
        row = LearningRecord(pattern_key=key, regime=signal["reasoning"]["regime"],
                             pair=signal["pair"], wins=0, losses=0, avg_rr=0.0, weight=1.0)
        db.add(row)
    if signal["status"] == "win": row.wins += 1
    else: row.losses += 1
    total = row.wins + row.losses
    wr = row.wins / total
    # weight: shrink confidence multiplier toward 0.5..1.5 based on observed edge
    row.weight = max(0.5, min(1.5, 0.5 + wr))
    row.updated_at = datetime.utcnow()
    await db.commit()
    return {"key": key, "wins": row.wins, "losses": row.losses, "weight": row.weight}


async def insights(db: AsyncSession, limit: int = 20) -> list[dict]:
    rows = (await db.execute(select(LearningRecord).order_by(LearningRecord.weight.desc()).limit(limit))).scalars().all()
    return [{
        "pattern": r.pattern_key, "regime": r.regime, "pair": r.pair,
        "wins": r.wins, "losses": r.losses, "weight": r.weight,
        "win_rate": round(r.wins / max(r.wins + r.losses, 1) * 100, 1),
    } for r in rows]
