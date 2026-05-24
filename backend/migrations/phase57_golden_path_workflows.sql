CREATE TABLE IF NOT EXISTS golden_path_workflows (
  id SERIAL PRIMARY KEY,
  workflow_name VARCHAR(128) NOT NULL,
  workflow_type VARCHAR(64) NOT NULL,
  guided_steps JSONB NOT NULL DEFAULT '[]'::jsonb,
  workflow_scores JSONB NOT NULL DEFAULT '{}'::jsonb,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_golden_path_workflows_name ON golden_path_workflows(workflow_name);
CREATE INDEX IF NOT EXISTS idx_golden_path_workflows_type ON golden_path_workflows(workflow_type);

CREATE TABLE IF NOT EXISTS golden_path_checklists (
  id SERIAL PRIMARY KEY,
  workflow_name VARCHAR(128) NOT NULL,
  required_files JSONB NOT NULL DEFAULT '[]'::jsonb,
  required_tests JSONB NOT NULL DEFAULT '[]'::jsonb,
  validation_commands JSONB NOT NULL DEFAULT '[]'::jsonb,
  rollback_notes TEXT NOT NULL DEFAULT '',
  scorecard_checks JSONB NOT NULL DEFAULT '[]'::jsonb,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_golden_path_checklists_name ON golden_path_checklists(workflow_name);

CREATE TABLE IF NOT EXISTS golden_path_deviation_reviews (
  id SERIAL PRIMARY KEY,
  workflow_name VARCHAR(128) NOT NULL,
  deviation_reason TEXT NOT NULL DEFAULT '',
  risk_introduced VARCHAR(32) NOT NULL DEFAULT 'moderate',
  affected_standards JSONB NOT NULL DEFAULT '[]'::jsonb,
  compensating_controls JSONB NOT NULL DEFAULT '[]'::jsonb,
  rollback_recovery_notes TEXT NOT NULL DEFAULT '',
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_golden_path_deviation_reviews_name ON golden_path_deviation_reviews(workflow_name);
