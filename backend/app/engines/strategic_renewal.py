from __future__ import annotations
from datetime import UTC, datetime


def adaptability_status(payload: dict) -> dict:
    governance_resp = float(payload.get("governance_responsiveness", 0.7))
    recommendation_adapt = float(payload.get("recommendation_adaptability", 0.7))
    workflow_adapt = float(payload.get("workflow_adaptability", 0.7))
    replay_adapt = float(payload.get("replay_adaptability", 0.7))
    profile_adapt = float(payload.get("profile_adaptability", 0.7))
    calibration_adapt = float(payload.get("calibration_adaptability", 0.7))

    strategic_inertia = round((1 - recommendation_adapt) * 100, 2)
    governance_inertia = round((1 - governance_resp) * 100, 2)
    replay_rigidity = round((1 - replay_adapt) * 100, 2)
    archive_stagnation = round(float(payload.get("archive_stagnation", 0.3)) * 100, 2)
    workflow_stagnation = round((1 - workflow_adapt) * 100, 2)
    adaptation_responsiveness = round((governance_resp + recommendation_adapt + workflow_adapt + replay_adapt + profile_adapt + calibration_adapt) / 6 * 100, 2)
    innovation_pressure = round(float(payload.get("innovation_pressure", 0.4)) * 100, 2)

    return {
        "strategic_inertia": strategic_inertia,
        "governance_inertia": governance_inertia,
        "replay_rigidity": replay_rigidity,
        "archive_stagnation": archive_stagnation,
        "workflow_stagnation": workflow_stagnation,
        "adaptation_responsiveness": adaptation_responsiveness,
        "innovation_pressure": innovation_pressure,
    }


def anti_dogma_scan(payload: dict) -> dict:
    warnings = []
    if int(payload.get("unchallenged_assumptions", 0)) > 5:
        warnings.append("assumptions_never_challenged")
    if int(payload.get("stale_narratives", 0)) > 4:
        warnings.append("stale_strategic_narratives")
    if float(payload.get("governance_ossification", 0)) > 0.6:
        warnings.append("governance_ossification")
    if float(payload.get("replay_lock_in", 0)) > 0.6:
        warnings.append("replay_methodology_lock_in")
    if float(payload.get("recommendation_monoculture", 0)) > 0.6:
        warnings.append("recommendation_monoculture")
    if float(payload.get("evidence_stagnation", 0)) > 0.6:
        warnings.append("evidence_stagnation")
    recommendations = [
        "schedule assumption renewal review",
        "run sandbox methodology refresh",
        "prioritize diversification of recommendation strategies",
    ] if warnings else ["continue monitored renewal cadence"]
    return {"warnings": warnings, "renewal_recommendations": recommendations, "advisory_only": True}


def renewal_workflow(item: dict) -> dict:
    return {
        "workflow_type": item.get("workflow_type", "assumption_renewal"),
        "operator_reviewed": bool(item.get("operator_reviewed", False)),
        "auditable": True,
        "reproducible": True,
        "reversible": bool(item.get("reversible", True)),
        "status": "approved" if item.get("operator_reviewed", False) else "pending_review",
    }


def evolution_plan(payload: dict) -> dict:
    return {
        "proposed_evolution": payload.get("proposed_evolution", "unspecified"),
        "rationale": payload.get("rationale", ""),
        "affected_systems": payload.get("affected_systems", []),
        "compatibility_impact": payload.get("compatibility_impact", "low"),
        "replay_impact": payload.get("replay_impact", "low"),
        "governance_impact": payload.get("governance_impact", "medium"),
        "survivability_impact": payload.get("survivability_impact", "medium"),
        "rollback_strategy": payload.get("rollback_strategy", "manual rollback plan"),
        "created_at": datetime.now(UTC).isoformat(),
        "operator_review_required": True,
    }


def identity_health(payload: dict) -> dict:
    return {
        "constitutional_principles_preserved": bool(payload.get("constitutional_principles_preserved", True)),
        "strategic_philosophy_continuity": float(payload.get("strategic_philosophy_continuity", 0.85)),
        "governance_identity": float(payload.get("governance_identity", 0.85)),
        "explainability_identity": float(payload.get("explainability_identity", 0.9)),
        "human_sovereignty_guarantees": bool(payload.get("human_sovereignty_guarantees", True)),
        "institutional_mission_continuity": float(payload.get("institutional_mission_continuity", 0.88)),
    }


def sandbox_experiment(payload: dict) -> dict:
    return {
        "experiment_type": payload.get("experiment_type", "governance_experiment"),
        "sandboxed": True,
        "auto_promote": False,
        "reproducible": True,
        "continuity_lineage_preserved": True,
        "result": payload.get("result", "pending"),
    }
