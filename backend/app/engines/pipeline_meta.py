ENGINE_VERSION = "phase8-v1"
WEIGHTING_VERSION = "rw-1"
DISCIPLINE_VERSION = "disc-1"
PROFILE_VERSION = "profile-1"


def config_snapshot(profile: dict, runtime: dict | None = None) -> dict:
    runtime = runtime or {
        "allow_synthetic_signals": False,
        "default_slippage_pips": 0.5,
        "default_spread_pips": {"EUR/USD": 1.0},
    }
    return {
        "engine_version": ENGINE_VERSION,
        "weighting_version": WEIGHTING_VERSION,
        "discipline_version": DISCIPLINE_VERSION,
        "strategy_profile_version": PROFILE_VERSION,
        "min_confidence": profile["min_confidence"],
        "cooldown_minutes": profile["cooldown_minutes"],
        "allow_synthetic_signals": runtime["allow_synthetic_signals"],
        "default_slippage_pips": runtime["default_slippage_pips"],
        "default_spread_pips": runtime["default_spread_pips"],
    }
