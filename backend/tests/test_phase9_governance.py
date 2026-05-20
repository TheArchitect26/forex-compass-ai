import unittest
from backend.app.engines.governance import regression_severity, compare_metrics
from backend.app.engines.pipeline_meta import config_snapshot
from backend.app.engines.strategy_profiles import profile_or_default


class Phase9GovernanceTests(unittest.TestCase):
    def test_regression_detection(self):
        base = {"net_pips": 5, "invalidation_rate": 0.1, "calibration_alignment": 3, "reliability": 60, "hold_rate": 0.2, "aggressiveness": 0.4}
        cand = {"net_pips": 1, "invalidation_rate": 0.5, "calibration_alignment": 1, "reliability": 40, "hold_rate": 0.5, "aggressiveness": 1.0}
        self.assertIn(regression_severity(base, cand), {"regression", "critical regression"})

    def test_compare_contains_metadata(self):
        out = compare_metrics({"net_pips": 1}, {"net_pips": 1})
        self.assertIn("computed_at", out)

    def test_config_snapshot_versioned(self):
        s = config_snapshot(profile_or_default("intraday"))
        self.assertIn("engine_version", s)
        self.assertIn("strategy_profile_version", s)


if __name__ == "__main__":
    unittest.main()
