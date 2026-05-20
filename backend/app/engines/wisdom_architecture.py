from __future__ import annotations


def wisdom_status(payload: dict) -> dict:
    return {
        "wisdom_score": round(float(payload.get("wisdom", 0.82)) * 100, 2),
        "restraint_score": round(float(payload.get("restraint", 0.84)) * 100, 2),
        "proportionality_score": round(float(payload.get("proportionality", 0.81)) * 100, 2),
        "uncertainty_integrity_score": round(float(payload.get("uncertainty_integrity", 0.8)) * 100, 2),
        "strategic_maturity_score": round(float(payload.get("strategic_maturity", 0.83)) * 100, 2),
        "institutional_humility_score": round(float(payload.get("institutional_humility", 0.85)) * 100, 2),
    }


def judgment_status(payload: dict) -> dict:
    return {
        "decision_quality_trend": payload.get("decision_quality_trend", "stable"),
        "recommendation_usefulness": float(payload.get("recommendation_usefulness", 0.78)),
        "false_urgency_frequency": int(payload.get("false_urgency_frequency", 1)),
        "recommendation_reversals": int(payload.get("recommendation_reversals", 2)),
        "overconfident_conclusions": int(payload.get("overconfident_conclusions", 1)),
        "complexity_escalation_events": int(payload.get("complexity_escalation_events", 1)),
        "governance_overreach_events": int(payload.get("governance_overreach_events", 0)),
        "strategic_stability_impact": payload.get("strategic_stability_impact", "positive"),
    }


def strategic_restraint_scan(payload: dict) -> dict:
    flags = []
    if float(payload.get("optimization_pressure", 0)) > 0.6: flags.append("excessive_optimization_pressure")
    if float(payload.get("escalation_spiral", 0)) > 0.6: flags.append("recommendation_escalation_spiral")
    if float(payload.get("institutional_expansion", 0)) > 0.6: flags.append("institutional_over_expansion")
    if float(payload.get("system_proliferation", 0)) > 0.6: flags.append("unnecessary_system_proliferation")
    if float(payload.get("recursive_governance_amplification", 0)) > 0.6: flags.append("recursive_governance_amplification")
    if float(payload.get("over_analysis_loops", 0)) > 0.6: flags.append("over_analysis_loops")
    if float(payload.get("strategic_maximalism", 0)) > 0.6: flags.append("strategic_maximalism")
    return {
        "flags": flags,
        "restraint_recommendations": ["de-escalate recommendation surface", "reduce optimization breadth", "prioritize high-value simplification"] if flags else ["restraint posture healthy"],
        "proportionality_warnings": flags,
    }


def uncertainty_integrity(payload: dict) -> dict:
    false_certainty = []
    if float(payload.get("confidence_uncertainty_gap", 0)) > 0.5:
        false_certainty.append("false_certainty_inflation")
    if float(payload.get("unsupported_strategic_confidence", 0)) > 0.5:
        false_certainty.append("unsupported_strategic_confidence")
    if float(payload.get("narrative_certainty_drift", 0)) > 0.5:
        false_certainty.append("narrative_certainty_drift")
    return {
        "confidence_uncertainty": float(payload.get("confidence_uncertainty", 0.3)),
        "evidence_gaps": payload.get("evidence_gaps", []),
        "replay_uncertainty": float(payload.get("replay_uncertainty", 0.25)),
        "historical_ambiguity": float(payload.get("historical_ambiguity", 0.3)),
        "unresolved_contradictions": int(payload.get("unresolved_contradictions", 0)),
        "low_certainty_zones": payload.get("low_certainty_zones", []),
        "false_certainty_flags": false_certainty,
    }


def anti_maximalism(payload: dict) -> dict:
    flags = []
    if float(payload.get("more_intelligence_bias", 0)) > 0.6: flags.append("more_intelligence_always_better_drift")
    if float(payload.get("optimization_loop", 0)) > 0.6: flags.append("endless_optimization_loops")
    if float(payload.get("replay_excess", 0)) > 0.6: flags.append("replay_excess")
    if float(payload.get("governance_inflation", 0)) > 0.6: flags.append("governance_inflation")
    if float(payload.get("strategic_perfectionism", 0)) > 0.6: flags.append("strategic_perfectionism")
    if float(payload.get("self_importance_growth", 0)) > 0.6: flags.append("institutional_self_importance_growth")
    return {
        "flags": flags,
        "minimalism_recommendations": ["reduce scope", "prune low-value loops", "enforce bounded analysis windows"] if flags else ["maximalism risk low"],
        "complexity_rollback_guidance": ["rollback non-critical expansions", "collapse redundant review cycles"] if flags else [],
    }


def sobriety_warnings(payload: dict) -> dict:
    flags = []
    if float(payload.get("institutional_grandiosity", 0)) > 0.6: flags.append("institutional_grandiosity")
    if float(payload.get("strategic_overconfidence", 0)) > 0.6: flags.append("strategic_overconfidence")
    if float(payload.get("governance_performativity", 0)) > 0.6: flags.append("governance_performativity")
    if float(payload.get("intellectualization", 0)) > 0.6: flags.append("unnecessary_intellectualization")
    if float(payload.get("recommendation_theater", 0)) > 0.6: flags.append("recommendation_theater")
    if float(payload.get("complexity_without_value", 0)) > 0.6: flags.append("complexity_without_value")
    return {"sobriety_warnings": flags, "guidance": ["recenter on mission-critical actions", "simplify strategic language"] if flags else ["sobriety healthy"]}
