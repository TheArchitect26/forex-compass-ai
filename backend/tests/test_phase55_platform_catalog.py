from app.engines.platform_catalog import (
    platform_catalog_status,
    catalog_entities,
    ownership_audit,
    dependency_map,
    golden_paths,
    platform_catalog_memory,
)


def test_catalog_entity_output():
    out = catalog_entities({})
    assert "entities" in out
    assert out["entities"][0]["entity_type"] in {"engine", "capability_flag"}


def test_ownership_audit_detection():
    out = ownership_audit({})
    assert "missing_owner" in out
    assert "orphaned_capability" in out


def test_dependency_map_shape():
    out = dependency_map({})
    assert {"upstream_dependencies", "downstream_dependents", "related_subsystems", "risk_if_changed", "operational_coupling", "consolidation_opportunity"}.issubset(out.keys())


def test_golden_path_output():
    out = golden_paths({})
    assert "golden_paths" in out
    item = out["golden_paths"][0]
    assert {"required_files", "required_tests", "required_readme_update", "required_router_registration", "required_migration_when_applicable", "validation_commands", "rollback_notes", "human_approval_required"}.issubset(item.keys())


def test_catalog_scoring():
    out = platform_catalog_status()
    assert {"catalog_completeness_score", "ownership_clarity_score", "documentation_readiness_score", "operational_discoverability_score", "dependency_clarity_score", "lifecycle_clarity_score", "golden_path_maturity_score", "platform_coherence_score"}.issubset(out.keys())


def test_advisory_only_safeguards():
    out = platform_catalog_status()
    assert out["advisory_only"] is True
    assert out["auto_apply"] is False
    assert out["human_approval_required"] is True
    assert out["never_auto_create_files"] is True
    assert out["never_auto_delete_capabilities"] is True
    assert out["never_auto_change_ownership"] is True
    assert out["never_auto_register_routers"] is True
    assert out["never_auto_run_migrations"] is True


def test_memory_shape():
    out = platform_catalog_memory()
    assert {"catalog_snapshots", "ownership_audit_snapshots", "dependency_map_snapshots", "golden_path_reviews", "integration_snapshot", "safety_principles"}.issubset(out.keys())
