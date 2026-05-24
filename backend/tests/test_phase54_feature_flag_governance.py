from app.engines.feature_flag_governance import (
    feature_flags_status,
    feature_flag_audit,
    stale_review,
    cleanup_plan,
    rollout_safety,
    feature_flags_memory,
)


def test_lifecycle_state_output():
    out = feature_flags_status()
    assert "flag_lifecycle_states" in out
    assert "stable" in out["flag_lifecycle_states"]


def test_flag_audit_shape():
    out = feature_flag_audit({})
    assert "registry" in out
    item = out["registry"][0]
    assert {
        "flag_name",
        "lifecycle_state",
        "capability_controlled",
        "owner",
        "intended_lifespan_days",
        "cleanup_due_at",
        "affected_systems",
        "default_state",
        "rollback_role",
        "operator_visibility",
        "human_approval_required",
    }.issubset(item.keys())


def test_stale_flag_detection():
    out = stale_review({})
    assert "flags_with_no_owner" in out
    assert "flags_older_than_intended_lifespan" in out


def test_cleanup_plan_shape():
    out = cleanup_plan({})
    assert "cleanup_actions" in out
    assert "priority_order" in out


def test_rollout_safety_output():
    out = rollout_safety({})
    assert {"blast_radius", "rollback_usefulness", "monitoring_readiness"}.issubset(out.keys())


def test_advisory_only_safeguards():
    out = feature_flags_status()
    assert out["advisory_only"] is True
    assert out["auto_apply"] is False
    assert out["human_approval_required"] is True
    assert out["never_auto_enable_flags"] is True
    assert out["never_auto_disable_flags"] is True
    assert out["never_auto_delete_flags"] is True
    assert out["never_auto_change_rollout_state"] is True
    assert out["never_auto_change_production_behavior"] is True


def test_memory_shape():
    out = feature_flags_memory()
    assert {
        "flag_audit_snapshots",
        "stale_flag_reviews",
        "cleanup_plan_reviews",
        "rollout_safety_reviews",
        "integration_snapshot",
        "safety_principles",
    }.issubset(out.keys())


def test_registry_item_shape():
    out = feature_flag_audit({})
    item = out["registry"][0]
    assert isinstance(item["affected_systems"], list)
    assert item["default_state"] in {"on", "off"}
