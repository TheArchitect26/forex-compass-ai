"""Notifications — Telegram / Discord / Email dispatch."""
import httpx
from app.config import settings


async def notify_signal(signal: dict) -> dict:
    msg = (f"📊 {signal['direction']} {signal['pair']} | conf {signal['confidence']}%\n"
           f"Entry {signal['entry']}  SL {signal['stop_loss']}  TP {signal['take_profit']}\n"
           f"{signal['explanation']}")
    sent = {}
    async with httpx.AsyncClient(timeout=10) as c:
        if settings.TELEGRAM_BOT_TOKEN and settings.TELEGRAM_CHAT_ID:
            try:
                await c.post(f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
                             json={"chat_id": settings.TELEGRAM_CHAT_ID, "text": msg})
                sent["telegram"] = True
            except Exception as e: sent["telegram"] = str(e)
        if settings.DISCORD_WEBHOOK_URL:
            try:
                await c.post(settings.DISCORD_WEBHOOK_URL, json={"content": msg})
                sent["discord"] = True
            except Exception as e: sent["discord"] = str(e)
    return sent
