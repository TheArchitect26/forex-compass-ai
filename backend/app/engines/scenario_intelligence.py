from __future__ import annotations


def scenario_status() -> dict:
    return {
        "available_scenarios": [
            "governance_simplification",
            "replay_cadence_increase",
            "attention_load_reduction",
            "strategy_profile_tightening",
            "data_integrity_degradation",
            "operator_workload_reduction",
            "research_expansion_pause",
            "calibration_drift_escalation",
            "portfolio_stress_increase",
            "mission_alignment_recovery",
        ],
        "advisory_only": True,
        "auto_apply": False,
    }


def run_scenario(payload: dict) -> dict:
    scenario = payload.get("scenario", "governance_simplification")
    return {
        "scenario": scenario,
        "assumptions": payload.get("assumptions", ["no market execution", "human review required"]),
        "primary_effects": ["reduced immediate complexity"],
        "second_order_effects": ["possible delayed blind spots"],
        "tradeoffs": ["simplicity vs depth"],
        "risks_reduced": ["operator overload"],
        "risks_introduced": ["under-monitoring risk"],
        "operator_impact": "moderate load reduction",
        "governance_impact": "streamlined controls",
        "reality_usefulness_impact": "improves short-term clarity",
        "replay_research_impact": "slower coverage expansion",
        "attention_impact": "higher focus density",
        "time_horizon": "1-4 weeks",
        "scores": {
            "upside_score": float(payload.get("upside_score", 0.72)),
            "downside_risk_score": float(payload.get("downside_risk_score", 0.41)),
            "reversibility_score": float(payload.get("reversibility_score", 0.78)),
            "confidence_score": float(payload.get("confidence_score", 0.63)),
            "operator_burden_score": float(payload.get("operator_burden_score", 0.38)),
            "strategic_fit_score": float(payload.get("strategic_fit_score", 0.74)),
            "implementation_difficulty": float(payload.get("implementation_difficulty", 0.44)),
            "unintended_consequence_risk": float(payload.get("unintended_consequence_risk", 0.36)),
        },
        "estimates": ["scores are scenario estimates, not forecasts"],
        "facts": payload.get("facts", []),
        "uncertainty_notes": ["scenario planning is non-deterministic", "second-order effects can compound"],
        "recommended_human_review": "review by operator before any policy change",
        "advisory_only": True,
        "auto_apply": False,
    }


def compare_scenarios(payload: dict) -> dict:
    left = payload.get("left", "simplify_governance")
    right = payload.get("right", "increase_replay_audits")
    left_score = float(payload.get("left_score", 0.68))
    right_score = float(payload.get("right_score", 0.64))
    preferred = left if left_score >= right_score else right
    return {
        "preferred_option": preferred,
        "reasoning": f"{preferred} has higher strategic-fit minus burden balance",
        "tradeoff_table": [
            {"option": left, "fit": left_score, "burden": float(payload.get("left_burden", 0.42))},
            {"option": right, "fit": right_score, "burden": float(payload.get("right_burden", 0.48))},
        ],
        "uncertainty_notes": ["small score differences are not decisive"],
        "human_review_required": True,
        "advisory_only": True,
        "auto_apply": False,
    }


def scenario_memory() -> dict:
    return {
        "scenario_runs": ["governance_simplification_v1"],
        "comparisons": ["simplify_governance vs increase_replay_audits"],
        "consequence_assessments": ["attention improved, replay depth temporarily reduced"],
        "false_assumptions": ["operator capacity overestimated"],
        "missed_consequences": ["governance drift follow-up lag"],
    }
