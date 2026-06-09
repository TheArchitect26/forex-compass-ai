CREATE TABLE IF NOT EXISTS training_runs (
  id SERIAL PRIMARY KEY,
  started_at TIMESTAMP NOT NULL DEFAULT NOW(),
  completed_at TIMESTAMP NULL,
  last_scan_at TIMESTAMP NULL,
  status VARCHAR(16) NOT NULL DEFAULT 'running',
  interval_minutes INTEGER NOT NULL DEFAULT 30,
  symbols JSONB NOT NULL DEFAULT '[]'::jsonb,
  total_scans INTEGER NOT NULL DEFAULT 0,
  provider_backed_signals INTEGER NOT NULL DEFAULT 0,
  synthetic_skipped INTEGER NOT NULL DEFAULT 0,
  unavailable_skipped INTEGER NOT NULL DEFAULT 0,
  error_message TEXT NULL
);
CREATE INDEX IF NOT EXISTS idx_training_runs_started_at ON training_runs(started_at);
CREATE INDEX IF NOT EXISTS idx_training_runs_status ON training_runs(status);

CREATE TABLE IF NOT EXISTS training_signal_samples (
  id SERIAL PRIMARY KEY,
  training_run_id INTEGER NOT NULL REFERENCES training_runs(id),
  signal_id INTEGER NOT NULL UNIQUE REFERENCES signals(id),
  symbol VARCHAR(16) NOT NULL,
  direction VARCHAR(8) NOT NULL,
  data_mode VARCHAR(32) NOT NULL,
  demo_only BOOLEAN NOT NULL DEFAULT FALSE,
  execution_grade BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_training_signal_samples_run_id ON training_signal_samples(training_run_id);
CREATE INDEX IF NOT EXISTS idx_training_signal_samples_signal_id ON training_signal_samples(signal_id);
CREATE INDEX IF NOT EXISTS idx_training_signal_samples_symbol ON training_signal_samples(symbol);
CREATE INDEX IF NOT EXISTS idx_training_signal_samples_data_mode ON training_signal_samples(data_mode);
