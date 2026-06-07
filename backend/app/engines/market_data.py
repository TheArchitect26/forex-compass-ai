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
RECENT_FAILURE_TTL = timedelta(hours=6)

TWELVE_DATA_FOREX_MAJORS = [
    "EUR/USD",
    "GBP/USD",
    "USD/JPY",
    "AUD/USD",
    "USD/CAD",
    "USD/CHF",
    "NZD/USD",
]
TWELVE_DATA_COMMODITIES = ["XAU/USD"]
TWELVE_DATA_EXPERIMENTAL = ["EUR/GBP", "EUR/JPY", "GBP/JPY"]
TWELVE_DATA_UNSUPPORTED = ["BTC/USD", "ETH/USD"]


class MarketDataEngine:
    def __init__(self):
        self._client = httpx.AsyncClient(timeout=15.0)
        self._cache: dict[tuple, tuple[datetime, pd.DataFrame]] = {}
        self._last_source: dict[tuple[str, str, int], str] = {}
        self._last_warning: dict[tuple[str, str, int], str | None] = {}
        self._symbol_results: dict[str, dict] = {}
        self._provider_last_success: datetime | None = None
        self._provider_last_error: datetime | None = None
        self._provider_last_error_message: str | None = None

    async def close(self): await self._client.aclose()

    async def ohlcv(self, pair: str, timeframe: Timeframe = "1h", limit: int = 300) -> pd.DataFrame:
        key = (pair, timeframe, limit)
        if key in self._cache:
            ts, df = self._cache[key]
            if utc_now() - ts < timedelta(seconds=30):
                source = self._last_source.get(key, "synthetic")
                provider_cache = source == "twelve_data"
                self.record_symbol_result(
                    pair,
                    status="cached" if provider_cache else "unknown",
                    data_mode="cached" if provider_cache else "synthetic_demo",
                    provider_name="cached_provider" if provider_cache else "synthetic",
                    last_success=ts if provider_cache else None,
                )
                return df
        df = await self._fetch(pair, timeframe, limit)
        self._cache[key] = (utc_now(), df)
        return df

    def source_info(self, pair: str, timeframe: Timeframe, limit: int) -> dict:
        key = (pair, timeframe, limit)
        source = self._last_source.get(key, "synthetic")
        warning = self._last_warning.get(key)
        data_mode = "provider" if source == "twelve_data" else "synthetic_demo"
        if key in self._cache:
            ts, _ = self._cache[key]
            if utc_now() - ts < timedelta(seconds=30):
                data_mode = "cached"
        return {"source": source, "warning": warning, "data_mode": data_mode}

    @staticmethod
    def _safe_error(message: str | None) -> str | None:
        if not message:
            return None
        safe = str(message)
        if settings.TWELVE_DATA_API_KEY:
            safe = safe.replace(settings.TWELVE_DATA_API_KEY, "[redacted]")
        return safe[:240]

    def record_symbol_result(
        self,
        pair: str,
        *,
        status: str,
        data_mode: str,
        provider_name: str = "twelve_data",
        last_success: datetime | None = None,
        last_error: datetime | None = None,
        last_error_message: str | None = None,
    ) -> None:
        existing = self._symbol_results.get(pair, {})
        payload = {
            "symbol": pair,
            "status": status,
            "data_mode": data_mode,
            "provider_name": provider_name,
            "last_success": (last_success or existing.get("last_success")),
            "last_error": (last_error or existing.get("last_error")),
            "last_error_message": self._safe_error(last_error_message) if last_error_message else existing.get("last_error_message"),
        }
        self._symbol_results[pair] = payload
        if payload["last_success"]:
            self._provider_last_success = payload["last_success"]
        if payload["last_error"]:
            self._provider_last_error = payload["last_error"]
            self._provider_last_error_message = payload["last_error_message"]

    def symbol_presets(self) -> dict:
        return {
            "forex_majors": TWELVE_DATA_FOREX_MAJORS,
            "commodities": TWELVE_DATA_COMMODITIES,
            "experimental": TWELVE_DATA_EXPERIMENTAL,
            "unsupported": TWELVE_DATA_UNSUPPORTED,
        }

    def is_recently_failed(self, symbol: str) -> bool:
        stored = self._symbol_results.get(symbol, {})
        last_error = stored.get("last_error")
        if stored.get("status") not in {"provider_failed", "failed", "unavailable"}:
            return False
        if not last_error:
            return True
        return utc_now() - last_error < RECENT_FAILURE_TTL

    def unavailable_symbols(self, symbols: list[str]) -> list[str]:
        unsupported = set(TWELVE_DATA_UNSUPPORTED)
        return [symbol for symbol in symbols if symbol in unsupported or self.is_recently_failed(symbol)]

    def recommended_symbols(self, symbols: list[str]) -> list[str]:
        baseline = [s for s in [*TWELVE_DATA_FOREX_MAJORS, *TWELVE_DATA_COMMODITIES] if s in symbols]
        unavailable = set(self.unavailable_symbols(symbols))
        return [symbol for symbol in baseline if symbol not in unavailable]

    def scan_symbols(self, requested: list[str] | None, retry_symbols: list[str] | None = None) -> tuple[list[str], list[str]]:
        symbols = requested or settings.PAIRS
        retry = set(retry_symbols or [])
        unsupported = set(TWELVE_DATA_UNSUPPORTED)
        blocked = [
            symbol
            for symbol in symbols
            if symbol in unsupported or (self.is_recently_failed(symbol) and symbol not in retry)
        ]
        return [symbol for symbol in symbols if symbol not in blocked], blocked

    def clear_symbol_failures(self, symbols: list[str]) -> None:
        for symbol in symbols:
            stored = self._symbol_results.get(symbol)
            if not stored:
                continue
            stored["status"] = "unknown"
            stored["last_error"] = None
            stored["last_error_message"] = None
            if stored.get("data_mode") == "unavailable":
                stored["data_mode"] = "unknown"

    def provider_diagnostics(self, symbols: list[str]) -> dict:
        items = []
        provider_configured = bool(settings.TWELVE_DATA_API_KEY.strip())
        unavailable = set(self.unavailable_symbols(symbols))
        for symbol in symbols:
            stored = self._symbol_results.get(symbol, {})
            status = stored.get("status") or "unknown"
            data_mode = stored.get("data_mode") or ("synthetic_demo" if not provider_configured else "unknown")
            if symbol in TWELVE_DATA_UNSUPPORTED:
                status = "unsupported"
                data_mode = "unavailable"
            elif symbol in unavailable:
                data_mode = "unavailable"
            last_success = stored.get("last_success")
            last_error = stored.get("last_error")
            items.append({
                "symbol": symbol,
                "status": status,
                "data_mode": data_mode,
                "provider_name": stored.get("provider_name") or "twelve_data",
                "last_success": last_success.isoformat() if last_success else None,
                "last_error": last_error.isoformat() if last_error else None,
                "last_error_message": stored.get("last_error_message"),
            })
        return {
            "provider_name": "twelve_data",
            "provider_configured": provider_configured,
            "last_success": self._provider_last_success.isoformat() if self._provider_last_success else None,
            "last_error": self._provider_last_error.isoformat() if self._provider_last_error else None,
            "last_error_message": self._provider_last_error_message,
            "symbols": items,
            "symbol_presets": self.symbol_presets(),
            "recommended_symbols": self.recommended_symbols(symbols),
            "unavailable_symbols": sorted(unavailable | set(TWELVE_DATA_UNSUPPORTED)),
            "auto_trade": False,
            "no_execution": True,
        }

    async def _fetch(self, pair: str, timeframe: Timeframe, limit: int) -> pd.DataFrame:
        if settings.TWELVE_DATA_API_KEY:
            try:
                df = await self._twelve(pair, timeframe, limit)
                self._last_source[(pair, timeframe, limit)] = "twelve_data"
                self._last_warning[(pair, timeframe, limit)] = None
                now = utc_now()
                self.record_symbol_result(pair, status="supported", data_mode="provider", provider_name="twelve_data", last_success=now)
                return df
            except Exception as e:
                logger.warning(f"Twelve Data failed: {e}; falling back to synthetic")
                now = utc_now()
                self._last_source[(pair, timeframe, limit)] = "synthetic"
                self._last_warning[(pair, timeframe, limit)] = "Twelve Data request failed; using synthetic demo data."
                self.record_symbol_result(
                    pair,
                    status="provider_failed",
                    data_mode="synthetic_demo",
                    provider_name="twelve_data",
                    last_error=now,
                    last_error_message=str(e),
                )
                return self._synthetic(pair, timeframe, limit)
        self._last_source[(pair, timeframe, limit)] = "synthetic"
        self._last_warning[(pair, timeframe, limit)] = "TWELVE_DATA_API_KEY missing; using synthetic demo data."
        self.record_symbol_result(pair, status="unknown", data_mode="synthetic_demo", provider_name="synthetic")
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
