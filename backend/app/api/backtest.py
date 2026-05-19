from fastapi import APIRouter
from app.engines.backtest import run_ema_cross
from app.engines.strategy import evolve_ema

router = APIRouter()


@router.get("/ema-cross")
async def ema(pair: str = "EUR/USD", timeframe: str = "1h", fast: int = 20, slow: int = 50):
    return await run_ema_cross(pair, timeframe, fast, slow)


@router.get("/evolve")
async def evolve(pair: str = "EUR/USD", timeframe: str = "1h"):
    return await evolve_ema(pair, timeframe)
