from app.engines.anticipatory_intelligence import early_warnings, foresight_scores, detect_trajectory, intervention_plan, foresight_memory


def test_early_warning_classification():
    out = early_warnings({"operator_overload": 0.9})
    assert out["warnings"][0]["classification"] == "critical"


def test_pressure_accumulation_scoring():
    out = foresight_scores({"pressure_accumulation": 0.77})
    assert out["pressure_accumulation"] == 0.77


def test_trajectory_detection():
    out = detect_trajectory({"trajectory_index": -0.5})
    assert out["trajectory"] == "simplification"


def test_intervention_plan_output():
    out = intervention_plan({"intervention_urgency": 0.81})
    assert "escalate human review" in out["intervention_plan"]


def test_advisory_only_safeguards():
    out = intervention_plan({})
    assert out["advisory_only"] is True
    assert out["auto_apply"] is False


def test_foresight_memory_shape_and_false_alarm_handling():
    out = foresight_memory()
    assert {"early_warnings", "forecasts", "intervention_plans", "resolved_warnings", "false_alarms", "missed_warnings", "trajectory_changes"}.issubset(out.keys())
