from __future__ import annotations


def timing_status(payload: dict) -> dict:
    return {
        "short_term_turbulence": float(payload.get("short_term_turbulence", 0.55)),
        "medium_term_shifts": float(payload.get("medium_term_shifts", 0.62)),
        "long_term_structural_changes": float(payload.get("long_term_structural_changes", 0.48)),
        "timing_sensitivity": float(payload.get("timing_sensitivity", 0.67)),
        "urgency_half_life_hours": int(payload.get("urgency_half_life_hours", 24)),
        "strategic_recurrence": float(payload.get("strategic_recurrence", 0.4)),
        "rhythm_disruptions": int(payload.get("rhythm_disruptions", 1)),
        "advisory_only": True,
    }


def classify_timing(item: dict) -> dict:
    score = float(item.get("priority", 0.5))
    if score >= 0.9:
        cls = "immediate"
    elif score >= 0.75:
        cls = "soon"
    elif score >= 0.55:
        cls = "monitor"
    elif score >= 0.35:
        cls = "defer"
    elif score >= 0.15:
        cls = "archive"
    else:
        cls = "obsolete"
    return {"timing_classification": cls, "human_override_allowed": True}


def rhythm_scan(payload: dict) -> dict:
    volatility = float(payload.get("volatility", 0.5))
    workload = float(payload.get("operator_workload", 0.5))
    alerts = float(payload.get("alert_frequency", 0.5))
    if max(volatility, workload, alerts) > 0.85:
        state = "unstable rhythm"
    elif alerts > 0.7 and workload > 0.7:
        state = "accelerating rhythm"
    elif volatility < 0.3 and alerts < 0.3:
        state = "decaying rhythm"
    elif abs(volatility - workload) > 0.45:
        state = "disrupted rhythm"
    else:
        state = "normal rhythm"
    return {"rhythm_state": state, "inputs": payload}


def relevance_decay(payload: dict) -> dict:
    age_days = int(payload.get("age_days", 0))
    reinforced = bool(payload.get("reinforced", False))
    unresolved_critical = bool(payload.get("unresolved_critical", False))
    recurring = bool(payload.get("recurring", False))
    base = max(0.0, 1.0 - (age_days / 14))
    if reinforced:
        base += 0.2
    if recurring:
        base += 0.2
    if unresolved_critical:
        base = max(base, 0.85)
    return {"relevance_score": round(min(1.0, max(0.0, base)), 3)}


def detect_cycles(payload: dict) -> dict:
    keys = [
        "recurring_drift_cycles", "repeated_replay_failures", "periodic_calibration_degradation",
        "repeated_operator_overload_cycles", "recurring_governance_incidents", "recurring_regime_instability",
    ]
    found = [k for k in keys if int(payload.get(k, 0)) > 0]
    return {"detected_cycles": found, "cycle_count": len(found)}


def timing_conflicts(payload: dict) -> dict:
    conflicts = []
    if payload.get("urgent_low_importance"):
        conflicts.append("urgent items are low importance")
    if payload.get("important_not_urgent"):
        conflicts.append("important items are not urgent")
    if payload.get("stale_demanding_attention"):
        conflicts.append("stale items still demand attention")
    if payload.get("long_term_as_emergency"):
        conflicts.append("long-term issues treated like emergencies")
    if payload.get("short_term_over_governed"):
        conflicts.append("short-term noise is over-governed")
    return {"conflicts": conflicts, "requires_human_judgment": True}


def pacing_recommendation(payload: dict) -> dict:
    urgency = float(payload.get("urgency", 0.5))
    importance = float(payload.get("importance", 0.5))
    if importance > 0.8 and urgency > 0.7:
        action = "act now"
    elif importance > 0.7:
        action = "review today"
    elif urgency > 0.6:
        action = "review this week"
    elif importance > 0.4:
        action = "monitor quietly"
    elif urgency < 0.2:
        action = "archive later"
    else:
        action = "pause/simplify"
    return {"strategic_pacing": action, "advisory_only": True}
