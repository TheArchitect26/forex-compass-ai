import unittest
from app.engines.human_sovereignty import (
    complexity_pressure,
    simplification_engine,
    apply_focus_mode,
    operator_load,
    reset_action,
)


class Phase18HumanSovereigntyTests(unittest.TestCase):
    def test_complexity_pressure_escalation(self):
        out = complexity_pressure({"dashboard_overload": 4, "recommendation_saturation": 4, "unresolved_workflow_accumulation": 4})
        self.assertIn(out["level"], {"elevated", "high"})

    def test_simplification_consistency(self):
        inp = {"recommendations": [{"recommendation": "reduce risk"}, {"recommendation": "reduce risk"}], "workflows": [{"impact": 0.9}, {"impact": 0.1}]}
        a = simplification_engine(inp)
        b = simplification_engine(inp)
        self.assertEqual(a, b)
        self.assertEqual(len(a["merged_recommendations"]), 1)

    def test_focus_mode_filtering(self):
        out = apply_focus_mode("replay_focus", [{"title": "replay drift", "tags": ["replay"]}, {"title": "governance note", "tags": ["governance"]}])
        self.assertEqual(len(out), 1)

    def test_cognitive_load_scoring(self):
        out = operator_load({"complexity_pressure": 60, "alert_density": 40, "recommendation_saturation": 30})
        self.assertGreater(out["cognitive_load_score"], 0)

    def test_human_override_guarantee(self):
        reset = reset_action("archive_consolidation", approved_by_human=True)
        self.assertTrue(reset["applied"])
        denied = reset_action("archive_consolidation", approved_by_human=False)
        self.assertFalse(denied["applied"])

    def test_reset_reversibility(self):
        reset = reset_action("baseline_refresh", approved_by_human=True)
        self.assertTrue(reset["reversible"])
        self.assertTrue(reset["auditable"])


if __name__ == '__main__':
    unittest.main()
