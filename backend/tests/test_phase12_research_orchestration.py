import unittest
from app.engines.research_orchestration import (
    priority_from_signals,
    coordinated_health,
    generate_insights,
    recommendations_from_insights,
)


class Phase12ResearchTests(unittest.TestCase):
    def test_priority_escalation(self):
        self.assertEqual(priority_from_signals({"integrity_score": 50}), "critical")
        self.assertEqual(priority_from_signals({"drift_score": 80}), "high")

    def test_health_scoring(self):
        out = coordinated_health({"drift_score": 20})
        self.assertIn("score", out)
        self.assertIn("components", out)

    def test_reproducible_findings(self):
        e = {"volatility": "high", "session": "london_overlap", "reliability_delta": -10, "correlated_gold_usd": True}
        self.assertEqual(generate_insights(e), generate_insights(e))

    def test_recommendation_explainability(self):
        insights = [{"message": "Aggressive profile reliability degraded after volatility regime shift."}]
        recs = recommendations_from_insights(insights)
        self.assertFalse(recs[0]["auto_apply"])
        self.assertTrue(recs[0]["explainability"])


if __name__ == '__main__':
    unittest.main()
