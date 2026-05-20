from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_db
from app.models import ConstitutionalRule, GovernanceIncident, RecommendationLifecycle, StrategicMemoryEvent, StrategicAssumption, ContradictionWorkflow, InstitutionalArchive, EvolutionLineage, InstitutionalMigration, EvolutionPlan, RenewalWorkflow, GlossaryTerm, ConceptLineage, MissionAnchor, MissionTimelineEvent
from app.engines.constitutional_governance import (
    CONSTITUTIONAL_RULES,
    validate_consistency,
    explainability_score,
    trust_pressure,
    recommendation_with_trust_fields,
    confidence_decay,
)
from app.engines.epistemic_integrity import evaluate_epistemic_integrity, detect_knowledge_fragmentation, assumption_decay, archive_stabilization, lifecycle_review_gate
from app.engines.human_sovereignty import SOVEREIGNTY_GUARANTEES, simplification_engine, apply_focus_mode, explainability_layers, reset_action
from app.engines.longevity import survivability_scores, replay_compatibility_mode, lineage_entry, migration_plan, deprecation_workflow, archive_durability_check
from app.engines.strategic_renewal import adaptability_status, anti_dogma_scan, renewal_workflow, evolution_plan, identity_health, sandbox_experiment
from app.engines.semantic_stability import concept_lineage_entry
from app.engines.mission_integrity import MISSION_PROFILE, mission_status, detect_mission_drift, optimization_vs_purpose, humility_safeguards, anchor_note, anti_hollowing

router = APIRouter()

@router.get('/constitution')
async def get_constitution(db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(ConstitutionalRule).order_by(ConstitutionalRule.id.asc()))
    rows = q.scalars().all()
    if not rows:
        for idx, text in enumerate(CONSTITUTIONAL_RULES, start=1):
            db.add(ConstitutionalRule(rule_key=f"rule_{idx}", rule_text=text, enabled=True))
        await db.commit()
        q = await db.execute(select(ConstitutionalRule).order_by(ConstitutionalRule.id.asc()))
        rows = q.scalars().all()
    return {"rules": [{"key": r.rule_key, "text": r.rule_text, "enabled": r.enabled} for r in rows], "no_execution": True}

@router.post('/validate-consistency')
async def post_validate_consistency(body: dict):
    return validate_consistency(body)

@router.get('/explainability-score')
async def get_explainability_score():
    payload = {
        "evidence_completeness": 0.82,
        "reproducibility_coverage": 0.85,
        "narrative_consistency": 0.78,
        "recommendation_traceability": 0.8,
        "audit_completeness": 0.81,
        "governance_compliance": 0.92,
    }
    return explainability_score(payload)

@router.post('/trust-pressure')
async def get_trust_pressure(body: dict):
    return trust_pressure(body)

@router.post('/recommendation/enrich')
async def enrich_recommendation(body: dict, db: AsyncSession = Depends(get_db)):
    enriched = recommendation_with_trust_fields(body)
    lifecycle = RecommendationLifecycle(
        recommendation_key=str(body.get("recommendation_key", body.get("recommendation", "unknown"))),
        state=body.get("state", "active"),
        evidence_strength=float(body.get("evidence_coverage", 0.7)),
        contradicted=bool(body.get("contradicted", False)),
        governance_concern=bool(body.get("governance_concern", False)),
        changes=body.get("changes", []),
    )
    db.add(lifecycle)
    await db.commit()
    return {"recommendation": enriched, "auto_apply": False}

@router.get('/continuity/summary')
async def continuity_summary(db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(StrategicMemoryEvent).order_by(StrategicMemoryEvent.created_at.desc()).limit(500))
    rows = q.scalars().all()
    return {
        "yearly_strategic_summaries": [r.details for r in rows[:5]],
        "major_regime_eras": [r.title for r in rows if "regime" in r.event_type][:10],
        "major_governance_events": [r.title for r in rows if "governance" in r.event_type][:10],
        "historical_reliability_eras": [r.title for r in rows if "reliability" in r.event_type][:10],
        "major_anomaly_eras": [r.title for r in rows if "anomaly" in r.event_type][:10],
        "major_adaptation_cycles": [r.title for r in rows if "adapt" in r.event_type][:10],
    }

@router.post('/incidents')
async def create_incident(body: dict, db: AsyncSession = Depends(get_db)):
    inc = GovernanceIncident(
        incident_type=body.get("incident_type", "governance_rule_violation"),
        severity=body.get("severity", "warning"),
        details=body.get("details", {}),
        resolved=bool(body.get("resolved", False)),
    )
    db.add(inc); await db.commit(); await db.refresh(inc)
    return {"id": inc.id, "severity": inc.severity}

