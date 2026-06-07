import unittest
from datetime import datetime, timedelta, timezone
from backend.app.engines.outcome_rules import evaluate_outcome
from backend.app.engines.signal_discipline import apply_quality_gates, blocked_by_synthetic_policy, is_duplicate_recent


class Phase4DisciplineTests(unittest.TestCase):
    def test_invalidation_hit_before_tp_sl(self):
        now = datetime.now(timezone.utc)
        res = evaluate_outcome("BUY", "EUR/USD", 1.1000, 1.0950, 1.1100, 1.0980, [{"high": 1.1010, "low": 1.0970}], now + timedelta(hours=1), now)
        self.assertEqual(res["outcome"], "invalidated")

    def test_low_confidence_downgraded(self):
        s = apply_quality_gates({"direction":"BUY","confidence":40,"strength":"strong","risk_level":"low","reason_summary":"x"}, 60)
        self.assertEqual(s["direction"], "HOLD")

    def test_duplicate_cooldown(self):
        self.assertTrue(is_duplicate_recent(datetime.now(timezone.utc) - timedelta(minutes=5), 30))

    def test_synthetic_buy_sell_blocked_default(self):
        self.assertTrue(blocked_by_synthetic_policy({"direction":"BUY","data_source":"synthetic"}, False))

    def test_performance_default_excludes_synthetic_semantic(self):
        self.assertFalse(blocked_by_synthetic_policy({"direction":"BUY","data_source":"real"}, False))


if __name__ == "__main__":
    unittest.main()
