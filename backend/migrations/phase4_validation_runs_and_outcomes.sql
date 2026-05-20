CREATE TABLE IF NOT EXISTS validation_runs (
  id SERIAL PRIMARY KEY,
  started_at TIMESTAMP NOT NULL DEFAULT now(),
  completed_at TIMESTAMP NULL,
  status VARCHAR(16) NOT NULL DEFAULT 'running',
  signals_checked INTEGER NOT NULL DEFAULT 0,
  outcomes_updated INTEGER NOT NULL DEFAULT 0,
  error_message TEXT NULL
);
CREATE INDEX IF NOT EXISTS idx_validation_runs_started ON validation_runs(started_at);
CREATE INDEX IF NOT EXISTS idx_validation_runs_status ON validation_runs(status);
