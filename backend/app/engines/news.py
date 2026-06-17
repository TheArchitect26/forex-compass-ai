"""News & Macro Engine — free provider-backed calendar and market headlines."""
from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone
from time import monotonic
from typing import Any

import feedparser
import httpx

from app.config import settings

_RSS = [
    "https://www.forexlive.com/feed/news",
    "https://www.investing.com/rss/news_25.rss",
]

_FOREX_CURRENCIES = {"USD", "EUR", "GBP", "JPY", "CHF", "CAD", "AUD", "NZD"}
_COUNTRY_TO_CURRENCY = {
    "united states": "USD",
    "euro area": "EUR",
    "european union": "EUR",
    "united kingdom": "GBP",
    "japan": "JPY",
    "switzerland": "CHF",
    "canada": "CAD",
    "australia": "AUD",
    "new zealand": "NZD",
}

_CACHE: dict[str, tuple[float, Any]] = {}


def _cache_get(key: str) -> Any | None:
    item = _CACHE.get(key)
    if not item:
        return None
    expires_at, value = item
    if monotonic() >= expires_at:
        _CACHE.pop(key, None)
        return None
    return value


def _cache_set(key: str, value: Any, ttl_seconds: int) -> Any:
    _CACHE[key] = (monotonic() + ttl_seconds, value)
    return value


def provider_status() -> dict:
    headline_providers = []
    if settings.ALPHA_VANTAGE_API_KEY.strip():
        headline_providers.append("alpha_vantage")
    if settings.FINNHUB_API_KEY.strip():
        headline_providers.append("finnhub")
    headline_providers.append("rss")

    return {
        "calendar": {
            "provider": "fmp" if settings.FMP_API_KEY.strip() else None,
            "configured": bool(settings.FMP_API_KEY.strip()),
            "cache_minutes": 30,
        },
        "headlines": {
            "providers": headline_providers,
            "alpha_vantage_configured": bool(settings.ALPHA_VANTAGE_API_KEY.strip()),
            "finnhub_configured": bool(settings.FINNHUB_API_KEY.strip()),
            "rss_enabled": True,
            "alpha_vantage_cache_minutes": 60,
            "finnhub_cache_minutes": 15,
            "rss_cache_minutes": 15,
        },
        "sentiment": {
            "provider": "internal_lexicon",
            "configured": True,
        },
    }


def _impact(value: Any) -> str:
    if isinstance(value, (int, float)):
        return "high" if value >= 3 else "medium" if value == 2 else "low"
    text = str(value or "").strip().lower()
    if text in {"3", "high"}:
        return "high"
    if text in {"2", "medium", "moderate"}:
        return "medium"
    if text in {"1", "low"}:
        return "low"
    return text or "unknown"


def _normalise_currency(item: dict) -> str:
    currency = str(item.get("currency") or item.get("Currency") or "").upper().strip()
    if currency:
        return currency
    country = str(item.get("country") or item.get("Country") or "").lower().strip()
    return _COUNTRY_TO_CURRENCY.get(country, "")


def _normalise_fmp_event(item: dict) -> dict:
    return {
        "time": item.get("date") or item.get("Date") or item.get("time"),
        "currency": _normalise_currency(item),
        "country": item.get("country") or item.get("Country") or "",
        "event": item.get("event") or item.get("Event") or item.get("name") or "Economic event",
        "impact": _impact(item.get("impact") or item.get("Importance") or item.get("importance")),
        "actual": item.get("actual") if item.get("actual") is not None else item.get("Actual", ""),
        "forecast": (
            item.get("estimate")
            if item.get("estimate") is not None
            else item.get("forecast")
            if item.get("forecast") is not None
            else item.get("Forecast", "")
        ),
        "previous": item.get("previous") if item.get("previous") is not None else item.get("Previous", ""),
        "unit": item.get("unit") or item.get("Unit") or "",
        "source": "fmp",
    }


async def _fetch_fmp_calendar() -> list[dict]:
    key = settings.FMP_API_KEY.strip()
    if not key:
        return []

    cached = _cache_get("fmp_calendar")
    if cached is not None:
        return cached

    today = datetime.now(timezone.utc).date()
    date_from = today.isoformat()
    date_to = (today + timedelta(days=7)).isoformat()
    endpoints = [
        "https://financialmodelingprep.com/stable/economic-calendar",
        "https://financialmodelingprep.com/api/v3/economic_calendar",
    ]

    payload: Any = []
    async with httpx.AsyncClient(timeout=20) as client:
        for url in endpoints:
            try:
                response = await client.get(
                    url,
                    params={"from": date_from, "to": date_to, "apikey": key},
                )
                response.raise_for_status()
                candidate = response.json()
                if isinstance(candidate, list):
                    payload = candidate
                    break
            except (httpx.HTTPError, ValueError):
                continue

    if not isinstance(payload, list):
        payload = []

    events = [_normalise_fmp_event(item) for item in payload if isinstance(item, dict)]
    forex_events = [
        event
        for event in events
        if not event["currency"] or event["currency"] in _FOREX_CURRENCIES
    ]
    forex_events.sort(key=lambda event: str(event.get("time") or ""))
    return _cache_set("fmp_calendar", forex_events[:75], 30 * 60)


