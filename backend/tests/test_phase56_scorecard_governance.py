from app.engines.scorecard_governance import (
    scorecard_status,
    evaluate_scorecards,
    entity_scorecard,
    readiness_gates,
    improvement_plan,
    scorecard_memory,
)


def test_scorecard_category_output():
    out = scorecard_status()
    assert "scorecard_categories" in out
    assert "production_readiness" in out["scorecard_categories"]


def test_entity_scorecard_shape():
    out = entity_scorecard({})
    assert "scorecard" in out
    assert "owner_present" in out["scorecard"]


def test_readiness_gate_detection():
    out = readiness_gates({})
    assert "missing_tests" in out
    assert "unregistered_router" in out


def test_gap_detection():
    out = readiness_gates({})
    assert "missing_documentation" in out
    assert "orphaned_frontend_console" in out


def test_improvement_plan_shape():
    out = improvement_plan({})
    assert "improvements" in out
    assert "priority_order" in out


def test_advisory_only_safeguards():
    out = scorecard_status()
    assert out["advisory_only"] is True
    assert out["auto_apply"] is False
    assert out["human_approval_required"] is True
    assert out["never_auto_pass_capabilities"] is True
    assert out["never_auto_change_lifecycle_state"] is True
    assert out["never_auto_create_files"] is True
    assert out["never_auto_register_routers"] is True
    assert out["never_auto_run_migrations"] is True


def test_memory_shape():
    out = scorecard_memory()
    assert {"scorecard_snapshots", "readiness_gate_reviews", "gap_detection_reviews", "improvement_plan_reviews", "integration_snapshot", "safety_principles"}.issubset(out.keys())


def test_scorecard_scoring_output():
    out = evaluate_scorecards({})
    assert {"overall_score", "category_scores", "pass_fail_status", "readiness_level", "evidence_strength", "gap_severity", "improvement_priority"}.issubset(out.keys())
