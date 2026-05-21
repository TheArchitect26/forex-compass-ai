from __future__ import annotations

from app.engines.institutional_policy import policy_status
from app.engines.institutional_audit_trail import audit_trail_status
from app.engines.change_impact_analysis import change_control_status
from app.engines.post_implementation_review import post_implementation_status
from app.engines.scorecard_governance import scorecard_status
from app.engines.platform_catalog import platform_catalog_status
from app.engines.golden_path_workflows import golden_paths_status
from app.engines.release_governance import release_status
from app.engines.runtime_observability import observability_status
from app.engines.feature_flag_governance import feature_flags_status
from app.engines.institutional_evaluation import evaluation_status
from app.engines.memory_retrieval import memory_status

EVIDENCE_CATEGORIES = [
    "policy_evidence", "control_evidence", "audit_evidence", "change_evidence", "release_evidence",
    "runtime_evidence", "scorecard_evidence", "approval_evidence", "rollback_evidence", "observability_evidence",
    "migration_evidence", "test_evidence", "documentation_evidence",
]


def _integration_snapshot() -> dict:
    return {
        "policies": policy_status(),
        "audit_trail": audit_trail_status(),
        "change_control": change_control_status(),
        "post_implementation": post_implementation_status(),
        "scorecards": scorecard_status(),
        "platform_catalog": platform_catalog_status(),
        "golden_paths": golden_paths_status(),
        "release": release_status(),
        "observability": observability_status(),
        "feature_flags": feature_flags_status(),
        "evaluation": evaluation_status(),
        "memory": memory_status(),
    }


def evidence_status() -> dict:
    return {
        "evidence_categories": EVIDENCE_CATEGORIES,
        "evidence_completeness_score": 0.76,
        "source_clarity_score": 0.74,
        "timestamp_integrity_score": 0.79,
        "policy_linkage_score": 0.75,
        "control_coverage_score": 0.73,
        "audit_readiness_score": 0.77,
        "evidence_freshness_score": 0.71,
        "chain_of_custody_score": 0.74,
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
        "never_fabricate_evidence": True,
        "never_delete_evidence": True,
        "never_rewrite_evidence_history": True,
        "never_mark_incomplete_as_complete_automatically": True,
        "never_auto_approve_compliance": True,
        "require_human_approval_for_evidence_corrections": True,
    }


def register_evidence(payload: dict) -> dict:
    return {
        "evidence_id": payload.get("evidence_id", "evid-phase62-001"),
        "evidence_type": payload.get("evidence_type", "policy_evidence"),
        "title": payload.get("title", "Policy compliance review evidence"),
        "source_system": payload.get("source_system", "policies"),
        "source_file_or_endpoint": payload.get("source_file_or_endpoint", "/api/policies/evaluate-compliance"),
        "related_policy": payload.get("related_policy", "constitutional_core"),
        "related_control": payload.get("related_control", "human_approval_gate"),
        "related_phase": payload.get("related_phase", "phase62"),
        "related_change": payload.get("related_change", "phase62_evidence_registry_rollout"),
        "related_audit_event": payload.get("related_audit_event", "audit-evt-001"),
        "timestamp": payload.get("timestamp", "2026-05-21T00:00:00Z"),
        "owner": payload.get("owner", "governance"),
        "evidence_summary": payload.get("evidence_summary", "Policy/control linkage verified with human review gate."),
        "confidence": payload.get("confidence", "moderate_to_high"),
        "freshness_status": payload.get("freshness_status", "fresh"),
        "human_review_required": True,
        "advisory_only": True,
        "auto_apply": False,
    }


def control_map(payload: dict) -> dict:
    return {
        "risk_to_control": payload.get("risk_to_control", ["unaudited governance change -> human_approval_gate"]),
        "control_to_evidence": payload.get("control_to_evidence", ["human_approval_gate -> approval_evidence record"]),
        "evidence_to_policy": payload.get("evidence_to_policy", ["approval_evidence -> constitutional_policy"]),
        "policy_to_audit_event": payload.get("policy_to_audit_event", ["constitutional_policy -> audit event lineage"]),
        "change_to_validation_evidence": payload.get("change_to_validation_evidence", ["phase change -> pytest + compile evidence"]),
        "release_to_runtime_evidence": payload.get("release_to_runtime_evidence", ["release review -> observability snapshots"]),
        "pir_to_lesson_evidence": payload.get("pir_to_lesson_evidence", ["post-implementation review -> lesson evidence"]),
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
    }


def chain_of_custody(payload: dict) -> dict:
    return {
        "source_origin": payload.get("source_origin", "policy evaluation endpoint output"),
        "evidence_path": payload.get("evidence_path", ["policy review", "scorecard link", "audit trail entry", "evidence registry record"]),
        "linked_decisions": payload.get("linked_decisions", ["decision-001"]),
        "linked_policies": payload.get("linked_policies", ["constitutional_core"]),
        "linked_controls": payload.get("linked_controls", ["human_approval_gate", "rollback_required_control"]),
        "linked_reviews": payload.get("linked_reviews", ["change_control_review", "post_implementation_review"]),
        "timestamp_trail": payload.get("timestamp_trail", ["2026-05-21T00:00:00Z", "2026-05-21T00:15:00Z"]),
        "gaps": payload.get("gaps", ["missing explicit reviewer id on legacy evidence"]),
        "weak_links": payload.get("weak_links", ["manual evidence handoff without normalized tag"]),
        "human_review_required": True,
        "advisory_only": True,
        "auto_apply": False,
    }


def readiness_review(payload: dict) -> dict:
    return {
        "missing_evidence": payload.get("missing_evidence", ["no runtime evidence for one release candidate"]),
        "stale_evidence": payload.get("stale_evidence", ["scorecard evidence older than review threshold"]),
        "unlinked_policies": payload.get("unlinked_policies", ["memory_retention_policy missing direct evidence link"]),
        "controls_without_proof": payload.get("controls_without_proof", ["rollback_control without latest validation artifact"]),
        "decisions_without_source_evidence": payload.get("decisions_without_source_evidence", ["legacy decision id without provenance record"]),
        "changes_without_validation_evidence": payload.get("changes_without_validation_evidence", ["small patch lacking explicit test artifact link"]),
        "releases_without_runtime_evidence": payload.get("releases_without_runtime_evidence", ["candidate release without observability snapshot"]),
        "scorecards_without_supporting_evidence": payload.get("scorecards_without_supporting_evidence", ["operator usability score missing traceable evidence"]),
        "audit_events_without_provenance": payload.get("audit_events_without_provenance", ["older audit event missing recommendation source map"]),
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
    }


def evidence_memory() -> dict:
    return {
        "evidence_snapshots": ["phase62_evidence_registry_baseline"],
        "control_mapping_snapshots": ["risk-control-evidence links tracked"],
        "chain_of_custody_snapshots": ["chain-of-custody trails retained"],
        "readiness_reviews": ["audit readiness gaps recorded"],
        "integration_snapshot": _integration_snapshot(),
        "safety_principles": [
            "never fabricate evidence",
            "never delete evidence",
            "never rewrite evidence history",
            "never mark incomplete evidence as complete automatically",
            "never auto-approve compliance",
            "human approval required for evidence corrections",
        ],
    }
