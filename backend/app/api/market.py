import pandas as pd
from fastapi import APIRouter, Query, HTTPException
from app.engines.market_data import market_data
from app.engines.mt5_market_data import mt5_market_data
from app.engines.regime import detect_details
from app.config import settings

router = APIRouter()


@router.get("/pairs")
async def pairs():
    return {"pairs": settings.PAIRS, "timeframes": settings.TIMEFRAMES}


@router.get("/ohlcv")
async def ohlcv(pair: str = "EUR/USD", timeframe: str = "1h", limit: int = 300):
    df = await market_data.ohlcv(pair, timeframe, limit)
    source_info = market_data.source_info(pair, timeframe, limit)
    return {
        "pair": pair, "timeframe": timeframe,
        "source": source_info["source"],
        "warning": source_info["warning"],
        "candles": [
            {"time": int(r.datetime.timestamp()), "open": r.open, "high": r.high,
             "low": r.low, "close": r.close, "volume": int(r.volume)}
            for r in df.itertuples()
        ],
    }


@router.get("/heatmap")
async def heatmap():
    """Pct change vs N bars ago across the universe."""
    out = []
    for p in settings.PAIRS:
        df = await market_data.ohlcv(p, "1h", 25)
        change = (df["close"].iloc[-1] / df["close"].iloc[0] - 1) * 100
        out.append({"pair": p, "change_pct": round(float(change), 3), "price": float(df["close"].iloc[-1])})
    return {"items": out}


@router.get("/regime")
async def regime(pair: str = "EUR/USD", timeframe: str = "1h"):
    if pair not in settings.PAIRS:
        raise HTTPException(400, "Unsupported pair")
    if timeframe not in settings.TIMEFRAMES:
        raise HTTPException(400, "Unsupported timeframe")
    df = await market_data.ohlcv(pair, timeframe, 220)
    details = detect_details(df)
    return {"pair": pair, "timeframe": timeframe, **details}



@router.get("/compare-providers")
async def compare_providers(
    pair: str = "EUR/USD",
    timeframe: str = "1h",
    limit: int = 200,
):
    if limit < 20 or limit > 1000:
        raise HTTPException(
            400,
            "limit must be between 20 and 1000",
        )

    comparison_fetch_limit = min(
        1000,
        max(
            limit * 4,
            limit + 200,
        ),
    )

    try:
        mt5_frame = await mt5_market_data.ohlcv(
            pair,
            timeframe,
            comparison_fetch_limit,
        )
    except Exception as exc:
        raise HTTPException(
            404,
            f"MT5 data unavailable: {exc}",
        ) from exc

    twelve_frame = await market_data.ohlcv(
        pair,
        timeframe,
        comparison_fetch_limit,
    )

    source_info = market_data.source_info(
        pair,
        timeframe,
        comparison_fetch_limit,
    )

    if source_info.get("source") != "twelve_data":
        raise HTTPException(
            503,
            "Twelve Data unavailable; "
            "comparison cannot be trusted",
        )

    mt5 = mt5_frame[
        [
            "datetime",
            "open",
            "high",
            "low",
            "close",
            "volume",
        ]
    ].copy()

    twelve = twelve_frame[
        [
            "datetime",
            "open",
            "high",
            "low",
            "close",
            "volume",
        ]
    ].copy()

    mt5["datetime"] = pd.to_datetime(
        mt5["datetime"],
        utc=True,
    ).dt.tz_convert(None)

    twelve["datetime"] = pd.to_datetime(
        twelve["datetime"],
        utc=True,
    ).dt.tz_convert(None)

    merged = mt5.merge(
        twelve,
        on="datetime",
        how="inner",
        suffixes=("_mt5", "_twelve"),
    )

    merged = (
        merged
        .sort_values("datetime")
        .tail(limit)
        .reset_index(drop=True)
    )

    if len(merged) < 5:
        raise HTTPException(
            422,
            "Not enough matching timestamps "
            "between MT5 and Twelve Data",
        )

    denominator = (
        merged["close_twelve"]
        .abs()
        .replace(0, pd.NA)
    )

    close_difference_bps = (
        (
            merged["close_mt5"]
            - merged["close_twelve"]
        )
        .abs()
        / denominator
        * 10000
    ).dropna()

    returns = merged[
        ["close_mt5", "close_twelve"]
    ].pct_change().dropna()

    correlation_value = returns[
        "close_mt5"
    ].corr(
        returns["close_twelve"]
    )

    correlation = (
        None
        if pd.isna(correlation_value)
        else round(
            float(correlation_value),
            6,
        )
    )

    coverage_ratio = round(
        len(merged) / max(1, limit),
        4,
    )

    median_difference_bps = round(
        float(close_difference_bps.median()),
        4,
    )

    maximum_difference_bps = round(
        float(close_difference_bps.max()),
        4,
    )

    latest_mt5 = mt5["datetime"].max()
    latest_twelve = twelve["datetime"].max()

    freshness_gap_seconds = abs(
        int(
            (
                latest_mt5
                - latest_twelve
            ).total_seconds()
        )
    )

    minimum_overlap = max(
        20,
        int(limit * 0.9),
    )

    reasons = []

    if len(merged) < minimum_overlap:
        reasons.append("low timestamp overlap")

    if coverage_ratio < 0.70:
        reasons.append("low coverage ratio")

    if median_difference_bps > 5:
        reasons.append(
            "median price difference above 5 bps"
        )

    if (
        correlation is not None
        and correlation < 0.98
    ):
        reasons.append(
            "return correlation below 0.98"
        )

    verdict = (
        "pass"
        if not reasons
        else "warning"
    )

    samples = []

    for row in merged.tail(5).itertuples():
        samples.append({
            "datetime": row.datetime.isoformat(),
            "mt5_close": float(row.close_mt5),
            "twelve_close": float(
                row.close_twelve
            ),
            "difference_bps": round(
                abs(
                    float(row.close_mt5)
                    - float(row.close_twelve)
                )
                / max(
                    abs(float(row.close_twelve)),
                    1e-12,
                )
                * 10000,
                4,
            ),
        })

    return {
        "mode": "comparison_only",
        "signals_unchanged": True,
        "pair": pair,
        "timeframe": timeframe,
        "requested_candles": limit,
        "mt5_candles": len(mt5),
        "twelve_candles": len(twelve),
        "matched_candles": len(merged),
        "coverage_ratio": coverage_ratio,
        "return_correlation": correlation,
        "median_close_difference_bps": (
            median_difference_bps
        ),
        "maximum_close_difference_bps": (
            maximum_difference_bps
        ),
        "mt5_latest": latest_mt5.isoformat(),
        "twelve_latest": (
            latest_twelve.isoformat()
        ),
        "freshness_gap_seconds": (
            freshness_gap_seconds
        ),
        "verdict": verdict,
        "reasons": reasons,
        "latest_samples": samples,
    }
