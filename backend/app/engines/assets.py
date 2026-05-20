ASSETS = {
    "EUR/USD": {"asset_class": "forex", "pip_size": 0.0001, "spread_pips": 1.0, "liquidity": "high", "vol_profile": "medium", "session": "24x5"},
    "GBP/USD": {"asset_class": "forex", "pip_size": 0.0001, "spread_pips": 1.3, "liquidity": "high", "vol_profile": "medium", "session": "24x5"},
    "USD/JPY": {"asset_class": "forex", "pip_size": 0.01, "spread_pips": 1.2, "liquidity": "high", "vol_profile": "medium", "session": "24x5"},
    "XAU/USD": {"asset_class": "gold", "pip_size": 0.1, "spread_pips": 3.0, "liquidity": "medium", "vol_profile": "high", "session": "24x5"},
    "BTC/USD": {"asset_class": "crypto", "pip_size": 1.0, "spread_pips": 10.0, "liquidity": "medium", "vol_profile": "high", "session": "24x7"},
    "SPX/USD": {"asset_class": "index", "pip_size": 1.0, "spread_pips": 2.0, "liquidity": "medium", "vol_profile": "medium", "session": "us_hours"},
}

def get_asset_meta(pair: str) -> dict:
    return ASSETS.get(pair.upper(), {"asset_class": "forex", "pip_size": 0.0001, "spread_pips": 1.5, "liquidity": "unknown", "vol_profile": "unknown", "session": "24x5"})
