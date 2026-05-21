from app.engines.operator_experience import ux_status, usability_audit, navigation_audit, readability_review, simplification_plan, ux_memory


def test_ux_scoring():
    out = ux_status()
    assert isinstance(out["operator_experience_score"], float)
    assert isinstance(out["usability_clarity_score"], float)
    assert isinstance(out["interface_coherence_score"], float)


def test_usability_audit_shape():
    out = usability_audit({})
    assert {"visibility_of_system_status", "system_operator_language_match", "consistency_across_consoles", "human_control_and_freedom"}.issubset(out.keys())


def test_navigation_audit_output():
    out = navigation_audit({})
    assert out["too_many_sidebar_items"] is True
    assert "missing_daily_use_pathway" in out


def test_readability_review_output():
    out = readability_review({})
    assert "dense_cards" in out
    assert "small_screen_layout_risk" in out


def test_simplification_plan_shape():
    out = simplification_plan({})
    assert len(out["recommendations"]) >= 5
    assert "daily_use_pathway" in out


def test_advisory_only_safeguards():
    out = ux_status()
    assert out["advisory_only"] is True
    assert out["auto_apply"] is False
    assert out["never_auto_delete_pages"] is True
    assert out["never_auto_change_navigation"] is True
    assert out["never_auto_hide_critical_warnings"] is True


def test_memory_shape():
    out = ux_memory()
    assert {"ux_audits", "usability_findings", "navigation_reviews", "readability_reviews", "simplification_reviews", "integration_snapshot", "safety_principles"}.issubset(out.keys())
