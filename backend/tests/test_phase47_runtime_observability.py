from app.engines.runtime_observability import observability_status, runtime_scan, endpoint_health, regression_check, incident_summary, observability_memory


def test_runtime_scoring():
    out = observability_status()
    assert isinstance(out["runtime_health_score"], float)
    assert isinstance(out["endpoint_reliability_score"], float)
    assert isinstance(out["monitoring_readiness_score"], float)


def test_endpoint_health_output():
    out = endpoint_health({})
    assert len(out["endpoint_observations"]) > 0
    first = out["endpoint_observations"][0]
    assert {"endpoint_path", "method", "expected_status", "observed_status", "latency_estimate_ms", "error_pattern", "affected_subsystem", "severity", "recommended_human_review"}.issubset(first.keys())


def test_regression_detection():
    out = regression_check({})
    assert "routes_failing_after_release" in out
    assert "api_base_url_mismatch" in out
    assert "repeated_500_or_404_patterns" in out


def test_incident_summary_shape():
    out = incident_summary({})
    assert {"likely_issue", "affected_routes", "severity", "possible_cause", "rollback_relevance", "debugging_next_steps", "human_review_required", "advisory_only", "auto_apply"}.issubset(out.keys())


def test_advisory_only_safeguards():
    out = observability_status()
    assert out["advisory_only"] is True
    assert out["auto_apply"] is False
    assert out["never_auto_rollback"] is True
    assert out["never_auto_disable_routes"] is True
    assert out["never_auto_change_env"] is True
    assert out["never_auto_deploy_fixes"] is True


def test_memory_shape():
    out = observability_memory()
    assert {"runtime_audits", "endpoint_observations", "regression_reviews", "incident_reviews", "integration_snapshot", "safety_principles"}.issubset(out.keys())


def test_runtime_scan_shape():
    out = runtime_scan({})
    assert {"api_health", "frontend_backend_route_compatibility", "latency_pressure", "runtime_error_patterns", "failed_endpoint_patterns", "post_release_instability"}.issubset(out.keys())
