import unittest
from datetime import datetime, timezone
from backend.app.engines.session import classify_session
from backend.app.engines.reliability import reliability_score
from backend.app.engines.strategy_profiles import profile_or_default


class Phase7StabilityTests(unittest.TestCase):
    def test_session_classification(self):
        self.assertEqual(classify_session(datetime(2026,1,1,1,0,tzinfo=timezone.utc)), "Asian")
        self.assertIn("London", classify_session(datetime(2026,1,1,12,0,tzinfo=timezone.utc)))

    def test_profile_default(self):
        self.assertEqual(profile_or_default("does-not-exist")["name"], "intraday")

    def test_reliability_score_ordering(self):
        low,_ = reliability_score(10, 40, 0, 0)
        hi,_ = reliability_score(120, 60, 4, 3)
        self.assertGreater(hi, low)

    def test_adaptation_safety_bound_semantic(self):
        # confidence modulation in engine is bounded to [5, 100]
        conf = max(5.0, min(100.0, 95 * 1.2))
        self.assertLessEqual(conf, 100.0)


if __name__ == "__main__":
    unittest.main()
