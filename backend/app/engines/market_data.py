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
from app.engines.mt5_market_data import mt5_market_data

Timeframe = Literal["1min", "5min", "15min", "30min", "1h", "4h", "1day"]
_TF_MIN = {"1min":1,"5min":5,"15min":15,"30min":30,"1h":60,"4h":240,"1day":1440}
RECENT_FAILURE_TTL = timedelta(hours=6)

MT5_PRIMARY_PAIRS = {
    "EUR/USD",
    "GBP/USD",
    "USD/JPY",
    "USD/CHF",
}

MT5_PRIMARY_TIMEFRAMES = {
    "15min",
    "1h",
    "4h",
}

MT5_MAX_OPEN_AGE_MINUTES = {
    "15min": 50,
    "1h": 150,
    "4h": 540,
}

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

    async def close(self):
        await self._client.aclose()

    @staticmethod
    def _mt5_is_primary(
        pair: str,
        timeframe: str,
    ) -> bool:
        return (
            settings.MT5_MARKET_DATA_ENABLED
            and pair in MT5_PRIMARY_PAIRS
            and timeframe in MT5_PRIMARY_TIMEFRAMES
        )

    @staticmethod
    def _market_is_closed(
        now: pd.Timestamp,
    ) -> bool:
        weekday = now.weekday()

        if weekday == 5:
            return True

        if weekday == 6 and now.hour < 21:
            return True

        if weekday == 4 and now.hour >= 21:
            return True

        return False

    @classmethod
    def _mt5_is_fresh(
        cls,
        frame: pd.DataFrame,
        timeframe: str,
    ) -> tuple[bool, int]:
        if frame.empty:
            return False, -1

        latest = pd.Timestamp(
            frame.iloc[-1]["datetime"]
        )

        if latest.tzinfo is None:
            latest = latest.tz_localize("UTC")
        else:
            latest = latest.tz_convert("UTC")

        now = pd.Timestamp(utc_now())

        if now.tzinfo is None:
            now = now.tz_localize("UTC")
        else:
            now = now.tz_convert("UTC")

        age = now - latest

        if age < pd.Timedelta(0):
            return False, int(
                age.total_seconds()
            )

        if cls._market_is_closed(now):
            maximum_age = pd.Timedelta(
                hours=72
            )
        else:
            maximum_age = pd.Timedelta(
                minutes=MT5_MAX_OPEN_AGE_MINUTES[
                    timeframe
                ]
            )

        return (
            age <= maximum_age,
            int(age.total_seconds()),
        )

    async def _mt5(
        self,
        pair: str,
        timeframe: Timeframe,
        limit: int,
    ) -> pd.DataFrame:
        frame = await mt5_market_data.ohlcv(
            pair,
            timeframe,
            limit,
        )

        if len(frame) < limit:
            raise RuntimeError(
                f"MT5 returned only {len(frame)} "
                f"of {limit} requested candles"
            )

        fresh, age_seconds = self._mt5_is_fresh(
            frame,
            timeframe,
        )

        if not fresh:
            raise RuntimeError(
                "MT5 candles are stale or "
                f"future-dated: age={age_seconds}s"
            )

        return frame


    async def ohlcv(self, pair: str, timeframe: Timeframe = "1h", limit: int = 300) -> pd.DataFrame:
        key = (pair, timeframe, limit)
        if key in self._cache:
            ts, df = self._cache[key]
            if utc_now() - ts < timedelta(seconds=30):
                source = self._last_source.get(
                    key,
                    "synthetic",
                )

                provider_cache = source in {
                    "mt5_hantec",
                    "twelve_data",
                }

                self.record_symbol_result(
                    pair,
                    status=(
                        "cached"
                        if provider_cache
                        else "unknown"
                    ),
                    data_mode=(
                        "cached"
                        if provider_cache
                        else "synthetic_demo"
                    ),
                    provider_name=(
                        source
                        if provider_cache
                        else "synthetic"
                    ),
                    last_success=(
                        ts
                        if provider_cache
                        else None
                    ),
                )
                return df
        df = await self._fetch(pair, timeframe, limit)
        self._cache[key] = (utc_now(), df)
        return df

    def source_info(self, pair: str, timeframe: Timeframe, limit: int) -> dict:
        key = (pair, timeframe, limit)
        source = self._last_source.get(key, "synthetic")
        warning = self._last_warning.get(key)
        data_mode = (
            "provider"
            if source in {
                "mt5_hantec",
                "twelve_data",
            }
            else "synthetic_demo"
        )
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
            "mt5_primary": sorted(
                MT5_PRIMARY_PAIRS
            ),
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
        provider_configured = (
            settings.MT5_MARKET_DATA_ENABLED
            or bool(
                settings.TWELVE_DATA_API_KEY.strip()
            )
        )
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

    async def _fetch(
        self,
        pair: str,
        timeframe: Timeframe,
        limit: int,
    ) -> pd.DataFrame:
        key = (
            pair,
            timeframe,
            limit,
        )

        mt5_error = None

        if self._mt5_is_primary(
            pair,
            timeframe,
        ):
            try:
                frame = await self._mt5(
                    pair,
                    timeframe,
                    limit,
                )

                self._last_source[key] = (
                    "mt5_hantec"
                )

                self._last_warning[key] = None

                now = utc_now()

                self.record_symbol_result(
                    pair,
                    status="supported",
                    data_mode="provider",
                    provider_name="mt5_hantec",
                    last_success=now,
                )

                return frame

            except Exception as exc:
                mt5_error = str(exc)

                logger.warning(
                    "MT5 provider failed for "
                    f"{pair} {timeframe}: "
                    f"{exc}; trying Twelve Data"
                )

        if settings.TWELVE_DATA_API_KEY:
            try:
                frame = await self._twelve(
                    pair,
                    timeframe,
                    limit,
                )

                self._last_source[key] = (
                    "twelve_data"
                )

                self._last_warning[key] = (
                    "MT5 unavailable; using "
                    "Twelve Data fallback."
                    if mt5_error
                    else None
                )

                now = utc_now()

                self.record_symbol_result(
                    pair,
                    status="supported",
                    data_mode="provider",
                    provider_name="twelve_data",
                    last_success=now,
                )

                return frame

            except Exception as exc:
                logger.warning(
                    "Twelve Data failed for "
                    f"{pair} {timeframe}: "
                    f"{exc}; using synthetic data"
                )

                now = utc_now()

                self._last_source[key] = (
                    "synthetic"
                )

                self._last_warning[key] = (
                    "MT5 and Twelve Data "
                    "unavailable; using "
                    "synthetic demo data."
                    if mt5_error
                    else
                    "Twelve Data request failed; "
                    "using synthetic demo data."
                )

                self.record_symbol_result(
                    pair,
                    status="provider_failed",
                    data_mode="synthetic_demo",
                    provider_name="twelve_data",
                    last_error=now,
                    last_error_message=str(exc),
                )

                return self._synthetic(
                    pair,
                    timeframe,
                    limit,
                )

        self._last_source[key] = "synthetic"

        self._last_warning[key] = (
            "MT5 unavailable and "
            "TWELVE_DATA_API_KEY missing; "
            "using synthetic demo data."
            if mt5_error
            else
            "TWELVE_DATA_API_KEY missing; "
            "using synthetic demo data."
        )

        self.record_symbol_result(
            pair,
            status="unknown",
            data_mode="synthetic_demo",
            provider_name="synthetic",
        )

        return self._synthetic(
            pair,
            timeframe,
            limit,
        )

    async def _twelve(self, pair: str, timeframe: Timeframe, limit: int) -> pd.DataFrame:
        url = "https://api.twelvedata.com/time_series"
        params = {
            "symbol": pair,
            "interval": timeframe,
            "outputsize": limit,
            "apikey": settings.TWELVE_DATA_API_KEY,
            "format": "JSON",
            "timezone": "UTC",
        }
        r = await self._client.get(url, params=params)
        r.raise_for_status()
        data = r.json()
        if "values" not in data:
            raise RuntimeError(f"Twelve Data error: {data}")
        df = pd.DataFrame(data["values"])
        df["datetime"] = (
            pd.to_datetime(df["datetime"], utc=True)
            .dt.tz_convert(None)
        )
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
