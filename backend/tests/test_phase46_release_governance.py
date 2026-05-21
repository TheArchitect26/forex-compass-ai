from app.engines.release_governance import release_status, release_readiness_check, build_risk, rollback_plan, post_release_review, release_memory


def test_release_readiness_scoring():
    out = release_status()
    assert isinstance(out["release_readiness_score"], float)
    assert isinstance(out["build_confidence_score"], float)
    assert isinstance(out["production_suitability_score"], float)


def test_deployment_risk_detection():
    out = build_risk({})
    assert "unresolved_dependency_versions" in out
    assert "frontend_backend_api_mismatch" in out
    assert "missing_python_version_lock" in out


def test_rollback_plan_shape():
    out = rollback_plan({})
    assert len(out["rollback_steps"]) > 0
    assert "post_rollback_validation" in out


def test_post_release_review_shape():
    out = post_release_review({})
    assert {"build_result", "deployment_result", "runtime_errors", "failed_api_routes", "follow_up_debt_items"}.issubset(out.keys())


def test_environment_readiness_checks():
    out = release_readiness_check({})
    assert "required_env_vars_documented" in out["checklist"]
    assert "frontend_api_base_matches_deploy_config" in out["checklist"]


def test_advisory_only_safeguards():
    out = release_status()
    assert out["advisory_only"] is True
    assert out["auto_apply"] is False
    assert out["never_auto_deploy"] is True
    assert out["never_auto_rollback"] is True
    assert out["never_auto_run_migrations"] is True


def test_memory_shape():
    out = release_memory()
    assert {"release_audits", "deployment_risk_reviews", "rollback_reviews", "post_release_reviews", "integration_snapshot", "safety_principles"}.issubset(out.keys())
