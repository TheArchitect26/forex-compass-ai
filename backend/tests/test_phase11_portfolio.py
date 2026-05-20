import unittest
from backend.app.engines.portfolio import estimate_position_size, correlation_bucket, compute_metrics


class Phase11PortfolioTests(unittest.TestCase):
    def test_position_sizing_modes(self):
        a = estimate_position_size('fixed_lot', 10000, 60, 0.005)
        b = estimate_position_size('confidence_adjusted', 10000, 80, 0.005)
        self.assertNotEqual(a, b)

    def test_correlation_warning(self):
        self.assertEqual(correlation_bucket('EUR/USD', 'GBP/USD'), 'positive')

    def test_drawdown_metric(self):
        m = compute_metrics([10000, 10050, 9900, 10100])
        self.assertGreaterEqual(m['max_drawdown'], 0)

    def test_replay_realism_assumption(self):
        # deterministic function output for same input
        m1 = compute_metrics([10000, 9990, 10020])
        m2 = compute_metrics([10000, 9990, 10020])
        self.assertEqual(m1, m2)


if __name__ == '__main__':
    unittest.main()
