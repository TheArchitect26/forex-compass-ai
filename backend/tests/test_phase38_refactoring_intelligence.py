from app.engines.refactoring_intelligence import refactoring_status, entropy_scan, recovery_plan, coupling_analysis, refactor_priorities, refactoring_memory


def test_entropy_scoring():
    out = refactoring_status()
    for key in ["entropy_score", "coupling_risk_score", "maintainability_score", "refactor_priority_score", "subsystem_drift_score", "architectural_recovery_score", "simplification_opportunity_score"]:
        assert isinstance(out[key], float)


def test_coupling_analysis():
    out = coupling_analysis({})
    assert "tightly_coupled_modules" in out
    assert "hidden_dependency_chains" in out


def test_recovery_plan_shape():
    out = recovery_plan({})
    assert "architectural_recovery_proposals" in out
    assert len(out["architectural_recovery_proposals"]) > 0


def test_refactor_priority_ranking():
    out = refactor_priorities({})
    assert len(out["priority_rankings"]) > 0
    assert out["priority_rankings"][0]["priority"] == 1


def test_simplification_opportunity_output():
    out = refactor_priorities({})
    assert len(out["simplification_opportunities"]) > 0


def test_advisory_only_safeguards():
    assert refactoring_status()["advisory_only"] is True
    assert refactoring_status()["auto_apply"] is False
    assert entropy_scan({})["advisory_only"] is True
    assert entropy_scan({})["auto_apply"] is False
    assert recovery_plan({})["human_approval_required"] is True


def test_memory_shape():
    out = refactoring_memory()
    assert {"entropy_audits", "recovery_history", "coupling_findings", "priority_decisions", "lessons"}.issubset(out.keys())
