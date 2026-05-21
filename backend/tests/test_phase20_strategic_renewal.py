import unittest
from app.engines.strategic_renewal import (
    adaptability_status,
    renewal_workflow,
    evolution_plan,
    anti_dogma_scan,
    sandbox_experiment,
    identity_health,
)


class Phase20StrategicRenewalTests(unittest.TestCase):
    def test_inertia_scoring(self):
        scores = adaptability_status({"governance_responsiveness": 0.5, "recommendation_adaptability": 0.4, "workflow_adaptability": 0.6, "replay_adaptability": 0.4})
        self.assertGreater(scores["strategic_inertia"], 0)

    def test_renewal_workflow_integrity(self):
        wf = renewal_workflow({"workflow_type": "assumption_renewal", "operator_reviewed": True})
        self.assertTrue(wf["auditable"])
        self.assertEqual(wf["status"], "approved")

    def test_evolution_plan_reproducibility(self):
        a = evolution_plan({"proposed_evolution": "replay adapter modernization"})
        self.assertTrue(a["operator_review_required"])
        self.assertIn("rollback_strategy", a)

    def test_anti_dogma_detection(self):
        out = anti_dogma_scan({"unchallenged_assumptions": 7, "stale_narratives": 5})
        self.assertGreaterEqual(len(out["warnings"]), 1)

    def test_adaptability_scoring(self):
        out = adaptability_status({"governance_responsiveness": 0.9, "recommendation_adaptability": 0.9, "workflow_adaptability": 0.9, "replay_adaptability": 0.9, "profile_adaptability": 0.9, "calibration_adaptability": 0.9})
        self.assertGreater(out["adaptation_responsiveness"], 80)

    def test_sandbox_isolation(self):
        out = sandbox_experiment({"experiment_type": "governance_experiment"})
        self.assertTrue(out["sandboxed"])
        self.assertFalse(out["auto_promote"])

    def test_identity_preservation_guarantees(self):
        out = identity_health({"constitutional_principles_preserved": True, "human_sovereignty_guarantees": True})
        self.assertTrue(out["constitutional_principles_preserved"])
        self.assertTrue(out["human_sovereignty_guarantees"])


if __name__ == '__main__':
    unittest.main()
