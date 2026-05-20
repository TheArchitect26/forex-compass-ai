from app.engines.scenario_intelligence import run_scenario, compare_scenarios, scenario_memory


def test_scenario_output_shape():
    out = run_scenario({"scenario": "attention_load_reduction"})
    assert {"primary_effects", "second_order_effects", "tradeoffs", "scores", "uncertainty_notes"}.issubset(out.keys())


def test_consequence_scoring_and_reversibility():
    out = run_scenario({"reversibility_score": 0.88, "upside_score": 0.7})
    assert out["scores"]["reversibility_score"] == 0.88


def test_tradeoff_comparison():
    out = compare_scenarios({"left": "pause_expansion", "right": "continue_research", "left_score": 0.7, "right_score": 0.6})
    assert out["preferred_option"] == "pause_expansion"


def test_advisory_only_safeguards_and_uncertainty_notes():
    out = compare_scenarios({})
    assert out["advisory_only"] is True
    assert out["auto_apply"] is False
    assert len(out["uncertainty_notes"]) > 0


def test_scenario_memory_shape():
    out = scenario_memory()
    assert {"scenario_runs", "comparisons", "consequence_assessments", "false_assumptions", "missed_consequences"}.issubset(out.keys())
