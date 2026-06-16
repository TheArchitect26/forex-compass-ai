"""Adaptive Learning Engine — pattern memory and gradual reweighting."""

from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import LearningRecord
from app.utils_time import utc_now


def _value(signal: Any, key: str, default=None):
    if isinstance(signal, dict):
        return signal.get(key, default)
    return getattr(signal, key, default)


def pattern_key_for_direction(
    signal: Any,
    direction: str,
) -> str:
    reasoning = _value(signal, "reasoning", {}) or {}
    patterns = reasoning.get("patterns") or []
    pattern = patterns[0] if patterns else "none"
    regime = reasoning.get("regime") or _value(
        signal, "market_regime", "unknown"
    )
    structure = reasoning.get("structure") or {}
    structure_state = structure.get("state", "unknown")

    return (
        f"{regime}|{structure_state}|{pattern}|{direction}"
    )


def pattern_key(signal: Any) -> str:
    return pattern_key_for_direction(
        signal,
        _value(signal, "direction", "UNKNOWN"),
    )


# Backwards-compatible alias for older imports.
_key = pattern_key


async def record_outcome(
    db: AsyncSession,
    signal: Any,
    *,
    commit: bool = True,
) -> dict:
    status = _value(signal, "status")
    if status not in {"win", "loss"}:
        return {"skipped": True}

    key = pattern_key(signal)
    reasoning = _value(signal, "reasoning", {}) or {}
    regime = reasoning.get("regime") or _value(
        signal, "market_regime", "unknown"
    )
    pair = _value(signal, "pair", "unknown")

    row = (
        await db.execute(
            select(LearningRecord).where(
                LearningRecord.pattern_key == key
            )
        )
    ).scalar_one_or_none()

    if row is None:
        row = LearningRecord(
            pattern_key=key,
            regime=regime,
            pair=pair,
            wins=0,
            losses=0,
            avg_rr=0.0,
            weight=1.0,
        )
        db.add(row)

    if status == "win":
        row.wins += 1
    else:
        row.losses += 1

    total = row.wins + row.losses

    # Bayesian smoothing prevents one early result from causing
    # a violent confidence swing.
    posterior_win_rate = (row.wins + 2) / (total + 4)
    row.weight = round(
        max(0.60, min(1.40, 0.60 + posterior_win_rate * 0.8)),
        4,
    )
    row.updated_at = utc_now().replace(tzinfo=None)

    if commit:
        await db.commit()
    else:
        await db.flush()

    return {
        "key": key,
        "wins": row.wins,
        "losses": row.losses,
        "weight": row.weight,
        "updated_after_trade": True,
    }


async def insights(
    db: AsyncSession,
    limit: int = 20,
) -> list[dict]:
    rows = (
        await db.execute(
            select(LearningRecord)
            .order_by(LearningRecord.weight.desc())
            .limit(limit)
        )
    ).scalars().all()

    return [
        {
            "pattern": row.pattern_key,
            "regime": row.regime,
            "pair": row.pair,
            "wins": row.wins,
            "losses": row.losses,
            "weight": row.weight,
            "win_rate": round(
                row.wins / max(row.wins + row.losses, 1) * 100,
                1,
            ),
        }
        for row in rows
    ]