async def upcoming_events() -> list[dict]:
    """Return the free FMP economic calendar without synthetic placeholders."""
    return await _fetch_fmp_calendar()


def _parse_alpha_time(value: Any) -> str:
    text = str(value or "").strip()
    for fmt in ("%Y%m%dT%H%M%S", "%Y%m%dT%H%M"):
        try:
            return datetime.strptime(text, fmt).replace(tzinfo=timezone.utc).isoformat()
        except ValueError:
            continue
    return text


async def _alpha_vantage_headlines() -> list[dict]:
    key = settings.ALPHA_VANTAGE_API_KEY.strip()
    if not key:
        return []

    cached = _cache_get("alpha_vantage_headlines")
    if cached is not None:
        return cached

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(
                "https://www.alphavantage.co/query",
                params={
                    "function": "NEWS_SENTIMENT",
                    "topics": "economy_monetary",
                    "sort": "LATEST",
                    "limit": 30,
                    "apikey": key,
                },
            )
            response.raise_for_status()
            payload = response.json()
    except (httpx.HTTPError, ValueError):
        payload = {}

    feed = payload.get("feed", []) if isinstance(payload, dict) else []
    items: list[dict] = []
    for item in feed:
        if not isinstance(item, dict) or not item.get("title"):
            continue
        items.append(
            {
                "title": item.get("title", ""),
                "link": item.get("url", ""),
                "published": _parse_alpha_time(item.get("time_published")),
                "source": item.get("source") or "Alpha Vantage",
                "summary": item.get("summary") or "",
                "provider": "alpha_vantage",
                "sentiment_score": item.get("overall_sentiment_score"),
                "sentiment_label": item.get("overall_sentiment_label"),
            }
        )

    return _cache_set("alpha_vantage_headlines", items[:30], 60 * 60)


def _finnhub_datetime(value: Any) -> str:
    try:
        return datetime.fromtimestamp(int(value), tz=timezone.utc).isoformat()
    except (TypeError, ValueError, OSError):
        return ""


async def _finnhub_headlines() -> list[dict]:
    key = settings.FINNHUB_API_KEY.strip()
    if not key:
        return []

    cached = _cache_get("finnhub_headlines")
    if cached is not None:
        return cached

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(
                "https://finnhub.io/api/v1/news",
                params={"category": "forex", "token": key},
            )
            response.raise_for_status()
            payload = response.json()
    except (httpx.HTTPError, ValueError):
        payload = []

    items: list[dict] = []
    if isinstance(payload, list):
        for item in payload[:30]:
            if not isinstance(item, dict) or not item.get("headline"):
                continue
            items.append(
                {
                    "title": item.get("headline", ""),
                    "link": item.get("url", ""),
                    "published": _finnhub_datetime(item.get("datetime")),
                    "source": item.get("source") or "Finnhub",
                    "summary": item.get("summary") or "",
                    "provider": "finnhub",
                }
            )

    return _cache_set("finnhub_headlines", items, 15 * 60)


def _parse_rss(url: str) -> list[dict]:
    feed = feedparser.parse(url)
    source_title = getattr(getattr(feed, "feed", {}), "title", "") or "RSS"
    items: list[dict] = []
    for entry in feed.entries[:15]:
        title = getattr(entry, "title", "")
        if not title:
            continue
        items.append(
            {
                "title": title,
                "link": getattr(entry, "link", ""),
                "published": getattr(entry, "published", ""),
                "source": source_title,
                "summary": getattr(entry, "summary", ""),
                "provider": "rss",
            }
        )
    return items


async def _rss_headlines() -> list[dict]:
    cached = _cache_get("rss_headlines")
    if cached is not None:
        return cached

    results = await asyncio.gather(
        *(asyncio.to_thread(_parse_rss, url) for url in _RSS),
        return_exceptions=True,
    )
    items: list[dict] = []
    for result in results:
        if isinstance(result, list):
            items.extend(result)
    return _cache_set("rss_headlines", items, 15 * 60)


def _dedupe(items: list[dict], limit: int = 40) -> list[dict]:
    seen: set[str] = set()
    output: list[dict] = []
    for item in items:
        key = " ".join(str(item.get("title") or "").lower().split())
        if not key or key in seen:
            continue
        seen.add(key)
        output.append(item)
        if len(output) >= limit:
            break
    return output


async def headlines() -> list[dict]:
    """Combine Alpha Vantage, Finnhub, and RSS while respecting free-tier quotas."""
    cached = _cache_get("combined_headlines")
    if cached is not None:
        return cached

    alpha_items, finnhub_items, rss_items = await asyncio.gather(
        _alpha_vantage_headlines(),
        _finnhub_headlines(),
        _rss_headlines(),
    )
    combined = _dedupe([*alpha_items, *finnhub_items, *rss_items], limit=40)
    return _cache_set("combined_headlines", combined, 5 * 60)
