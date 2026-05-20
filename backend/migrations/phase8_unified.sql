CREATE TABLE IF NOT EXISTS maintenance_runs (
  id SERIAL PRIMARY KEY,
  job_type VARCHAR(64) NOT NULL,
  started_at TIMESTAMP NOT NULL DEFAULT now(),
  completed_at TIMESTAMP NULL,
  status VARCHAR(16) NOT NULL DEFAULT 'running',
  rows_cleaned INTEGER NOT NULL DEFAULT 0,
  warnings_errors TEXT NULL
);
