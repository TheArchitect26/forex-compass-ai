import unittest
from backend.app.engines.signal_rules import evaluate_signal_components, assess_risk_and_strength


class SignalTrustTests(unittest.TestCase):
    def _tech(self, trend, rsi, momentum, close=1.1, atr=0.001):
        return {"trend": trend, "rsi": rsi, "momentum": momentum, "close": close, "atr": atr}

    def test_buy_signal_strong_confluence(self):
        c = evaluate_signal_components(
            self._tech("bullish", 32, "up"),
            self._tech("bullish", 40, "up"),
            self._tech("bullish", 34, "up"),
            {"state": "bullish_bos"},
            ["bullish_engulfing"],
        )
        self.assertEqual(c["direction"], "BUY")
        self.assertGreaterEqual(c["confidence"], 60)

    def test_sell_signal_strong_confluence(self):
        c = evaluate_signal_components(
            self._tech("bearish", 70, "down"),
            self._tech("bearish", 68, "down"),
            self._tech("bearish", 71, "down"),
            {"state": "bearish_bos"},
            ["bearish_engulfing"],
        )
        self.assertEqual(c["direction"], "SELL")
        self.assertGreaterEqual(c["confidence"], 60)

    def test_hold_when_conflict(self):
        c = evaluate_signal_components(
            self._tech("bullish", 50, "up"),
            self._tech("bearish", 50, "down"),
            self._tech("neutral", 50, "up"),
            {"state": "neutral"},
            [],
        )
        self.assertEqual(c["direction"], "HOLD")
        self.assertLessEqual(c["confidence"], 45)

    def test_high_risk_extreme_volatility(self):
        risk, strength, warnings = assess_risk_and_strength("BUY", 80, close=1.0, atr=0.05, stop_loss=0.98)
        self.assertEqual(risk, "high")
        self.assertTrue(any("Extreme ATR volatility" in w for w in warnings))

    def test_synthetic_warning_path(self):
        risk, _, warnings = assess_risk_and_strength("BUY", 70, close=1.0, atr=0.001, stop_loss=0.999)
        self.assertIn(risk, ["low", "medium", "high"])
        self.assertIsInstance(warnings, list)


if __name__ == "__main__":
    unittest.main()
