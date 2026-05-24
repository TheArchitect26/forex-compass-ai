from app.engines.memory_retrieval import memory_status, memory_search, contextual_recall, related_items, staleness_review, memory_index


def test_memory_search_output():
    out = memory_search({})
    assert "matches" in out
    assert len(out["matches"]) > 0


def test_retrieval_scoring():
    out = memory_search({})
    scoring = out["retrieval_scoring"]
    assert {"relevance_score", "recency_score", "strategic_importance_score", "confidence_score", "source_clarity_score", "usefulness_score", "actionability_score", "staleness_risk_score"}.issubset(scoring.keys())


def test_contextual_recall_shape():
    out = contextual_recall({})
    assert {"most_relevant_prior_lessons", "related_decisions", "related_incidents", "related_assumptions", "related_warnings", "related_phases", "stale_or_outdated_knowledge_risks"}.issubset(out.keys())


def test_related_items_output():
    out = related_items({})
    assert "related_phase_history" in out
    assert "related_unresolved_issues" in out


def test_staleness_review_output():
    out = staleness_review({})
    assert "old_assumptions_no_longer_reliable" in out
    assert "old_lessons_needing_revalidation" in out


def test_advisory_only_safeguards():
    out = memory_status()
    assert out["advisory_only"] is True
    assert out["auto_apply"] is False
    assert out["never_auto_delete_memory"] is True
    assert out["never_auto_rewrite_history"] is True
    assert out["never_auto_resolve_assumptions"] is True


def test_index_shape():
    out = memory_index()
    assert "categories" in out
    assert "example_entries" in out
