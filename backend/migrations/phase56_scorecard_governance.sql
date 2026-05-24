CREATE TABLE IF NOT EXISTS capability_scorecards (
  id SERIAL PRIMARY KEY,
  capability_name VARCHAR(128) NOT NULL,
  entity_type VARCHAR(32) NOT NULL DEFAULT 'engine',
  overall_score DOUBLE PRECISION NOT NULL DEFAULT 0.0,
  category_scores JSONB NOT NULL DEFAULT '{}'::jsonb,
  pass_fail_status VARCHAR(32) NOT NULL DEFAULT 'conditional_pass',
  readiness_level VARCHAR(32) NOT NULL DEFAULT 'developing',
  evidence_strength VARCHAR(32) NOT NULL DEFAULT 'moderate',
  gap_severity VARCHAR(32) NOT NULL DEFAULT 'moderate',
  improvement_priority VARCHAR(32) NOT NULL DEFAULT 'high',
  human_review_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_capability_scorecards_name ON capability_scorecards(capability_name);

CREATE TABLE IF NOT EXISTS scorecard_findings (
  id SERIAL PRIMARY KEY,
  capability_name VARCHAR(128) NOT NULL,
  finding_type VARCHAR(64) NOT NULL,
  severity VARCHAR(32) NOT NULL DEFAULT 'moderate',
  evidence TEXT NOT NULL DEFAULT '',
  recommended_action TEXT NOT NULL DEFAULT '',
  human_review_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_scorecard_findings_capability ON scorecard_findings(capability_name);
CREATE INDEX IF NOT EXISTS idx_scorecard_findings_type ON scorecard_findings(finding_type);

CREATE TABLE IF NOT EXISTS readiness_gate_reviews (
  id SERIAL PRIMARY KEY,
  capability_name VARCHAR(128) NOT NULL,
  gate_results JSONB NOT NULL DEFAULT '{}'::jsonb,
  validation_commands JSONB NOT NULL DEFAULT '[]'::jsonb,
  review_summary TEXT NOT NULL DEFAULT '',
  human_review_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_readiness_gate_reviews_capability ON readiness_gate_reviews(capability_name);
