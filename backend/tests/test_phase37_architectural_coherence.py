from app.engines.architectural_coherence import coherence_status, overlap_scan, consolidation_plan, simplification_risk, architecture_memory


def test_overlap_scan_shape():
    out = overlap_scan({})
    required = {
        "duplicated_engine_responsibilities", "overlapping_apis", "repeated_governance_logic",
        "similar_scoring_systems", "stale_consoles", "unused_workflows",
        "fragmented_terminology", "model_table_overlap", "redundant_memory_systems", "advisory_only"
    }
    assert required.issubset(out.keys())


def test_coherence_scoring():
    out = coherence_status()
    for key in ["subsystem_coherence", "api_clarity", "model_uniqueness", "terminology_consistency", "frontend_navigation_clarity", "architectural_simplicity", "maintenance_burden", "consolidation_opportunity"]:
        assert isinstance(out[key], float)


def test_consolidation_proposal_output():
    out = consolidation_plan({})
    assert len(out["proposals"]) > 0
    assert "migration_needs" in out and len(out["migration_needs"]) > 0


def test_simplification_risk_detection():
    out = simplification_risk({"high_burden_subsystems": ["api overlap zone"]})
    assert "api overlap zone" in out["high_burden_subsystems"]


def test_advisory_only_safeguards():
    assert coherence_status()["advisory_only"] is True
    assert coherence_status()["auto_apply"] is False
    assert consolidation_plan({})["advisory_only"] is True
    assert consolidation_plan({})["auto_apply"] is False
    assert simplification_risk({})["advisory_only"] is True
    assert simplification_risk({})["auto_apply"] is False


def test_memory_shape():
    out = architecture_memory()
    assert {"architecture_audits", "overlap_findings", "consolidation_proposals", "simplification_incidents", "lessons"}.issubset(out.keys())
