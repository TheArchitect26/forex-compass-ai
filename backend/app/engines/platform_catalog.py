from __future__ import annotations

from app.engines.architectural_coherence import coherence_status
from app.engines.controlled_evolution import evolution_control_status
from app.engines.feature_flag_governance import feature_flags_status
from app.engines.institutional_evaluation import evaluation_status
from app.engines.knowledge_compression import compression_status
from app.engines.memory_retrieval import memory_status
from app.engines.operator_experience import ux_status
from app.engines.refactoring_intelligence import refactoring_status
from app.engines.release_governance import release_status
from app.engines.runtime_observability import observability_status
from app.engines.technical_debt_observatory import debt_status

ENTITY_TYPES = [
    "engine", "api_router", "frontend_console", "migration", "test_suite", "governance_layer",
    "release_system", "observability_system", "memory_system", "capability_flag", "operational_pathway", "golden_path",
]


def _integration_snapshot() -> dict:
    return {
        "feature_flags": feature_flags_status(),
        "controlled_evolution": evolution_control_status(),
        "evaluation": evaluation_status(),
        "technical_debt": debt_status(),
        "release": release_status(),
        "observability": observability_status(),
        "architecture": coherence_status(),
        "refactoring": refactoring_status(),
        "memory": memory_status(),
        "compression": compression_status(),
        "ux": ux_status(),
    }


def _entities(payload: dict) -> list[dict]:
    return payload.get("entities", [
        {
            "entity_name": "platform_catalog",
            "entity_type": "engine",
            "lifecycle_state": "active",
            "owner": "platform-governance",
            "description": "Institutional service catalog and governance scorecards",
            "related_phase": "phase55",
            "related_files": ["backend/app/engines/platform_catalog.py", "backend/app/api/platform_catalog.py"],
            "related_apis": ["/api/platform-catalog/status", "/api/platform-catalog/entities"],
            "related_frontend_page": "/platform-catalog",
            "dependencies": ["feature_flag_governance", "controlled_evolution", "release_governance"],
            "operational_importance": "high",
            "documentation_status": "documented",
            "human_review_required": True,
        },
        {
            "entity_name": "feature_flag_governance",
            "entity_type": "capability_flag",
            "lifecycle_state": "active",
            "owner": "release-governance",
            "description": "Toggle hygiene and lifecycle controls",
            "related_phase": "phase54",
            "related_files": ["backend/app/engines/feature_flag_governance.py"],
            "related_apis": ["/api/feature-flags/status", "/api/feature-flags/audit"],
            "related_frontend_page": "/feature-flags",
            "dependencies": ["runtime_observability", "technical_debt_observatory"],
            "operational_importance": "high",
            "documentation_status": "documented",
            "human_review_required": True,
        },
    ])


def platform_catalog_status() -> dict:
    return {
        "entity_types": ENTITY_TYPES,
        "catalog_completeness_score": 0.74,
        "ownership_clarity_score": 0.69,
        "documentation_readiness_score": 0.71,
        "operational_discoverability_score": 0.73,
        "dependency_clarity_score": 0.68,
        "lifecycle_clarity_score": 0.70,
        "golden_path_maturity_score": 0.66,
        "platform_coherence_score": 0.72,
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
        "never_auto_create_files": True,
        "never_auto_delete_capabilities": True,
        "never_auto_change_ownership": True,
        "never_auto_register_routers": True,
        "never_auto_run_migrations": True,
    }


def catalog_entities(payload: dict) -> dict:
    return {"entities": _entities(payload), "advisory_only": True, "auto_apply": False, "human_approval_required": True}


def ownership_audit(payload: dict) -> dict:
    return {
        "missing_owner": payload.get("missing_owner", ["legacy_console_x"]),
        "unclear_lifecycle_state": payload.get("unclear_lifecycle_state", ["experimental_panel_without_state"]),
        "missing_tests": payload.get("missing_tests", ["engine_without_phase_test"]),
        "missing_readme_documentation": payload.get("missing_readme_documentation", ["undocumented_operator_subsystem"]),
        "missing_migration_where_persistence_exists": payload.get("missing_migration_where_persistence_exists", ["new_table_declared_without_phase_sql"]),
        "frontend_page_without_api": payload.get("frontend_page_without_api", ["/orphan-console"]),
        "api_without_frontend_visibility": payload.get("api_without_frontend_visibility", ["/api/hidden-capability/status"]),
        "engine_without_tests": payload.get("engine_without_tests", ["orphan_engine_module"]),
        "orphaned_capability": payload.get("orphaned_capability", ["legacy_crosscutting_capability"]),
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
    }


def dependency_map(payload: dict) -> dict:
    return {
        "upstream_dependencies": payload.get("upstream_dependencies", ["release_governance", "runtime_observability", "technical_debt_observatory"]),
        "downstream_dependents": payload.get("downstream_dependents", ["operator_console", "executive_console", "platform_catalog_console"]),
        "related_subsystems": payload.get("related_subsystems", ["feature_flag_governance", "controlled_evolution", "institutional_evaluation"]),
        "risk_if_changed": payload.get("risk_if_changed", "moderate_to_high"),
        "operational_coupling": payload.get("operational_coupling", "moderate"),
        "consolidation_opportunity": payload.get("consolidation_opportunity", ["merge duplicate governance summaries", "unify lifecycle status cards"]),
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
    }


def golden_paths(payload: dict) -> dict:
    return {
        "golden_paths": payload.get("golden_paths", [
            {
                "path_name": "add_new_phase",
                "required_files": ["backend/app/engines/<engine>.py", "backend/tests/test_phaseXX_<name>.py", "backend/migrations/phaseXX_<name>.sql", "README.md"],
                "required_tests": ["phase unit tests", "py_compile touched backend files"],
                "required_readme_update": True,
                "required_router_registration": False,
                "required_migration_when_applicable": True,
                "validation_commands": ["PYTHONPATH=backend pytest -q backend/tests/test_phaseXX_<name>.py", "python -m py_compile backend/app/main.py"],
                "rollback_notes": "revert phase commit; keep schema migrations gated by human review",
                "human_approval_required": True,
            },
            {
                "path_name": "add_new_api",
                "required_files": ["backend/app/api/<route>.py", "backend/app/main.py", "backend/tests/test_phaseXX_<api>.py", "README.md"],
                "required_tests": ["endpoint shape tests", "router registration checks"],
                "required_readme_update": True,
                "required_router_registration": True,
                "required_migration_when_applicable": False,
                "validation_commands": ["PYTHONPATH=backend pytest -q backend/tests/test_phaseXX_<api>.py", "python -m py_compile backend/app/api/<route>.py backend/app/main.py"],
                "rollback_notes": "unregister router and revert API module if not production-approved",
                "human_approval_required": True,
            },
        ]),
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
    }


def platform_catalog_memory() -> dict:
    return {
        "catalog_snapshots": ["phase55_platform_catalog_baseline"],
        "ownership_audit_snapshots": ["owner/lifecycle/documentation gaps tracked"],
        "dependency_map_snapshots": ["cross-subsystem coupling baselined"],
        "golden_path_reviews": ["phase/api/frontend/migration/governance/release-retirement paths documented"],
        "integration_snapshot": _integration_snapshot(),
        "safety_principles": [
            "never auto-create files",
            "never auto-delete capabilities",
            "never auto-change ownership",
            "never auto-register routers",
            "never auto-run migrations",
            "human approval required for governance changes",
        ],
    }
