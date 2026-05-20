from __future__ import annotations


def _classify_severity(score: float) -> str:
    if score >= 0.85:
        return "critical"
    if score >= 0.65:
        return "serious"
    if score >= 0.45:
        return "caution"
    return "watch"


def foresight_scores(payload: dict) -> dict:
    instability = float(payload.get("instability_probability", 0.42))
    pressure = float(payload.get("pressure_accumulation", 0.48))
    return {
        "foresight_confidence": float(payload.get("foresight_confidence", 0.74)),
        "instability_probability": instability,
        "pressure_accumulation": pressure,
        "time_to_risk_estimate_days": int(payload.get("time_to_risk_estimate_days", 14)),
        "intervention_urgency": float(payload.get("intervention_urgency", max(instability, pressure))),
        "preventability_score": float(payload.get("preventability_score", 0.69)),
        "strategic_exposure_score": float(payload.get("strategic_exposure_score", 0.58)),
    }


def early_warnings(payload: dict) -> dict:
    domains = {
        "reliability_collapse": float(payload.get("reliability_collapse", 0)),
        "operator_overload": float(payload.get("operator_overload", 0)),
        "attention_fatigue": float(payload.get("attention_fatigue", 0)),
        "drift_pressure": float(payload.get("drift_pressure", 0)),
        "governance_fragmentation": float(payload.get("governance_fragmentation", 0)),
        "replay_debt": float(payload.get("replay_debt", 0)),
        "data_integrity_degradation": float(payload.get("data_integrity_degradation", 0)),
        "mission_drift": float(payload.get("mission_drift", 0)),
        "confidence_inflation": float(payload.get("confidence_inflation", 0)),
        "institutional_complexity_growth": float(payload.get("institutional_complexity_growth", 0)),
    }
    warnings = []
    for source, score in domains.items():
        if score <= 0.35:
            continue
        warnings.append({
            "warning": source,
            "classification": _classify_severity(score),
            "signal_source": source,
            "evidence": [{"metric": source, "score": round(score, 3)}],
            "likely_trajectory": "worsening" if score > 0.6 else "monitor",
            "estimated_time_horizon": "7-14 days" if score > 0.6 else "2-6 weeks",
            "suggested_human_review": "operator review within 24h" if score > 0.75 else "operator review this week",
            "advisory_only": True,
            "auto_apply": False,
        })
    return {"warnings": warnings}


def detect_trajectory(payload: dict) -> dict:
    idx = float(payload.get("trajectory_index", 0.0))
    if idx >= 0.7:
        t = "escalation"
    elif idx >= 0.4:
        t = "fragmentation"
    elif idx >= 0.2:
        t = "overload"
    elif idx <= -0.7:
        t = "renewal"
    elif idx <= -0.4:
        t = "simplification"
    elif idx <= -0.2:
        t = "stability"
    elif abs(idx) < 0.1:
        t = "stagnation"
    else:
        t = "drift"
    return {"trajectory": t}


def intervention_plan(payload: dict) -> dict:
    urgency = float(payload.get("intervention_urgency", 0.5))
    plan = ["monitor quietly"]
    if urgency > 0.35:
        plan.append("review this week")
    if urgency > 0.5:
        plan += ["simplify workload", "run replay audit"]
    if urgency > 0.65:
        plan += ["check data integrity", "pause expansion", "consolidate workflows"]
    if urgency > 0.8:
        plan.append("escalate human review")
    return {"intervention_plan": plan, "advisory_only": True, "auto_apply": False}


def foresight_memory() -> dict:
    return {
        "early_warnings": ["operator_overload:serious"],
        "forecasts": ["possible replay debt growth in 2 weeks"],
        "intervention_plans": ["simplify workload + replay audit"],
        "resolved_warnings": ["attention fatigue normalized"],
        "false_alarms": ["temporary governance spike"],
        "missed_warnings": ["late detection of drift pressure"],
        "trajectory_changes": ["overload -> simplification"],
    }
