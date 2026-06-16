from datetime import datetime, timedelta, timezone
from hmac import compare_digest

from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db import get_db
from app.engines.historical import (
    detect_gaps,
    integrity_score,
    malformed_ohlc,
    normalize_pair,
    normalize_timeframe,
)
from app.engines.market_data import market_data
from app.models import HistoricalCandle, IngestionRun, Signal


router = APIRouter()


MT5_TIMEFRAME_ALIASES = {
    "M1": "1min",
    "1M": "1min",
    "1MIN": "1min",
    "M5": "5min",
    "5M": "5min",
    "5MIN": "5min",
    "M15": "15min",
    "15M": "15min",
    "15MIN": "15min",
    "M30": "30min",
    "30M": "30min",
    "30MIN": "30min",
    "H1": "1h",
    "1H": "1h",
    "H4": "4h",
    "4H": "4h",
    "D1": "1day",
    "1D": "1day",
}


class MT5CandlePayload(BaseModel):
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float = 0.0


class MT5BatchPayload(BaseModel):
    pair: str
    timeframe: str
    broker_symbol: str = ""
    source: str = "mt5_hantec"
    candles: list[MT5CandlePayload]


def normalize_mt5_timeframe(value: str) -> str:
    cleaned = (value or "").strip().upper()
    mapped = MT5_TIMEFRAME_ALIASES.get(cleaned)

    if mapped:
        return mapped

    normalized = normalize_timeframe((value or "").strip().lower())

    if normalized == "1h" and cleaned not in {"H1", "1H", "1HOUR"}:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unsupported timeframe: {value}",
        )

    return normalized


def normalize_timestamp(value: datetime) -> datetime:
    if value.tzinfo is None:
        normalized = value.replace(tzinfo=None)
    else:
        normalized = (
            value
            .astimezone(timezone.utc)
            .replace(tzinfo=None)
        )

    return normalized + timedelta(
        minutes=settings.MT5_TIMESTAMP_OFFSET_MINUTES
    )


def verify_mt5_key(provided_key: str | None) -> None:
    configured_key = settings.MT5_INGEST_API_KEY.strip()

    if not configured_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="MT5 ingestion is not configured",
        )

    if not provided_key or not compare_digest(
        provided_key,
        configured_key,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid MT5 ingestion key",
        )


@router.get("/integrity")
async def integrity(db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(Signal))).scalars().all()

    malformed = [
        row.id
        for row in rows
        if "/" not in row.pair
        or row.timeframe
        not in {
            "1min",
            "5min",
            "15min",
            "30min",
            "1h",
            "4h",
            "1day",
        }
    ]

    synthetic = sum(
        1
        for row in rows
        if row.data_source == "synthetic"
    )

    duplicate_pairs = {}

    for row in rows:
        key = (
            row.pair,
            row.timeframe,
            row.created_at.replace(
                second=0,
                microsecond=0,
            ),
        )
        duplicate_pairs[key] = duplicate_pairs.get(key, 0) + 1

    duplicate_estimate = sum(
        1
        for value in duplicate_pairs.values()
        if value > 1
    )

    score = max(
        0,
        100
        - len(malformed) * 5
        - duplicate_estimate * 2
        - (20 if synthetic > 0 else 0),
    )

    return {
        "source_checks": {
            "synthetic_count": synthetic,
        },
        "duplicate_candle_detection": {
            "estimated_duplicates": duplicate_estimate,
        },
        "malformed_ohlc_detection": {
            "malformed_signal_refs": malformed,
        },
        "synthetic_contamination_checks": {
            "synthetic_ratio": round(
                synthetic / max(1, len(rows)),
                3,
            ),
        },
        "replay_dataset_integrity_score": score,
    }


@router.get("/integrity/datasets")
async def integrity_datasets(
    db: AsyncSession = Depends(get_db),
):
    candles = (
        await db.execute(
            select(HistoricalCandle)
            .order_by(HistoricalCandle.timestamp.asc())
        )
    ).scalars().all()

    grouped = {}

    for candle in candles:
        grouped.setdefault(
            (candle.pair, candle.timeframe),
            [],
        ).append(candle)

    items = []

    for (pair, timeframe), rows in grouped.items():
        timestamps = [row.timestamp for row in rows]

        duplicates = (
            len(rows)
            - len({
                timestamp.isoformat()
                for timestamp in timestamps
            })
        )

        gaps = detect_gaps(timestamps, timeframe)

        malformed = sum(
            1
            for row in rows
            if malformed_ohlc(
                row.open,
                row.high,
                row.low,
                row.close,
            )
        )

        synthetic = sum(
            1
            for row in rows
            if row.source == "synthetic"
        )

        score = integrity_score(
            len(rows),
            duplicates,
            gaps,
            malformed,
            synthetic / max(1, len(rows)),
        )

        items.append({
            "pair": pair,
            "timeframe": timeframe,
            "rows": len(rows),
            "duplicates": duplicates,
            "gaps": gaps,
            "malformed": malformed,
            "synthetic_ratio": round(
                synthetic / max(1, len(rows)),
                3,
            ),
            "integrity_score": score,
        })

    return {"datasets": items}


