import unittest
from app.engines.meta_operating import (
    build_coordination_graph,
    synchronization_check,
    coordination_status,
    meta_resilience,
    timeline_merge,
    consolidation_recommendations,
    meta_explainability,
)


class Phase21MetaOperatingTests(unittest.TestCase):
    def test_coordination_graph_consistency(self):
        out = build_coordination_graph(
            [{"id": "gov"}, {"id": "replay"}],
            [{"source": "gov", "target": "replay", "dependency_strength": 0.8, "synchronization_status": "ok", "conflict_risk": 0.2}],
        )
        self.assertGreater(out["dependency_strength_avg"], 0)

    def test_synchronization_validation(self):
        out = synchronization_check({"unsynchronized_eras": True, "replay_governance_drift": True})
        self.assertFalse(out["synchronized"])

    def test_coordination_pressure_escalation(self):
        out = coordination_status({"subsystem_divergence": 0.9, "duplicated_governance_logic": 0.8, "workflow_fragmentation": 0.8, "replay_inconsistency_pressure": 0.9, "recommendation_fragmentation": 0.8, "synchronization_failures": 0.9, "coordination_overhead": 0.8})
        self.assertEqual(out["level"], "high")

    def test_resilience_scoring(self):
        out = meta_resilience({"coordination_resilience": 0.9})
        self.assertGreater(out["coordination_resilience"], 0)

    def test_institutional_timeline_consistency(self):
        out = timeline_merge({"strategic_eras": ["era1"], "incidents": [{"id": 1}]})
        self.assertGreaterEqual(len(out), 2)

    def test_workflow_consolidation_integrity(self):
        out = consolidation_recommendations({"overlapping_workflows": 4, "duplicated_narratives": 3})
        self.assertGreaterEqual(len(out["recommendations"]), 1)

    def test_meta_explainability_reproducibility(self):
        a = meta_explainability({"executive": "x"})
        b = meta_explainability({"executive": "x"})
        self.assertEqual(a, b)


if __name__ == '__main__':
    unittest.main()
