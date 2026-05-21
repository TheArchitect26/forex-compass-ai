from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_db
from app.models import MetaCoordinationEvent
from app.engines.meta_operating import (
    coordination_status,
    build_coordination_graph,
    synchronization_check,
    meta_explainability,
    meta_resilience,
    consolidation_recommendations,
    timeline_merge,
)
from app.engines.semantic_stability import orientation, orientation_score, detect_meaning_conflicts, stabilize_narratives, comprehension_safeguards

router = APIRouter()

@router.get('/coordination-status')
async def get_coordination_status():
    payload = {
        "subsystem_divergence": 0.32,
        "duplicated_governance_logic": 0.28,
        "workflow_fragmentation": 0.35,
        "replay_inconsistency_pressure": 0.29,
        "recommendation_fragmentation": 0.3,
        "synchronization_failures": 0.2,
        "coordination_overhead": 0.33,
    }
    return coordination_status(payload)

@router.post('/coordination-graph')
async def coordination_graph(body: dict):
    return build_coordination_graph(body.get('nodes', []), body.get('links', []))

@router.post('/synchronization-check')
async def sync_check(body: dict):
    return synchronization_check(body)

@router.post('/explainability')
async def explainability(body: dict):
    return meta_explainability(body)

@router.get('/resilience')
async def resilience():
    return {"resilience": meta_resilience({}), "operator_review_required": True}

@router.post('/simplification')
async def simplification(body: dict):
    return consolidation_recommendations(body)

@router.get('/timeline')
async def timeline(db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(MetaCoordinationEvent).order_by(MetaCoordinationEvent.created_at.desc()).limit(300))
    rows = q.scalars().all()
    events = {
        "strategic_eras": [r.details.get("era") for r in rows if r.event_type == "strategic_era"],
        "replay_eras": [r.details.get("era") for r in rows if r.event_type == "replay_era"],
        "governance_transitions": [r.details.get("transition") for r in rows if r.event_type == "governance_transition"],
        "incidents": [r.details for r in rows if r.event_type == "incident"],
        "migrations": [r.details for r in rows if r.event_type == "migration"],
        "renewals": [r.details for r in rows if r.event_type == "renewal"],
        "strategic_shifts": [r.details for r in rows if r.event_type == "strategic_shift"],
        "continuity_breaks": [r.details for r in rows if r.event_type == "continuity_break"],
        "survivability_recoveries": [r.details for r in rows if r.event_type == "survivability_recovery"],
    }
    return {"timeline": timeline_merge(events)}

@router.post('/memory/event')
async def add_meta_event(body: dict, db: AsyncSession = Depends(get_db)):
    row = MetaCoordinationEvent(
        event_type=body.get("event_type", "incident"),
        details=body.get("details", {}),
        severity=body.get("severity", "info"),
    )
    db.add(row); await db.commit(); await db.refresh(row)
    return {"id": row.id}

@router.get('/orientation')
async def get_orientation():
    return orientation({
        "recent_assumption_changes": ["aggressive-breakout assumption confidence reduced"],
        "rising_risks": ["semantic drift in governance terminology"],
        "complexity_hotspots": ["multi-console narrative duplication"],
    })

@router.get('/orientation-score')
async def get_orientation_score():
    return {"orientation_score": orientation_score({})}

@router.post('/meaning-conflicts')
async def meaning_conflicts(body: dict):
    return detect_meaning_conflicts(body.get("concepts", []))

@router.post('/narrative-stabilization')
async def narrative_stabilization(body: dict):
    return stabilize_narratives(body.get("narratives", []))

@router.post('/comprehension-safeguards')
async def comprehension(body: dict):
    return comprehension_safeguards(body)
