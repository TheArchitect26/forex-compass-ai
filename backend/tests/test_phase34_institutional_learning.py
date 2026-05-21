from app.engines.institutional_learning import extract_lessons, intervention_review, forecast_review, assumption_review, learning_memory


def test_lesson_extraction_shape():
    out = extract_lessons({})
    assert "lessons" in out and len(out["lessons"]) > 0


def test_intervention_effectiveness_scoring():
    out = intervention_review({"effectiveness_score": 0.8})
    assert out["effectiveness_score"] == 0.8


def test_forecast_review_behavior_and_weak_evidence():
    out = forecast_review({"accuracy_score": 0.4})
    assert out["weak_evidence"] is True


def test_assumption_review_behavior():
    out = assumption_review({"status": "retire"})
    assert out["status"] == "retire"


def test_advisory_only_safeguards():
    out = intervention_review({})
    assert out["advisory_only"] is True
    assert out["auto_apply"] is False
    assert out["human_review_required"] is True


def test_learning_memory_shape():
    out = learning_memory()
    assert {"institutional_lessons", "intervention_reviews", "forecast_reviews", "assumption_reviews", "successful_patterns", "failed_patterns"}.issubset(out.keys())
