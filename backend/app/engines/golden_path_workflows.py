from __future__ import annotations

from app.engines.architectural_coherence import coherence_status
from app.engines.controlled_evolution import evolution_control_status
from app.engines.feature_flag_governance import feature_flags_status
from app.engines.institutional_evaluation import evaluation_status
from app.engines.platform_catalog import platform_catalog_status
from app.engines.refactoring_intelligence import refactoring_status
from app.engines.release_governance import release_status
from app.engines.runtime_observability import observability_status
from app.engines.scorecard_governance import scorecard_status
from app.engines.technical_debt_observatory import debt_status
from app.engines.operator_experience import ux_status

WORKFLOW_TYPES = [
    "phase_addition", "api_addition", "frontend_console_addition", "migration_addition", "test_addition",
    "release_preparation", "incident_review", "capability_retirement", "capability_consolidation",
    "documentation_update", "scorecard_remediation",
]


def _integration_snapshot() -> dict:
    return {
        "platform_catalog": platform_catalog_status(),
        "scorecards": scorecard_status(),
        "release": release_status(),
        "observability": observability_status(),
        "technical_debt": debt_status(),
        "feature_flags": feature_flags_status(),
        "controlled_evolution": evolution_control_status(),
        "ux": ux_status(),
        "architecture": coherence_status(),
        "refactoring": refactoring_status(),
        "evaluation": evaluation_status(),
    }


def golden_paths_status() -> dict:
    return {
        "workflow_types": WORKFLOW_TYPES,
        "workflow_completeness_score": 0.75,
        "safety_coverage_score": 0.78,
        "reversibility_score": 0.71,
        "validation_readiness_score": 0.74,
        "documentation_readiness_score": 0.72,
        "operator_clarity_score": 0.76,
        "governance_alignment_score": 0.77,
        "execution_risk_score": 0.36,
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
        "never_auto_create_files": True,
        "never_auto_run_commands": True,
        "never_auto_commit_changes": True,
        "never_auto_register_routers": True,
        "never_auto_run_migrations": True,
        "never_force_workflow_without_human_approval": True,
    }


def workflow(payload: dict) -> dict:
    return {
        "workflow_name": payload.get("workflow_name", "add_new_api_router"),
        "guided_steps": payload.get("guided_steps", [
            "define scope and ownership",
            "create engine or API module",
            "add tests and validation commands",
            "register router and frontend visibility if operator-facing",
            "update README and safety notes",
            "run validation and prepare rollback notes",
        ]),
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
    }


def checklist(payload: dict) -> dict:
    return {
        "required_files": payload.get("required_files", ["backend/app/engines/<module>.py", "backend/app/api/<router>.py", "backend/app/main.py", "backend/tests/test_phaseXX_<name>.py", "README.md"]),
        "required_tests": payload.get("required_tests", ["phase-focused pytest", "py_compile touched backend files"]),
        "required_readme_update": payload.get("required_readme_update", True),
        "required_migration_if_persistence_exists": payload.get("required_migration_if_persistence_exists", True),
        "required_router_registration_if_api_exists": payload.get("required_router_registration_if_api_exists", True),
        "required_frontend_sidebar_if_operator_facing": payload.get("required_frontend_sidebar_if_operator_facing", True),
        "validation_commands": payload.get("validation_commands", ["PYTHONPATH=backend pytest -q backend/tests/test_phaseXX_<name>.py", "python -m py_compile backend/app/main.py"]),
        "rollback_notes": payload.get("rollback_notes", "revert change set and unregister related router entries after human review"),
        "scorecard_checks": payload.get("scorecard_checks", ["ownership_readiness", "test_readiness", "release_safety", "observability_readiness"]),
        "human_approval_required": True,
        "advisory_only": True,
        "auto_apply": False,
    }


def validate_plan(payload: dict) -> dict:
    return {
        "platform_catalog_alignment": payload.get("platform_catalog_alignment", "aligned"),
        "scorecard_alignment": payload.get("scorecard_alignment", "conditional_pass"),
        "technical_debt_alignment": payload.get("technical_debt_alignment", "watch"),
        "release_readiness_alignment": payload.get("release_readiness_alignment", "moderate"),
        "feature_flag_governance_alignment": payload.get("feature_flag_governance_alignment", "aligned"),
        "controlled_evolution_alignment": payload.get("controlled_evolution_alignment", "aligned"),
        "ux_quality_alignment": payload.get("ux_quality_alignment", "monitor"),
        "no_execution_safeguards": payload.get("no_execution_safeguards", "confirmed"),
        "validation_readiness": payload.get("validation_readiness", "ready_with_human_review"),
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
    }


def deviation_review(payload: dict) -> dict:
    return {
        "deviation_reason": payload.get("deviation_reason", "time-sensitive release patch requiring narrower workflow"),
        "risk_introduced": payload.get("risk_introduced", "moderate"),
        "affected_standards": payload.get("affected_standards", ["documentation_update", "frontend_api_alignment"]),
        "compensating_controls": payload.get("compensating_controls", ["extra peer review", "post-release validation", "temporary feature flag"]),
        "required_human_review": True,
        "rollback_recovery_notes": payload.get("rollback_recovery_notes", "revert commit, disable affected route via manual rollback, and re-run validation checks"),
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
    }


def golden_paths_memory() -> dict:
    return {
        "workflow_snapshots": ["phase57_golden_path_workflow_baseline"],
        "checklist_snapshots": ["required files/tests/readme/migration/router/sidebar/validation/rollback tracked"],
        "plan_validation_reviews": ["catalog/scorecard/release/safety alignment reviewed"],
        "deviation_reviews": ["safe deviation records with compensating controls"],
        "integration_snapshot": _integration_snapshot(),
        "safety_principles": [
            "never auto-create files",
            "never auto-run commands",
            "never auto-commit changes",
            "never auto-register routers",
            "never auto-run migrations",
            "never force workflows without human approval",
        ],
    }
