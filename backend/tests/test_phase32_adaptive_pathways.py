from app.engines.adaptive_pathways import evaluate_triggers, recommend_pathway, compare_pathways, pathways_memory


def test_pathway_recommendation():
    out = recommend_pathway({"pressure": 0.8, "operator_capacity": 0.3, "replay_confidence": 0.6, "data_integrity": 0.7})
    assert out["recommended_pathway"] in {"operator_load_reduction_pathway", "simplification_pathway"}


def test_trigger_evaluation_and_exit_behavior():
    out = evaluate_triggers({"pressure": 0.2, "operator_capacity": 0.8, "replay_confidence": 0.8, "data_integrity": 0.9})
    assert out["triggers"]["high_pressure"] is False


def test_escalation_deescalation_logic():
    out = recommend_pathway({"pressure": 0.9, "operator_capacity": 0.2, "replay_confidence": 0.4, "data_integrity": 0.6})
    assert len(out["escalation_rules"]) > 0
    assert len(out["de_escalation_rules"]) > 0


def test_reversibility_output_and_human_approval():
    out = recommend_pathway({})
    assert "reversible" in out["reversibility_notes"]
    assert out["human_approval_required"] is True
    assert out["advisory_only"] is True
    assert out["auto_apply"] is False


def test_memory_shape():
    out = pathways_memory()
    assert {"adaptive_pathways", "evaluations", "decisions", "reversals", "lessons"}.issubset(out.keys())


def test_compare_output():
    out = compare_pathways({"left": "simplification_pathway", "right": "expansion_pathway", "left_fit": 0.7, "right_fit": 0.5})
    assert out["preferred_pathway"] == "simplification_pathway"
