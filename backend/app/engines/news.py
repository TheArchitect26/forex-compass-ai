"""News & Macro Engine — provider-backed calendar and market headlines."""
from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Any

import feedparser
import httpx

from app.config import settings

_RSS = [
    "https://www.forexlive.com/feed/news",
    "https://www.investing.com/rss/news_25.rss",
]


def provider_status() -> dict:
    return {
        "calendar": {
            "provider": "trading_economics" if settings.TRADING_ECONOMICS_KEY.strip() else None,
            "configured": bool(settings.TRADING_ECONOMICS_KEY.strip()),
        },
        "headlines": {
            "provider": "finnhub+rss" if settings.FINNHUB_API_KEY.strip() else "rss",
            "finnhub_configured": bool(settings.FINNHUB_API_KEY.strip()),
            "rss_enabled": True,
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


def _normalise_calendar_event(item: dict) -> dict:
    return {
        "time": item.get("Date") or item.get("date") or item.get("time"),
        "currency": item.get("Currency") or item.get("currency") or item.get("Country") or "",
        "country": item.get("Country") or item.get("country") or "",
        "event": item.get("Event") or item.get("Category") or item.get("event") or "Economic event",
        "impact": _impact(item.get("Importance") or item.get("importance") or item.get("impact")),
        "actual": item.get("Actual") or item.get("actual") or "",
        "forecast": item.get("Forecast") or item.get("forecast") or item.get("TEForecast") or "",
        "previous": item.get("Previous") or item.get("previous") or "",
        "unit": item.get("Unit") or item.get("unit") or "",
        "source": "trading_economics",
    }


async def upcoming_events() -> list[dict]:
    """Return normalised Trading Economics events; never invent placeholder events."""
    key = settings.TRADING_ECONOMICS_KEY.strip()
    if not key:
        return []

    url = "https://api.tradingeconomics.com/calendar"
    params = {"c": key, "f": "json"}

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            payload = response.json()
    except (httpx.HTTPError, ValueError):
        return []

    if not isinstance(payload, list):
        return []

    events = [_normalise_calendar_event(item) for item in payload if isinstance(item, dict)]
    return events[:50]


def _finnhub_datetime(value: Any) -> str:
    try:
        return datetime.fromtimestamp(int(value), tz=timezone.utc).isoformat()
    except (TypeError, ValueError, OSError):
        return ""


async def _finnhub_headlines() -> list[dict]:
    key = settings.FINNHUB_API_KEY.strip()
    if not key:
        return []

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(
                "https://finnhub.io/api/v1/news",
                params={"category": "forex", "token": key},
            )
            response.raise_for_status()
            payload = response.json()
    except (httpx.HTTPError, ValueError):
        return []

    if not isinstance(payload, list):
        return []

    items: list[dict] = []
    for item in payload[:30]:
        if not isinstance(item, dict) or not item.get("headline"):
            continue
        items.append(
            {
                "title": item.get("headline", ""),
                "link": item.get("url", ""),
                "published": _finnhub_datetime(item.get("datetime")),
                "source": item.get("source") or "finnhub",
                "summary": item.get("summary") or "",
                "provider": "finnhub",
            }
        )
    return items


def _parse_rss(url: str) -> list[dict]:
    feed = feedparser.parse(url)
    source_title = getattr(getattr(feed, "feed", {}), "title", "") or "rss"
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
    results = await asyncio.gather(
        *(asyncio.to_thread(_parse_rss, url) for url in _RSS),
        return_exceptions=True,
    )
    items: list[dict] = []
    for result in results:
        if isinstance(result, list):
            items.extend(result)
    return items


def _dedupe(items: list[dict], limit: int = 30) -> list[dict]:
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
    """Prefer Finnhub when configured and retain RSS as a resilient fallback."""
    finnhub_items, rss_items = await asyncio.gather(
        _finnhub_headlines(),
        _rss_headlines(),
    )
    return _dedupe([*finnhub_items, *rss_items], limit=30)
