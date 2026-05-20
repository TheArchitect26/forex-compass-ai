from app.engines.attention_architecture import extract_strategic_signal, detect_attention_fatigue, relevance_half_life, focus_mode, anti_noise_governance, priority_status


def test_signal_extraction_consistency():
    out = extract_strategic_signal({"highest_impact_findings": ["x"], "redundant_alerts": ["r1"]})
    assert out["highest_impact_findings"] == ["x"]
    assert out["suppressed_items"]["redundant_alerts"] == ["r1"]


def test_attention_fatigue_detection():
    out = detect_attention_fatigue({"alert_fatigue": 0.8, "context_switch_pressure": 0.9})
    assert "alert_fatigue" in out["fatigue_flags"]


def test_relevance_decay_tracking():
    out = relevance_half_life({"alerts_decay_days": 2})
    assert out["alerts_decay_days"] == 2


def test_focus_mode_prioritization():
    out = focus_mode("deep_research")
    assert "full evidence chains" in out["priorities"]


def test_anti_noise_governance_flags():
    out = anti_noise_governance({"metric_inflation": 0.8, "dashboard_sprawl": 0.7})
    assert "metric_inflation" in out["anti_noise_flags"]


def test_urgency_and_suppression_consistency():
    out = priority_status({"urgency_score": 0.66, "signal_to_noise_ratio": 0.8})
    assert out["urgency_score"] == 66.0
    assert out["signal_to_noise_ratio"] == 80.0
