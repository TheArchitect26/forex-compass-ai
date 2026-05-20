import unittest
from app.engines.cognitive_compression import (
    compress_intelligence,
    generate_strategic_narratives,
    synthesize_recommendations,
    confidence_hierarchy,
)


class Phase15CognitiveWorkflowTests(unittest.TestCase):
    def test_cognitive_compression_consistency(self):
        inp = {"themes": [1,2,3,4,5,6], "instability_patterns": ["a"]}
        self.assertEqual(compress_intelligence(inp), compress_intelligence(inp))

    def test_strategic_narrative_reproducibility(self):
        e = {"aggressive_instability_trend": "up", "volatility_overlap": True, "refs": ["r1"]}
        self.assertEqual(generate_strategic_narratives(e), generate_strategic_narratives(e))

    def test_recommendation_synthesis(self):
        out = synthesize_recommendations([
            {"recommendation": "increase replay depth", "horizon": "short", "resolved": False},
            {"recommendation": "reduce concurrency", "horizon": "short", "resolved": False, "severity": "critical"},
        ])
        self.assertTrue(out["conflicting_priorities"])
        self.assertEqual(out["recurring_unresolved_issues"], 2)

    def test_confidence_hierarchy_integrity(self):
        out = confidence_hierarchy({"raw_signal_confidence": 0.7, "strategic_confidence": 0.8})
        self.assertIn("governance_confidence", out)
        self.assertGreater(out["strategic_confidence"], 0)


if __name__ == '__main__':
    unittest.main()
