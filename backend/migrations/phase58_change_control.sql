CREATE TABLE IF NOT EXISTS change_impact_assessments (
  id SERIAL PRIMARY KEY,
  change_type VARCHAR(64) NOT NULL,
  change_summary TEXT NOT NULL DEFAULT '',
  affected_systems JSONB NOT NULL DEFAULT '[]'::jsonb,
  affected_files JSONB NOT NULL DEFAULT '[]'::jsonb,
  risk_level VARCHAR(32) NOT NULL DEFAULT 'moderate',
  scores JSONB NOT NULL DEFAULT '{}'::jsonb,
  required_human_reviewers JSONB NOT NULL DEFAULT '[]'::jsonb,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_change_impact_assessments_type ON change_impact_assessments(change_type);

CREATE TABLE IF NOT EXISTS change_review_requirements (
  id SERIAL PRIMARY KEY,
  change_type VARCHAR(64) NOT NULL,
  review_flags JSONB NOT NULL DEFAULT '{}'::jsonb,
  rationale TEXT NOT NULL DEFAULT '',
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_change_review_requirements_type ON change_review_requirements(change_type);

CREATE TABLE IF NOT EXISTS change_approval_briefs (
  id SERIAL PRIMARY KEY,
  change_summary TEXT NOT NULL DEFAULT '',
  reason_for_change TEXT NOT NULL DEFAULT '',
  expected_benefit TEXT NOT NULL DEFAULT '',
  risk_if_approved TEXT NOT NULL DEFAULT '',
  risk_if_rejected TEXT NOT NULL DEFAULT '',
  validation_plan JSONB NOT NULL DEFAULT '[]'::jsonb,
  rollback_plan JSONB NOT NULL DEFAULT '[]'::jsonb,
  open_questions JSONB NOT NULL DEFAULT '[]'::jsonb,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_change_approval_briefs_created_at ON change_approval_briefs(created_at);
