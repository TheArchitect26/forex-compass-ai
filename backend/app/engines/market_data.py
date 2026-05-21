"""Market Data Engine — unified async access to multiple providers.

Providers (free tiers): Twelve Data (primary), Alpha Vantage, Finnhub.
Falls back to deterministic synthetic data if no key is configured, so the
system runs end-to-end in dev without external dependencies.
"""
from __future__ import annotations
from app.utils_time import utc_now
import asyncio
from datetime import datetime, timedelta
from typing import Literal
import httpx
import numpy as np
import pandas as pd
from loguru import logger
from app.config import settings

Timeframe = Literal["1min", "5min", "15min", "30min", "1h", "4h", "1day"]
_TF_MIN = {"1min":1,"5min":5,"15min":15,"30min":30,"1h":60,"4h":240,"1day":1440}


class MarketDataEngine:
    def __init__(self):
        self._client = httpx.AsyncClient(timeout=15.0)
        self._cache: dict[tuple, tuple[datetime, pd.DataFrame]] = {}
        self._last_source: dict[tuple[str, str, int], str] = {}
        self._last_warning: dict[tuple[str, str, int], str | None] = {}

    async def close(self): await self._client.aclose()

    async def ohlcv(self, pair: str, timeframe: Timeframe = "1h", limit: int = 300) -> pd.DataFrame:
        key = (pair, timeframe, limit)
        if key in self._cache:
            ts, df = self._cache[key]
            if utc_now() - ts < timedelta(seconds=30):
                return df
        df = await self._fetch(pair, timeframe, limit)
        self._cache[key] = (utc_now(), df)
        return df

    def source_info(self, pair: str, timeframe: Timeframe, limit: int) -> dict:
        key = (pair, timeframe, limit)
        source = self._last_source.get(key, "synthetic")
        warning = self._last_warning.get(key)
        return {"source": source, "warning": warning}

    async def _fetch(self, pair: str, timeframe: Timeframe, limit: int) -> pd.DataFrame:
        if settings.TWELVE_DATA_API_KEY:
            try:
                df = await self._twelve(pair, timeframe, limit)
                self._last_source[(pair, timeframe, limit)] = "twelve_data"
                self._last_warning[(pair, timeframe, limit)] = None
                return df
            except Exception as e:
                logger.warning(f"Twelve Data failed: {e}; falling back to synthetic")
                self._last_source[(pair, timeframe, limit)] = "synthetic"
                self._last_warning[(pair, timeframe, limit)] = "Twelve Data request failed; using synthetic demo data."
                return self._synthetic(pair, timeframe, limit)
        self._last_source[(pair, timeframe, limit)] = "synthetic"
        self._last_warning[(pair, timeframe, limit)] = "TWELVE_DATA_API_KEY missing; using synthetic demo data."
        return self._synthetic(pair, timeframe, limit)

    async def _twelve(self, pair: str, timeframe: Timeframe, limit: int) -> pd.DataFrame:
        url = "https://api.twelvedata.com/time_series"
        params = {
            "symbol": pair,
            "interval": timeframe,
            "outputsize": limit,
            "apikey": settings.TWELVE_DATA_API_KEY,
            "format": "JSON",
        }
        r = await self._client.get(url, params=params)
        r.raise_for_status()
        data = r.json()
        if "values" not in data:
            raise RuntimeError(f"Twelve Data error: {data}")
        df = pd.DataFrame(data["values"])
        df["datetime"] = pd.to_datetime(df["datetime"])
        for c in ("open", "high", "low", "close"):
            df[c] = df[c].astype(float)
        df["volume"] = df.get("volume", 0)
        df = df.sort_values("datetime").reset_index(drop=True)
        return df

    def _synthetic(self, pair: str, timeframe: Timeframe, limit: int) -> pd.DataFrame:
        """Deterministic GBM-ish synthetic series so the app works without an API key."""
        seed = abs(hash((pair, timeframe))) % (2**32)
        rng = np.random.default_rng(seed)
        base = {"XAU/USD": 2350.0, "USD/JPY": 155.0}.get(pair, 1.1)
        minutes = _TF_MIN[timeframe]
        end = utc_now().replace(second=0, microsecond=0)
        idx = pd.date_range(end=end, periods=limit, freq=f"{minutes}min")
        returns = rng.normal(0, 0.0008, size=limit)
        close = base * np.exp(np.cumsum(returns))
        high = close * (1 + np.abs(rng.normal(0, 0.0006, limit)))
        low = close * (1 - np.abs(rng.normal(0, 0.0006, limit)))
        open_ = np.concatenate([[close[0]], close[:-1]])
        vol = rng.integers(800, 5000, size=limit)
        return pd.DataFrame({
            "datetime": idx, "open": open_, "high": high,
            "low": low, "close": close, "volume": vol,
        })


market_data = MarketDataEngine()
