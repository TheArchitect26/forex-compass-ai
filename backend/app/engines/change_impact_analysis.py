from __future__ import annotations

from app.engines.architectural_coherence import coherence_status
from app.engines.controlled_evolution import evolution_control_status
from app.engines.feature_flag_governance import feature_flags_status
from app.engines.golden_path_workflows import golden_paths_status
from app.engines.institutional_evaluation import evaluation_status
from app.engines.platform_catalog import platform_catalog_status
from app.engines.refactoring_intelligence import refactoring_status
from app.engines.release_governance import release_status
from app.engines.runtime_observability import observability_status
from app.engines.scorecard_governance import scorecard_status
from app.engines.technical_debt_observatory import debt_status
from app.engines.operator_experience import ux_status

CHANGE_TYPES = [
    "new_phase", "backend_engine_change", "api_router_change", "frontend_console_change", "migration_change",
    "dependency_change", "release_change", "feature_flag_change", "governance_change", "refactor_change",
    "retirement_change", "emergency_fix",
]


def _integration_snapshot() -> dict:
    return {
        "platform_catalog": platform_catalog_status(),
        "scorecards": scorecard_status(),
        "golden_paths": golden_paths_status(),
        "release": release_status(),
        "observability": observability_status(),
        "technical_debt": debt_status(),
        "feature_flags": feature_flags_status(),
        "controlled_evolution": evolution_control_status(),
        "architecture": coherence_status(),
        "refactoring": refactoring_status(),
        "ux": ux_status(),
        "evaluation": evaluation_status(),
    }


def change_control_status() -> dict:
    return {
        "change_types": CHANGE_TYPES,
        "change_impact_score": 0.58,
        "implementation_risk_score": 0.47,
        "dependency_risk_score": 0.44,
        "migration_risk_score": 0.39,
        "rollback_complexity_score": 0.42,
        "review_urgency_score": 0.55,
        "operator_impact_score": 0.51,
        "production_safety_score": 0.74,
        "approval_readiness_score": 0.69,
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
        "never_auto_approve_changes": True,
        "never_auto_reject_changes": True,
        "never_run_commands": True,
        "never_create_commits": True,
        "never_deploy": True,
        "never_rollback": True,
        "never_run_migrations": True,
    }


def impact_analysis(payload: dict) -> dict:
    return {
        "affected_systems": payload.get("affected_systems", ["backend/api", "backend/engines", "frontend/consoles"]),
        "affected_files": payload.get("affected_files", ["backend/app/main.py", "backend/app/engines/<module>.py", "frontend/app/<console>/page.tsx"]),
        "upstream_dependencies": payload.get("upstream_dependencies", ["platform_catalog", "scorecard_governance", "release_governance"]),
        "downstream_dependents": payload.get("downstream_dependents", ["operator_console", "executive_console", "change_control_console"]),
        "risk_level": payload.get("risk_level", "moderate"),
        "required_tests": payload.get("required_tests", ["phase-targeted pytest", "regression checks"]),
        "required_docs": payload.get("required_docs", ["README phase section", "change summary notes"]),
        "required_migrations": payload.get("required_migrations", ["phase migration when persistence changes"]),
        "required_scorecard_checks": payload.get("required_scorecard_checks", ["production_readiness", "test_readiness", "release_safety"]),
        "required_rollback_notes": payload.get("required_rollback_notes", ["revert commit path", "rollback verification steps"]),
        "required_human_reviewers": payload.get("required_human_reviewers", ["release reviewer", "architecture reviewer", "operator reviewer"]),
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
    }


def review_requirements(payload: dict) -> dict:
    return {
        "normal_review": payload.get("normal_review", True),
        "release_review": payload.get("release_review", True),
        "architecture_review": payload.get("architecture_review", True),
        "security_secrets_review": payload.get("security_secrets_review", False),
        "migration_review": payload.get("migration_review", True),
        "ux_review": payload.get("ux_review", True),
        "governance_review": payload.get("governance_review", True),
        "emergency_review": payload.get("emergency_review", False),
        "rollback_review": payload.get("rollback_review", True),
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
    }


def rollback_readiness(payload: dict) -> dict:
    return {
        "rollback_plan_present": payload.get("rollback_plan_present", True),
        "rollback_steps_documented": payload.get("rollback_steps_documented", True),
        "rollback_validation_commands": payload.get("rollback_validation_commands", ["run targeted pytest", "verify health endpoint", "verify affected APIs"]),
        "rollback_owner_assigned": payload.get("rollback_owner_assigned", True),
        "rollback_risk_level": payload.get("rollback_risk_level", "moderate"),
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
    }


def approval_brief(payload: dict) -> dict:
    return {
        "change_summary": payload.get("change_summary", "Proposed backend/frontend governance capability update"),
        "reason_for_change": payload.get("reason_for_change", "Improve institutional visibility and safety review consistency"),
        "affected_systems": payload.get("affected_systems", ["api", "engines", "frontend", "docs"]),
        "expected_benefit": payload.get("expected_benefit", "clearer governance, safer releases, and reduced change ambiguity"),
        "risk_if_approved": payload.get("risk_if_approved", "moderate implementation complexity and coupling risk"),
        "risk_if_rejected": payload.get("risk_if_rejected", "continued governance blind spots and slower review cycles"),
        "validation_plan": payload.get("validation_plan", ["run phase tests", "compile touched backend files", "review endpoint responses"]),
        "rollback_plan": payload.get("rollback_plan", ["revert commit", "restore prior router state", "re-run validation checks"]),
        "open_questions": payload.get("open_questions", ["Are additional observability hooks required?", "Is migration sequencing acceptable?"]),
        "human_approval_required": True,
        "advisory_only": True,
        "auto_apply": False,
    }


def change_control_memory() -> dict:
    return {
        "impact_snapshots": ["phase58_change_control_baseline"],
        "review_requirement_snapshots": ["review board requirements tracked"],
        "rollback_readiness_snapshots": ["rollback plans and ownership checks recorded"],
        "approval_brief_snapshots": ["human-readable approval briefs retained"],
        "integration_snapshot": _integration_snapshot(),
        "safety_principles": [
            "never auto-approve changes",
            "never auto-reject changes",
            "never run commands",
            "never create commits",
            "never deploy",
            "never rollback",
            "never run migrations",
            "human approval required for change decisions",
        ],
    }
