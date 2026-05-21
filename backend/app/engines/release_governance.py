from __future__ import annotations

from app.engines.architectural_coherence import coherence_status
from app.engines.ecosystem_intelligence import ecosystem_status
from app.engines.evolutionary_resilience import evolution_status
from app.engines.meta_governance import metagovernance_status
from app.engines.operational_orchestration import operational_status
from app.engines.refactoring_intelligence import refactoring_status
from app.engines.technical_debt_observatory import debt_status, dependency_risk
from app.engines.trust_calibration import trust_status

REQUIRED_ENV_VARS = [
    "DATABASE_URL",
    "REDIS_URL",
    "SECRET_KEY",
    "ACCESS_TOKEN_EXPIRE_MINUTES",
    "NEXT_PUBLIC_API_URL",
]


def _integration_snapshot() -> dict:
    return {
        "technical_debt": debt_status(),
        "dependency_risk": dependency_risk({}),
        "ecosystem": ecosystem_status(),
        "refactoring": refactoring_status(),
        "evolutionary_resilience": evolution_status(),
        "operations": operational_status(),
        "architecture": coherence_status(),
        "trust_calibration": trust_status(),
        "meta_governance": metagovernance_status(),
    }


def release_status() -> dict:
    return {
        "build_readiness": "caution",
        "deployment_readiness": "caution",
        "rollback_readiness": "moderate",
        "test_confidence": 0.74,
        "dependency_stability": 0.62,
        "migration_safety": 0.63,
        "environment_variable_completeness": 0.72,
        "frontend_backend_route_compatibility": 0.69,
        "vercel_serverless_compatibility": 0.66,
        "post_release_monitoring_readiness": 0.71,
        "release_readiness_score": 0.68,
        "build_confidence_score": 0.67,
        "deployment_risk_score": 0.42,
        "rollback_readiness_score": 0.64,
        "migration_risk_score": 0.37,
        "environment_readiness_score": 0.72,
        "post_release_monitoring_score": 0.71,
        "production_suitability_score": 0.66,
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
        "never_auto_deploy": True,
        "never_auto_rollback": True,
        "never_auto_run_migrations": True,
        "never_auto_change_env": True,
    }


def release_readiness_check(payload: dict) -> dict:
    return {
        "checklist": {
            "backend_compiles": payload.get("backend_compiles", True),
            "frontend_builds": payload.get("frontend_builds", True),
            "tests_pass": payload.get("tests_pass", True),
            "dependency_resolver_works": payload.get("dependency_resolver_works", True),
            "python_version_locked": payload.get("python_version_locked", False),
            "node_next_version_acceptable": payload.get("node_next_version_acceptable", True),
            "required_env_vars_documented": payload.get("required_env_vars_documented", REQUIRED_ENV_VARS),
            "migrations_present": payload.get("migrations_present", True),
            "api_route_prefix_correct": payload.get("api_route_prefix_correct", True),
            "frontend_api_base_matches_deploy_config": payload.get("frontend_api_base_matches_deploy_config", True),
            "no_unsupported_serverless_assumptions": payload.get("no_unsupported_serverless_assumptions", False),
            "rollback_plan_exists": payload.get("rollback_plan_exists", True),
        },
        "release_readiness_score": payload.get("release_readiness_score", 0.68),
        "environment_readiness_score": payload.get("environment_readiness_score", 0.72),
        "production_suitability_score": payload.get("production_suitability_score", 0.66),
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
    }


def build_risk(payload: dict) -> dict:
    return {
        "unresolved_dependency_versions": payload.get("unresolved_dependency_versions", ["mixed strict/loose pins can drift between environments"]),
        "deprecated_nextjs_warnings": payload.get("deprecated_nextjs_warnings", []),
        "missing_python_version_lock": payload.get("missing_python_version_lock", True),
        "frontend_backend_api_mismatch": payload.get("frontend_backend_api_mismatch", ["frontend console assumes routes that may not be enabled in all deployments"]),
        "migration_drift": payload.get("migration_drift", ["schema version endpoint lags recent migration phases"]),
        "serverless_cold_start_risk": payload.get("serverless_cold_start_risk", "moderate"),
        "missing_production_env_vars": payload.get("missing_production_env_vars", ["explicit production checklist not centrally enforced"]),
        "unsafe_fallback_assumptions": payload.get("unsafe_fallback_assumptions", ["synthetic fallback should never be interpreted as execution-grade live feed"]),
        "test_gaps_new_routers": payload.get("test_gaps_new_routers", ["limited end-to-end route compatibility tests across growing API surface"]),
        "deployment_risk_score": payload.get("deployment_risk_score", 0.42),
        "build_confidence_score": payload.get("build_confidence_score", 0.67),
        "migration_risk_score": payload.get("migration_risk_score", 0.37),
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
    }


def rollback_plan(payload: dict) -> dict:
    return {
        "rollback_steps": payload.get("rollback_steps", [
            "revert offending commit and rebuild artifacts",
            "restore previous environment-variable snapshot",
            "pause new release route usage behind feature toggle",
            "disable frontend Release console entry if needed",
            "restore previous dependency lock files",
            "issue database rollback warning and review irreversible operations",
            "apply migration caution: prefer forward-fix when rollback is unsafe",
            "run post-rollback validation checklist",
        ]),
        "database_rollback_warning": payload.get("database_rollback_warning", "Do not auto-rollback schema changes; require explicit human DBA review."),
        "migration_caution": payload.get("migration_caution", "Some migrations may be non-reversible; use forward remediation when needed."),
        "post_rollback_validation": payload.get("post_rollback_validation", ["health checks", "critical route checks", "env completeness checks", "operator sign-off"]),
        "rollback_readiness_score": payload.get("rollback_readiness_score", 0.64),
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
        "never_auto_rollback": True,
    }


def post_release_review(payload: dict) -> dict:
    return {
        "build_result": payload.get("build_result", "unknown"),
        "deployment_result": payload.get("deployment_result", "unknown"),
        "runtime_errors": payload.get("runtime_errors", []),
        "failed_api_routes": payload.get("failed_api_routes", []),
        "missing_env_vars": payload.get("missing_env_vars", []),
        "unexpected_warnings": payload.get("unexpected_warnings", []),
        "operator_review_notes": payload.get("operator_review_notes", []),
        "follow_up_debt_items": payload.get("follow_up_debt_items", []),
        "post_release_monitoring_score": payload.get("post_release_monitoring_score", 0.71),
        "human_approval_required": True,
        "advisory_only": True,
        "auto_apply": False,
    }


def release_memory() -> dict:
    return {
        "release_audits": ["phase46_release_governance_baseline"],
        "deployment_risk_reviews": ["dependency drift and env readiness monitored"],
        "rollback_reviews": ["human-reviewed rollback playbook maintained"],
        "post_release_reviews": ["runtime and route health tracked post-release"],
        "integration_snapshot": _integration_snapshot(),
        "safety_principles": [
            "never auto-deploy",
            "never auto-rollback",
            "never auto-run migrations",
            "never auto-change environment variables",
            "human approval required for all release actions",
        ],
    }
