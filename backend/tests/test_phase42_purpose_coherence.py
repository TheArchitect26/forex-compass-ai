from app.engines.purpose_coherence import purpose_status, coherence_audit, meaning_drift, anti_hollowing, mission_alignment, purpose_memory


def test_purpose_scoring():
    out = purpose_status()
    assert isinstance(out["purpose_coherence_score"], float)
    assert isinstance(out["mission_alignment_score"], float)


def test_meaning_drift_detection():
    out = meaning_drift({})
    assert "drift_signals" in out
    assert "symbolic_governance_layers" in out


def test_anti_hollowing_output():
    out = anti_hollowing({})
    assert "anti_hollowing_warnings" in out
    assert len(out["purpose_preservation_recommendations"]) > 0


def test_mission_alignment_review():
    out = mission_alignment({})
    assert "stated_doctrine" in out
    assert "doctrine_embodiment_check" in out


def test_doctrine_embodiment_check():
    out = mission_alignment({})
    assert len(out["doctrine_embodiment_check"]) > 0


def test_advisory_only_safeguards():
    assert purpose_status()["advisory_only"] is True
    assert purpose_status()["auto_apply"] is False
    assert anti_hollowing({})["human_approval_required"] is True


def test_memory_shape():
    out = purpose_memory()
    assert {"coherence_audits", "meaning_drift_reviews", "anti_hollowing_reviews", "mission_alignment_reviews", "lessons"}.issubset(out.keys())
