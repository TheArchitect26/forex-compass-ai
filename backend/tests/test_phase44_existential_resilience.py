from app.engines.existential_resilience import resilience_status, crisis_scan, continuity_plan, black_swan_review, recovery_readiness, resilience_memory


def test_crisis_scoring():
    out = resilience_status()
    assert isinstance(out["existential_resilience_score"], float)
    assert isinstance(out["recovery_readiness_score"], float)


def test_black_swan_review_output():
    out = black_swan_review({})
    assert "assumptions_invalidated_by_shock" in out
    assert "risk_of_overreaction" in out


def test_continuity_plan_shape():
    out = continuity_plan({})
    assert "critical_systems_to_preserve" in out
    assert "systems_to_pause" in out


def test_minimum_viable_mode_output():
    out = continuity_plan({})
    assert "minimum_viable_operating_mode" in out
    assert "no execution" in out["minimum_viable_operating_mode"]


def test_recovery_readiness_scoring():
    out = recovery_readiness({})
    assert isinstance(out["recovery_readiness_score"], float)


def test_advisory_only_safeguards():
    assert resilience_status()["advisory_only"] is True
    assert resilience_status()["auto_apply"] is False
    assert continuity_plan({})["human_approval_required"] is True


def test_memory_shape():
    out = resilience_memory()
    assert {"crisis_audits", "continuity_plans", "black_swan_reviews", "recovery_reviews", "lessons"}.issubset(out.keys())
