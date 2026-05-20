CREATE TABLE IF NOT EXISTS strategy_state (
  id SERIAL PRIMARY KEY,
  active_profile VARCHAR(32) NOT NULL UNIQUE,
  source VARCHAR(16) NOT NULL DEFAULT 'default',
  updated_at TIMESTAMP NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS explainability_audit (
  id SERIAL PRIMARY KEY,
  timestamp TIMESTAMP NOT NULL DEFAULT now(),
  pair VARCHAR(16) NOT NULL,
  timeframe VARCHAR(8) NOT NULL,
  regime VARCHAR(32) NOT NULL,
  strategy_profile VARCHAR(32) NOT NULL,
  signal_decision VARCHAR(8) NOT NULL,
  confidence_before DOUBLE PRECISION NOT NULL,
  confidence_after DOUBLE PRECISION NOT NULL,
  adaptive_changes JSONB NOT NULL DEFAULT '{}'::jsonb,
  drift_warnings JSONB NOT NULL DEFAULT '[]'::jsonb,
  reasons TEXT NOT NULL DEFAULT ''
);
