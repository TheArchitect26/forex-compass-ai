import unittest
from backend.app.engines.pipeline_meta import config_snapshot
from backend.app.engines.strategy_profiles import profile_or_default
from backend.app.engines.session import classify_session
from datetime import datetime, timezone


class Phase8InfraTests(unittest.TestCase):
    def test_config_snapshot_persistence_shape(self):
        snap = config_snapshot(profile_or_default("intraday"))
        self.assertIn("engine_version", snap)
        self.assertIn("discipline_version", snap)

    def test_profile_default_and_repeatability(self):
        p1 = profile_or_default("intraday")
        p2 = profile_or_default("intraday")
        self.assertEqual(p1, p2)

    def test_session_deterministic(self):
        dt = datetime(2026, 1, 1, 13, 0, tzinfo=timezone.utc)
        self.assertEqual(classify_session(dt), classify_session(dt))


if __name__ == "__main__":
    unittest.main()
