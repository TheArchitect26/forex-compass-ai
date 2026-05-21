from app.engines.strategic_synthesis import condensed_brief, detect_cross_layer_conflicts, run_synthesis, synthesis_memory


def test_condensation_output_shape():
    out = condensed_brief({"priorities": [{"label": "a", "score": 1}], "noise": [{"label": "n", "noise_score": 1}], "risks": [{"label": "r", "score": 1}]})
    assert {"top_priorities", "ignore_for_now", "risks_to_monitor", "recommended_focus_mode", "recommended_next_review_window"}.issubset(out.keys())


def test_conflict_detection():
    out = detect_cross_layer_conflicts({"attention_urgent": True, "wisdom_wait": True})
    assert "attention says urgent, wisdom says wait" in out


def test_focus_recommendation_and_priority_ranking():
    out = run_synthesis({"priorities": [{"label": "low", "score": 0.2}, {"label": "high", "score": 0.9}], "noise": [], "risks": []})
    assert out["top_strategic_priorities"][0]["label"] == "high"


def test_suppressed_noise_logic():
    out = run_synthesis({"priorities": [], "noise": [{"label": "x", "noise_score": 0.8}], "risks": []})
    assert out["suppressed_noise"][0]["label"] == "x"


def test_human_sovereignty_guarantee():
    out = run_synthesis({"priorities": [], "noise": [], "risks": []})
    assert out["human_judgment_final"] is True
    assert out["auto_apply"] is False


def test_synthesis_memory_shape():
    out = synthesis_memory()
    assert {"recent_snapshots", "recent_conflicts", "focus_decisions", "preserved_safety_warnings"}.issubset(out.keys())
