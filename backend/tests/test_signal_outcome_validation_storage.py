import asyncio
from datetime import timedelta

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.db import Base
from app.engines.outcome_validation import validate_pending_outcomes
from app.models import HistoricalCandle, Signal, SignalScanContext
from app.utils_time import utc_now


def _run(coro):
    return asyncio.run(coro)


async def _session():
    engine = create_async_engine(
        "sqlite+aiosqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return async_sessionmaker(engine, expire_on_commit=False)


async def _add_signal(db, *, direction="BUY", demo_only=False, with_future=True):
    created_at = utc_now() - timedelta(minutes=60)
    signal = Signal(
        pair="EUR/USD",
        direction=direction,
        timeframe="15min",
        entry=1.1000,
        stop_loss=1.0975,
        take_profit=1.1040,
        risk_reward=1.6,
        confidence=80,
        strength="strong",
        risk_level="low",
        reason_summary="test",
        indicators_used=[],
        invalidation_price=1.0975,
        data_source="synthetic" if demo_only else "real",
        market_regime="trending",
        reasoning={},
        explanation="test",
        created_at=created_at,
    )
    db.add(signal)
    await db.flush()
    db.add(SignalScanContext(
        signal_id=signal.id,
        symbol=signal.pair,
        interval=signal.timeframe,
        signal_timestamp=created_at,
        direction=signal.direction,
        confidence=signal.confidence,
        entry_price=signal.entry,
        data_mode="synthetic_demo" if demo_only else "provider",
        provider_name="synthetic" if demo_only else "twelve_data",
        demo_only=demo_only,
        candle_snapshot={"rows": 1, "demo_only": demo_only},
    ))
    if with_future:
        high, low = (1.1045, 1.0990) if direction == "BUY" else (1.1005, 1.0955)
        db.add(HistoricalCandle(
            pair=signal.pair,
            timeframe=signal.timeframe,
            timestamp=created_at + timedelta(minutes=15),
            open=1.1000,
            high=high,
            low=low,
            close=1.1020,
            volume=1000,
            source="twelve_data",
        ))
    await db.commit()
    return signal.id


def test_missing_future_candles_stays_pending():
    async def case():
        maker = await _session()
        async with maker() as db:
            await _add_signal(db, with_future=False)
            result = await validate_pending_outcomes(db)
            assert result["provider_candidates"] == 1
            assert result["missing_data"] == 1
            assert result["provider_pending"] == 1
            assert result["pending"] == 1
            assert result["validated"] == 0
    _run(case())


def test_synthetic_demo_signal_is_skipped():
    async def case():
        maker = await _session()
        async with maker() as db:
            await _add_signal(db, demo_only=True)
            result = await validate_pending_outcomes(db)
            assert result["skipped_demo"] == 1
            assert result["provider_pending"] == 0
            assert result["pending"] == 0
            assert result["validated"] == 0
    _run(case())


def test_hold_signal_is_skipped_from_win_loss_validation():
    async def case():
        maker = await _session()
        async with maker() as db:
            await _add_signal(db, direction="HOLD", with_future=True)
            result = await validate_pending_outcomes(db)
            assert result["skipped_hold"] == 1
            assert result["provider_candidates"] == 0
            assert result["wins"] == 0
            assert result["losses"] == 0
    _run(case())


def test_provider_backed_future_candles_validate_win():
    async def case():
        maker = await _session()
        async with maker() as db:
            await _add_signal(db, direction="SELL")
            result = await validate_pending_outcomes(db)
            assert result["provider_candidates"] == 1
            assert result["validated"] == 1
            assert result["wins"] == 1
            assert result["auto_trade"] is False
            assert result["no_execution"] is True
    _run(case())
