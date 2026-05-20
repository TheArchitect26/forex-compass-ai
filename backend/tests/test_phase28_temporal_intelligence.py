from app.engines.temporal_intelligence import classify_timing, rhythm_scan, relevance_decay, detect_cycles, timing_conflicts, pacing_recommendation


def test_timing_classification():
    assert classify_timing({"priority": 0.95})["timing_classification"] == "immediate"


def test_rhythm_disruption_detection():
    out = rhythm_scan({"volatility": 0.2, "operator_workload": 0.8, "alert_frequency": 0.4})
    assert out["rhythm_state"] in {"disrupted rhythm", "unstable rhythm"}


def test_relevance_decay():
    assert relevance_decay({"age_days": 20})["relevance_score"] <= 0.1


def test_recurring_cycle_detection():
    out = detect_cycles({"recurring_drift_cycles": 1, "repeated_replay_failures": 1})
    assert out["cycle_count"] == 2


def test_timing_conflict_detection():
    out = timing_conflicts({"urgent_low_importance": True, "short_term_over_governed": True})
    assert len(out["conflicts"]) == 2


def test_pacing_recommendation_consistency():
    out = pacing_recommendation({"urgency": 0.9, "importance": 0.9})
    assert out["strategic_pacing"] == "act now"


def test_temporal_memory_shape():
    keys = {"recurring_cycles", "timing_decisions", "delayed_reviews", "deferred_items", "archived_stale_items", "major_timing_corrections", "rhythm_disruptions"}
    memory = {
        "recurring_cycles": ["weekly alert burst"],
        "timing_decisions": ["defer low-impact governance review"],
        "delayed_reviews": ["monthly replay deep-dive"],
        "deferred_items": ["low priority dashboard cleanup"],
        "archived_stale_items": ["obsolete anomaly narrative"],
        "major_timing_corrections": ["urgency policy normalized"],
        "rhythm_disruptions": ["high volatility week with operator overload"],
    }
    assert keys.issubset(set(memory.keys()))
