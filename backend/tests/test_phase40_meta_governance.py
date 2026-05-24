from app.engines.meta_governance import metagovernance_status, policy_conflicts, safeguard_audit, harmonization_plan, doctrine_drift, metagovernance_memory


def test_policy_conflict_detection():
    out = policy_conflicts({})
    assert "policy_contradictions" in out
    assert "escalation_conflicts" in out


def test_safeguard_consistency_scoring():
    out = metagovernance_status()
    assert isinstance(out["governance_alignment_score"], float)
    assert isinstance(out["safeguard_consistency_score"], float)


def test_doctrine_hierarchy_output():
    out = metagovernance_status()
    assert "doctrine_hierarchy" in out
    assert "no execution / no autonomous trading" in out["doctrine_hierarchy"]


def test_harmonization_plan_shape():
    out = harmonization_plan({})
    assert len(out["harmonization_proposals"]) > 0
    assert "affected_systems" in out["harmonization_proposals"][0]


def test_doctrine_drift_detection():
    out = doctrine_drift({})
    assert "drift_warnings" in out
    assert isinstance(out["doctrine_drift_score"], float)


def test_advisory_only_safeguards():
    assert metagovernance_status()["advisory_only"] is True
    assert metagovernance_status()["auto_apply"] is False
    assert harmonization_plan({})["human_approval_required"] is True


def test_memory_shape():
    out = metagovernance_memory()
    assert {"policy_audits", "conflict_log", "harmonization_decisions", "doctrine_drift_reviews", "lessons"}.issubset(out.keys())
