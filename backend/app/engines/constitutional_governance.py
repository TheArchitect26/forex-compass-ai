from __future__ import annotations
from datetime import UTC, datetime

CONSTITUTIONAL_RULES = [
    "no autonomous execution",
    "no silent adaptation",
    "explainability required",
    "reproducibility required",
    "sandbox before promotion",
    "operator approval required",
    "integrity before optimization",
    "reliability before aggressiveness",
]


def validate_consistency(payload: dict) -> dict:
    narratives = payload.get("narratives", [])
    recommendations = payload.get("recommendations", [])
    hierarchy = payload.get("confidence_hierarchy", {})
    strategic_scores = payload.get("strategic_scores", {})

    contradictions = []
    if any("increased" in n.lower() for n in narratives) and any("decreased" in n.lower() for n in narratives):
        contradictions.append("contradictory_narratives")
    if any("increase" in str(r.get("recommendation", "")).lower() for r in recommendations) and any("reduce" in str(r.get("recommendation", "")).lower() for r in recommendations):
        contradictions.append("unstable_recommendations")
    if float(hierarchy.get("strategic_confidence", 0.6)) > float(hierarchy.get("raw_signal_confidence", 0.6)) + 0.25:
        contradictions.append("confidence_inflation")
    if float(strategic_scores.get("governance_integrity_score", 100)) < 40 and float(strategic_scores.get("intelligence_confidence_score", 0)) > 70:
        contradictions.append("score_mismatch")

    governance_violations = [r for r in payload.get("rules_checked", []) if r.get("status") == "violated"]
    return {
        "ok": len(contradictions) == 0 and len(governance_violations) == 0,
        "contradictions": contradictions,
        "governance_violations": governance_violations,
        "reproducible": True,
    }


def explainability_score(payload: dict) -> dict:
    evidence = float(payload.get("evidence_completeness", 0.8))
    reproducibility = float(payload.get("reproducibility_coverage", 0.8))
    narrative = float(payload.get("narrative_consistency", 0.8))
    traceability = float(payload.get("recommendation_traceability", 0.8))
    audit = float(payload.get("audit_completeness", 0.8))
    compliance = float(payload.get("governance_compliance", 0.9))
    score = (evidence + reproducibility + narrative + traceability + audit + compliance) / 6
    return {
        "score": round(score * 100, 2),
        "components": {
            "evidence_completeness": evidence,
            "reproducibility_coverage": reproducibility,
            "narrative_consistency": narrative,
            "recommendation_traceability": traceability,
            "audit_completeness": audit,
            "governance_compliance": compliance,
        },
    }


def confidence_decay(confidence: float, days_stale: int, unresolved_anomalies: int, stale_replay_days: int) -> float:
    decay = days_stale * 0.002 + unresolved_anomalies * 0.015 + stale_replay_days * 0.001
    return round(max(0.0, confidence - decay), 4)


def trust_pressure(payload: dict) -> dict:
    pressure = 0.0
    pressure += float(payload.get("unresolved_contradictions", 0)) * 8
    pressure += float(payload.get("confidence_inflation", 0)) * 15
    pressure += float(payload.get("recommendation_reversals", 0)) * 6
    pressure += float(payload.get("anomaly_fatigue", 0)) * 10
    pressure += float(payload.get("governance_overrides", 0)) * 9
    pressure += float(payload.get("critical_drift_unresolved", 0)) * 14
    level = "low" if pressure < 25 else "elevated" if pressure < 55 else "high"
    return {"trust_pressure_score": round(min(100, pressure), 2), "level": level}


def recommendation_with_trust_fields(rec: dict) -> dict:
    evidence_cov = float(rec.get("evidence_coverage", 0.7))
    speculative = evidence_cov < 0.5 or rec.get("reproducibility_status") == "unverified"
    return {
        **rec,
        "reversibility": rec.get("reversibility", "high"),
        "governance_risk": rec.get("governance_risk", "low"),
        "historical_consistency": rec.get("historical_consistency", 0.7),
        "speculative": speculative,
        "weak_evidence": evidence_cov < 0.55,
        "generated_at": datetime.now(UTC).isoformat(),
        "advisory_only": True,
    }
