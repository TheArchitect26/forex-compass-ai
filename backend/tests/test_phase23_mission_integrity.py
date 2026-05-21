import unittest
from app.engines.mission_integrity import (
    detect_mission_drift,
    optimization_vs_purpose,
    humility_safeguards,
    mission_status,
    anchor_note,
    anti_hollowing,
)


class Phase23MissionIntegrityTests(unittest.TestCase):
    def test_mission_drift_detection(self):
        out = detect_mission_drift({"mission_drift": 0.7, "optimization_drift": 0.7})
        self.assertTrue(out["alignment_warning"])
        self.assertIn("mission_drift", out["drift_flags"])

    def test_optimization_vs_purpose_analysis(self):
        out = optimization_vs_purpose({"metrics_without_value": 4, "recommendation_proliferation": 6})
        self.assertGreaterEqual(len(out["warnings"]), 1)

    def test_strategic_humility_safeguards(self):
        out = humility_safeguards({"overconfidence_inflation": 0.7, "excessive_abstraction": 0.7})
        self.assertGreaterEqual(len(out["humility_flags"]), 1)

    def test_mission_coherence_scoring(self):
        out = mission_status({"mission_alignment": 0.9})
        self.assertGreater(out["mission_alignment_score"], 0)

    def test_operator_anchor_persistence_shape(self):
        out = anchor_note({"operator_note": "keep human-in-loop", "anti_drift_confirmation": True})
        self.assertTrue(out["anti_drift_confirmation"])
        self.assertTrue(out["created_at"])

    def test_anti_hollowing_detection(self):
        out = anti_hollowing({"purposeless_systems": 1, "recommendation_inflation": 5})
        self.assertGreaterEqual(len(out["flags"]), 1)

    def test_existential_timeline_integrity_inputs(self):
        # timeline-related structures depend on event types; this checks stable result shape of drift + status composition
        drift = detect_mission_drift({})
        status = mission_status({})
        self.assertIn("drift_flags", drift)
        self.assertIn("existential_coherence_score", status)


if __name__ == '__main__':
    unittest.main()
