import unittest
from datetime import timezone
from backend.app.utils_time import utc_now
from backend.app.engines.pips import pip_size
from backend.app.engines.outcome_rules import evaluate_outcome
from backend.app.engines.reliability import classify_alignment, reliability_score


class Phase5Tests(unittest.TestCase):
    def test_utc_helper_timezone_aware(self):
        self.assertEqual(utc_now().tzinfo, timezone.utc)

    def test_pip_size_pairs(self):
        self.assertEqual(pip_size("EUR/USD"), 0.0001)
        self.assertEqual(pip_size("USD/JPY"), 0.01)
        self.assertGreater(pip_size("XAU/USD"), 0)

    def test_net_pips_after_costs(self):
        res = evaluate_outcome("BUY", "EUR/USD", 1.1000, 1.0950, 1.1050, 1.0950, [{"high": 1.1060, "low": 1.0990}], utc_now(), utc_now())
        self.assertLess(res["net_result_pips"], res["gross_result_pips"])

    def test_calibration_bucket_alignment(self):
        self.assertEqual(classify_alignment(70, 70), "aligned")

    def test_reliability_low_small_sample(self):
        score, label = reliability_score(5, 50, 1, 1)
        self.assertLess(score, 45)
        self.assertIn(label, {"unproven", "weak"})


if __name__ == "__main__":
    unittest.main()
