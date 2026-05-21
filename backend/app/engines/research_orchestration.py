from __future__ import annotations
from app.engines.portfolio import compute_metrics


def priority_from_signals(payload: dict) -> str:
    drift = float(payload.get("drift_score", 0))
    integrity = float(payload.get("integrity_score", 100))
    regime_instability = float(payload.get("regime_instability", 0))
    regression_failures = int(payload.get("regression_failures", 0))
    drawdown = float(payload.get("drawdown", 0))
    if integrity < 60 or drawdown > 500:
        return "critical"
    if drift > 70 or regime_instability > 65 or regression_failures >= 3:
        return "high"
    if drift > 40 or regime_instability > 40:
        return "elevated"
    return "normal"


def coordinated_health(payload: dict) -> dict:
    components = {
        "data_health": float(payload.get("data_health", 80)),
        "calibration_health": float(payload.get("calibration_health", 75)),
        "replay_integrity": float(payload.get("replay_integrity", 80)),
        "portfolio_reliability": float(payload.get("portfolio_reliability", 70)),
        "adaptive_stability": float(payload.get("adaptive_stability", 72)),
        "governance_safety": float(payload.get("governance_safety", 90)),
        "drift_pressure": max(0.0, 100.0 - float(payload.get("drift_score", 30))),
    }
    score = round(sum(components.values()) / len(components), 2)
    return {"score": score, "components": components}


def generate_insights(evidence: dict) -> list[dict]:
    insights = []
    if evidence.get("volatility") == "high" and evidence.get("session") == "london_overlap":
        insights.append({
            "message": "RSI weighting underperforms during high-volatility London overlap.",
            "confidence": 0.74,
            "regimes": ["high_volatility"],
            "profiles": ["aggressive"],
            "evidence_refs": ["replay", "calibration"],
            "reproducible": True,
        })
    if float(evidence.get("reliability_delta", 0)) < -8:
        insights.append({
            "message": "Aggressive profile reliability degraded after volatility regime shift.",
            "confidence": 0.79,
            "regimes": ["regime_shift"],
            "profiles": ["aggressive"],
            "evidence_refs": ["reliability", "regime"],
            "reproducible": True,
        })
    if evidence.get("correlated_gold_usd"):
        insights.append({
            "message": "Portfolio exposure risk increases during correlated gold/USD moves.",
            "confidence": 0.71,
            "regimes": ["risk_off"],
            "profiles": ["intraday", "swing"],
            "evidence_refs": ["portfolio_stress", "replay"],
            "reproducible": True,
        })
    return insights


def recommendations_from_insights(insights: list[dict]) -> list[dict]:
    out = []
    for i in insights:
        msg = i["message"].lower()
        if "underperforms" in msg:
            out.append({"recommendation": "re-run calibration", "explainability": "signal weighting degradation evidence", "auto_apply": False})
        elif "degraded" in msg:
            out.append({"recommendation": "reduce aggressive weighting", "explainability": "reliability trend decline", "auto_apply": False})
        elif "exposure risk" in msg:
            out.append({"recommendation": "inspect integrity gaps", "explainability": "portfolio correlation stress signal", "auto_apply": False})
    return out
