import unittest
from app.engines.meta_intelligence import (
    detect_anomalies,
    synthesize_strategic_view,
    detect_recommendation_conflicts,
    dependency_map_snapshot,
)


class Phase14MetaIntelligenceTests(unittest.TestCase):
    def test_anomaly_interpretation(self):
        anomalies = detect_anomalies({"replay_outlier_rate": 0.3, "calibration_drift_jump": 20, "workload_spike": 1})
        self.assertGreaterEqual(len(anomalies), 2)
        self.assertTrue(all(a["reproducible"] for a in anomalies))

    def test_strategic_scoring(self):
        out = synthesize_strategic_view({"regime_instability": 62, "drift_pressure": 50, "integrity_degradation": 40, "reliability_drop": 10, "workload_pressure": 55})
        self.assertIn("scores", out)
        self.assertIn("strategic_stability_score", out["scores"])

    def test_recommendation_conflicts(self):
        conflicts = detect_recommendation_conflicts([
            {"recommendation": "increase aggressive exploration"},
            {"recommendation": "reduce exposure due to integrity risk"},
        ])
        self.assertEqual(len(conflicts), 1)

    def test_dependency_mapping(self):
        deps = dependency_map_snapshot({})
        self.assertGreaterEqual(len(deps), 3)

    def test_cross_system_synthesis_consistency(self):
        a = synthesize_strategic_view({"regime_instability": 70, "drift_pressure": 60, "integrity_degradation": 50, "reliability_drop": 12, "workload_pressure": 40})
        b = synthesize_strategic_view({"regime_instability": 70, "drift_pressure": 60, "integrity_degradation": 50, "reliability_drop": 12, "workload_pressure": 40})
        self.assertEqual(a, b)


if __name__ == '__main__':
    unittest.main()
