CREATE TABLE IF NOT EXISTS reliability_history (
  id SERIAL PRIMARY KEY,
  score DOUBLE PRECISION NOT NULL,
  label VARCHAR(16) NOT NULL,
  sample_size INTEGER NOT NULL DEFAULT 0,
  win_rate DOUBLE PRECISION NOT NULL DEFAULT 0,
  avg_net_pips DOUBLE PRECISION NOT NULL DEFAULT 0,
  drift_warning TEXT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_reliability_history_created_at ON reliability_history(created_at);
