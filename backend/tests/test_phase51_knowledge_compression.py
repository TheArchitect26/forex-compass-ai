from app.engines.knowledge_compression import compression_status, distill, strategic_lessons, anti_patterns, heuristics, compression_memory


def test_compression_scoring():
    out = compression_status()
    assert isinstance(out["compression_efficiency_score"], float)
    assert isinstance(out["insight_density_score"], float)
    assert isinstance(out["knowledge_durability_score"], float)


def test_lesson_distillation_output():
    out = strategic_lessons({})
    assert "what_repeatedly_worked" in out
    assert "what_repeatedly_failed" in out


def test_anti_pattern_extraction():
    out = anti_patterns({})
    assert "recurring_anti_patterns" in out
    assert "dashboard sprawl" in out["recurring_anti_patterns"]


def test_heuristic_generation():
    out = heuristics({})
    assert len(out["institutional_heuristics"]) >= 5


def test_clutter_reduction_logic():
    out = strategic_lessons({})
    assert "clutter_reduction_opportunities" in out


def test_advisory_only_safeguards():
    out = compression_status()
    assert out["advisory_only"] is True
    assert out["auto_apply"] is False
    assert out["never_auto_delete_historical_records"] is True
    assert out["never_rewrite_institutional_history"] is True
    assert out["never_hide_critical_warnings"] is True


def test_memory_shape():
    out = compression_memory()
    assert {"distilled_insights", "strategic_heuristics", "anti_pattern_library", "retention_checks", "integration_snapshot", "safety_principles"}.issubset(out.keys())
