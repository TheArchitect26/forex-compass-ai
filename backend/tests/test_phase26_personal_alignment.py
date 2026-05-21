from app.engines.personal_alignment import context_status, adaptive_workflow, energy_safeguards, alignment_score, simplification_layer


def test_context_state_transitions():
    out = context_status({"maintenance_phase": False, "experimentation_phase": True})
    assert out["maintenance_phase"] is False
    assert out["experimentation_phase"] is True


def test_focus_mode_adaptation():
    out = adaptive_workflow("simplified_mode", {"preferred_complexity_level": "low"})
    assert "top-3-actions-only" in out["adapted_workflow"]


def test_overload_detection():
    out = energy_safeguards({"operator_overload": 0.8, "workflow_saturation": 0.9})
    assert "operator_overload" in out["overload_flags"]
    assert len(out["pause_recommendations"]) > 0


def test_alignment_scoring():
    out = alignment_score({"operator_relevance_score": 0.9})
    assert out["operator_relevance_score"] == 90.0


def test_simplification_consistency():
    out = simplification_layer({})
    assert len(out["retirement_suggestions"]) > 0
