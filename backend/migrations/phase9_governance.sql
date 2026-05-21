CREATE TABLE IF NOT EXISTS version_registry (
  id SERIAL PRIMARY KEY,
  engine_version VARCHAR(32) NOT NULL,
  weighting_version VARCHAR(32) NOT NULL,
  calibration_version VARCHAR(32) NOT NULL,
  adaptation_version VARCHAR(32) NOT NULL,
  discipline_version VARCHAR(32) NOT NULL,
  active BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMP NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS experiment_runs (
  id SERIAL PRIMARY KEY,
  experiment_id VARCHAR(64) NOT NULL UNIQUE,
  name VARCHAR(128) NOT NULL,
  description TEXT NOT NULL DEFAULT '',
  status VARCHAR(16) NOT NULL DEFAULT 'draft',
  target_logic_area VARCHAR(64) NOT NULL DEFAULT '',
  baseline_version VARCHAR(64) NOT NULL DEFAULT '',
  candidate_version VARCHAR(64) NOT NULL DEFAULT '',
  metrics_summary JSONB NOT NULL DEFAULT '{}'::jsonb,
  rollback_status VARCHAR(32) NOT NULL DEFAULT 'none',
  dataset_used VARCHAR(64) NOT NULL DEFAULT '',
  config_snapshot JSONB NOT NULL DEFAULT '{}'::jsonb,
  strategy_profile VARCHAR(32) NOT NULL DEFAULT '',
  regime_conditions JSONB NOT NULL DEFAULT '{}'::jsonb,
  replay_metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  comparison_results JSONB NOT NULL DEFAULT '{}'::jsonb,
  regression_analysis JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMP NOT NULL DEFAULT now()
);
