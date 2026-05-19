from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.db import init_db
from app.api import auth, market, signals, analysis, journal, news, sentiment, backtest, learning, performance, ws


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="AI Forex Intelligence API",
    version="0.1.0",
    description="Signal-only Forex market intelligence. Never auto-trades.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(market.router, prefix="/api/market", tags=["market"])
app.include_router(signals.router, prefix="/api/signals", tags=["signals"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["analysis"])
app.include_router(journal.router, prefix="/api/journal", tags=["journal"])
app.include_router(news.router, prefix="/api/news", tags=["news"])
app.include_router(sentiment.router, prefix="/api/sentiment", tags=["sentiment"])
app.include_router(backtest.router, prefix="/api/backtest", tags=["backtest"])
app.include_router(learning.router, prefix="/api/learning", tags=["learning"])
app.include_router(performance.router, prefix="/api/performance", tags=["performance"])
app.include_router(ws.router, tags=["ws"])


@app.get("/")
async def root():
    return {"status": "ok", "service": "ai-forex-intelligence", "auto_trade": False}
