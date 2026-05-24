from app.engines.operator_control_plane import control_plane_status, control_plane_summary, top_actions, console_sprawl, focus_view, control_plane_memory


def test_control_plane_summary_shape():
    out = control_plane_summary({})
    assert len(out["top_institutional_priorities"]) == 5
    assert len(out["top_ignore_or_defer"]) == 5
    assert "critical_warnings" in out


def test_top_actions_output():
    out = top_actions({})
    assert len(out["top_actions"]) >= 5
    assert "action" in out["top_actions"][0]


def test_console_sprawl_detection():
    out = console_sprawl({})
    assert out["too_many_sidebar_items"] is True
    assert "dashboards_to_group" in out


def test_focus_view_filtering():
    out = focus_view({"view": "Minimal Daily View"})
    assert out["view"] == "Minimal Daily View"
    assert out["suppressed_noise"] is True


def test_critical_warning_preservation():
    out = focus_view({"view": "Executive View"})
    assert out["critical_warnings_preserved"] is True


def test_advisory_only_safeguards():
    out = control_plane_status()
    assert out["advisory_only"] is True
    assert out["auto_apply"] is False
    assert out["never_hide_critical_warnings"] is True
    assert out["never_delete_consoles"] is True
    assert out["never_change_navigation_automatically"] is True


def test_memory_shape():
    out = control_plane_memory()
    assert {"control_plane_snapshots", "focus_decisions", "sprawl_audits", "critical_warning_preservation_checks", "integration_snapshot", "safety_principles"}.issubset(out.keys())
