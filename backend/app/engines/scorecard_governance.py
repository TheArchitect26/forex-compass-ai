from __future__ import annotations

from app.engines.architectural_coherence import coherence_status
from app.engines.controlled_evolution import evolution_control_status
from app.engines.feature_flag_governance import feature_flags_status
from app.engines.institutional_evaluation import evaluation_status
from app.engines.platform_catalog import platform_catalog_status
from app.engines.refactoring_intelligence import refactoring_status
from app.engines.release_governance import release_status
from app.engines.runtime_observability import observability_status
from app.engines.technical_debt_observatory import debt_status
from app.engines.operator_experience import ux_status

SCORECARD_CATEGORIES = [
    "production_readiness", "ownership_readiness", "documentation_readiness", "test_readiness", "migration_readiness",
    "frontend_api_alignment", "observability_readiness", "release_safety", "lifecycle_governance", "operator_usability",
]


def _integration_snapshot() -> dict:
    return {
        "platform_catalog": platform_catalog_status(),
        "feature_flags": feature_flags_status(),
        "controlled_evolution": evolution_control_status(),
        "evaluation": evaluation_status(),
        "release": release_status(),
        "observability": observability_status(),
        "technical_debt": debt_status(),
        "ux": ux_status(),
        "architecture": coherence_status(),
        "refactoring": refactoring_status(),
    }


def scorecard_status() -> dict:
    return {
        "scorecard_categories": SCORECARD_CATEGORIES,
        "overall_score": 0.72,
        "readiness_level": "developing",
        "evidence_strength": "moderate",
        "gap_severity": "moderate",
        "improvement_priority": "high",
        "pass_fail_status": "conditional_pass",
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
        "never_auto_pass_capabilities": True,
        "never_auto_change_lifecycle_state": True,
        "never_auto_create_files": True,
        "never_auto_register_routers": True,
        "never_auto_run_migrations": True,
    }


def evaluate_scorecards(payload: dict) -> dict:
    return {
        "overall_score": payload.get("overall_score", 0.72),
        "category_scores": payload.get("category_scores", {
            "production_readiness": 0.74,
            "ownership_readiness": 0.68,
            "documentation_readiness": 0.71,
            "test_readiness": 0.69,
            "migration_readiness": 0.73,
            "frontend_api_alignment": 0.70,
            "observability_readiness": 0.72,
            "release_safety": 0.75,
            "lifecycle_governance": 0.70,
            "operator_usability": 0.74,
        }),
        "pass_fail_status": payload.get("pass_fail_status", "conditional_pass"),
        "readiness_level": payload.get("readiness_level", "developing"),
        "evidence_strength": payload.get("evidence_strength", "moderate"),
        "gap_severity": payload.get("gap_severity", "moderate"),
        "improvement_priority": payload.get("improvement_priority", "high"),
        "human_review_requirement": True,
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
    }


def entity_scorecard(payload: dict) -> dict:
    return {
        "entity_name": payload.get("entity_name", "platform_catalog"),
        "entity_type": payload.get("entity_type", "engine"),
        "scorecard": payload.get("scorecard", {
            "owner_present": True,
            "lifecycle_state_present": True,
            "readme_coverage": "partial",
            "tests_present": True,
            "migration_present_if_needed": True,
            "router_registered_if_api": True,
            "frontend_visibility_if_operator_facing": True,
            "validation_commands_present": True,
            "advisory_safeguards_present": True,
            "no_execution_guarantee_present": True,
        }),
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
    }


def readiness_gates(payload: dict) -> dict:
    return {
        "missing_tests": payload.get("missing_tests", ["capability_without_phase_test"]),
        "missing_documentation": payload.get("missing_documentation", ["capability_not_listed_in_readme"]),
        "missing_owner": payload.get("missing_owner", ["orphan_capability_owner"]),
        "missing_migration": payload.get("missing_migration", ["persistence_change_without_phase_sql"]),
        "missing_frontend_api_alignment": payload.get("missing_frontend_api_alignment", ["frontend_console_without_api_binding"]),
        "weak_observability": payload.get("weak_observability", ["capability_without_runtime_signals"]),
        "weak_release_validation": payload.get("weak_release_validation", ["release_checklist_missing_validation_step"]),
        "unclear_lifecycle_state": payload.get("unclear_lifecycle_state", ["lifecycle_state_unspecified"]),
        "unregistered_router": payload.get("unregistered_router", ["new_api_router_not_in_main"]),
        "orphaned_frontend_console": payload.get("orphaned_frontend_console", ["/unmapped-console"]),
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
    }


def improvement_plan(payload: dict) -> dict:
    return {
        "improvements": payload.get("improvements", [
            "add missing tests",
            "add missing README section",
            "clarify ownership",
            "add migration",
            "register router",
            "add frontend console link",
            "improve observability",
            "strengthen validation",
            "consolidate weak capability",
            "mark capability for review",
        ]),
        "priority_order": payload.get("priority_order", [
            "missing owner",
            "unregistered router",
            "missing tests",
            "missing documentation",
            "weak observability",
        ]),
        "human_review_required": True,
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
    }


def scorecard_memory() -> dict:
    return {
        "scorecard_snapshots": ["phase56_scorecard_baseline"],
        "readiness_gate_reviews": ["ownership/docs/tests/migration alignment tracked"],
        "gap_detection_reviews": ["gaps triaged by severity and priority"],
        "improvement_plan_reviews": ["human-reviewed quality gate plan drafted"],
        "integration_snapshot": _integration_snapshot(),
        "safety_principles": [
            "never auto-pass capabilities",
            "never auto-change lifecycle state",
            "never auto-create files",
            "never auto-register routers",
            "never auto-run migrations",
            "human approval required for quality-gate decisions",
        ],
    }
