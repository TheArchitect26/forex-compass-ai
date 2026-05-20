from __future__ import annotations


def pathway_catalog() -> dict:
    return {
        "pathways": [
            "stability_pathway",
            "simplification_pathway",
            "recovery_pathway",
            "expansion_pathway",
            "governance_tightening_pathway",
            "replay_confidence_recovery_pathway",
            "operator_load_reduction_pathway",
            "data_integrity_repair_pathway",
        ],
        "advisory_only": True,
        "auto_apply": False,
    }


def evaluate_triggers(payload: dict) -> dict:
    pressure = float(payload.get("pressure", 0.5))
    operator_capacity = float(payload.get("operator_capacity", 0.5))
    replay_confidence = float(payload.get("replay_confidence", 0.5))
    data_integrity = float(payload.get("data_integrity", 0.5))
    triggers = {
        "high_pressure": pressure > 0.7,
        "low_operator_capacity": operator_capacity < 0.4,
        "low_replay_confidence": replay_confidence < 0.45,
        "data_integrity_degraded": data_integrity < 0.5,
    }
    return {"triggers": triggers}


def recommend_pathway(payload: dict) -> dict:
    t = evaluate_triggers(payload)["triggers"]
    if t["data_integrity_degraded"]:
        pathway = "data_integrity_repair_pathway"
    elif t["low_replay_confidence"]:
        pathway = "replay_confidence_recovery_pathway"
    elif t["high_pressure"] and t["low_operator_capacity"]:
        pathway = "operator_load_reduction_pathway"
    elif t["high_pressure"]:
        pathway = "simplification_pathway"
    else:
        pathway = "stability_pathway"
    return {
        "recommended_pathway": pathway,
        "trigger_conditions": t,
        "entry_criteria": ["operator confirms pathway relevance", "no critical contradictions unresolved"],
        "exit_criteria": ["pressure normalizes", "operator capacity recovers"],
        "recommended_actions": ["apply minimum viable changes", "monitor outcomes for 1 week"],
        "escalation_rules": ["if pressure worsens, escalate human review"],
        "de_escalation_rules": ["if metrics stabilize, return to stability_pathway"],
        "risks_reduced": ["runaway complexity", "operator overload"],
        "risks_introduced": ["temporary slower exploration"],
        "reversibility_notes": "all pathway shifts are reversible with operator approval",
        "human_approval_required": True,
        "advisory_only": True,
        "auto_apply": False,
    }


def compare_pathways(payload: dict) -> dict:
    left = payload.get("left", "simplification_pathway")
    right = payload.get("right", "expansion_pathway")
    left_fit = float(payload.get("left_fit", 0.71))
    right_fit = float(payload.get("right_fit", 0.52))
    preferred = left if left_fit >= right_fit else right
    return {
        "preferred_pathway": preferred,
        "reasoning": f"{preferred} has stronger fit under current constraints",
        "comparison": [
            {"pathway": left, "fit": left_fit, "risk": float(payload.get("left_risk", 0.39))},
            {"pathway": right, "fit": right_fit, "risk": float(payload.get("right_risk", 0.58))},
        ],
        "human_approval_required": True,
        "advisory_only": True,
        "auto_apply": False,
    }


def pathways_memory() -> dict:
    return {
        "adaptive_pathways": ["simplification_pathway activated"],
        "evaluations": ["pressure-triggered evaluation cycle"],
        "decisions": ["operator approved operator_load_reduction_pathway"],
        "reversals": ["returned to stability_pathway after recovery"],
        "lessons": ["earlier de-escalation reduced fatigue"],
    }
