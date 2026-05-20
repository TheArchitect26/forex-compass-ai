from __future__ import annotations


def _clamp(score: float) -> float:
    return max(0.0, min(100.0, round(score, 2)))


def reality_status(payload: dict) -> dict:
    practical_utility = float(payload.get("practical_utility", 0.75))
    empirical_grounding = float(payload.get("empirical_grounding", 0.74))
    real_world_relevance = float(payload.get("real_world_relevance", 0.73))
    recommendation_applicability = float(payload.get("recommendation_applicability", 0.72))
    operator_utility = float(payload.get("operator_utility", 0.76))
    replay_to_reality_consistency = float(payload.get("replay_to_reality_consistency", 0.71))
    strategic_usefulness_decay = float(payload.get("strategic_usefulness_decay", 0.2))

    return {
        "practical_usefulness": _clamp(practical_utility * 100),
        "empirical_grounding": _clamp(empirical_grounding * 100),
        "real_world_relevance": _clamp(real_world_relevance * 100),
        "recommendation_applicability": _clamp(recommendation_applicability * 100),
        "operator_utility": _clamp(operator_utility * 100),
        "replay_to_reality_consistency": _clamp(replay_to_reality_consistency * 100),
        "strategic_usefulness_decay": _clamp(strategic_usefulness_decay * 100),
        "human_final_authority": True,
        "autonomous_strategy_authority": False,
    }


def relevance_score(payload: dict) -> dict:
    practical_utility_score = _clamp(float(payload.get("practical_utility_score", 0.76)) * 100)
    empirical_grounding_score = _clamp(float(payload.get("empirical_grounding_score", 0.74)) * 100)
    strategic_usefulness_score = _clamp(float(payload.get("strategic_usefulness_score", 0.73)) * 100)
    operator_relevance_score = _clamp(float(payload.get("operator_relevance_score", 0.77)) * 100)
    reality_alignment_score = _clamp(float(payload.get("reality_alignment_score", 0.75)) * 100)
    external_validity_score = _clamp(float(payload.get("external_validity_score", 0.72)) * 100)
    overall = _clamp((practical_utility_score + empirical_grounding_score + strategic_usefulness_score + operator_relevance_score + reality_alignment_score + external_validity_score) / 6)
    return {
        "practical_utility_score": practical_utility_score,
        "empirical_grounding_score": empirical_grounding_score,
        "strategic_usefulness_score": strategic_usefulness_score,
        "operator_relevance_score": operator_relevance_score,
        "reality_alignment_score": reality_alignment_score,
        "external_validity_score": external_validity_score,
        "overall_relevance_score": overall,
    }


def detect_internal_loops(payload: dict) -> dict:
    checks = {
        "self_referential_governance_loops": float(payload.get("self_referential_governance_loops", 0)),
        "internally_reinforced_narratives": float(payload.get("internally_reinforced_narratives", 0)),
        "replay_only_optimization": float(payload.get("replay_only_optimization", 0)),
        "metrics_detached_from_usefulness": float(payload.get("metrics_detached_from_usefulness", 0)),
        "institutional_self_validation_cycles": float(payload.get("institutional_self_validation_cycles", 0)),
        "recommendation_recursion": float(payload.get("recommendation_recursion", 0)),
        "framework_preservation_without_value": float(payload.get("framework_preservation_without_value", 0)),
    }
    flags = [k for k, v in checks.items() if v > 0.6]
    return {
        "grounding_warnings": flags,
        "external_validation_recommendations": ["run replay-to-reality audit", "collect operator usefulness feedback", "prune low-value governance loops"] if flags else ["external grounding healthy"],
        "simplification_guidance": ["retire non-useful workflows", "collapse recursive governance layers"] if flags else ["no simplification pressure"],
    }


def pragmatism_safeguards(payload: dict) -> dict:
    signals = {
        "intellectual_overengineering": float(payload.get("intellectual_overengineering", 0)),
        "governance_ritualism": float(payload.get("governance_ritualism", 0)),
        "theoretical_sophistication_without_utility": float(payload.get("theoretical_sophistication_without_utility", 0)),
        "complexity_without_practical_gain": float(payload.get("complexity_without_practical_gain", 0)),
        "excessive_replay_abstraction": float(payload.get("excessive_replay_abstraction", 0)),
        "institutional_inwardness": float(payload.get("institutional_inwardness", 0)),
    }
    warnings = [k for k, v in signals.items() if v > 0.6]
    return {
        "pragmatism_warnings": warnings,
        "retirement_or_simplification_recommendations": ["retire systems maintained without value", "simplify governance pathways", "prefer actionable clarity over theory"] if warnings else ["pragmatism healthy"],
    }


def reality_workflows(payload: dict) -> dict:
    return {
        "practical_usefulness_reviews": payload.get("practical_usefulness_reviews", []),
        "replay_to_reality_audits": payload.get("replay_to_reality_audits", []),
        "recommendation_usefulness_reviews": payload.get("recommendation_usefulness_reviews", []),
        "governance_value_audits": payload.get("governance_value_audits", []),
        "strategic_simplification_reviews": payload.get("strategic_simplification_reviews", []),
        "external_grounding_assessments": payload.get("external_grounding_assessments", []),
        "operator_reviewed": True,
    }
