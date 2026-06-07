from datetime import timedelta

import pytest

from app.api.signals import review_signals
from app.models import SignalOutcome, SignalScanContext
from app.utils_time import utc_now


pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    return "asyncio"


class _FakeResult:
    def __init__(self, rows: list[tuple[SignalScanContext, SignalOutcome | None]]):
        self._rows = rows

    def all(self) -> list[tuple[SignalScanContext, SignalOutcome | None]]:
        return self._rows


class _FakeSession:
    def __init__(self, rows: list[tuple[SignalScanContext, SignalOutcome | None]]):
        self._rows = rows

    async def execute(self, _statement):
        return _FakeResult(self._rows)


def _context(
    signal_id: int,
    *,
    pair: str,
    direction: str,
    data_mode: str,
    provider_name: str,
    demo_only: bool,
    minutes_ago: int,
    timeframe: str = "15min",
) -> SignalScanContext:
    created_at = utc_now() - timedelta(minutes=minutes_ago)
    return SignalScanContext(
        id=signal_id,
        signal_id=signal_id,
        symbol=pair,
        interval=timeframe,
        signal_timestamp=created_at,
        direction=direction,
        confidence=80,
        entry_price=1.1000,
        data_mode=data_mode,
        provider_name=provider_name,
        demo_only=demo_only,
        candle_snapshot={"rows": 1, "demo_only": demo_only},
        created_at=created_at,
    )


def _outcome(context: SignalScanContext, outcome: str) -> SignalOutcome:
    return SignalOutcome(
        signal_id=context.signal_id,
        pair=context.symbol,
        timeframe=context.interval,
        direction=context.direction,
        entry_price=context.entry_price,
        stop_loss=1.0975,
        take_profit=1.1040,
        invalidation_price=1.0975,
        outcome=outcome,
    )


def _review_session() -> _FakeSession:
    provider = _context(1, pair="EUR/USD", direction="BUY", data_mode="provider", provider_name="twelve_data", demo_only=False, minutes_ago=5)
    cached = _context(2, pair="GBP/USD", direction="SELL", data_mode="cached", provider_name="cached_provider", demo_only=False, minutes_ago=10)
    hold = _context(3, pair="USD/JPY", direction="HOLD", data_mode="provider", provider_name="twelve_data", demo_only=False, minutes_ago=15, timeframe="1h")
    demo = _context(4, pair="AUD/USD", direction="BUY", data_mode="synthetic_demo", provider_name="synthetic", demo_only=True, minutes_ago=20)
    unavailable = _context(5, pair="NZD/USD", direction="SELL", data_mode="unavailable", provider_name="twelve_data", demo_only=False, minutes_ago=25)
    return _FakeSession([
        (provider, _outcome(provider, "win")),
        (cached, _outcome(cached, "loss")),
        (hold, None),
        (demo, None),
        (unavailable, None),
    ])


async def _call_review(db: _FakeSession | None = None, **kwargs):
    params = {"db": db or _review_session(), "demo_only": None, "limit": 50, "offset": 0}
    params.update(kwargs)
    return await review_signals(**params)


async def test_review_endpoint_returns_recent_records():
    payload = await _call_review()
    assert [item["symbol"] for item in payload["items"][:3]] == ["EUR/USD", "GBP/USD", "USD/JPY"]
    assert payload["summary"]["total"] == 5
    assert payload["summary"]["wins"] == 1
    assert payload["summary"]["losses"] == 1
    assert payload["auto_trade"] is False
    assert payload["no_execution"] is True
    assert payload["advisory_only"] is True


async def test_review_filters_work():
    payload = await _call_review(
        symbol="EUR/USD",
        interval="15min",
        direction="BUY",
        validation_status="validated",
        demo_only=False,
        data_mode="provider",
    )
    assert payload["summary"]["total"] == 1
    assert payload["items"][0]["symbol"] == "EUR/USD"
    assert payload["items"][0]["validation_status"] == "validated"


async def test_review_hold_records_show_review_only():
    payload = await _call_review(direction="HOLD")
    item = payload["items"][0]
    assert item["validation_status"] == "skipped_hold"
    assert item["execution_grade"] == "review_only"
    assert "not validated" in item["outcome_notes"]


async def test_review_demo_records_are_clearly_separated():
    payload = await _call_review(demo_only=True)
    assert payload["summary"]["total"] == 1
    assert payload["summary"]["demo_only"] == 1
    assert payload["items"][0]["data_mode"] == "synthetic_demo"
    assert payload["items"][0]["validation_status"] == "skipped_demo"


async def test_review_provider_records_are_separated_from_demo_and_unavailable():
    db = _review_session()
    provider = await _call_review(db=db, data_mode="provider")
    cached = await _call_review(db=db, data_mode="cached")
    unavailable = await _call_review(db=db, data_mode="unavailable")

    assert provider["summary"]["provider_backed"] == 2
    assert all(item["data_mode"] == "provider" for item in provider["items"])
    assert all(item["demo_only"] is False for item in provider["items"])
    assert cached["summary"]["provider_backed"] == 1
    assert cached["items"][0]["data_mode"] == "cached"
    assert cached["items"][0]["demo_only"] is False
    assert unavailable["summary"]["unavailable"] == 1
    assert unavailable["items"][0]["data_mode"] == "unavailable"


async def test_review_endpoint_exposes_no_trading_or_execution_behavior():
    payload = await _call_review()
    forbidden = {"execute", "trade", "order", "broker", "position_size", "close_url"}
    assert payload["auto_trade"] is False
    assert payload["no_execution"] is True
    assert forbidden.isdisjoint(payload.keys())
    for item in payload["items"]:
        assert item["auto_trade"] is False
        assert item["no_execution"] is True
        assert item["advisory_only"] is True
        assert forbidden.isdisjoint(item.keys())
        assert item["execution_grade"] in {"validation_candidate", "review_only"}


async def test_review_no_auto_trading_introduced():
    payload = await _call_review()
    assert payload["auto_trade"] is False
    assert all(item["auto_trade"] is False for item in payload["items"])
