from fastapi import APIRouter, Query
from app.engines.market_data import market_data
from app.config import settings

router = APIRouter()


@router.get("/pairs")
async def pairs():
    return {"pairs": settings.PAIRS, "timeframes": settings.TIMEFRAMES}


@router.get("/ohlcv")
async def ohlcv(pair: str = "EUR/USD", timeframe: str = "1h", limit: int = 300):
    df = await market_data.ohlcv(pair, timeframe, limit)
    return {
        "pair": pair, "timeframe": timeframe,
        "candles": [
            {"time": int(r.datetime.timestamp()), "open": r.open, "high": r.high,
             "low": r.low, "close": r.close, "volume": int(r.volume)}
            for r in df.itertuples()
        ],
    }


@router.get("/heatmap")
async def heatmap():
    """Pct change vs N bars ago across the universe."""
    out = []
    for p in settings.PAIRS:
        df = await market_data.ohlcv(p, "1h", 25)
        change = (df["close"].iloc[-1] / df["close"].iloc[0] - 1) * 100
        out.append({"pair": p, "change_pct": round(float(change), 3), "price": float(df["close"].iloc[-1])})
    return {"items": out}
