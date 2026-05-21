from __future__ import annotations


def learning_status() -> dict:
    return {
        "learning_sources": [
            "causal_analyses",
            "foresight_warnings",
            "scenario_runs",
            "pathway_decisions",
            "governance_incidents",
            "reality_reviews",
            "attention_interventions",
            "simplification_actions",
            "replay_audits",
            "operator_feedback",
        ],
        "advisory_only": True,
        "auto_apply": False,
    }


def intervention_review(payload: dict) -> dict:
    intended = payload.get("intended_outcome", "reduce overload")
    actual = payload.get("actual_outcome", "partial overload reduction")
    effectiveness = float(payload.get("effectiveness_score", 0.67))
    confidence = float(payload.get("confidence_in_lesson", 0.58))
    return {
        "intended_outcome": intended,
        "actual_outcome": actual,
        "effectiveness_score": effectiveness,
        "time_to_impact_days": int(payload.get("time_to_impact_days", 10)),
        "side_effects": payload.get("side_effects", ["temporary throughput dip"]),
        "reversibility_success": bool(payload.get("reversibility_success", True)),
        "operator_burden": float(payload.get("operator_burden", 0.44)),
        "confidence_in_lesson": confidence,
        "weak_evidence": confidence < 0.5,
        "human_review_required": True,
        "advisory_only": True,
        "auto_apply": False,
    }


def extract_lessons(payload: dict) -> dict:
    lessons = payload.get("lessons", [
        {
            "lesson": "Simplification pathway reduced overload pressure.",
            "evidence": ["operator_load trend", "attention fatigue decline"],
            "confidence": 0.72,
            "affected_systems": ["attention", "operator_load", "pathways"],
            "limitations": ["short observation window"],
        },
        {
            "lesson": "Governance tightening increased burden without usefulness gain.",
            "evidence": ["governance incidents flat", "operator burden up"],
            "confidence": 0.55,
            "affected_systems": ["governance", "operator_load"],
            "limitations": ["causation uncertain"],
        },
    ])
    for l in lessons:
        l["advisory_only"] = True
        l["auto_apply"] = False
        l["weak_evidence"] = float(l.get("confidence", 0)) < 0.5
    return {"lessons": lessons, "human_review_required": True}


def forecast_review(payload: dict) -> dict:
    predicted = payload.get("predicted", "replay debt increase")
    actual = payload.get("actual", "replay debt stable")
    accuracy = float(payload.get("accuracy_score", 0.46))
    return {
        "predicted": predicted,
        "actual": actual,
        "accuracy_score": accuracy,
        "miss_reason": payload.get("miss_reason", "mitigations applied earlier than expected"),
        "weak_evidence": accuracy < 0.5,
        "advisory_only": True,
        "auto_apply": False,
    }


def assumption_review(payload: dict) -> dict:
    return {
        "assumption": payload.get("assumption", "governance expansion improves resilience"),
        "status": payload.get("status", "weaken"),
        "evidence": payload.get("evidence", ["burden rose, incidents unchanged"]),
        "confidence": float(payload.get("confidence", 0.54)),
        "recommendation": "human review before updating assumption registry",
        "advisory_only": True,
        "auto_apply": False,
        "human_review_required": True,
    }


def learning_memory() -> dict:
    return {
        "institutional_lessons": ["simplification helped attention stability"],
        "intervention_reviews": ["replay audit cycle effectiveness moderate"],
        "forecast_reviews": ["drift escalation overestimated"],
        "assumption_reviews": ["governance-tightening assumption weakened"],
        "successful_patterns": ["early simplification + replay audit combo"],
        "failed_patterns": ["complexity-first expansion during overload"],
    }
