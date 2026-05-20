from __future__ import annotations
from datetime import UTC, datetime


def evaluate_epistemic_integrity(payload: dict) -> dict:
    evidence_quality = float(payload.get("evidence_quality", 0.75))
    evidence_freshness = float(payload.get("evidence_freshness", 0.7))
    contradiction_density = float(payload.get("contradiction_density", 0.2))
    unsupported_risk = float(payload.get("unsupported_narrative_risk", 0.2))
    stale_assumptions = float(payload.get("stale_assumptions", 0.2))
    circular_logic = float(payload.get("circular_recommendation_logic", 0.1))
    weak_inference = float(payload.get("weak_inference_chains", 0.2))

    epistemic_integrity = max(0.0, (evidence_quality * 0.3 + evidence_freshness * 0.25 + (1-contradiction_density) * 0.15 + (1-unsupported_risk) * 0.1 + (1-stale_assumptions) * 0.1 + (1-circular_logic) * 0.05 + (1-weak_inference) * 0.05))
    contradiction_pressure = min(1.0, contradiction_density * 0.5 + unsupported_risk * 0.3 + circular_logic * 0.2)
    institutional_coherence = max(0.0, 1 - (contradiction_density * 0.4 + stale_assumptions * 0.3 + weak_inference * 0.3))
    strategic_fragmentation = min(1.0, float(payload.get("fragmented_clusters", 0)) * 0.2 + float(payload.get("isolated_conclusions", 0)) * 0.2)
    governance_resilience = max(0.0, 1 - float(payload.get("recurring_governance_incidents", 0)) * 0.08)

    return {
        "epistemic_integrity": round(epistemic_integrity * 100, 2),
        "contradiction_pressure": round(contradiction_pressure * 100, 2),
        "institutional_coherence": round(institutional_coherence * 100, 2),
        "evidence_freshness": round(evidence_freshness * 100, 2),
        "strategic_fragmentation": round(strategic_fragmentation * 100, 2),
        "governance_resilience": round(governance_resilience * 100, 2),
    }


def detect_knowledge_fragmentation(nodes: list[dict], edges: list[dict]) -> dict:
    connected = set()
    for e in edges:
        connected.add(e.get("source"))
        connected.add(e.get("target"))
    isolated = [n for n in nodes if n.get("id") not in connected]
    contradictions = [e for e in edges if e.get("relation") == "contradicts"]
    unresolved_chains = [e for e in contradictions if not e.get("resolved", False)]
    return {
        "fragmented_clusters": max(0, len(isolated)),
        "isolated_conclusions": [n.get("id") for n in isolated],
        "unresolved_contradiction_chains": len(unresolved_chains),
    }


def assumption_decay(confidence: float, days_since_validation: int, replay_coverage: float, contradictory_evidence_count: int) -> float:
    decay = days_since_validation * 0.0015 + (1 - replay_coverage) * 0.2 + contradictory_evidence_count * 0.03
    return round(max(0.0, confidence - decay), 4)


def archive_stabilization(archives: list[dict]) -> dict:
    seen_titles = set()
    duplicates = []
    contradictions = []
    grouped = {}
    for a in archives:
        title = str(a.get("title", "")).strip().lower()
        if title in seen_titles:
            duplicates.append(a.get("id"))
        seen_titles.add(title)
        key = a.get("group", a.get("archive_type", "general"))
        grouped.setdefault(key, 0)
        grouped[key] += 1
        if a.get("conflicts_with"):
            contradictions.append(a.get("id"))
    return {
        "duplicate_narratives": duplicates,
        "conflicting_archives": contradictions,
        "grouped_investigations": grouped,
    }


def lifecycle_review_gate(change: dict) -> dict:
    return {
        "requires_operator_review": True,
        "review_type": change.get("review_type", "assumption_update"),
        "auto_apply": False,
        "submitted_at": datetime.now(UTC).isoformat(),
    }