@router.get('/incidents')
async def list_incidents(db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(GovernanceIncident).order_by(GovernanceIncident.created_at.desc()).limit(200))
    rows = q.scalars().all()
    return [{"id": r.id, "incident_type": r.incident_type, "severity": r.severity, "resolved": r.resolved} for r in rows]

@router.post('/confidence/decay')
async def decay_confidence(body: dict):
    decayed = confidence_decay(
        float(body.get("confidence", 0.8)),
        int(body.get("days_stale", 0)),
        int(body.get("unresolved_anomalies", 0)),
        int(body.get("stale_replay_days", 0)),
    )
    return {"decayed_confidence": decayed}

@router.get('/assumptions')
async def assumptions(db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(StrategicAssumption).order_by(StrategicAssumption.last_validation_date.desc()).limit(200))
    rows = q.scalars().all()
    return [{"id": r.id, "assumption": r.assumption_text, "supporting_evidence": r.supporting_evidence, "contradictory_evidence": r.contradictory_evidence, "historical_confidence": r.historical_confidence, "last_validation_date": r.last_validation_date.isoformat(), "replay_coverage": r.replay_coverage, "regimes_affected": r.regimes_affected, "active": r.active} for r in rows]

@router.post('/assumptions')
async def create_assumption(body: dict, db: AsyncSession = Depends(get_db)):
    row = StrategicAssumption(
        assumption_text=body.get("assumption_text", ""),
        supporting_evidence=body.get("supporting_evidence", []),
        contradictory_evidence=body.get("contradictory_evidence", []),
        historical_confidence=float(body.get("historical_confidence", 0.7)),
        replay_coverage=float(body.get("replay_coverage", 0.5)),
        regimes_affected=body.get("regimes_affected", []),
        active=bool(body.get("active", True)),
    )
    db.add(row); await db.commit(); await db.refresh(row)
    return {"id": row.id}

@router.get('/coherence-status')
async def coherence_status():
    payload = {"evidence_quality": 0.8, "evidence_freshness": 0.75, "contradiction_density": 0.25, "unsupported_narrative_risk": 0.2, "stale_assumptions": 0.3, "circular_recommendation_logic": 0.1, "weak_inference_chains": 0.2, "fragmented_clusters": 1, "isolated_conclusions": 1, "recurring_governance_incidents": 1}
    return {"coherence_scores": evaluate_epistemic_integrity(payload), "advisory_only": True}

@router.post('/contradictions/workflow')
async def create_contradiction_workflow(body: dict, db: AsyncSession = Depends(get_db)):
    wf = ContradictionWorkflow(
        workflow_kind=body.get("workflow_kind", "contradiction_review"),
        state=body.get("state", "open"),
        linked_assumption_id=body.get("linked_assumption_id"),
        evidence_arbitration_notes=body.get("evidence_arbitration_notes", ""),
        recommendation_deprecation_candidates=body.get("recommendation_deprecation_candidates", []),
        stale_strategy_retirement_candidates=body.get("stale_strategy_retirement_candidates", []),
        review_history=body.get("review_history", []),
    )
    db.add(wf); await db.commit(); await db.refresh(wf)
    return {"id": wf.id, "state": wf.state}

@router.get('/contradictions/workflow')
async def list_contradiction_workflows(db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(ContradictionWorkflow).order_by(ContradictionWorkflow.created_at.desc()).limit(200))
    rows = q.scalars().all()
    return {"workflows": [{"id": r.id, "kind": r.workflow_kind, "state": r.state, "linked_assumption_id": r.linked_assumption_id} for r in rows]}

@router.post('/assumptions/decay')
async def decay_assumption(body: dict):
    return {"decayed_confidence": assumption_decay(float(body.get("confidence", 0.8)), int(body.get("days_since_validation", 30)), float(body.get("replay_coverage", 0.5)), int(body.get("contradictory_evidence_count", 0)))}

@router.post('/archive/stabilize')
async def stabilize_archive(body: dict):
    return {"stabilization": archive_stabilization(body.get("archives", []))}

@router.post('/knowledge/fragmentation')
async def knowledge_fragmentation(body: dict):
    return {"fragmentation": detect_knowledge_fragmentation(body.get("nodes", []), body.get("edges", []))}

@router.post('/review/gate')
async def review_gate(body: dict):
    return lifecycle_review_gate(body)

@router.get('/human-sovereignty')
async def human_sovereignty():
    return {"guarantees": SOVEREIGNTY_GUARANTEES, "human_final_authority": True, "auto_execution": False}

