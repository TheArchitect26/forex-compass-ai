from __future__ import annotations


def coherence_status() -> dict:
    return {
        "subsystem_coherence": 0.63,
        "api_clarity": 0.58,
        "model_uniqueness": 0.52,
        "terminology_consistency": 0.57,
        "frontend_navigation_clarity": 0.49,
        "architectural_simplicity": 0.46,
        "maintenance_burden": 0.71,
        "consolidation_opportunity": 0.78,
        "advisory_only": True,
        "auto_apply": False,
    }


def overlap_scan(payload: dict) -> dict:
    return {
        "duplicated_engine_responsibilities": payload.get("duplicated_engine_responsibilities", ["scenario vs pathways recommendation scoring"]),
        "overlapping_apis": payload.get("overlapping_apis", ["/api/scenario/compare vs /api/pathways/compare"]),
        "repeated_governance_logic": payload.get("repeated_governance_logic", ["human_review_required flags duplicated across layers"]),
        "similar_scoring_systems": payload.get("similar_scoring_systems", ["multiple fit/risk scores with inconsistent naming"]),
        "stale_consoles": payload.get("stale_consoles", []),
        "unused_workflows": payload.get("unused_workflows", ["legacy validation-only loop"]),
        "fragmented_terminology": payload.get("fragmented_terminology", ["risk score vs exposure score vs burden score"]),
        "model_table_overlap": payload.get("model_table_overlap", ["multiple memory tables for adjacent concerns"]),
        "redundant_memory_systems": payload.get("redundant_memory_systems", ["parallel memory endpoints with similar payload shapes"]),
        "advisory_only": True,
    }


def consolidation_plan(payload: dict) -> dict:
    return {
        "benefits": ["lower maintenance burden", "clearer operator mental model", "reduced duplication"],
        "risks": ["migration complexity", "temporary API churn"],
        "migration_needs": ["compat aliases", "schema compatibility mapping", "docs/sidebar update"],
        "reversibility": "high with phased rollout",
        "affected_files": payload.get("affected_files", ["backend/app/engines/*.py", "backend/app/api/*.py", "frontend/components/Sidebar.tsx"]),
        "proposals": [
            "merge similar comparison endpoints into shared comparison utility",
            "group consoles by operational domain with collapsible navigation",
            "standardize scoring vocabulary across subsystems",
            "consolidate memory endpoints via typed envelope pattern",
        ],
        "human_approval_required": True,
        "advisory_only": True,
        "auto_apply": False,
    }


def simplification_risk(payload: dict) -> dict:
    return {
        "high_burden_subsystems": payload.get("high_burden_subsystems", ["governance + synthesis + foresight overlap zone"]),
        "simplification_risks": payload.get("simplification_risks", ["loss of nuanced controls if over-consolidated"]),
        "mitigations": payload.get("mitigations", ["phased deprecation", "operator sign-off gates", "compatibility tests"]),
        "advisory_only": True,
        "auto_apply": False,
    }


def architecture_memory() -> dict:
    return {
        "architecture_audits": ["phase37_baseline_audit"],
        "overlap_findings": ["duplicate comparison APIs detected"],
        "consolidation_proposals": ["shared scoring vocabulary proposal"],
        "simplification_incidents": ["navigation sprawl flagged"],
        "lessons": ["consolidate terminology before merging endpoints"],
    }
