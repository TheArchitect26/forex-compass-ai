from app.engines.evidence_registry import (
    evidence_status,
    register_evidence,
    control_map,
    chain_of_custody,
    readiness_review,
    evidence_memory,
)


def test_evidence_record_shape():
    out = register_evidence({})
    assert {"evidence_id", "evidence_type", "title", "source_system", "source_file_or_endpoint", "related_policy", "related_control", "related_phase", "related_change", "related_audit_event", "timestamp", "owner", "evidence_summary", "confidence", "freshness_status", "human_review_required", "advisory_only", "auto_apply"}.issubset(out.keys())


def test_control_mapping_output():
    out = control_map({})
    assert {"risk_to_control", "control_to_evidence", "evidence_to_policy", "policy_to_audit_event", "change_to_validation_evidence", "release_to_runtime_evidence", "pir_to_lesson_evidence"}.issubset(out.keys())


def test_chain_of_custody_output():
    out = chain_of_custody({})
    assert {"source_origin", "evidence_path", "linked_decisions", "linked_policies", "linked_controls", "linked_reviews", "timestamp_trail", "gaps", "weak_links", "human_review_required"}.issubset(out.keys())


def test_readiness_review_gap_detection():
    out = readiness_review({})
    assert {"missing_evidence", "stale_evidence", "unlinked_policies", "controls_without_proof", "decisions_without_source_evidence", "changes_without_validation_evidence", "releases_without_runtime_evidence", "scorecards_without_supporting_evidence", "audit_events_without_provenance"}.issubset(out.keys())


def test_evidence_scoring():
    out = evidence_status()
    assert {"evidence_completeness_score", "source_clarity_score", "timestamp_integrity_score", "policy_linkage_score", "control_coverage_score", "audit_readiness_score", "evidence_freshness_score", "chain_of_custody_score"}.issubset(out.keys())


def test_advisory_only_safeguards():
    out = evidence_status()
    assert out["advisory_only"] is True
    assert out["auto_apply"] is False
    assert out["human_approval_required"] is True
    assert out["never_fabricate_evidence"] is True
    assert out["never_delete_evidence"] is True
    assert out["never_rewrite_evidence_history"] is True
    assert out["never_mark_incomplete_as_complete_automatically"] is True
    assert out["never_auto_approve_compliance"] is True


def test_memory_shape():
    out = evidence_memory()
    assert {"evidence_snapshots", "control_mapping_snapshots", "chain_of_custody_snapshots", "readiness_reviews", "integration_snapshot", "safety_principles"}.issubset(out.keys())
