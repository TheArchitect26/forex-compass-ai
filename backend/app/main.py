from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy import text
from redis.asyncio import from_url as redis_from_url

from app.db import init_db
from app.config import settings
from app.api import auth, market, signals, analysis, journal, news, sentiment, backtest, learning, performance, ws, strategies, audit, versions, experiments, data, replay, system, research, strategic, cognitive, governance, meta, reality, context, attention, temporal, synthesis, foresight, scenario, pathways, causal, ecosystem


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
    allow_origins=settings.CORS_ORIGINS,
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
app.include_router(strategies.router, prefix="/api/strategies", tags=["strategies"])
app.include_router(audit.router, prefix="/api/audit", tags=["audit"])
app.include_router(versions.router, prefix="/api/versions", tags=["versions"])
app.include_router(experiments.router, prefix="/api/experiments", tags=["experiments"])
app.include_router(data.router, prefix="/api/data", tags=["data"])
app.include_router(replay.router, prefix="/api/replay", tags=["replay"])
app.include_router(system.router, prefix="/api/system", tags=["system"])
app.include_router(research.router, prefix="/api/research", tags=["research"])
app.include_router(strategic.router, prefix="/api/system", tags=["strategic"])
app.include_router(cognitive.router, prefix="/api/system", tags=["cognitive"])
app.include_router(governance.router, prefix="/api/governance", tags=["governance"])
app.include_router(reality.router, prefix="/api/governance", tags=["reality"])
app.include_router(context.router, prefix="/api/context", tags=["context"])
app.include_router(attention.router, prefix="/api/attention", tags=["attention"])
app.include_router(temporal.router, prefix="/api/temporal", tags=["temporal"])
app.include_router(synthesis.router, prefix="/api/synthesis", tags=["synthesis"])
app.include_router(foresight.router, prefix="/api/foresight", tags=["foresight"])
app.include_router(scenario.router, prefix="/api/scenario", tags=["scenario"])
app.include_router(pathways.router, prefix="/api/pathways", tags=["pathways"])
app.include_router(causal.router, prefix="/api/causal", tags=["causal"])
app.include_router(ecosystem.router, prefix="/api/ecosystem", tags=["ecosystem"])
app.include_router(meta.router, prefix="/api/meta", tags=["meta"])


@app.get("/")
async def root():
    return {"status": "ok", "service": "ai-forex-intelligence", "auto_trade": False}


@app.get("/api/health")
async def health():
    db_status = "ok"
    redis_status = "ok"

    try:
        from app.db import SessionLocal
        async with SessionLocal() as session:
            await session.execute(text("SELECT 1"))
    except Exception:
        db_status = "error"

    try:
        client = redis_from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
        await client.ping()
        await client.aclose()
    except Exception:
        redis_status = "error"

    market_mode = "real" if settings.TWELVE_DATA_API_KEY else "synthetic"
    return {
        "backend": "ok",
        "database": db_status,
        "redis": redis_status,
        "market_data_mode": market_mode,
        "twelve_data_configured": bool(settings.TWELVE_DATA_API_KEY),
        "version": app.version,
    }


@app.get("/api/schema-version")
async def schema_version():
    return {"schema_version": "phase23", "migrations": ["phase2", "phase3", "phase4", "phase6", "phase7", "phase8", "phase9", "phase10", "phase11", "phase12", "phase13", "phase14", "phase15", "phase16", "phase17", "phase18", "phase19", "phase20", "phase21", "phase22", "phase23"]}

@app.get("/api/config-validate")
async def config_validate():
    issues = []
    if settings.MIN_SIGNAL_CONFIDENCE < 0 or settings.MIN_SIGNAL_CONFIDENCE > 100: issues.append("MIN_SIGNAL_CONFIDENCE out of range")
    if settings.SIGNAL_COOLDOWN_MINUTES < 0: issues.append("SIGNAL_COOLDOWN_MINUTES negative")
    return {"ok": len(issues)==0, "issues": issues}
