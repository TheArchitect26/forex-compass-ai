import unittest
from app.engines.distributed_research import queue_priority, replay_checkpoint, restore_checkpoint
from app.engines.research_index import index_search
from app.engines.system_metrics import aggregate_metrics
from app.engines.recommendation_priority import prioritize_recommendation


class Phase13DistributedTests(unittest.TestCase):
    def test_queue_prioritization(self):
        self.assertGreater(queue_priority({"priority": 50, "integrity_incident": True}), 50)

    def test_replay_checkpoint_restore(self):
        cp = replay_checkpoint("2024-01-01T00:00:00", 44, {"regime": "trend"})
        restored = restore_checkpoint(cp)
        self.assertEqual(restored["steps"], 44)
        self.assertTrue(restored["resumed"])

    def test_indexing_correctness(self):
        rows = [{"id": "1", "kind": "finding", "message": "drift incident in london", "severity": "high", "regimes": ["volatile"], "profiles": ["aggressive"]}]
        out = index_search(rows, q="drift", filters={"profile": "aggressive"})
        self.assertEqual(len(out), 1)

    def test_metrics_aggregation(self):
        metrics = aggregate_metrics([
            {"status": "queued", "type": "replay_batch", "throughput": 3, "latency_ms": 50},
            {"status": "failed", "type": "ingestion_scan", "throughput": 2, "latency_ms": 100},
        ], [{"id": 1}])
        self.assertEqual(metrics["queue_backlog"], 1)
        self.assertEqual(metrics["failed_tasks"], 1)

    def test_recommendation_prioritization(self):
        out = prioritize_recommendation({"impact": 0.9, "confidence": 0.8, "reproducible": True})
        self.assertEqual(out["severity"], "critical")
        self.assertFalse(out["auto_apply"])


if __name__ == '__main__':
    unittest.main()
