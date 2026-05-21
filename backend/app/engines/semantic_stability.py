from __future__ import annotations
from datetime import UTC, datetime


def orientation(payload: dict) -> dict:
    return {
        "optimization_target": payload.get("optimization_target", "reliable explainable research insights"),
        "constant_principles": payload.get("constant_principles", ["human sovereignty", "no autonomous execution", "reproducibility"]),
        "recent_assumption_changes": payload.get("recent_assumption_changes", []),
        "dominant_priorities": payload.get("dominant_priorities", ["replay integrity", "governance coherence"]),
        "rising_risks": payload.get("rising_risks", []),
        "complexity_hotspots": payload.get("complexity_hotspots", []),
    }


def orientation_score(payload: dict) -> dict:
    return {
        "semantic_coherence_score": round(float(payload.get("semantic_coherence", 0.82)) * 100, 2),
        "strategic_clarity_score": round(float(payload.get("strategic_clarity", 0.8)) * 100, 2),
        "institutional_comprehensibility_score": round(float(payload.get("institutional_comprehensibility", 0.79)) * 100, 2),
        "governance_interpretability_score": round(float(payload.get("governance_interpretability", 0.83)) * 100, 2),
        "operator_orientation_stability_score": round(float(payload.get("operator_orientation_stability", 0.81)) * 100, 2),
    }


def detect_meaning_conflicts(concepts: list[dict]) -> dict:
    by_term = {}
    conflicts = []
    for c in concepts:
        term = str(c.get("term", "")).strip().lower()
        meaning = str(c.get("meaning", "")).strip().lower()
        if not term:
            continue
        if term in by_term and by_term[term] != meaning:
            conflicts.append({"term": term, "type": "contradictory_terminology", "meanings": [by_term[term], meaning]})
        else:
            by_term[term] = meaning
    recommendations = ["clarify canonical glossary definitions", "consolidate duplicate concepts", "add successor/deprecation links"] if conflicts else ["semantic landscape stable"]
    return {"conflicts": conflicts, "clarification_recommendations": recommendations}


def stabilize_narratives(narratives: list[dict]) -> dict:
    seen = set()
    consolidated = []
    stale_ids = []
    for n in narratives:
        key = str(n.get("title", "")).strip().lower()
        if key in seen:
            continue
        seen.add(key)
        consolidated.append(n)
        if n.get("stale"):
            stale_ids.append(n.get("id"))
    return {
        "consolidated_narratives": consolidated,
        "stale_narrative_candidates": stale_ids,
        "irreversible_delete_applied": False,
    }


def comprehension_safeguards(payload: dict) -> dict:
    flags = []
    if float(payload.get("abstraction_layers", 0)) > 5: flags.append("excessive_abstraction_layers")
    if float(payload.get("terminology_overload", 0)) > 0.6: flags.append("terminology_overload")
    if float(payload.get("recursive_governance_complexity", 0)) > 0.6: flags.append("recursive_governance_complexity")
    if float(payload.get("narrative_readability_risk", 0)) > 0.6: flags.append("unreadable_strategic_narratives")
    if float(payload.get("explanation_inflation", 0)) > 0.6: flags.append("explanation_inflation")
    if float(payload.get("audit_chain_incomprehensibility", 0)) > 0.6: flags.append("audit_chain_incomprehensibility")
    return {"flags": flags, "simplification_guidance": ["reduce terminology variants", "promote glossary canonical terms", "collapse low-value explanation layers"] if flags else ["comprehension healthy"]}


def concept_lineage_entry(item: dict) -> dict:
    return {
        "concept": item.get("concept", "unknown"),
        "origin": item.get("origin", "unspecified"),
        "revisions": item.get("revisions", []),
        "contradictions": item.get("contradictions", []),
        "retired_meanings": item.get("retired_meanings", []),
        "successor_concepts": item.get("successor_concepts", []),
        "confidence_evolution": item.get("confidence_evolution", []),
        "created_at": datetime.now(UTC).isoformat(),
    }
