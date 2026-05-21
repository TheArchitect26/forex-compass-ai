from __future__ import annotations

from app.engines.architectural_coherence import coherence_status
from app.engines.controlled_evolution import evolution_control_status
from app.engines.ecosystem_intelligence import ecosystem_status
from app.engines.institutional_evaluation import evaluation_status
from app.engines.operator_experience import ux_status
from app.engines.refactoring_intelligence import refactoring_status
from app.engines.release_governance import release_status
from app.engines.runtime_observability import observability_status
from app.engines.technical_debt_observatory import debt_status

FLAG_LIFECYCLE_STATES = [
    "proposed", "experimental", "rollout", "active", "stable", "cleanup_due", "stale", "deprecated", "retired_candidate", "permanent_control",
]


def _integration_snapshot() -> dict:
    return {
        "controlled_evolution": evolution_control_status(), "release": release_status(), "observability": observability_status(),
        "technical_debt": debt_status(), "refactoring": refactoring_status(), "architecture": coherence_status(),
        "evaluation": evaluation_status(), "operator_experience": ux_status(), "ecosystem": ecosystem_status(),
    }


def feature_flags_status() -> dict:
    return {
        "flag_lifecycle_states": FLAG_LIFECYCLE_STATES,
        "flag_hygiene_score": 0.68,
        "lifecycle_clarity_score": 0.66,
        "stale_flag_risk_score": 0.41,
        "ownership_clarity_score": 0.62,
        "cleanup_urgency_score": 0.57,
        "complexity_risk_score": 0.49,
        "rollback_usefulness_score": 0.71,
        "operator_confusion_risk_score": 0.46,
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
        "never_auto_enable_flags": True,
        "never_auto_disable_flags": True,
        "never_auto_delete_flags": True,
        "never_auto_change_rollout_state": True,
        "never_auto_change_production_behavior": True,
    }


def _registry(payload: dict) -> list[dict]:
    return payload.get("registry_items", [
        {
            "flag_name": "control_plane_grouped_nav_experiment",
            "capability_controlled": "grouped sidebar navigation",
            "owner": "operator-experience",
            "lifecycle_state": "experimental",
            "created_at": "2026-05-20",
            "intended_lifespan_days": 30,
            "cleanup_due_at": "2026-06-19",
            "affected_systems": ["frontend/sidebar", "control-plane"],
            "default_state": "off",
            "rollback_role": "revert to current navigation",
            "operator_visibility": "high",
            "human_approval_required": True,
        },
        {
            "flag_name": "release_runtime_strict_parity_gate",
            "capability_controlled": "strict env/route parity check",
            "owner": "release-governance",
            "lifecycle_state": "rollout",
            "created_at": "2026-05-20",
            "intended_lifespan_days": 45,
            "cleanup_due_at": "2026-07-04",
            "affected_systems": ["backend/release", "backend/observability"],
            "default_state": "on",
            "rollback_role": "fall back to warning-only mode",
            "operator_visibility": "medium",
            "human_approval_required": True,
        },
    ])


def feature_flag_audit(payload: dict) -> dict:
    return {"registry": _registry(payload), "advisory_only": True, "auto_apply": False, "human_approval_required": True}


def stale_review(payload: dict) -> dict:
    return {
        "flags_with_no_owner": payload.get("flags_with_no_owner", ["legacy_experiment_flag_x"]),
        "flags_without_cleanup_date": payload.get("flags_without_cleanup_date", ["temporary_warning_mode_toggle"]),
        "flags_older_than_intended_lifespan": payload.get("flags_older_than_intended_lifespan", ["old_runtime_fallback_experiment"]),
        "flags_controlling_obsolete_features": payload.get("flags_controlling_obsolete_features", ["deprecated_console_gate"]),
        "duplicate_flags": payload.get("duplicate_flags", ["two toggles controlling similar nav grouping behavior"]),
        "unclear_default_behavior": payload.get("unclear_default_behavior", ["flag default differs by environment without docs"]),
        "permanent_temporary_flags": payload.get("permanent_temporary_flags", ["temporary rollout guard still active after stabilization"]),
        "complexity_increasing_flags": payload.get("complexity_increasing_flags", ["multiple nested gates around same code path"]),
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
    }


def cleanup_plan(payload: dict) -> dict:
    return {
        "cleanup_actions": payload.get("cleanup_actions", [
            "assign explicit owner to orphan flags",
            "set cleanup_due_at for every experimental flag",
            "retire obsolete feature gates",
            "merge duplicate flags controlling same capability",
            "document default behavior per environment",
            "archive resolved rollout toggles",
        ]),
        "priority_order": payload.get("priority_order", ["ownerless flags", "obsolete feature flags", "duplicate flags", "documentation gaps"]),
        "human_approval_required": True,
        "advisory_only": True,
        "auto_apply": False,
    }


def rollout_safety(payload: dict) -> dict:
    return {
        "blast_radius": payload.get("blast_radius", "moderate"),
        "rollback_usefulness": payload.get("rollback_usefulness", "high"),
        "testing_coverage": payload.get("testing_coverage", "moderate"),
        "dependency_risk": payload.get("dependency_risk", "moderate"),
        "migration_interaction": payload.get("migration_interaction", "low_to_moderate"),
        "frontend_backend_compatibility": payload.get("frontend_backend_compatibility", "monitor"),
        "operator_visibility": payload.get("operator_visibility", "medium"),
        "monitoring_readiness": payload.get("monitoring_readiness", "good"),
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
    }


def feature_flags_memory() -> dict:
    return {
        "flag_audit_snapshots": ["phase54_feature_flag_governance_baseline"],
        "stale_flag_reviews": ["ownerless and obsolete flags detected"],
        "cleanup_plan_reviews": ["human-reviewed cleanup sequence drafted"],
        "rollout_safety_reviews": ["flag rollout safety checklist recorded"],
        "integration_snapshot": _integration_snapshot(),
        "safety_principles": [
            "never auto-enable flags", "never auto-disable flags", "never auto-delete flags",
            "never auto-change rollout state", "never auto-change production behavior", "human approval required for flag changes",
        ],
    }
