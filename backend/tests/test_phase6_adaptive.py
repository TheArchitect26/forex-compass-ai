import unittest
import pandas as pd
from backend.app.engines.regime import detect_details
from backend.app.engines.signal_intelligence import regime_weight_adjustments
from backend.app.engines.strategy_profiles import set_active_profile, get_active_profile
from backend.app.engines.reliability import reliability_score


class Phase6AdaptiveTests(unittest.TestCase):
    def test_regime_detection(self):
        df = pd.DataFrame({"open":[1,1.01,1.02,1.03,1.04,1.05,1.06,1.07,1.08,1.09],"high":[1.01,1.02,1.03,1.04,1.05,1.06,1.07,1.08,1.09,1.10],"low":[0.99,1.0,1.01,1.02,1.03,1.04,1.05,1.06,1.07,1.08],"close":[1.0,1.01,1.02,1.03,1.04,1.05,1.06,1.07,1.08,1.09],"volume":[100]*10})
        d = detect_details(df)
        self.assertIn("regime", d)

    def test_regime_weight_change(self):
        t = regime_weight_adjustments("trending")
        r = regime_weight_adjustments("ranging")
        self.assertNotEqual(t["weights"]["rsi"], r["weights"]["rsi"])

    def test_profile_switching(self):
        set_active_profile("conservative")
        self.assertEqual(get_active_profile()["name"], "conservative")

    def test_drift_lowers_reliability_semantic(self):
        s1,_ = reliability_score(80, 60, 5, 3)
        s2,_ = reliability_score(10, 40, 0, 0)
        self.assertGreater(s1, s2)


if __name__ == "__main__":
    unittest.main()
