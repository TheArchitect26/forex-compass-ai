import unittest
from datetime import datetime, timedelta, timezone
from backend.app.engines.outcome_rules import evaluate_outcome
from app.engines.outcome_validation import classify_threshold_outcome


class OutcomeValidationTests(unittest.TestCase):
    def test_buy_tp_first_win(self):
        now = datetime.now(timezone.utc)
        res = evaluate_outcome("BUY", "EUR/USD", 1.1000, 1.0950, 1.1050, 1.0950, [{"high": 1.1060, "low": 1.0990}], now + timedelta(hours=1), now)
        self.assertEqual(res["outcome"], "win")

    def test_buy_sl_first_loss(self):
        now = datetime.now(timezone.utc)
        res = evaluate_outcome("BUY", "EUR/USD", 1.1000, 1.0950, 1.1050, 1.0900, [{"high": 1.1020, "low": 1.0940}], now + timedelta(hours=1), now)
        self.assertEqual(res["outcome"], "loss")

    def test_sell_tp_first_win(self):
        now = datetime.now(timezone.utc)
        res = evaluate_outcome("SELL", "EUR/USD", 1.1000, 1.1050, 1.0950, 1.1050, [{"high": 1.1010, "low": 1.0940}], now + timedelta(hours=1), now)
        self.assertEqual(res["outcome"], "win")

    def test_sell_sl_first_loss(self):
        now = datetime.now(timezone.utc)
        res = evaluate_outcome("SELL", "EUR/USD", 1.1000, 1.1050, 1.0950, 1.1100, [{"high": 1.1060, "low": 1.0980}], now + timedelta(hours=1), now)
        self.assertEqual(res["outcome"], "loss")

    def test_hold_expires_neutral(self):
        now = datetime.now(timezone.utc)
        res = evaluate_outcome("HOLD", "EUR/USD", 1.1, 1.09, 1.11, 1.09, [], now - timedelta(minutes=1), now - timedelta(hours=1))
        self.assertEqual(res["outcome"], "neutral")

    def test_win_rate_excludes_hold(self):
        outcomes = [
            {"direction": "BUY", "outcome": "win"},
            {"direction": "SELL", "outcome": "loss"},
            {"direction": "HOLD", "outcome": "neutral"},
        ]
        trade = [o for o in outcomes if o["direction"] in {"BUY", "SELL"} and o["outcome"] in {"win", "loss", "expired"}]
        wins = sum(1 for o in trade if o["outcome"] == "win")
        self.assertEqual(round(wins / len(trade) * 100, 2), 50.0)

    def test_threshold_buy_win_loss_pending(self):
        win = classify_threshold_outcome("BUY", "EUR/USD", 1.1000, [{"high": 1.1045, "low": 1.0995}], horizon_candles=2, take_profit_pips=40, stop_loss_pips=25)
        loss = classify_threshold_outcome("BUY", "EUR/USD", 1.1000, [{"high": 1.1010, "low": 1.0970}], horizon_candles=2, take_profit_pips=40, stop_loss_pips=25)
        pending = classify_threshold_outcome("BUY", "EUR/USD", 1.1000, [], horizon_candles=2, take_profit_pips=40, stop_loss_pips=25)
        self.assertEqual(win["outcome"], "win")
        self.assertEqual(loss["outcome"], "loss")
        self.assertEqual(pending["outcome"], "pending")

    def test_threshold_sell_win_loss_pending(self):
        win = classify_threshold_outcome("SELL", "EUR/USD", 1.1000, [{"high": 1.1005, "low": 1.0955}], horizon_candles=2, take_profit_pips=40, stop_loss_pips=25)
        loss = classify_threshold_outcome("SELL", "EUR/USD", 1.1000, [{"high": 1.1030, "low": 1.0990}], horizon_candles=2, take_profit_pips=40, stop_loss_pips=25)
        pending = classify_threshold_outcome("SELL", "EUR/USD", 1.1000, [], horizon_candles=2, take_profit_pips=40, stop_loss_pips=25)
        self.assertEqual(win["outcome"], "win")
        self.assertEqual(loss["outcome"], "loss")
        self.assertEqual(pending["outcome"], "pending")


if __name__ == "__main__":
    unittest.main()
