from app.engines.post_implementation_review import (
    post_implementation_status,
    review,
    expected_vs_actual,
    lessons_learned,
    improvement_actions,
    post_implementation_memory,
)


def test_pir_output_shape():
    out = review({})
    assert {"change_summary", "planned_outcome", "actual_outcome", "deviations", "what_worked", "what_failed", "unexpected_impacts", "affected_systems", "incident_links_references", "rollback_status", "operator_impact", "lessons_learned", "recommended_improvements", "human_review_required"}.issubset(out.keys())


def test_expected_vs_actual_comparison():
    out = expected_vs_actual({})
    assert {"predicted_vs_actual_affected_systems", "expected_vs_actual_risk", "expected_vs_actual_operator_impact", "planned_vs_actual_validation", "planned_vs_actual_rollback", "expected_vs_actual_benefit"}.issubset(out.keys())


def test_lessons_learned_output():
    out = lessons_learned({})
    assert {"golden_paths_lessons", "scorecards_lessons", "release_governance_lessons", "change_control_lessons", "runtime_observability_lessons", "feature_flags_lessons", "platform_catalog_lessons", "ux_quality_lessons", "technical_debt_lessons", "memory_retrieval_lessons", "knowledge_compression_lessons"}.issubset(out.keys())


def test_improvement_action_output():
    out = improvement_actions({})
    assert {"actions", "priority_order", "human_review_required"}.issubset(out.keys())


def test_scoring_output():
    out = post_implementation_status()
    assert {"implementation_success_score", "expected_vs_actual_alignment_score", "incident_severity_score", "rollback_effectiveness_score", "operator_impact_score", "lesson_value_score", "process_improvement_priority_score", "future_risk_reduction_score"}.issubset(out.keys())


def test_advisory_only_safeguards():
    out = post_implementation_status()
    assert out["advisory_only"] is True
    assert out["auto_apply"] is False
    assert out["human_approval_required"] is True
    assert out["never_rewrite_history"] is True
    assert out["never_auto_close_improvement_actions"] is True
    assert out["never_auto_change_scorecards"] is True
    assert out["never_auto_update_golden_paths"] is True
    assert out["never_auto_run_commands"] is True
    assert out["never_deploy"] is True
    assert out["never_rollback"] is True


def test_memory_shape():
    out = post_implementation_memory()
    assert {"pir_snapshots", "expected_vs_actual_reviews", "lesson_snapshots", "improvement_action_snapshots", "integration_snapshot", "safety_principles"}.issubset(out.keys())
