from app.engines.technical_debt_observatory import debt_status, debt_scan, prioritize_debt, paydown_plan, dependency_risk, debt_memory


def test_debt_scoring():
    out = debt_status()
    assert isinstance(out["technical_debt_score"], float)
    assert isinstance(out["debt_paydown_priority_score"], float)


def test_debt_classification():
    out = prioritize_debt({})
    assert out["prioritized_debt_items"][0]["category"] in {
        "code debt", "architecture debt", "dependency debt", "migration debt", "test debt", "documentation debt", "deployment debt", "frontend UX debt", "data/model debt"
    }


def test_prioritization_output():
    out = prioritize_debt({})
    assert len(out["priority_ordering"]) > 0


def test_paydown_plan_shape():
    out = paydown_plan({})
    assert len(out["paydown_actions"]) > 0
    assert "owners" in out


def test_dependency_risk_detection():
    out = dependency_risk({})
    assert "fragile_pinned_packages" in out
    assert "frontend_backend_build_mismatch" in out


def test_advisory_only_safeguards():
    assert debt_status()["advisory_only"] is True
    assert debt_status()["auto_apply"] is False
    assert paydown_plan({})["human_approval_required"] is True


def test_memory_shape():
    out = debt_memory()
    assert {"debt_audits", "priority_decisions", "dependency_reviews", "paydown_reviews", "lessons"}.issubset(out.keys())
