from app.config import settings

def pip_size(pair: str) -> float:
    p = pair.upper()
    if p.endswith("JPY") or "/JPY" in p:
        return 0.01
    if p == "XAU/USD":
        return settings.XAU_PIP_SIZE
    return 0.0001

def pips_from_price_move(pair: str, price_move: float) -> float:
    return price_move / pip_size(pair)
