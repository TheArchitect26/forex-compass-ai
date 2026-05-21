from app.engines.institutional_evaluation import evaluation_status, maturity_assessment, benchmark, improvement_plan, regression_review, evaluation_memory


def test_maturity_scoring():
    out = evaluation_status()
    assert isinstance(out["institutional_maturity_score"], float)
    assert isinstance(out["usability_maturity_score"], float)
    assert isinstance(out["operator_clarity_score"], float)


def test_benchmark_output_shape():
    out = benchmark({})
    assert "benchmarks" in out
    assert len(out["benchmarks"]) >= 5
    b = out["benchmarks"][0]
    assert {"category", "current_score", "target_score", "evidence", "trend", "maturity_level", "recommended_improvement", "human_review_required"}.issubset(b.keys())


def test_regression_review_output():
    out = regression_review({})
    assert "more_navigation_burden" in out
    assert "more_technical_debt" in out


def test_improvement_plan_shape():
    out = improvement_plan({})
    assert "plan_items" in out
    assert len(out["plan_items"]) >= 5


def test_evidence_requirement():
    out = regression_review({})
    assert out["evidence_required"] is True


def test_advisory_only_safeguards():
    out = evaluation_status()
    assert out["advisory_only"] is True
    assert out["auto_apply"] is False
    assert out["never_auto_change_scores_without_evidence"] is True
    assert out["never_auto_approve_maturity_claims"] is True
    assert out["never_hide_regressions"] is True


def test_memory_shape():
    out = evaluation_memory()
    assert {"evaluation_snapshots", "benchmark_history", "regression_reviews", "improvement_plan_history", "integration_snapshot", "safety_principles"}.issubset(out.keys())
