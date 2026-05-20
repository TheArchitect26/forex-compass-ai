from __future__ import annotations


def prioritize_recommendation(rec: dict) -> dict:
    impact = float(rec.get("impact", 0.5))
    confidence = float(rec.get("confidence", 0.5))
    reproducible = bool(rec.get("reproducible", True))
    urgency = "high" if impact > 0.75 else "medium" if impact > 0.4 else "low"
    severity = "critical" if impact > 0.85 else "elevated" if impact > 0.6 else "normal"
    return {
        **rec,
        "urgency": urgency,
        "severity": severity,
        "research_impact": round(impact * 100, 1),
        "confidence": confidence,
        "reproducibility_status": "verified" if reproducible else "unverified",
        "auto_apply": False,
    }
