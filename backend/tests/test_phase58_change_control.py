from app.engines.change_impact_analysis import (
    change_control_status,
    impact_analysis,
    review_requirements,
    rollback_readiness,
    approval_brief,
    change_control_memory,
)


def test_impact_analysis_output_shape():
    out = impact_analysis({})
    assert {"affected_systems", "affected_files", "upstream_dependencies", "downstream_dependents", "risk_level", "required_tests", "required_docs", "required_migrations", "required_scorecard_checks", "required_rollback_notes", "required_human_reviewers"}.issubset(out.keys())


def test_review_requirements_detection():
    out = review_requirements({})
    assert {"normal_review", "release_review", "architecture_review", "migration_review", "ux_review", "governance_review", "rollback_review"}.issubset(out.keys())


def test_rollback_readiness_output():
    out = rollback_readiness({})
    assert {"rollback_plan_present", "rollback_steps_documented", "rollback_validation_commands", "rollback_owner_assigned", "rollback_risk_level"}.issubset(out.keys())


def test_approval_brief_shape():
    out = approval_brief({})
    assert {"change_summary", "reason_for_change", "affected_systems", "expected_benefit", "risk_if_approved", "risk_if_rejected", "validation_plan", "rollback_plan", "open_questions", "human_approval_required"}.issubset(out.keys())


def test_scoring_output():
    out = change_control_status()
    assert {"change_impact_score", "implementation_risk_score", "dependency_risk_score", "migration_risk_score", "rollback_complexity_score", "review_urgency_score", "operator_impact_score", "production_safety_score", "approval_readiness_score"}.issubset(out.keys())


def test_advisory_only_safeguards():
    out = change_control_status()
    assert out["advisory_only"] is True
    assert out["auto_apply"] is False
    assert out["human_approval_required"] is True
    assert out["never_auto_approve_changes"] is True
    assert out["never_auto_reject_changes"] is True
    assert out["never_run_commands"] is True
    assert out["never_create_commits"] is True
    assert out["never_deploy"] is True
    assert out["never_rollback"] is True
    assert out["never_run_migrations"] is True


def test_memory_shape():
    out = change_control_memory()
    assert {"impact_snapshots", "review_requirement_snapshots", "rollback_readiness_snapshots", "approval_brief_snapshots", "integration_snapshot", "safety_principles"}.issubset(out.keys())
