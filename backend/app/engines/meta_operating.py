from __future__ import annotations
from datetime import UTC, datetime


def coordination_status(payload: dict) -> dict:
    divergence = float(payload.get("subsystem_divergence", 0.2))
    duplicated_logic = float(payload.get("duplicated_governance_logic", 0.2))
    workflow_frag = float(payload.get("workflow_fragmentation", 0.2))
    replay_pressure = float(payload.get("replay_inconsistency_pressure", 0.2))
    rec_frag = float(payload.get("recommendation_fragmentation", 0.2))
    sync_fail = float(payload.get("synchronization_failures", 0.1))
    overhead = float(payload.get("coordination_overhead", 0.3))

    pressure = min(100.0, (divergence + duplicated_logic + workflow_frag + replay_pressure + rec_frag + sync_fail + overhead) / 7 * 100)
    level = "low" if pressure < 35 else "elevated" if pressure < 65 else "high"
    return {
        "coordination_pressure": round(pressure, 2),
        "level": level,
        "signals": {
            "subsystem_divergence": divergence,
            "duplicated_governance_logic": duplicated_logic,
            "workflow_fragmentation": workflow_frag,
            "replay_inconsistency_pressure": replay_pressure,
            "recommendation_fragmentation": rec_frag,
            "synchronization_failures": sync_fail,
            "coordination_overhead": overhead,
        },
    }


def build_coordination_graph(nodes: list[dict], links: list[dict]) -> dict:
    conflict_risk = [l for l in links if float(l.get("conflict_risk", 0)) > 0.6]
    unsynced = [l for l in links if l.get("synchronization_status") in {"stale", "failed"}]
    return {
        "nodes": nodes,
        "links": links,
        "dependency_strength_avg": round(sum(float(l.get("dependency_strength", 0.5)) for l in links) / max(1, len(links)), 3),
        "coordination_pressure_links": len(conflict_risk),
        "unsynchronized_links": len(unsynced),
    }


def synchronization_check(payload: dict) -> dict:
    flags = []
    if payload.get("unsynchronized_eras"):
        flags.append("unsynchronized_eras")
    if payload.get("incompatible_governance_assumptions"):
        flags.append("incompatible_governance_assumptions")
    if payload.get("replay_governance_drift"):
        flags.append("replay_governance_drift")
    if payload.get("stale_continuity_mappings"):
        flags.append("stale_continuity_mappings")
    return {"synchronized": len(flags) == 0, "flags": flags, "operator_review_required": True}


def meta_explainability(payload: dict) -> dict:
    return {
        "executive": payload.get("executive", "Coordination stable with monitored divergence."),
        "strategic": payload.get("strategic", "Subsystem narratives are aligned with minor synchronization pressure."),
        "technical": payload.get("technical", "Link-level dependency checks indicate moderate graph cohesion."),
        "audit": payload.get("audit", []),
        "reproducible": True,
    }


def meta_resilience(payload: dict) -> dict:
    return {
        "coordination_resilience": round(float(payload.get("coordination_resilience", 0.8)) * 100, 2),
        "synchronization_integrity": round(float(payload.get("synchronization_integrity", 0.78)) * 100, 2),
        "institutional_cohesion": round(float(payload.get("institutional_cohesion", 0.82)) * 100, 2),
        "subsystem_alignment": round(float(payload.get("subsystem_alignment", 0.79)) * 100, 2),
        "strategic_continuity_integrity": round(float(payload.get("strategic_continuity_integrity", 0.81)) * 100, 2),
        "governance_coordination_health": round(float(payload.get("governance_coordination_health", 0.84)) * 100, 2),
    }


def consolidation_recommendations(payload: dict) -> dict:
    recs = []
    if int(payload.get("overlapping_workflows", 0)) > 3:
        recs.append("consolidate overlapping workflows")
    if int(payload.get("duplicated_narratives", 0)) > 2:
        recs.append("merge duplicated strategic narratives")
    if int(payload.get("redundant_rules", 0)) > 2:
        recs.append("prune redundant governance rules")
    if int(payload.get("stale_links", 0)) > 3:
        recs.append("refresh stale coordination links")
    if int(payload.get("dead_zones", 0)) > 0:
        recs.append("investigate synchronization dead zones")
    return {"recommendations": recs or ["no simplification action required"], "advisory_only": True}


def timeline_merge(events: dict) -> list[dict]:
    merged = []
    for k, vals in events.items():
        for v in vals:
            merged.append({"type": k, "value": v})
    merged.append({"type": "generated_at", "value": datetime.now(UTC).isoformat()})
    return merged
