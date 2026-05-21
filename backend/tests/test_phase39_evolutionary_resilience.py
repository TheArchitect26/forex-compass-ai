from app.engines.evolutionary_resilience import evolution_status, transition_assessment, migration_readiness, continuity_plan, rollback_plan, evolution_memory


def test_transition_assessment_shape():
    out = transition_assessment({})
    assert "major_architecture_transitions" in out
    assert "transition_risks_detected" in out


def test_migration_readiness_scoring():
    out = migration_readiness({})
    assert isinstance(out["transition_readiness_score"], float)
    assert isinstance(out["migration_risk_score"], float)


def test_continuity_plan_output():
    out = continuity_plan({})
    assert len(out["preservation_actions"]) > 0
    assert "validation_checks" in out


def test_rollback_plan_output():
    out = rollback_plan({})
    assert "rollback_feasibility" in out
    assert isinstance(out["rollback_readiness_score"], float)


def test_transition_risk_detection():
    out = transition_assessment({})
    assert "missing rollback path" in out["transition_risks_detected"]


def test_advisory_only_safeguards():
    assert evolution_status()["advisory_only"] is True
    assert evolution_status()["auto_apply"] is False
    assert migration_readiness({})["human_approval_required"] is True
    assert continuity_plan({})["human_approval_required"] is True
    assert rollback_plan({})["human_approval_required"] is True


def test_memory_shape():
    out = evolution_memory()
    assert {"transition_assessments", "continuity_decisions", "rollback_reviews", "trust_incidents", "lessons"}.issubset(out.keys())
