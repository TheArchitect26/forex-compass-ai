import unittest
from app.engines.epistemic_integrity import (
    evaluate_epistemic_integrity,
    detect_knowledge_fragmentation,
    assumption_decay,
    archive_stabilization,
    lifecycle_review_gate,
)


class Phase17EpistemicIntegrityTests(unittest.TestCase):
    def test_contradiction_detection(self):
        out = evaluate_epistemic_integrity({"contradiction_density": 0.8, "unsupported_narrative_risk": 0.7})
        self.assertLess(out["epistemic_integrity"], 70)
        self.assertGreater(out["contradiction_pressure"], 40)

    def test_assumption_confidence_decay(self):
        decayed = assumption_decay(0.85, 120, 0.3, 3)
        self.assertLess(decayed, 0.85)

    def test_coherence_scoring(self):
        scores = evaluate_epistemic_integrity({"evidence_quality": 0.9, "evidence_freshness": 0.9, "contradiction_density": 0.1})
        self.assertIn("institutional_coherence", scores)

    def test_stale_evidence_handling(self):
        scores = evaluate_epistemic_integrity({"evidence_freshness": 0.2, "stale_assumptions": 0.8})
        self.assertLess(scores["evidence_freshness"], 50)

    def test_archive_stabilization(self):
        out = archive_stabilization([
            {"id": 1, "title": "A", "archive_type": "briefing"},
            {"id": 2, "title": "A", "archive_type": "briefing", "conflicts_with": [1]},
        ])
        self.assertIn(2, out["duplicate_narratives"])
        self.assertIn(2, out["conflicting_archives"])

    def test_fragmented_knowledge_detection(self):
        out = detect_knowledge_fragmentation(
            [{"id": "a"}, {"id": "b"}, {"id": "c"}],
            [{"source": "a", "target": "b", "relation": "supports", "resolved": True}],
        )
        self.assertIn("c", out["isolated_conclusions"])

    def test_governance_review_workflow_integrity(self):
        gate = lifecycle_review_gate({"review_type": "narrative_change"})
        self.assertTrue(gate["requires_operator_review"])
        self.assertFalse(gate["auto_apply"])


if __name__ == '__main__':
    unittest.main()
