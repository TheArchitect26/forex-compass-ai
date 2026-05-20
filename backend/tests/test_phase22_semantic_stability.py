import unittest
from app.engines.semantic_stability import (
    detect_meaning_conflicts,
    concept_lineage_entry,
    orientation_score,
    stabilize_narratives,
    comprehension_safeguards,
    orientation,
)


class Phase22SemanticStabilityTests(unittest.TestCase):
    def test_semantic_conflict_detection(self):
        out = detect_meaning_conflicts([
            {"term": "risk envelope", "meaning": "max risk per cluster"},
            {"term": "risk envelope", "meaning": "max risk per position"},
        ])
        self.assertGreaterEqual(len(out["conflicts"]), 1)

    def test_concept_lineage_consistency(self):
        out = concept_lineage_entry({"concept": "governance drift", "origin": "phase16"})
        self.assertEqual(out["concept"], "governance drift")
        self.assertTrue(out["created_at"])

    def test_orientation_scoring(self):
        out = orientation_score({"semantic_coherence": 0.9})
        self.assertGreater(out["semantic_coherence_score"], 0)

    def test_narrative_stabilization(self):
        out = stabilize_narratives([
            {"id": 1, "title": "A"},
            {"id": 2, "title": "A", "stale": True},
        ])
        self.assertEqual(len(out["consolidated_narratives"]), 1)
        self.assertFalse(out["irreversible_delete_applied"])

    def test_comprehension_safeguard_escalation(self):
        out = comprehension_safeguards({"abstraction_layers": 6, "terminology_overload": 0.7})
        self.assertGreaterEqual(len(out["flags"]), 1)

    def test_glossary_governance_basics(self):
        out = orientation({"constant_principles": ["human sovereignty"]})
        self.assertIn("constant_principles", out)

    def test_terminology_drift_detection(self):
        out = detect_meaning_conflicts([
            {"term": "compatibility mode", "meaning": "legacy adapter active"},
            {"term": "compatibility mode", "meaning": "modern mode with no adapter"},
        ])
        self.assertEqual(out["conflicts"][0]["type"], "contradictory_terminology")


if __name__ == '__main__':
    unittest.main()
