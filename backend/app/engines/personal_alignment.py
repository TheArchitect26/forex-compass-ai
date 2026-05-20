from __future__ import annotations


def _clamp(v: float) -> float:
    return max(0.0, min(100.0, round(v, 2)))


def personal_alignment_status(payload: dict) -> dict:
    return {
        "operator_priorities": payload.get("operator_priorities", ["capital-preservation", "signal-quality", "time-efficiency"]),
        "strategic_goals": payload.get("strategic_goals", ["consistent-decision-support", "reduced-noise"]),
        "preferred_research_focus": payload.get("preferred_research_focus", ["regime-context", "risk-conditions"]),
        "cognitive_workload_tolerance": payload.get("cognitive_workload_tolerance", "moderate"),
        "risk_appetite_evolution": payload.get("risk_appetite_evolution", "stable"),
        "workflow_preferences": payload.get("workflow_preferences", ["simplified-mode", "replay-analysis-mode"]),
        "long_term_operational_intent": payload.get("long_term_operational_intent", "human-directed strategic support"),
        "human_choice_final": True,
        "autonomous_life_management": False,
    }


def context_status(payload: dict) -> dict:
    return {
        "active_focus_areas": payload.get("active_focus_areas", ["EURUSD", "risk-filtering"]),
        "current_strategic_concerns": payload.get("current_strategic_concerns", ["overtrading-risk", "headline-volatility"]),
        "reduced_capacity_period": bool(payload.get("reduced_capacity_period", False)),
        "high_stress_period": bool(payload.get("high_stress_period", False)),
        "experimentation_phase": bool(payload.get("experimentation_phase", False)),
        "maintenance_phase": bool(payload.get("maintenance_phase", True)),
        "simplification_phase": bool(payload.get("simplification_phase", True)),
    }


def alignment_score(payload: dict) -> dict:
    ors = _clamp(float(payload.get("operator_relevance_score", 0.78)) * 100)
    wus = _clamp(float(payload.get("workflow_usefulness_score", 0.74)) * 100)
    sas = _clamp(float(payload.get("strategic_alignment_score", 0.76)) * 100)
    css = _clamp(float(payload.get("cognitive_sustainability_score", 0.72)) * 100)
    ppas = _clamp(float(payload.get("personal_priority_alignment_score", 0.77)) * 100)
    overall = _clamp((ors + wus + sas + css + ppas) / 5)
    return {
        "operator_relevance_score": ors,
        "workflow_usefulness_score": wus,
        "strategic_alignment_score": sas,
        "cognitive_sustainability_score": css,
        "personal_priority_alignment_score": ppas,
        "overall_personal_alignment_score": overall,
    }


def adaptive_workflow(mode: str, payload: dict) -> dict:
    mappings = {
        "simplified_mode": ["suppress-low-priority-alerts", "top-3-actions-only"],
        "deep_research_mode": ["expanded-evidence-view", "contradiction-tracking-enabled"],
        "governance_review_mode": ["compliance-first-ordering", "incident-review-focus"],
        "maintenance_mode": ["backlog-pruning", "health-checks-first"],
        "replay_analysis_mode": ["replay-realism-deltas", "scenario-comparison-view"],
    }
    return {
        "mode": mode,
        "adapted_workflow": mappings.get(mode, ["balanced-default-workflow"]),
        "preferred_complexity_level": payload.get("preferred_complexity_level", "moderate"),
        "current_operational_phase": payload.get("current_operational_phase", "maintenance"),
    }


def energy_safeguards(payload: dict) -> dict:
    factors = {
        "operator_overload": float(payload.get("operator_overload", 0)),
        "research_exhaustion": float(payload.get("research_exhaustion", 0)),
        "governance_fatigue": float(payload.get("governance_fatigue", 0)),
        "alert_desensitization": float(payload.get("alert_desensitization", 0)),
        "workflow_saturation": float(payload.get("workflow_saturation", 0)),
        "strategic_burnout_risk": float(payload.get("strategic_burnout_risk", 0)),
    }
    flags = [k for k, v in factors.items() if v > 0.6]
    return {
        "overload_flags": flags,
        "simplification_recommendations": ["reduce dashboard surface", "defer noncritical governance reviews"] if flags else ["load sustainable"],
        "pause_recommendations": ["pause experimentation for 48h", "run maintenance-only cycle"] if flags else [],
        "focus_narrowing_suggestions": ["single-pair focus", "single-goal planning window"] if flags else [],
        "low_priority_suppression_guidance": ["suppress low-confidence and low-impact alerts"] if flags else [],
    }


def simplification_layer(payload: dict) -> dict:
    return {
        "retirement_suggestions": payload.get("retirement_suggestions", ["retire low-value replay routine"]),
        "simplification_plans": payload.get("simplification_plans", ["merge duplicate governance checks"]),
        "operational_lightening_recommendations": payload.get("operational_lightening_recommendations", ["weekly deep-review cap"]),
    }
