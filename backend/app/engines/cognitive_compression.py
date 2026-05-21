from __future__ import annotations


def compress_intelligence(payload: dict) -> dict:
    return {
        "key_strategic_themes": payload.get("themes", [])[:5],
        "recurring_instability_patterns": payload.get("instability_patterns", [])[:5],
        "recurring_successful_conditions": payload.get("successful_conditions", [])[:5],
        "major_regime_transitions": payload.get("regime_transitions", [])[:5],
        "critical_operational_risks": payload.get("operational_risks", [])[:5],
        "top_unresolved_anomalies": payload.get("unresolved_anomalies", [])[:5],
    }


def generate_strategic_narratives(evidence: dict) -> list[dict]:
    out = []
    if evidence.get("aggressive_instability_trend") == "up" and evidence.get("volatility_overlap"):
        out.append({
            "narrative": "Aggressive profile instability has increased steadily during overlapping London/New York volatility spikes.",
            "confidence": 0.77,
            "evidence_refs": evidence.get("refs", []),
            "reproducible": True,
        })
    if evidence.get("resilience_after_conservative_adjustment"):
        out.append({
            "narrative": "Portfolio resilience improved after conservative weighting adjustments in ranging conditions.",
            "confidence": 0.73,
            "evidence_refs": evidence.get("refs", []),
            "reproducible": True,
        })
    if evidence.get("integrity_backlog_correlation"):
        out.append({
            "narrative": "Integrity degradation repeatedly correlates with replay backlog pressure.",
            "confidence": 0.8,
            "evidence_refs": evidence.get("refs", []),
            "reproducible": True,
        })
    return out


def confidence_hierarchy(raw: dict) -> dict:
    return {
        "raw_signal_confidence": float(raw.get("raw_signal_confidence", 0.6)),
        "regime_confidence": float(raw.get("regime_confidence", 0.6)),
        "calibration_confidence": float(raw.get("calibration_confidence", 0.6)),
        "replay_confidence": float(raw.get("replay_confidence", 0.6)),
        "strategic_confidence": float(raw.get("strategic_confidence", 0.6)),
        "governance_confidence": float(raw.get("governance_confidence", 0.8)),
    }


def synthesize_recommendations(recs: list[dict]) -> dict:
    short_term = [r for r in recs if r.get("horizon") == "short"]
    medium_term = [r for r in recs if r.get("horizon") == "medium"]
    long_term = [r for r in recs if r.get("horizon") == "long"]
    unresolved = [r for r in recs if r.get("resolved") is False]
    return {
        "short_term_priorities": short_term,
        "medium_term_goals": medium_term,
        "long_term_concerns": long_term,
        "recurring_unresolved_issues": len(unresolved),
        "escalating_instability": any(r.get("severity") == "critical" for r in recs),
        "conflicting_priorities": any("increase" in str(a.get("recommendation", "")).lower() for a in recs) and any("reduce" in str(a.get("recommendation", "")).lower() for a in recs),
        "investigation_concentration_risk": len(short_term) > 5,
    }
