CREATE TABLE IF NOT EXISTS signal_outcomes (
  id SERIAL PRIMARY KEY,
  signal_id INTEGER UNIQUE NOT NULL REFERENCES signals(id),
  pair VARCHAR(16) NOT NULL,
  timeframe VARCHAR(8) NOT NULL,
  direction VARCHAR(8) NOT NULL,
  entry_price DOUBLE PRECISION NOT NULL,
  stop_loss DOUBLE PRECISION NOT NULL,
  take_profit DOUBLE PRECISION NOT NULL,
  invalidation_price DOUBLE PRECISION NOT NULL,
  outcome VARCHAR(16) NOT NULL DEFAULT 'pending',
  max_favorable_move DOUBLE PRECISION NOT NULL DEFAULT 0.0,
  max_adverse_move DOUBLE PRECISION NOT NULL DEFAULT 0.0,
  result_pips DOUBLE PRECISION NOT NULL DEFAULT 0.0,
  checked_at TIMESTAMP NULL,
  created_at TIMESTAMP NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_signal_outcomes_outcome ON signal_outcomes(outcome);
CREATE INDEX IF NOT EXISTS idx_signal_outcomes_pair ON signal_outcomes(pair);
CREATE INDEX IF NOT EXISTS idx_signal_outcomes_timeframe ON signal_outcomes(timeframe);