@router.post("/ingest")
async def ingest(
    body: dict,
    db: AsyncSession = Depends(get_db),
):
    pair = normalize_pair(
        body.get("pair", "EUR/USD")
    )

    timeframe = normalize_timeframe(
        body.get("timeframe", "1h")
    )

    limit = int(body.get("limit", 500))

    frame = await market_data.ohlcv(
        pair,
        timeframe,
        limit,
    )

    fetched = len(frame)
    inserted = 0
    malformed = 0

    source = market_data.source_info(
        pair,
        timeframe,
        limit,
    ).get("source", "synthetic")

    for row in frame.itertuples():
        if malformed_ohlc(
            row.open,
            row.high,
            row.low,
            row.close,
        ):
            malformed += 1
            continue

        exists = (
            await db.execute(
                select(HistoricalCandle)
                .where(
                    HistoricalCandle.pair == pair,
                    HistoricalCandle.timeframe == timeframe,
                    HistoricalCandle.timestamp == row.datetime,
                )
            )
        ).scalars().first()

        if exists:
            continue

        db.add(
            HistoricalCandle(
                pair=pair,
                timeframe=timeframe,
                timestamp=row.datetime,
                open=float(row.open),
                high=float(row.high),
                low=float(row.low),
                close=float(row.close),
                volume=float(row.volume),
                source=source,
            )
        )

        inserted += 1

    run = IngestionRun(
        pair=pair,
        timeframe=timeframe,
        source=source,
        candles_fetched=fetched,
        candles_inserted=inserted,
        gaps_detected=0,
        malformed_rows=malformed,
        retries=0,
        source_reliability=round(
            inserted / max(1, fetched),
            3,
        ),
        status="completed",
    )

    db.add(run)
    await db.commit()

    return {
        "pair": pair,
        "timeframe": timeframe,
        "candles_fetched": fetched,
        "candles_inserted": inserted,
        "malformed_rows": malformed,
    }


@router.post("/mt5-candles")
async def ingest_mt5_candles(
    body: MT5BatchPayload,
    x_mt5_key: str | None = Header(
        default=None,
        alias="X-MT5-Key",
    ),
    db: AsyncSession = Depends(get_db),
):
    verify_mt5_key(x_mt5_key)

    if not body.candles:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="At least one candle is required",
        )

    if len(body.candles) > 5000:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Maximum batch size is 5000 candles",
        )

    pair = normalize_pair(
        body.pair.strip().replace("+", "")
    )

    timeframe = normalize_mt5_timeframe(
        body.timeframe
    )

    source = (
        body.source.strip()[:32]
        or "mt5_hantec"
    )

    broker_symbol = (
        body.broker_symbol.strip()[:32]
        or body.pair.strip()[:32]
    )

    fetched = len(body.candles)
    malformed = 0

    normalized_rows: dict[
        datetime,
        MT5CandlePayload,
    ] = {}

    for candle in body.candles:
        timestamp = normalize_timestamp(
            candle.timestamp
        )

        if malformed_ohlc(
            candle.open,
            candle.high,
            candle.low,
            candle.close,
        ):
            malformed += 1
            continue

        normalized_rows[timestamp] = candle

    if not normalized_rows:
        run = IngestionRun(
            pair=pair,
            timeframe=timeframe,
            source=source,
            candles_fetched=fetched,
            candles_inserted=0,
            gaps_detected=0,
            malformed_rows=malformed,
            retries=0,
            source_reliability=0.0,
            status="rejected",
        )

        db.add(run)
        await db.commit()

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No valid candles were supplied",
        )

    timestamps = sorted(normalized_rows)

    existing_timestamps = set(
        (
            await db.execute(
                select(HistoricalCandle.timestamp)
                .where(
                    HistoricalCandle.pair == pair,
                    HistoricalCandle.timeframe == timeframe,
                    HistoricalCandle.source == source,
                    HistoricalCandle.timestamp
                    >= timestamps[0],
                    HistoricalCandle.timestamp
                    <= timestamps[-1],
                )
            )
        ).scalars().all()
    )

    inserted = 0

    for timestamp in timestamps:
        if timestamp in existing_timestamps:
            continue

        candle = normalized_rows[timestamp]

        db.add(
            HistoricalCandle(
                pair=pair,
                timeframe=timeframe,
                timestamp=timestamp,
                open=float(candle.open),
                high=float(candle.high),
                low=float(candle.low),
                close=float(candle.close),
                volume=max(
                    0.0,
                    float(candle.volume),
                ),
                source=source,
                integrity_flags={
                    "broker_symbol": broker_symbol,
                    "transport": "mt5_push",
                    "completed_candle": True,
                },
                dataset_version="mt5-v1",
            )
        )

        inserted += 1

    gaps = detect_gaps(
        timestamps,
        timeframe,
    )

    run = IngestionRun(
        pair=pair,
        timeframe=timeframe,
        source=source,
        candles_fetched=fetched,
        candles_inserted=inserted,
        gaps_detected=gaps,
        malformed_rows=malformed,
        retries=0,
        source_reliability=round(
            (fetched - malformed)
            / max(1, fetched),
            3,
        ),
        status="completed",
    )

    db.add(run)
    await db.commit()

    return {
        "status": "ok",
        "pair": pair,
        "timeframe": timeframe,
        "source": source,
        "broker_symbol": broker_symbol,
        "candles_received": fetched,
        "candles_valid": len(normalized_rows),
        "candles_inserted": inserted,
        "duplicates_skipped": (
            len(normalized_rows) - inserted
        ),
        "malformed_rows": malformed,
        "gaps_detected": gaps,
    }
