from app.engines.reality_anchoring import reality_status, relevance_score, detect_internal_loops, pragmatism_safeguards


def test_reality_alignment_scoring():
    out = reality_status({"practical_utility": 0.8, "replay_to_reality_consistency": 0.7})
    assert out["practical_usefulness"] == 80.0
    assert out["replay_to_reality_consistency"] == 70.0


def test_practical_relevance_scores_present():
    out = relevance_score({})
    assert "overall_relevance_score" in out
    assert out["overall_relevance_score"] > 0


def test_internal_loop_detection_flags():
    out = detect_internal_loops({"self_referential_governance_loops": 0.8, "recommendation_recursion": 0.9})
    assert "self_referential_governance_loops" in out["grounding_warnings"]
    assert len(out["external_validation_recommendations"]) > 0


def test_pragmatism_warning_generation():
    out = pragmatism_safeguards({"intellectual_overengineering": 0.7, "complexity_without_practical_gain": 0.8})
    assert "intellectual_overengineering" in out["pragmatism_warnings"]
    assert len(out["retirement_or_simplification_recommendations"]) > 0