@router.post('/simplification/run')
async def run_simplification(body: dict):
    return {"simplification": simplification_engine(body), "advisory_only": True}

@router.post('/focus-mode')
async def focus_mode(body: dict):
    mode = body.get("mode", "stability_focus")
    insights = body.get("insights", [])
    return {"mode": mode, "prioritized_insights": apply_focus_mode(mode, insights), "explainable": True}

@router.post('/explainability/layers')
async def layered_explainability(body: dict):
    return explainability_layers(body)

@router.post('/strategic-reset')
async def strategic_reset(body: dict):
    return reset_action(str(body.get("action", "baseline_refresh")), bool(body.get("approved_by_human", False)))

@router.get('/lineage')
async def get_lineage(db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(EvolutionLineage).order_by(EvolutionLineage.created_at.desc()).limit(200))
    rows = q.scalars().all()
    return [{"id": r.id, "changed_component": r.changed_component, "why": r.why, "expected_impact": r.expected_impact, "affected_assumptions": r.affected_assumptions, "affected_narratives": r.affected_narratives, "affected_replay_validity": r.affected_replay_validity, "compatibility_notes": r.compatibility_notes, "created_at": r.created_at.isoformat()} for r in rows]

@router.post('/lineage')
async def create_lineage(body: dict, db: AsyncSession = Depends(get_db)):
    row = lineage_entry(body)
    rec = EvolutionLineage(**row)
    db.add(rec); await db.commit(); await db.refresh(rec)
    return {"id": rec.id}

@router.post('/migration/plan')
async def create_migration_plan(body: dict, db: AsyncSession = Depends(get_db)):
    plan = migration_plan(body)
    rec = InstitutionalMigration(
        target=plan["target"],
        plan=plan,
        reversible=plan["reversible"],
        operator_approved=plan["operator_approved"],
        status=plan["status"],
    )
    db.add(rec); await db.commit(); await db.refresh(rec)
    return {"id": rec.id, "status": rec.status}

@router.get('/migration/plan')
async def list_migration_plans(db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(InstitutionalMigration).order_by(InstitutionalMigration.created_at.desc()).limit(200))
    rows = q.scalars().all()
    return {"plans": [{"id": r.id, "target": r.target, "status": r.status, "reversible": r.reversible, "operator_approved": r.operator_approved} for r in rows]}

@router.get('/survivability')
async def get_survivability():
    payload = {"architectural_survivability": 0.82, "migration_safety": 0.84, "replay_compatibility": 0.78, "governance_durability": 0.88, "archive_durability": 0.8, "institutional_continuity": 0.83, "operational_resilience": 0.79}
    return {"survivability": survivability_scores(payload), "human_oversight_required": True}

@router.post('/replay/compatibility')
async def replay_compatibility(body: dict):
    return replay_compatibility_mode(body)

@router.post('/deprecation/workflow')
async def create_deprecation_workflow(body: dict):
    return deprecation_workflow(body)

@router.post('/archive/durability')
async def archive_durability(body: dict):
    return archive_durability_check(body.get("items", []))

@router.get('/adaptability-status')
async def get_adaptability_status():
    payload = {
        "governance_responsiveness": 0.74,
        "recommendation_adaptability": 0.71,
        "workflow_adaptability": 0.69,
        "replay_adaptability": 0.7,
        "profile_adaptability": 0.73,
        "calibration_adaptability": 0.72,
        "archive_stagnation": 0.33,
        "innovation_pressure": 0.45,
    }
    return {"adaptability": adaptability_status(payload), "operator_review_required": True}

@router.post('/renewal/workflow')
async def create_renewal_workflow(body: dict, db: AsyncSession = Depends(get_db)):
    wf = renewal_workflow(body)
    rec = RenewalWorkflow(
        workflow_type=wf["workflow_type"],
        status=wf["status"],
        operator_reviewed=wf["operator_reviewed"],
        auditable=wf["auditable"],
        reproducible=wf["reproducible"],
        reversible=wf["reversible"],
        metadata=body,
    )
    db.add(rec); await db.commit(); await db.refresh(rec)
    return {"id": rec.id, "status": rec.status}

@router.get('/renewal/workflow')
async def list_renewal_workflows(db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(RenewalWorkflow).order_by(RenewalWorkflow.created_at.desc()).limit(200))
    rows = q.scalars().all()
    return {"workflows": [{"id": r.id, "type": r.workflow_type, "status": r.status, "operator_reviewed": r.operator_reviewed} for r in rows]}

