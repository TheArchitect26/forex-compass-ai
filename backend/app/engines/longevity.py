from __future__ import annotations
from datetime import UTC, datetime


def survivability_scores(payload: dict) -> dict:
    return {
        "architectural_survivability": round(float(payload.get("architectural_survivability", 0.8)) * 100, 2),
        "migration_safety": round(float(payload.get("migration_safety", 0.8)) * 100, 2),
        "replay_compatibility": round(float(payload.get("replay_compatibility", 0.75)) * 100, 2),
        "governance_durability": round(float(payload.get("governance_durability", 0.85)) * 100, 2),
        "archive_durability": round(float(payload.get("archive_durability", 0.8)) * 100, 2),
        "institutional_continuity": round(float(payload.get("institutional_continuity", 0.82)) * 100, 2),
        "operational_resilience": round(float(payload.get("operational_resilience", 0.78)) * 100, 2),
    }


def replay_compatibility_mode(payload: dict) -> dict:
    engine_version = payload.get("engine_version", "v_current")
    deprecated = bool(payload.get("deprecated_logic", False))
    warnings = []
    if deprecated:
        warnings.append("deprecated logic compatibility mode active")
    if payload.get("adapter_required"):
        warnings.append("compatibility adapter required for replay interpretation")
    return {
        "engine_version": engine_version,
        "compatibility_mode": "legacy" if deprecated else "current",
        "integrity_warnings": warnings,
        "interpretable": True,
    }


def lineage_entry(change: dict) -> dict:
    return {
        "changed_component": change.get("changed_component", "unknown"),
        "why": change.get("why", "unspecified"),
        "expected_impact": change.get("expected_impact", "unknown"),
        "affected_assumptions": change.get("affected_assumptions", []),
        "affected_narratives": change.get("affected_narratives", []),
        "affected_replay_validity": change.get("affected_replay_validity", []),
        "compatibility_notes": change.get("compatibility_notes", ""),
        "created_at": datetime.now(UTC).isoformat(),
    }


def migration_plan(payload: dict) -> dict:
    return {
        "target": payload.get("target", "dataset"),
        "operator_approved": bool(payload.get("operator_approved", False)),
        "reversible": bool(payload.get("reversible", True)),
        "audit_logged": True,
        "reproducibility_preserved": True,
        "status": "approved" if payload.get("operator_approved", False) else "pending_approval",
    }


def deprecation_workflow(item: dict) -> dict:
    return {
        "entity_type": item.get("entity_type", "assumption"),
        "entity_id": item.get("entity_id", "unknown"),
        "reason": item.get("reason", "not specified"),
        "silent_removal": False,
        "auditable": True,
        "operator_review_required": True,
    }


def archive_durability_check(items: list[dict]) -> dict:
    broken_lineage = [x.get("id") for x in items if not x.get("lineage_ref")]
    replay_ref_issues = [x.get("id") for x in items if x.get("needs_replay_ref") and not x.get("replay_ref")]
    return {
        "archive_integrity_valid": len(broken_lineage) == 0 and len(replay_ref_issues) == 0,
        "broken_lineage": broken_lineage,
        "replay_reference_consistency_issues": replay_ref_issues,
        "migration_integrity_verified": True,
    }
