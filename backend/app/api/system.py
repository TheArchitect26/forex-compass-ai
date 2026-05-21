from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.models import ResearchTask, ResearchFinding, ResearchWorkload, MissionTimelineEvent
from app.engines.research_orchestration import coordinated_health, priority_from_signals
from app.engines.system_metrics import aggregate_metrics
from app.engines.human_sovereignty import complexity_pressure, operator_load

router = APIRouter()

@router.get('/health')
async def system_health(db: AsyncSession = Depends(get_db)):
    payload = {
        "data_health": 82,
        "calibration_health": 74,
        "replay_integrity": 86,
        "portfolio_reliability": 71,
        "adaptive_stability": 77,
        "governance_safety": 93,
        "drift_score": 38,
    }
    health = coordinated_health(payload)
    return {"system_health": health, "no_execution": True, "auto_trade": False}

@router.post('/research/task')
async def create_research_task(body: dict, db: AsyncSession = Depends(get_db)):
    task = ResearchTask(
        task_type=body.get('type', 'integrity_audit'),
        status='pending',
        priority=priority_from_signals(body),
        triggered_by=body.get('triggered_by', 'manual'),
        linked_datasets=body.get('linked_datasets', []),
        linked_experiments=body.get('linked_experiments', []),
        linked_replay_sessions=body.get('linked_replay_sessions', []),
        findings_summary=body.get('findings_summary', ''),
        warnings=body.get('warnings', []),
        recommendations=body.get('recommendations', []),
        evidence=body.get('evidence', {}),
    )
    db.add(task)
    await db.commit(); await db.refresh(task)
    return {"id": task.id, "priority": task.priority, "status": task.status}

@router.get('/research/tasks')
async def list_tasks(db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select
    q = await db.execute(select(ResearchTask).order_by(ResearchTask.created_at.desc()).limit(30))
    tasks = q.scalars().all()
    return [{"id": t.id, "type": t.task_type, "status": t.status, "priority": t.priority, "warnings": t.warnings, "recommendations": t.recommendations} for t in tasks]

@router.get('/research/findings')
async def findings(db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select
    q = await db.execute(select(ResearchFinding).order_by(ResearchFinding.created_at.desc()).limit(50))
    rows = q.scalars().all()
    return [{"id": r.id, "message": r.message, "confidence": r.confidence, "evidence_refs": r.evidence_refs, "triggered_by_task_id": r.triggered_by_task_id} for r in rows]

@router.get('/metrics')
async def system_metrics(db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select
    wq = await db.execute(select(ResearchWorkload).limit(300))
    workloads = [{
        "id": w.id,
        "status": w.status,
        "type": w.workload_type,
        "throughput": (w.resource_estimate or {}).get("batch_size", 0),
        "latency_ms": w.execution_duration_ms,
    } for w in wq.scalars().all()]
    incidents = [w for w in workloads if w.get("status") == "failed"]
    return {"metrics": aggregate_metrics(workloads, incidents), "no_execution": True}

@router.get('/operator-load')
async def system_operator_load():
    pressure = complexity_pressure({
        "dashboard_overload": 2,
        "recommendation_saturation": 3,
        "unresolved_workflow_accumulation": 2,
        "alert_density": 2,
        "governance_burden": 2,
        "contradiction_backlog": 1,
        "investigation_sprawl": 2,
        "replay_backlog_pressure": 2,
    })
    load = operator_load({
        "complexity_pressure": pressure["complexity_pressure_score"],
        "alert_density": 20,
        "unresolved_issues": 8,
        "critical_alerts": 1,
        "recommendation_saturation": 18,
        "contradictions": 4,
        "governance_burden": 10,
    })
    return {"complexity_pressure": pressure, "operator_load": load, "human_directed": True}

@router.get('/eras')
async def system_eras():
    return {
        "reliability_eras": ["stabilization-era", "adaptive-era"],
        "governance_eras": ["baseline-governance", "constitutional-governance"],
        "volatility_eras": ["range-heavy-era", "high-volatility-era"],
        "calibration_eras": ["manual-calibration", "profile-calibration"],
        "major_strategic_transitions": ["phase12-research-orchestration", "phase16-constitutional", "phase18-sovereignty"],
        "institutional_crises": [],
        "major_replay_migrations": ["legacy-replay-adapter-introduced"],
    }

@router.get('/evolution-timeline')
async def evolution_timeline():
    return {
        "institutional_eras": ["foundation-era", "research-expansion-era", "governance-era"],
        "governance_transitions": ["baseline->constitutional", "constitutional->epistemic", "epistemic->sovereignty"],
        "major_renewals": ["assumption-renewal-cycle-1", "archive-consolidation-cycle-1"],
        "methodology_shifts": ["replay-v1->replay-v2-adapter", "manual-calibration->profile-calibration"],
        "replay_generation_changes": ["legacy-compat-mode-enabled"],
        "strategic_identity_transitions": ["signal-assistant->institutional-research-assistant"],
        "resilience_recoveries": [],
    }

@router.get('/mission-timeline')
async def mission_timeline(db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select
    q = await db.execute(select(MissionTimelineEvent).order_by(MissionTimelineEvent.created_at.desc()).limit(400))
    rows = q.scalars().all()
    return {
        "mission_revisions": [r.details for r in rows if r.event_type == "mission_revision"],
        "constitutional_reaffirmations": [r.details for r in rows if r.event_type == "constitutional_reaffirmation"],
        "purpose_preservation_events": [r.details for r in rows if r.event_type == "purpose_preservation"],
        "alignment_crises": [r.details for r in rows if r.event_type == "alignment_crisis"],
        "strategic_resets": [r.details for r in rows if r.event_type == "strategic_reset"],
        "anti_drift_recoveries": [r.details for r in rows if r.event_type == "anti_drift_recovery"],
        "governance_realignments": [r.details for r in rows if r.event_type == "governance_realignment"],
    }


@router.get('/reality-timeline')
async def reality_timeline():
    return {
        "major_grounding_corrections": ["reality-anchor-thresholds-tightened"],
        "practical_simplifications": ["retired-non-actionable-workflow-review"],
        "replay_realism_improvements": ["replay-to-reality-gap-monitoring-enabled"],
        "usefulness_recoveries": ["operator-utility-feedback-loop-added"],
        "anti_detachment_interventions": ["self-referential-loop-detection-enabled"],
        "strategic_refocusing_events": ["phase25-reality-anchoring"],
    }


@router.get('/personal-continuity')
async def personal_continuity_memory():
    return {
        "major_operator_priority_shifts": ["risk-first-over-growth-phase"],
        "strategic_goal_changes": ["from throughput to decision-quality"],
        "simplification_periods": ["q2-lightweight-operations"],
        "focus_transitions": ["broad-scan->eurusd-focused"],
        "major_workflow_retirements": ["low-signal replay branch retired"],
        "long_term_intent_evolution": ["operator-centered and sustainability-first"],
    }
