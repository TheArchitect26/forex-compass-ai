import unittest
from app.engines.longevity import (
    lineage_entry,
    migration_plan,
    replay_compatibility_mode,
    survivability_scores,
    deprecation_workflow,
    archive_durability_check,
)


class Phase19LongevityTests(unittest.TestCase):
    def test_lineage_preservation(self):
        out = lineage_entry({"changed_component": "replay_engine", "why": "adapter refactor"})
        self.assertEqual(out["changed_component"], "replay_engine")
        self.assertTrue(out["created_at"])

    def test_migration_reversibility(self):
        out = migration_plan({"target": "datasets", "operator_approved": True, "reversible": True})
        self.assertTrue(out["reversible"])
        self.assertEqual(out["status"], "approved")

    def test_replay_compatibility_mode(self):
        out = replay_compatibility_mode({"deprecated_logic": True, "adapter_required": True})
        self.assertEqual(out["compatibility_mode"], "legacy")
        self.assertGreaterEqual(len(out["integrity_warnings"]), 1)

    def test_survivability_scoring(self):
        scores = survivability_scores({"architectural_survivability": 0.9})
        self.assertGreater(scores["architectural_survivability"], 0)

    def test_deprecation_workflow(self):
        out = deprecation_workflow({"entity_type": "assumption", "entity_id": "a1"})
        self.assertTrue(out["operator_review_required"])
        self.assertFalse(out["silent_removal"])

    def test_archive_durability_validation(self):
        out = archive_durability_check([
            {"id": 1, "lineage_ref": "x", "needs_replay_ref": True, "replay_ref": "r1"},
            {"id": 2, "needs_replay_ref": True},
        ])
        self.assertFalse(out["archive_integrity_valid"])
        self.assertIn(2, out["broken_lineage"])


if __name__ == '__main__':
    unittest.main()
