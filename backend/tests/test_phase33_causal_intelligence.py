from app.engines.causal_intelligence import causal_graph, analyze_root_cause, propagation_estimate, intervention_effect, causal_memory


def test_causal_graph_output_shape():
    out = causal_graph({})
    assert {"nodes", "edges"}.issubset(out.keys())


def test_root_cause_ranking():
    out = analyze_root_cause({"root_causes": [{"cause": "a", "score": 0.2}, {"cause": "b", "score": 0.9}]})
    assert out["likely_root_causes"][0]["cause"] == "b"


def test_propagation_chain_generation():
    out = propagation_estimate({})
    assert len(out["propagation_chain"]) > 1


def test_intervention_effect_estimate_and_safeguards():
    out = intervention_effect({})
    assert "likely_benefit" in out
    assert out["advisory_only"] is True
    assert out["auto_apply"] is False
    assert out["human_review_required"] is True


def test_uncertainty_notes_present():
    out = analyze_root_cause({})
    assert len(out["uncertainty_notes"]) > 0


def test_memory_shape():
    out = causal_memory()
    assert {"analyses", "graph_snapshots", "intervention_estimates", "resolved_incidents", "false_links"}.issubset(out.keys())
