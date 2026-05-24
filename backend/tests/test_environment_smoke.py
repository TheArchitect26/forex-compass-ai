from importlib import import_module


def test_environment_import_smoke() -> None:
    mod = import_module("app.main")
    assert hasattr(mod, "app")


def test_models_import_smoke() -> None:
    mod = import_module("app.models")
    assert hasattr(mod, "ResearchGraphEdge")
    assert hasattr(mod, "FeatureFlagCleanupPlan")
