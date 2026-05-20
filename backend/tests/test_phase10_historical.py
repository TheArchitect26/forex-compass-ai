import unittest
from datetime import datetime, timezone, timedelta
from backend.app.engines.historical import malformed_ohlc, detect_gaps, normalize_pair, normalize_timeframe, integrity_score


class Phase10HistoricalTests(unittest.TestCase):
    def test_pair_timeframe_normalization(self):
        self.assertEqual(normalize_pair('eurusd'), 'EUR/USD')
        self.assertEqual(normalize_timeframe('bad'), '1h')

    def test_malformed_ohlc_detection(self):
        self.assertTrue(malformed_ohlc(1, 0.9, 1.1, 1))
        self.assertFalse(malformed_ohlc(1, 1.2, 0.8, 1.1))

    def test_gap_detection(self):
        ts = [datetime(2026,1,1,0,0,tzinfo=timezone.utc), datetime(2026,1,1,1,0,tzinfo=timezone.utc), datetime(2026,1,1,4,0,tzinfo=timezone.utc)]
        self.assertGreaterEqual(detect_gaps(ts, '1h'), 1)

    def test_integrity_score_bounds(self):
        s = integrity_score(100, 2, 1, 0, 0.1)
        self.assertTrue(0 <= s <= 100)


if __name__ == '__main__':
    unittest.main()
