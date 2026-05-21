from app.engines.institutional_policy import (
    policy_status,
    policies_list,
    evaluate_compliance,
    conflict_review,
    doctrine_summary,
    policy_memory,
)


def test_policy_output_shape():
    out = policy_status()
    assert "policy_categories" in out
    assert "constitutional_rules" in out


def test_compliance_review_output():
    out = evaluate_compliance({})
    assert {"violates_institutional_doctrine", "bypasses_safeguards", "lacks_review_requirements", "weakens_observability", "weakens_rollback_readiness", "weakens_operator_sovereignty", "weakens_documentation_discipline", "introduces_governance_contradiction"}.issubset(out.keys())


def test_doctrine_summary_generation():
    out = doctrine_summary({})
    assert {"institutional_operating_principles", "governance_philosophy", "review_obligations", "operational_safety_principles", "anti_automation_protections", "long_term_continuity_doctrine", "human_sovereignty_guarantees"}.issubset(out.keys())


def test_conflict_review_output():
    out = conflict_review({})
    assert {"conflict_summary", "affected_systems", "doctrine_violated", "risk_severity", "human_review_required", "recommended_resolution_path"}.issubset(out.keys())


def test_scoring_output():
    out = policy_status()
    assert {"policy_coverage_score", "enforcement_clarity_score", "doctrine_consistency_score", "institutional_protection_score", "review_discipline_score", "operational_resilience_score", "constitutional_alignment_score", "governance_completeness_score"}.issubset(out.keys())


def test_constitutional_safeguards():
    out = policy_status()
    rules = out["constitutional_rules"]
    assert any("advisory_only=true" in r for r in rules)
    assert any("auto_apply=false" in r for r in rules)


def test_advisory_only_safeguards():
    out = policy_status()
    assert out["advisory_only"] is True
    assert out["auto_apply"] is False
    assert out["human_approval_required"] is True
    assert out["never_auto_enforce_destructive_actions"] is True
    assert out["never_auto_delete_capabilities"] is True
    assert out["never_auto_change_governance_states"] is True
    assert out["never_auto_approve_compliance"] is True
    assert out["never_auto_rewrite_doctrine"] is True


def test_memory_shape():
    out = policy_memory()
    assert {"policy_snapshots", "compliance_reviews", "conflict_reviews", "doctrine_summaries", "integration_snapshot", "safety_principles"}.issubset(out.keys())


def test_policies_list_shape():
    out = policies_list({})
    assert "policies" in out
