from app.engines.operational_orchestration import review_plan, deferred_action, cadence_check, maintenance_cycle, operations_memory


def test_review_plan_shape():
    out = review_plan({})
    assert "review_plan" in out and len(out["review_plan"]) > 0


def test_deferred_action_scoring():
    out = deferred_action({"urgency": 0.9, "importance": 0.8})
    assert out["prioritization_score"] > 0


def test_cadence_health_output_and_overdue_detection():
    out = cadence_check({"cadence_adherence": 0.45, "overdue_detection": True})
    assert out["cadence_health"] == "at_risk"
    assert out["overdue_detection"] is True


def test_maintenance_cycle_generation():
    out = maintenance_cycle({})
    assert len(out["maintenance_plan"]) > 0


def test_advisory_only_safeguards():
    out = deferred_action({})
    assert out["advisory_only"] is True
    assert out["auto_apply"] is False


def test_operational_memory_shape():
    out = operations_memory()
    assert {"review_history", "deferred_actions_history", "maintenance_history", "overdue_history", "cadence_lessons"}.issubset(out.keys())
