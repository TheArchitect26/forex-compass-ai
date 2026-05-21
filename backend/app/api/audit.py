from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_db
from app.models import Signal, ExplainabilityAudit, ReliabilityHistory

router = APIRouter()


@router.get("/signals/{signal_id}")
async def audit_signal(signal_id: int, db: AsyncSession = Depends(get_db)):
    s = await db.get(Signal, signal_id)
    if not s:
        raise HTTPException(404, "Signal not found")
    a = (await db.execute(select(ExplainabilityAudit).where(ExplainabilityAudit.pair == s.pair, ExplainabilityAudit.timeframe == s.timeframe).order_by(ExplainabilityAudit.timestamp.desc()))).scalars().first()
    return {
        "signal_id": s.id,
        "pair": s.pair,
        "timeframe": s.timeframe,
        "decision": s.direction,
        "regime": s.market_regime,
        "profile": (s.reasoning or {}).get("profile"),
        "confidence": s.confidence,
        "confidence_evolution": {"before": a.confidence_before if a else None, "after": a.confidence_after if a else None},
        "adaptive_changes": a.adaptive_changes if a else {},
        "drift_warnings": a.drift_warnings if a else [],
        "reasons": a.reasons if a else s.reason_summary,
        "config_snapshot": (s.reasoning or {}).get("config_snapshot", {}),
    }


@router.get("/reliability/{rid}")
async def audit_reliability(rid: int, db: AsyncSession = Depends(get_db)):
    r = await db.get(ReliabilityHistory, rid)
    if not r:
        raise HTTPException(404, "Reliability snapshot not found")
    return {"id": r.id, "score": r.score, "label": r.label, "sample_size": r.sample_size, "win_rate": r.win_rate, "avg_net_pips": r.avg_net_pips, "drift_warning": r.drift_warning, "created_at": r.created_at.isoformat()}
