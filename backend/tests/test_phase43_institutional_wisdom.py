from app.engines.institutional_wisdom import wisdom_status, ambiguity_review, judgment_audit, restraint_check, prudence_review, wisdom_memory


def test_wisdom_scoring():
    out = wisdom_status()
    assert isinstance(out["wisdom_score"], float)
    assert isinstance(out["strategic_patience_score"], float)


def test_ambiguity_review_output():
    out = ambiguity_review({})
    assert "knowns" in out
    assert "uncertain" in out


def test_restraint_detection():
    out = restraint_check({})
    assert "overreaction_to_short_term_noise" in out
    assert "premature_pathway_selection" in out


def test_prudence_review_shape():
    out = prudence_review({})
    assert "reflective_reasoning" in out
    assert "mission_alignment" in out


def test_what_not_to_conclude_yet_output():
    out = ambiguity_review({})
    assert len(out["what_not_to_conclude_yet"]) > 0


def test_advisory_only_safeguards():
    assert wisdom_status()["advisory_only"] is True
    assert wisdom_status()["auto_apply"] is False
    assert prudence_review({})["human_review_required"] is True


def test_memory_shape():
    out = wisdom_memory()
    assert {"wisdom_audits", "ambiguity_reviews", "restraint_reviews", "prudence_reviews", "lessons"}.issubset(out.keys())
