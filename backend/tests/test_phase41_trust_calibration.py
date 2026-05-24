from app.engines.trust_calibration import trust_status, credibility_audit, recommendation_legitimacy, uncertainty_audit, overreach_scan, trust_memory


def test_credibility_scoring():
    out = trust_status()
    assert isinstance(out["institutional_credibility_score"], float)
    assert isinstance(out["confidence_calibration_score"], float)


def test_recommendation_legitimacy_output():
    out = recommendation_legitimacy({})
    assert "evidence_strength" in out
    assert "risk_of_overreach" in out


def test_uncertainty_audit_shape():
    out = uncertainty_audit({})
    assert {"facts", "estimates", "assumptions", "weak_signals", "speculative_forecasts", "low_confidence_conclusions", "human_review_required_areas"}.issubset(out.keys())


def test_overreach_detection():
    out = overreach_scan({})
    assert "excessive_confidence" in out
    assert "governance_overreach" in out


def test_confidence_calibration_flags():
    out = credibility_audit({})
    assert "confidence_calibration_flags" in out


def test_advisory_only_safeguards():
    assert trust_status()["advisory_only"] is True
    assert trust_status()["auto_apply"] is False
    assert recommendation_legitimacy({})["human_review_required"] is True


def test_memory_shape():
    out = trust_memory()
    assert {"trust_audits", "legitimacy_reviews", "uncertainty_reviews", "overreach_incidents", "lessons"}.issubset(out.keys())
