CREATE TABLE IF NOT EXISTS historical_candles (
  id SERIAL PRIMARY KEY,
  pair VARCHAR(16) NOT NULL,
  timeframe VARCHAR(8) NOT NULL,
  timestamp TIMESTAMP NOT NULL,
  open DOUBLE PRECISION NOT NULL,
  high DOUBLE PRECISION NOT NULL,
  low DOUBLE PRECISION NOT NULL,
  close DOUBLE PRECISION NOT NULL,
  volume DOUBLE PRECISION NOT NULL DEFAULT 0,
  source VARCHAR(32) NOT NULL DEFAULT 'twelve_data',
  integrity_flags JSONB NOT NULL DEFAULT '{}'::jsonb,
  dataset_version VARCHAR(32) NOT NULL DEFAULT 'ds-v1',
  created_at TIMESTAMP NOT NULL DEFAULT now()
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_hc_unique ON historical_candles(pair, timeframe, timestamp);
CREATE TABLE IF NOT EXISTS ingestion_runs (
  id SERIAL PRIMARY KEY,
  pair VARCHAR(16) NOT NULL,
  timeframe VARCHAR(8) NOT NULL,
  source VARCHAR(32) NOT NULL DEFAULT 'twelve_data',
  candles_fetched INTEGER NOT NULL DEFAULT 0,
  candles_inserted INTEGER NOT NULL DEFAULT 0,
  gaps_detected INTEGER NOT NULL DEFAULT 0,
  malformed_rows INTEGER NOT NULL DEFAULT 0,
  retries INTEGER NOT NULL DEFAULT 0,
  source_reliability DOUBLE PRECISION NOT NULL DEFAULT 0,
  status VARCHAR(16) NOT NULL DEFAULT 'completed',
  created_at TIMESTAMP NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS replay_sessions (
  id SERIAL PRIMARY KEY,
  pair VARCHAR(16) NOT NULL,
  timeframe VARCHAR(8) NOT NULL,
  strategy_profile VARCHAR(32) NOT NULL DEFAULT 'intraday',
  start_ts TIMESTAMP NOT NULL,
  end_ts TIMESTAMP NOT NULL,
  cursor_ts TIMESTAMP NULL,
  steps INTEGER NOT NULL DEFAULT 0,
  state JSONB NOT NULL DEFAULT '{}'::jsonb,
  status VARCHAR(16) NOT NULL DEFAULT 'running',
  dataset_snapshot VARCHAR(64) NOT NULL DEFAULT 'ds-v1',
  created_at TIMESTAMP NOT NULL DEFAULT now()
);
