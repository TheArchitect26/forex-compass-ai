from __future__ import annotations
from datetime import UTC, datetime

MISSION_PROFILE = {
    "foundational_mission": "Personal research and signal intelligence with human-directed decision support.",
    "enduring_objectives": [
        "Preserve explainability",
        "Preserve reproducibility",
        "Protect human sovereignty",
        "Improve strategic clarity",
    ],
    "strategic_non_goals": ["autonomous execution", "self-authorizing strategy mutation"],
    "constitutional_commitments": ["integrity before optimization", "operator approval required"],
    "human_sovereignty_guarantees": ["operator override", "no irreversible autonomous changes"],
    "anti_autonomy_boundaries": ["no auto-trading", "no autonomous authority"],
    "interpretability_commitments": ["layered explainability", "auditable reasoning chain"],
}


def mission_status(payload: dict) -> dict:
    return {
        "mission_alignment_score": round(float(payload.get("mission_alignment", 0.85)) * 100, 2),
        "existential_coherence_score": round(float(payload.get("existential_coherence", 0.84)) * 100, 2),
        "strategic_purpose_integrity_score": round(float(payload.get("strategic_purpose_integrity", 0.83)) * 100, 2),
        "human_intent_alignment_score": round(float(payload.get("human_intent_alignment", 0.88)) * 100, 2),
        "institutional_authenticity_score": round(float(payload.get("institutional_authenticity", 0.82)) * 100, 2),
    }


def detect_mission_drift(payload: dict) -> dict:
    flags = []
    if float(payload.get("mission_drift", 0)) > 0.6: flags.append("mission_drift")
    if float(payload.get("optimization_drift", 0)) > 0.6: flags.append("optimization_drift")
    if float(payload.get("governance_drift", 0)) > 0.6: flags.append("governance_drift")
    if float(payload.get("complexity_drift", 0)) > 0.6: flags.append("complexity_drift")
    if float(payload.get("purpose_erosion", 0)) > 0.6: flags.append("strategic_purpose_erosion")
    if float(payload.get("identity_fragmentation", 0)) > 0.6: flags.append("institutional_identity_fragmentation")
    if float(payload.get("recommendation_purpose_divergence", 0)) > 0.6: flags.append("recommendation_purpose_divergence")
    return {"drift_flags": flags, "alignment_warning": len(flags) > 0}


def optimization_vs_purpose(payload: dict) -> dict:
    warnings = []
    if payload.get("metrics_without_value", 0) > 3: warnings.append("metrics_optimized_without_strategic_value")
    if payload.get("governance_complexity_without_benefit", 0) > 2: warnings.append("governance_complexity_without_mission_benefit")
    if payload.get("replay_sophistication_without_interpretability", 0) > 1: warnings.append("replay_sophistication_without_interpretability_gain")
    if payload.get("recommendation_proliferation", 0) > 5: warnings.append("recommendation_proliferation_without_usefulness")
    if payload.get("institutional_growth_without_clarity", 0) > 1: warnings.append("institutional_growth_without_strategic_clarity")
    return {
        "warnings": warnings,
        "simplification_proposals": ["remove low-value metrics", "consolidate governance workflows", "reduce recommendation surface"] if warnings else ["purpose alignment healthy"],
        "purpose_recovery_recommendations": ["run mission reaffirmation review", "tighten strategic relevance thresholds"] if warnings else [],
    }


def humility_safeguards(payload: dict) -> dict:
    flags = []
    if float(payload.get("overconfidence_inflation", 0)) > 0.6: flags.append("overconfidence_inflation")
    if float(payload.get("self_importance_drift", 0)) > 0.6: flags.append("institutional_self_importance_drift")
    if float(payload.get("excessive_abstraction", 0)) > 0.6: flags.append("excessive_abstraction")
    if float(payload.get("recursive_governance_complexity", 0)) > 0.6: flags.append("recursive_governance_complexity")
    if float(payload.get("false_strategic_certainty", 0)) > 0.6: flags.append("false_strategic_certainty")
    if float(payload.get("recommendation_absolutism", 0)) > 0.6: flags.append("recommendation_absolutism")
    return {"humility_flags": flags, "guidance": ["restate uncertainty", "reduce abstraction layers", "require evidence counterpoints"] if flags else ["humility posture stable"]}


def anchor_note(note: dict) -> dict:
    return {
        "operator_note": note.get("operator_note", ""),
        "mission_reaffirmation": note.get("mission_reaffirmation", ""),
        "long_horizon_intent": note.get("long_horizon_intent", ""),
        "reset_intent": note.get("reset_intent", ""),
        "anti_drift_confirmation": bool(note.get("anti_drift_confirmation", False)),
        "created_at": datetime.now(UTC).isoformat(),
    }


def anti_hollowing(payload: dict) -> dict:
    flags = []
    if payload.get("purposeless_systems", 0) > 0: flags.append("systems_persist_without_purpose")
    if payload.get("stale_rituals", 0) > 1: flags.append("stale_governance_rituals")
    if payload.get("symbolic_workflows", 0) > 1: flags.append("symbolic_workflows_without_value")
    if payload.get("recommendation_inflation", 0) > 4: flags.append("recommendation_inflation")
    if payload.get("archive_accumulation_without_relevance", 0) > 2: flags.append("archive_accumulation_without_relevance")
    if payload.get("institutional_performativity", 0) > 1: flags.append("institutional_performativity")
    return {"flags": flags, "retirement_or_simplification": ["retire low-value workflows", "prune stale recommendations", "consolidate archival noise"] if flags else ["no hollowing risk detected"]}
