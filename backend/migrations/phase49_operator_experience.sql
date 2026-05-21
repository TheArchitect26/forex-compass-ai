CREATE TABLE IF NOT EXISTS operator_experience_audits (
  id SERIAL PRIMARY KEY,
  operator_experience_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  usability_clarity_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  navigation_simplicity_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  readability_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  actionability_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  warning_fatigue_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  mobile_usability_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  interface_coherence_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_operator_experience_audits_created_at ON operator_experience_audits(created_at);

CREATE TABLE IF NOT EXISTS usability_issues (
  id SERIAL PRIMARY KEY,
  issue_category VARCHAR(80) NOT NULL,
  severity VARCHAR(24) NOT NULL DEFAULT 'medium',
  affected_surfaces JSONB NOT NULL DEFAULT '[]'::jsonb,
  issue_description TEXT NOT NULL DEFAULT '',
  recommended_fix TEXT NOT NULL DEFAULT '',
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_usability_issues_category ON usability_issues(issue_category);

CREATE TABLE IF NOT EXISTS interface_simplification_plans (
  id SERIAL PRIMARY KEY,
  recommendations JSONB NOT NULL DEFAULT '[]'::jsonb,
  daily_use_pathway JSONB NOT NULL DEFAULT '[]'::jsonb,
  maintenance_view_outline JSONB NOT NULL DEFAULT '[]'::jsonb,
  crisis_view_outline JSONB NOT NULL DEFAULT '[]'::jsonb,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_interface_simplification_plans_created_at ON interface_simplification_plans(created_at);
