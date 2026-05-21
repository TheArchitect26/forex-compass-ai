from app.engines.golden_path_workflows import (
    golden_paths_status,
    workflow,
    checklist,
    validate_plan,
    deviation_review,
    golden_paths_memory,
)


def test_workflow_generation_shape():
    out = workflow({})
    assert "workflow_name" in out
    assert "guided_steps" in out


def test_checklist_output():
    out = checklist({})
    assert {"required_files", "required_tests", "validation_commands", "rollback_notes", "scorecard_checks"}.issubset(out.keys())


def test_plan_validation_output():
    out = validate_plan({})
    assert {"platform_catalog_alignment", "scorecard_alignment", "technical_debt_alignment", "release_readiness_alignment", "feature_flag_governance_alignment", "controlled_evolution_alignment", "ux_quality_alignment", "no_execution_safeguards"}.issubset(out.keys())


def test_deviation_review_output():
    out = deviation_review({})
    assert {"deviation_reason", "risk_introduced", "affected_standards", "compensating_controls", "required_human_review", "rollback_recovery_notes"}.issubset(out.keys())


def test_workflow_scoring():
    out = golden_paths_status()
    assert {"workflow_completeness_score", "safety_coverage_score", "reversibility_score", "validation_readiness_score", "documentation_readiness_score", "operator_clarity_score", "governance_alignment_score", "execution_risk_score"}.issubset(out.keys())


def test_advisory_only_safeguards():
    out = golden_paths_status()
    assert out["advisory_only"] is True
    assert out["auto_apply"] is False
    assert out["human_approval_required"] is True
    assert out["never_auto_create_files"] is True
    assert out["never_auto_run_commands"] is True
    assert out["never_auto_commit_changes"] is True
    assert out["never_auto_register_routers"] is True
    assert out["never_auto_run_migrations"] is True
    assert out["never_force_workflow_without_human_approval"] is True


def test_memory_shape():
    out = golden_paths_memory()
    assert {"workflow_snapshots", "checklist_snapshots", "plan_validation_reviews", "deviation_reviews", "integration_snapshot", "safety_principles"}.issubset(out.keys())
