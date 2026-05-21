from app.engines.institutional_audit_trail import (
    audit_trail_status,
    record_event,
    decision_provenance,
    trace,
    governance_lineage,
    audit_trail_memory,
)


def test_audit_event_shape():
    out = record_event({})
    assert {"what_decided_or_recommended", "why_produced", "source_systems", "evidence_used", "assumptions", "policy_references", "related_phase", "affected_capability", "human_reviewer_required", "advisory_only", "auto_apply"}.issubset(out.keys())


def test_provenance_output():
    out = decision_provenance({})
    assert {"decision_id", "recommendation_source", "review_inputs", "scorecard_evidence", "change_control_rationale", "post_implementation_lessons", "approval_assumptions", "governance_conflicts"}.issubset(out.keys())


def test_trace_output():
    out = trace({})
    assert {"trace_path", "traceability_gaps", "governance_lineage_links"}.issubset(out.keys())


def test_governance_lineage_output():
    out = governance_lineage({})
    assert {"lineage_summary", "policy_references", "related_reviews", "conflict_visibility", "human_review_required"}.issubset(out.keys())


def test_safeguard_flags():
    out = audit_trail_status()
    assert out["advisory_only"] is True
    assert out["auto_apply"] is False
    assert out["human_approval_required"] is True
    assert out["never_rewrite_history"] is True
    assert out["never_delete_audit_events"] is True
    assert out["never_auto_approve_decisions"] is True
    assert out["never_hide_governance_conflicts"] is True
    assert out["require_human_approval_for_audit_corrections"] is True


def test_memory_shape():
    out = audit_trail_memory()
    assert {"audit_event_snapshots", "decision_provenance_snapshots", "traceability_reviews", "governance_lineage_reviews", "integration_snapshot", "safety_principles"}.issubset(out.keys())
