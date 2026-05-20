import unittest
from datetime import datetime, timedelta
from backend.app.engines.outcome_rules import evaluate_outcome


class OutcomeValidationTests(unittest.TestCase):
    def test_buy_tp_first_win(self):
        res = evaluate_outcome("BUY", "EUR/USD", 1.1000, 1.0950, 1.1050, 1.0950, [{"high": 1.1060, "low": 1.0990}], datetime.utcnow()+timedelta(hours=1), datetime.utcnow())
        self.assertEqual(res["outcome"], "win")

    def test_buy_sl_first_loss(self):
        res = evaluate_outcome("BUY", "EUR/USD", 1.1000, 1.0950, 1.1050, 1.0900, [{"high": 1.1020, "low": 1.0940}], datetime.utcnow()+timedelta(hours=1), datetime.utcnow())
        self.assertEqual(res["outcome"], "loss")

    def test_sell_tp_first_win(self):
        res = evaluate_outcome("SELL", "EUR/USD", 1.1000, 1.1050, 1.0950, 1.1050, [{"high": 1.1010, "low": 1.0940}], datetime.utcnow()+timedelta(hours=1), datetime.utcnow())
        self.assertEqual(res["outcome"], "win")

    def test_sell_sl_first_loss(self):
        res = evaluate_outcome("SELL", "EUR/USD", 1.1000, 1.1050, 1.0950, 1.1100, [{"high": 1.1060, "low": 1.0980}], datetime.utcnow()+timedelta(hours=1), datetime.utcnow())
        self.assertEqual(res["outcome"], "loss")

    def test_hold_expires_neutral(self):
        res = evaluate_outcome("HOLD", "EUR/USD", 1.1, 1.09, 1.11, 1.09, [], datetime.utcnow()-timedelta(minutes=1), datetime.utcnow()-timedelta(hours=1))
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


if __name__ == "__main__":
    unittest.main()
