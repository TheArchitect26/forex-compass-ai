from __future__ import annotations


def _clamp(v: float) -> float:
    return max(0.0, min(100.0, round(v, 2)))


def classify_attention(payload: dict) -> dict:
    return {
        "critical_signals": payload.get("critical_signals", []),
        "high_value_insights": payload.get("high_value_insights", []),
        "low_value_noise": payload.get("low_value_noise", []),
        "repetitive_recommendations": payload.get("repetitive_recommendations", []),
        "strategic_distractions": payload.get("strategic_distractions", []),
        "urgency_inflation": payload.get("urgency_inflation", []),
        "attention_fragmentation": payload.get("attention_fragmentation", []),
        "human_attention_sovereign": True,
    }


def extract_strategic_signal(payload: dict) -> dict:
    return {
        "highest_impact_findings": payload.get("highest_impact_findings", []),
        "major_strategic_shifts": payload.get("major_strategic_shifts", []),
        "emerging_instability": payload.get("emerging_instability", []),
        "recurring_contradictions": payload.get("recurring_contradictions", []),
        "reliability_collapses": payload.get("reliability_collapses", []),
        "major_governance_risks": payload.get("major_governance_risks", []),
        "practical_opportunities": payload.get("practical_opportunities", []),
        "suppressed_items": {
            "redundant_alerts": payload.get("redundant_alerts", []),
            "low_impact_recommendations": payload.get("low_impact_recommendations", []),
            "repetitive_narratives": payload.get("repetitive_narratives", []),
            "non_actionable_complexity": payload.get("non_actionable_complexity", []),
        },
    }


def priority_status(payload: dict) -> dict:
    strategic_importance = _clamp(float(payload.get("strategic_importance_score", 0.79)) * 100)
    urgency = _clamp(float(payload.get("urgency_score", 0.65)) * 100)
    long_term_relevance = _clamp(float(payload.get("long_term_relevance_score", 0.77)) * 100)
    operator_impact = _clamp(float(payload.get("operator_impact_score", 0.74)) * 100)
    attention_efficiency = _clamp(float(payload.get("attention_efficiency_score", 0.72)) * 100)
    signal_to_noise = _clamp(float(payload.get("signal_to_noise_ratio", 0.7)) * 100)
    return {
        "strategic_importance_score": strategic_importance,
        "urgency_score": urgency,
        "long_term_relevance_score": long_term_relevance,
        "operator_impact_score": operator_impact,
        "attention_efficiency_score": attention_efficiency,
        "signal_to_noise_ratio": signal_to_noise,
    }


def detect_attention_fatigue(payload: dict) -> dict:
    factors = {
        "alert_fatigue": float(payload.get("alert_fatigue", 0)),
        "recommendation_overload": float(payload.get("recommendation_overload", 0)),
        "workflow_switching": float(payload.get("workflow_switching", 0)),
        "dashboard_fragmentation": float(payload.get("dashboard_fragmentation", 0)),
        "context_switch_pressure": float(payload.get("context_switch_pressure", 0)),
        "investigation_sprawl": float(payload.get("investigation_sprawl", 0)),
        "institutional_attention_dilution": float(payload.get("institutional_attention_dilution", 0)),
    }
    flags = [k for k, v in factors.items() if v > 0.6]
    return {
        "fatigue_flags": flags,
        "focus_recommendations": ["single-threaded triage", "top-3 strategic priorities"] if flags else ["attention load healthy"],
        "suppression_suggestions": ["mute low-impact alerts", "collapse repetitive recommendations"] if flags else [],
        "prioritization_guidance": ["escalate only high-impact contradictions", "defer low-urgency reviews"] if flags else [],
        "simplification_interventions": ["reduce dashboard modules", "archive stale investigations"] if flags else [],
    }


def relevance_half_life(payload: dict) -> dict:
    return {
        "recommendations_decay_days": int(payload.get("recommendations_decay_days", 7)),
        "anomalies_decay_days": int(payload.get("anomalies_decay_days", 5)),
        "alerts_decay_days": int(payload.get("alerts_decay_days", 3)),
        "workflows_decay_days": int(payload.get("workflows_decay_days", 14)),
        "investigations_decay_days": int(payload.get("investigations_decay_days", 10)),
        "strategic_narratives_decay_days": int(payload.get("strategic_narratives_decay_days", 21)),
    }


def focus_mode(mode: str) -> dict:
    profiles = {
        "executive_overview": ["top-priority intelligence", "urgency distribution", "major risks only"],
        "deep_research": ["full evidence chains", "contradiction map", "reliability trend"],
        "anomaly_investigation": ["anomaly timeline", "root-cause candidates", "escalation gates"],
        "governance_review": ["governance incidents", "policy pressure", "constitutional conflicts"],
        "replay_analysis": ["replay-to-reality deltas", "scenario outliers", "stability regressions"],
        "recovery_simplification": ["noise suppression", "workload reduction", "retirement opportunities"],
    }
    return {"mode": mode, "priorities": profiles.get(mode, ["balanced-priority-view"]), "preserves_explainability": True}


def anti_noise_governance(payload: dict) -> dict:
    factors = {
        "institutional_busyness_without_value": float(payload.get("institutional_busyness_without_value", 0)),
        "metric_inflation": float(payload.get("metric_inflation", 0)),
        "alert_proliferation": float(payload.get("alert_proliferation", 0)),
        "dashboard_sprawl": float(payload.get("dashboard_sprawl", 0)),
        "strategic_clutter": float(payload.get("strategic_clutter", 0)),
        "attention_fragmentation_loops": float(payload.get("attention_fragmentation_loops", 0)),
    }
    flags = [k for k, v in factors.items() if v > 0.6]
    return {
        "anti_noise_flags": flags,
        "pruning_recommendations": ["retire low-value metrics", "reduce alert classes", "merge overlapping dashboards"] if flags else ["noise governance healthy"],
    }
