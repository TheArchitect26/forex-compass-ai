from app.engines.ecosystem_intelligence import dependency_map, risk_scan, fallback_plan, environmental_pressure, ecosystem_memory


def test_dependency_map_output():
    out = dependency_map({})
    assert "dependencies" in out and len(out["dependencies"]) > 0


def test_risk_scoring():
    out = risk_scan({"dependency_risk_score": 0.8})
    assert out["ecosystem_risk_scores"]["dependency_risk_score"] == 0.8


def test_provider_concentration_detection():
    out = dependency_map({"dependencies": [{"name": "x", "concentration_risk": "high", "criticality": "high", "current_health": "ok", "dependency_type": "provider", "failure_impact": "a", "fallback_availability": True, "monitoring_recommendation": "m"}]})
    assert out["dependencies"][0]["concentration_risk"] == "high"


def test_fallback_plan_shape_and_safeguards():
    out = fallback_plan({})
    assert {"affected_systems", "temporary_workaround", "recovery_steps", "operator_action_required"}.issubset(out.keys())
    assert out["advisory_only"] is True
    assert out["auto_apply"] is False
    assert out["human_review_required"] is True


def test_environmental_pressure_detection():
    out = environmental_pressure({})
    assert "market_volatility_expansion" in out


def test_ecosystem_memory_shape():
    out = ecosystem_memory()
    assert {"dependency_incidents", "provider_failures", "fallback_activations", "recovery_outcomes", "external_pressure_periods", "fragility_lessons", "risk_changes"}.issubset(out.keys())