@router.post('/evolution/plan')
async def create_evolution_plan(body: dict, db: AsyncSession = Depends(get_db)):
    out = evolution_plan(body)
    rec = EvolutionPlan(**out)
    db.add(rec); await db.commit(); await db.refresh(rec)
    return {"id": rec.id}

@router.get('/evolution/plan')
async def list_evolution_plans(db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(EvolutionPlan).order_by(EvolutionPlan.created_at.desc()).limit(200))
    rows = q.scalars().all()
    return [{"id": r.id, "proposed_evolution": r.proposed_evolution, "compatibility_impact": r.compatibility_impact, "replay_impact": r.replay_impact, "governance_impact": r.governance_impact, "operator_review_required": r.operator_review_required} for r in rows]

@router.post('/innovation/sandbox')
async def innovation_sandbox(body: dict):
    return sandbox_experiment(body)

@router.post('/anti-dogma/scan')
async def anti_dogma(body: dict):
    return anti_dogma_scan(body)

@router.get('/identity/health')
async def identity():
    return identity_health({})

@router.get('/glossary')
async def glossary(db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(GlossaryTerm).order_by(GlossaryTerm.term.asc()).limit(500))
    rows = q.scalars().all()
    return [{"id": r.id, "term": r.term, "canonical_definition": r.canonical_definition, "deprecated": r.deprecated, "related_concepts": r.related_concepts, "historical_meanings": r.historical_meanings, "replay_version_relevance": r.replay_version_relevance, "governance_impact": r.governance_impact} for r in rows]

@router.post('/glossary')
async def add_glossary_term(body: dict, db: AsyncSession = Depends(get_db)):
    row = GlossaryTerm(
        term=body.get("term", ""),
        canonical_definition=body.get("canonical_definition", ""),
        deprecated=bool(body.get("deprecated", False)),
        related_concepts=body.get("related_concepts", []),
        historical_meanings=body.get("historical_meanings", []),
        replay_version_relevance=body.get("replay_version_relevance", []),
        governance_impact=body.get("governance_impact", ""),
    )
    db.add(row); await db.commit(); await db.refresh(row)
    return {"id": row.id}

@router.get('/concept-lineage')
async def concept_lineage(db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(ConceptLineage).order_by(ConceptLineage.created_at.desc()).limit(500))
    rows = q.scalars().all()
    return [{"id": r.id, "concept": r.concept, "origin": r.origin, "revisions": r.revisions, "contradictions": r.contradictions, "retired_meanings": r.retired_meanings, "successor_concepts": r.successor_concepts, "confidence_evolution": r.confidence_evolution} for r in rows]

@router.post('/concept-lineage')
async def add_concept_lineage(body: dict, db: AsyncSession = Depends(get_db)):
    row = ConceptLineage(**concept_lineage_entry(body))
    db.add(row); await db.commit(); await db.refresh(row)
    return {"id": row.id}

@router.get('/mission')
async def mission():
    return MISSION_PROFILE

@router.get('/mission-status')
async def get_mission_status():
    return {"mission_status": mission_status({}), "human_intent_anchor_required": True}

@router.post('/mission-drift')
async def mission_drift(body: dict):
    return detect_mission_drift(body)

@router.post('/optimization-vs-purpose')
async def optimization_purpose(body: dict):
    return optimization_vs_purpose(body)

@router.post('/humility-safeguards')
async def humility(body: dict):
    return humility_safeguards(body)

@router.post('/anchor-note')
async def add_anchor_note(body: dict, db: AsyncSession = Depends(get_db)):
    data = anchor_note(body)
    row = MissionAnchor(**data)
    db.add(row); await db.commit(); await db.refresh(row)
    return {"id": row.id}

@router.get('/anchor-note')
async def list_anchor_notes(db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(MissionAnchor).order_by(MissionAnchor.created_at.desc()).limit(300))
    rows = q.scalars().all()
    return [{"id": r.id, "operator_note": r.operator_note, "mission_reaffirmation": r.mission_reaffirmation, "long_horizon_intent": r.long_horizon_intent, "reset_intent": r.reset_intent, "anti_drift_confirmation": r.anti_drift_confirmation, "created_at": r.created_at.isoformat()} for r in rows]

@router.post('/anti-hollowing')
async def anti_hollow(body: dict):
    return anti_hollowing(body)

@router.post('/mission-timeline/event')
async def add_mission_timeline_event(body: dict, db: AsyncSession = Depends(get_db)):
    row = MissionTimelineEvent(
        event_type=body.get("event_type", "mission_revision"),
        details=body.get("details", {}),
        severity=body.get("severity", "info"),
    )
    db.add(row); await db.commit(); await db.refresh(row)
    return {"id": row.id}
