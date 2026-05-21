from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_db
from app.models import StrategicBriefing, StrategicMemoryEvent
from app.engines.meta_intelligence import synthesize_strategic_view, detect_anomalies, detect_recommendation_conflicts, dependency_map_snapshot

router = APIRouter()

@router.get('/briefings')
async def briefings(db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(StrategicBriefing).order_by(StrategicBriefing.generated_at.desc()).limit(50))
    rows = q.scalars().all()
    return [{
        "id": b.id,
        "title": b.title,
        "generated_at": b.generated_at.isoformat(),
        "severity": b.severity,
        "summary": b.summary,
        "supporting_evidence": b.supporting_evidence,
        "affected_systems": b.affected_systems,
        "confidence": b.confidence,
        "recommended_actions": b.recommended_actions,
        "reproducibility_refs": b.reproducibility_refs,
    } for b in rows]

@router.post('/briefings/generate')
async def generate_briefing(body: dict, db: AsyncSession = Depends(get_db)):
    view = synthesize_strategic_view(body)
    anomalies = detect_anomalies(body)
    title = view["summary"][0]
    severity = "critical" if view["scores"]["anomaly_pressure_score"] > 70 else "elevated" if view["scores"]["anomaly_pressure_score"] > 45 else "normal"
    recs = body.get("recommended_actions", [])
    briefing = StrategicBriefing(
        title=title,
        severity=severity,
        summary=" | ".join(view["summary"]),
        supporting_evidence=body.get("evidence", []),
        affected_systems=body.get("affected_systems", ["research", "replay"]),
        confidence=min(1.0, max(0.0, float(body.get("confidence", 0.75)))),
        recommended_actions=recs,
        reproducibility_refs=body.get("reproducibility_refs", []),
    )
    db.add(briefing)
    mem = StrategicMemoryEvent(
        event_type="strategic_briefing_generated",
        title=title,
        details={"scores": view["scores"], "anomaly_count": len(anomalies)},
        anomaly_timeline=anomalies,
        repeated_pattern_key=body.get("pattern_key", ""),
        successful_mitigation=body.get("mitigation", ""),
    )
    db.add(mem)
    await db.commit(); await db.refresh(briefing)
    return {"briefing_id": briefing.id, "severity": briefing.severity, "scores": view["scores"], "anomalies": anomalies, "advisory_only": True}

@router.get('/strategic-status')
async def strategic_status():
    signals = {
        "regime_instability": 61,
        "drift_pressure": 57,
        "integrity_degradation": 44,
        "reliability_drop": 9,
        "workload_pressure": 63,
        "usd_concentration_risk": 66,
    }
    view = synthesize_strategic_view(signals)
    deps = dependency_map_snapshot({})
    return {"strategic_scores": view["scores"], "highlights": view["summary"], "dependency_map": deps, "auto_trade": False}

@router.post('/anomalies/interpret')
async def interpret_anomalies(body: dict):
    anomalies = detect_anomalies(body)
    conflicts = detect_recommendation_conflicts(body.get("recommendations", []))
    return {"anomalies": anomalies, "recommendation_conflicts": conflicts, "reproducible": True, "advisory_only": True}

@router.get('/memory/events')
async def memory_events(db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(StrategicMemoryEvent).order_by(StrategicMemoryEvent.created_at.desc()).limit(100))
    rows = q.scalars().all()
    return [{"id": r.id, "event_type": r.event_type, "title": r.title, "details": r.details, "anomaly_timeline": r.anomaly_timeline, "created_at": r.created_at.isoformat()} for r in rows]
