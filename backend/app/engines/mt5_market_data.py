from __future__ import annotations

import pandas as pd
from sqlalchemy import select

from app.db import SessionLocal
from app.engines.historical import normalize_pair
from app.models import HistoricalCandle


DIRECT_TIMEFRAMES = {
    "1min": "1min",
    "5min": "5min",
    "1h": "1h",
}

RESAMPLED_TIMEFRAMES = {
    "15min": ("5min", "15min", 3),
    "30min": ("5min", "30min", 6),
    "4h": ("1h", "4h", 4),
}


class MT5MarketDataProvider:
    source_name = "mt5_hantec"

    async def ohlcv(
        self,
        pair: str,
        timeframe: str,
        limit: int = 300,
    ) -> pd.DataFrame:
        pair = normalize_pair(pair)
        timeframe = timeframe.strip().lower()
        limit = max(1, min(int(limit), 5000))

        if timeframe in DIRECT_TIMEFRAMES:
            base_timeframe = DIRECT_TIMEFRAMES[timeframe]
            fetch_limit = limit
            resample_rule = None
            required_count = 1

        elif timeframe in RESAMPLED_TIMEFRAMES:
            (
                base_timeframe,
                resample_rule,
                required_count,
            ) = RESAMPLED_TIMEFRAMES[timeframe]

            fetch_limit = min(
                5000,
                limit * required_count
                + required_count * 10,
            )

        else:
            raise ValueError(
                f"MT5 timeframe not supported: {timeframe}"
            )

        async with SessionLocal() as session:
            result = await session.execute(
                select(
                    HistoricalCandle.timestamp,
                    HistoricalCandle.open,
                    HistoricalCandle.high,
                    HistoricalCandle.low,
                    HistoricalCandle.close,
                    HistoricalCandle.volume,
                )
                .where(
                    HistoricalCandle.pair == pair,
                    HistoricalCandle.timeframe == base_timeframe,
                    HistoricalCandle.source == self.source_name,
                )
                .order_by(
                    HistoricalCandle.timestamp.desc()
                )
                .limit(fetch_limit)
            )

            rows = result.all()

        if not rows:
            raise RuntimeError(
                f"No MT5 candles found for "
                f"{pair} {base_timeframe}"
            )

        frame = pd.DataFrame(
            [tuple(row) for row in rows],
            columns=[
                "datetime",
                "open",
                "high",
                "low",
                "close",
                "volume",
            ],
        )

        frame["datetime"] = pd.to_datetime(
            frame["datetime"],
            utc=True,
        )

        frame = (
            frame
            .sort_values("datetime")
            .drop_duplicates(
                subset=["datetime"],
                keep="last",
            )
            .reset_index(drop=True)
        )

        for column in (
            "open",
            "high",
            "low",
            "close",
            "volume",
        ):
            frame[column] = frame[column].astype(float)

        if resample_rule is None:
            frame["datetime"] = (
                frame["datetime"]
                .dt.tz_convert(None)
            )

            return (
                frame
                .tail(limit)
                .reset_index(drop=True)
            )

        indexed = frame.set_index("datetime")

        resample_offset = (
            pd.Timedelta(hours=1)
            if timeframe == "4h"
            else pd.Timedelta(0)
        )

        resampled = indexed.resample(
            resample_rule,
            origin="epoch",
            offset=resample_offset,
            label="left",
            closed="left",
        ).agg({
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "volume": "sum",
        })

        counts = indexed["close"].resample(
            resample_rule,
            origin="epoch",
            offset=resample_offset,
            label="left",
            closed="left",
        ).count()

        resampled["base_count"] = counts

        resampled = resampled[
            resampled["base_count"] >= required_count
        ]

        resampled = (
            resampled
            .drop(columns=["base_count"])
            .dropna()
        )

        resampled.index = (
            resampled.index.tz_convert(None)
        )

        return (
            resampled
            .reset_index()
            .tail(limit)
            .reset_index(drop=True)
        )


mt5_market_data = MT5MarketDataProvider()
