from __future__ import annotations


def debt_status() -> dict:
    return {
        "technical_debt_score": 0.74,
        "maintainability_score": 0.52,
        "build_fragility_score": 0.43,
        "dependency_risk_score": 0.48,
        "migration_burden_score": 0.69,
        "test_confidence_score": 0.71,
        "refactor_urgency_score": 0.77,
        "debt_paydown_priority_score": 0.79,
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
    }


def debt_scan(payload: dict) -> dict:
    return {
        "code_complexity_hotspots": payload.get("code_complexity_hotspots", ["backend/app/models.py", "backend/app/main.py"]),
        "duplicated_logic": payload.get("duplicated_logic", ["parallel scoring and governance patterns across engines"]),
        "stale_todo_fixme_debt": payload.get("stale_todo_fixme_debt", ["TODO debt markers unresolved across phase expansions"]),
        "dependency_risk": payload.get("dependency_risk", ["mixed pinning strategy across backend/frontend stacks"]),
        "build_deploy_fragility": payload.get("build_deploy_fragility", ["frontend/backend integration sensitive to env mismatch"]),
        "migration_sprawl": payload.get("migration_sprawl", ["many phase migration files increasing maintenance overhead"]),
        "oversized_models_growth": payload.get("oversized_models_growth", ["models.py monolith growth increases review and merge risk"]),
        "excessive_router_growth": payload.get("excessive_router_growth", ["router registration concentration in main app"]),
        "frontend_console_sprawl": payload.get("frontend_console_sprawl", ["high number of specialized consoles with overlap"]),
        "test_coverage_imbalance": payload.get("test_coverage_imbalance", ["many unit-style checks, fewer integration cross-module checks"]),
        "brittle_imports": payload.get("brittle_imports", ["large import fan-in in main/router composition"]),
        "configuration_drift": payload.get("configuration_drift", ["increasing env/settings surface with uneven validation"]),
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
    }


def prioritize_debt(payload: dict) -> dict:
    items = payload.get("debt_items", [
        {
            "category": "architecture debt",
            "severity": "high",
            "affected_files": ["backend/app/models.py", "backend/app/main.py"],
            "impact": "slower change velocity and higher regression risk",
            "estimated_effort": "high",
            "risk_if_ignored": "rising coordination and defect cost",
            "recommended_owner_action": "plan modular extraction by bounded domains",
            "human_approval_required": True,
        },
        {
            "category": "migration debt",
            "severity": "medium",
            "affected_files": ["backend/migrations/*.sql"],
            "impact": "onboarding and migration sequencing complexity",
            "estimated_effort": "medium",
            "risk_if_ignored": "higher deployment fragility",
            "recommended_owner_action": "group/document migration waves and compatibility windows",
            "human_approval_required": True,
        },
    ])
    return {
        "prioritized_debt_items": items,
        "priority_ordering": payload.get("priority_ordering", ["architecture debt", "migration debt", "dependency debt", "frontend UX debt"]),
        "debt_paydown_priority_score": payload.get("debt_paydown_priority_score", 0.79),
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
    }


def paydown_plan(payload: dict) -> dict:
    return {
        "paydown_actions": payload.get("paydown_actions", [
            "remove dead/stale code",
            "reduce duplicate scoring logic",
            "split oversized models.py",
            "group migrations by maintainability waves",
            "improve dependency hygiene",
            "strengthen build tests",
            "simplify frontend navigation",
            "consolidate overlapping tests",
            "document unstable areas",
        ]),
        "recommended_timeline": payload.get("recommended_timeline", ["stabilize critical hotspots first", "phase modularization", "validate with regression checks"]),
        "owners": payload.get("owners", ["backend maintainers", "frontend maintainers", "platform reliability owner"]),
        "human_approval_required": True,
        "advisory_only": True,
        "auto_apply": False,
    }


def dependency_risk(payload: dict) -> dict:
    return {
        "fragile_pinned_packages": payload.get("fragile_pinned_packages", ["strict pins with unresolved transitive constraints"]),
        "unresolved_dependency_versions": payload.get("unresolved_dependency_versions", ["mixed loose/strict version strategy"]),
        "vercel_uv_failure_risk": payload.get("vercel_uv_failure_risk", ["build sensitivity to platform resolver differences"]),
        "deprecated_framework_versions": payload.get("deprecated_framework_versions", []),
        "missing_python_version_lock": payload.get("missing_python_version_lock", ["explicit interpreter lock not centralized"]),
        "frontend_backend_build_mismatch": payload.get("frontend_backend_build_mismatch", ["contract drift risk between API and UI assumptions"]),
        "environment_variable_drift": payload.get("environment_variable_drift", ["growing env matrix increases drift risk"]),
        "build_fragility_score": payload.get("build_fragility_score", 0.43),
        "dependency_risk_score": payload.get("dependency_risk_score", 0.48),
        "advisory_only": True,
        "auto_apply": False,
        "human_approval_required": True,
    }


def debt_memory() -> dict:
    return {
        "debt_audits": ["phase45_baseline_debt_observatory_scan"],
        "priority_decisions": ["models/router modularization prioritized"],
        "dependency_reviews": ["build/dependency drift risks logged"],
        "paydown_reviews": ["phased paydown plan drafted"],
        "lessons": ["preventive maintenance lowers long-run complexity and failure risk"],
    }
