import unittest
from app.engines.constitutional_governance import (
    validate_consistency,
    confidence_decay,
    explainability_score,
    trust_pressure,
    recommendation_with_trust_fields,
)


class Phase16ConstitutionalGovernanceTests(unittest.TestCase):
    def test_consistency_validation(self):
        out = validate_consistency({
            "narratives": ["reliability increased", "reliability decreased"],
            "recommendations": [{"recommendation": "increase risk"}, {"recommendation": "reduce exposure"}],
            "confidence_hierarchy": {"raw_signal_confidence": 0.5, "strategic_confidence": 0.9},
            "rules_checked": [{"rule": "no autonomous execution", "status": "ok"}],
        })
        self.assertFalse(out["ok"])
        self.assertIn("contradictory_narratives", out["contradictions"])

    def test_confidence_decay(self):
        self.assertLess(confidence_decay(0.9, 100, 2, 30), 0.9)

    def test_explainability_score(self):
        s = explainability_score({"evidence_completeness": 0.8, "reproducibility_coverage": 0.8, "narrative_consistency": 0.8, "recommendation_traceability": 0.8, "audit_completeness": 0.8, "governance_compliance": 0.8})
        self.assertGreaterEqual(s["score"], 0)

    def test_trust_pressure_escalation(self):
        t = trust_pressure({"unresolved_contradictions": 2, "confidence_inflation": 1, "critical_drift_unresolved": 1})
        self.assertIn(t["level"], {"elevated", "high"})

    def test_recommendation_enrichment(self):
        r = recommendation_with_trust_fields({"recommendation": "increase aggressiveness", "evidence_coverage": 0.4, "reproducibility_status": "unverified"})
        self.assertTrue(r["speculative"])
        self.assertTrue(r["weak_evidence"])


if __name__ == '__main__':
    unittest.main()
