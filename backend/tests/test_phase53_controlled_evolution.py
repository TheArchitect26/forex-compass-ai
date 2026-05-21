from app.engines.controlled_evolution import evolution_control_status, capability_audit, lifecycle_review, retirement_candidates, evolution_plan, evolution_control_memory


def test_lifecycle_state_output():
    out = evolution_control_status()
    assert "lifecycle_states" in out
    assert "stable" in out["lifecycle_states"]


def test_capability_audit_shape():
    out = capability_audit({})
    assert "capability_audit" in out
    item = out["capability_audit"][0]
    assert {"capability", "lifecycle_state", "value_evidence", "maintenance_burden", "overlap_risk", "maturity_level", "recommendation", "human_approval_required"}.issubset(item.keys())


def test_retirement_candidate_detection():
    out = retirement_candidates({})
    assert "unused_or_low_value_consoles" in out
    assert "repeated_summaries" in out


def test_consolidation_recommendation_shape():
    out = lifecycle_review({})
    assert "candidate_consolidations" in out


def test_freeze_recommendation_output():
    out = lifecycle_review({})
    assert "candidate_freezes" in out


def test_evolution_plan_shape():
    out = evolution_plan({})
    assert {"what_to_evolve_next", "what_to_freeze", "what_to_consolidate", "what_to_monitor", "what_to_retire_later", "what_not_to_touch", "risk_notes", "reversibility_notes"}.issubset(out.keys())


def test_advisory_only_safeguards():
    out = evolution_control_status()
    assert out["advisory_only"] is True
    assert out["auto_apply"] is False
    assert out["never_auto_delete_features"] is True
    assert out["never_auto_remove_routes"] is True
    assert out["never_auto_freeze_capabilities"] is True


def test_memory_shape():
    out = evolution_control_memory()
    assert {"lifecycle_snapshots", "retirement_watchlist", "freeze_decisions", "consolidation_reviews", "integration_snapshot", "safety_principles"}.issubset(out.keys())
