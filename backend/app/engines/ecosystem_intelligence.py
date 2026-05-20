from __future__ import annotations


def ecosystem_status() -> dict:
    return {
        "analysis_domains": [
            "data_provider_reliability",
            "api_dependency_risk",
            "infrastructure_fragility",
            "market_environment_pressure",
            "external_volatility_conditions",
            "geopolitical_systemic_event_pressure",
            "platform_dependency_concentration",
            "provider_outage_risk",
            "cost_resource_pressure",
            "external_reality_mismatch",
        ],
        "advisory_only": True,
        "auto_apply": False,
    }


def dependency_map(payload: dict) -> dict:
    deps = payload.get("dependencies", [
        {"name": "twelve_data", "dependency_type": "market_data_provider", "criticality": "high", "current_health": "degraded", "failure_impact": "ohlcv reliability drop", "fallback_availability": True, "concentration_risk": "high", "monitoring_recommendation": "track error-rate and latency"},
        {"name": "postgres", "dependency_type": "database", "criticality": "critical", "current_health": "healthy", "failure_impact": "persistence unavailable", "fallback_availability": False, "concentration_risk": "medium", "monitoring_recommendation": "monitor query latency + connection saturation"},
        {"name": "redis_celery", "dependency_type": "queue_cache", "criticality": "high", "current_health": "healthy", "failure_impact": "scheduled jobs delayed", "fallback_availability": "partial", "concentration_risk": "medium", "monitoring_recommendation": "track queue depth and worker heartbeats"},
    ])
    return {"dependencies": deps, "observed_vs_possible": "mixed"}


def risk_scan(payload: dict) -> dict:
    scores = {
        "dependency_risk_score": float(payload.get("dependency_risk_score", 0.58)),
        "provider_concentration_score": float(payload.get("provider_concentration_score", 0.71)),
        "infrastructure_resilience_score": float(payload.get("infrastructure_resilience_score", 0.64)),
        "external_volatility_pressure_score": float(payload.get("external_volatility_pressure_score", 0.6)),
        "data_source_fragility_score": float(payload.get("data_source_fragility_score", 0.66)),
        "operational_exposure_score": float(payload.get("operational_exposure_score", 0.57)),
        "fallback_readiness_score": float(payload.get("fallback_readiness_score", 0.69)),
    }
    return {"ecosystem_risk_scores": scores, "uncertainty_notes": ["scores are environment-sensitive estimates"]}


def fallback_plan(payload: dict) -> dict:
    outage = payload.get("outage", "data provider outage")
    return {
        "outage_type": outage,
        "affected_systems": payload.get("affected_systems", ["market_data", "analysis", "signals"]),
        "temporary_workaround": payload.get("temporary_workaround", "switch to synthetic data mode with warning banners"),
        "degraded_mode_behavior": payload.get("degraded_mode_behavior", "advisory scans continue with reduced confidence"),
        "recovery_steps": payload.get("recovery_steps", ["verify provider health", "backfill missing windows", "recalibrate reliability"]),
        "operator_action_required": payload.get("operator_action_required", "confirm fallback mode and approve recovery window"),
        "human_review_required": True,
        "advisory_only": True,
        "auto_apply": False,
    }


def environmental_pressure(payload: dict) -> dict:
    return {
        "market_volatility_expansion": float(payload.get("market_volatility_expansion", 0.62)),
        "data_reliability_degradation": float(payload.get("data_reliability_degradation", 0.55)),
        "api_failure_rate_increase": float(payload.get("api_failure_rate_increase", 0.48)),
        "infrastructure_instability": float(payload.get("infrastructure_instability", 0.41)),
        "economic_news_event_pressure": float(payload.get("economic_news_event_pressure", 0.67)),
        "session_liquidity_risk": float(payload.get("session_liquidity_risk", 0.44)),
        "provider_latency_outage_pattern": float(payload.get("provider_latency_outage_pattern", 0.53)),
        "uncertainty_notes": ["environmental pressure is dynamic and can change rapidly"],
    }


def ecosystem_memory() -> dict:
    return {
        "dependency_incidents": ["twelve_data transient outage"],
        "provider_failures": ["news api timeout cluster"],
        "fallback_activations": ["synthetic mode enabled during provider failure"],
        "recovery_outcomes": ["data backfill completed"],
        "external_pressure_periods": ["high-volatility macro week"],
        "fragility_lessons": ["single-provider concentration increased operational exposure"],
        "risk_changes": ["fallback readiness improved after runbook update"],
    }
