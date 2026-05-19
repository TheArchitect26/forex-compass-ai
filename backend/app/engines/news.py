"""News & Macro Engine — economic calendar + macro headlines."""
from __future__ import annotations
import httpx, feedparser
from datetime import datetime
from app.config import settings

_RSS = [
    "https://www.forexlive.com/feed/news",
    "https://www.investing.com/rss/news_25.rss",
]


async def upcoming_events() -> list[dict]:
    """Economic calendar from TradingEconomics if key set, else empty."""
    if not settings.TRADING_ECONOMICS_KEY:
        # Static placeholder — replace with ForexFactory scrape in prod
        return [
            {"time": datetime.utcnow().isoformat(), "currency": "USD", "event": "CPI m/m", "impact": "high", "forecast": "0.3%", "previous": "0.4%"},
            {"time": datetime.utcnow().isoformat(), "currency": "EUR", "event": "ECB Press Conference", "impact": "high", "forecast": "-", "previous": "-"},
        ]
    async with httpx.AsyncClient(timeout=10) as c:
        r = await c.get(f"https://api.tradingeconomics.com/calendar?c={settings.TRADING_ECONOMICS_KEY}&f=json")
        r.raise_for_status()
        return r.json()[:50]


async def headlines() -> list[dict]:
    items: list[dict] = []
    for url in _RSS:
        try:
            feed = feedparser.parse(url)
            for e in feed.entries[:10]:
                items.append({"title": e.title, "link": e.link, "published": getattr(e, "published", "")})
        except Exception:
            continue
    return items
