from importlib import import_module


def test_app_main_imports():
    mod = import_module("app.main")
    assert hasattr(mod, "app")


def test_app_models_imports_core_symbols():
    mod = import_module("app.models")
    assert hasattr(mod, "User")
    assert hasattr(mod, "Signal")
    assert hasattr(mod, "ResearchGraphEdge")
    assert hasattr(mod, "FeatureFlagCleanupPlan")
