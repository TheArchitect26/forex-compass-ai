CREATE TABLE IF NOT EXISTS institutional_policies (
  id SERIAL PRIMARY KEY,
  policy_name VARCHAR(128) NOT NULL,
  policy_category VARCHAR(64) NOT NULL,
  doctrine_text TEXT NOT NULL DEFAULT '',
  non_negotiable BOOLEAN NOT NULL DEFAULT TRUE,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_institutional_policies_name ON institutional_policies(policy_name);
CREATE INDEX IF NOT EXISTS idx_institutional_policies_category ON institutional_policies(policy_category);

CREATE TABLE IF NOT EXISTS governance_doctrines (
  id SERIAL PRIMARY KEY,
  doctrine_name VARCHAR(128) NOT NULL,
  principle_summary TEXT NOT NULL DEFAULT '',
  review_obligations JSONB NOT NULL DEFAULT '[]'::jsonb,
  anti_automation_protections JSONB NOT NULL DEFAULT '[]'::jsonb,
  continuity_principles JSONB NOT NULL DEFAULT '[]'::jsonb,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_governance_doctrines_name ON governance_doctrines(doctrine_name);

CREATE TABLE IF NOT EXISTS policy_compliance_reviews (
  id SERIAL PRIMARY KEY,
  subject_name VARCHAR(128) NOT NULL,
  subject_type VARCHAR(64) NOT NULL,
  compliance_flags JSONB NOT NULL DEFAULT '{}'::jsonb,
  conflict_summary TEXT NOT NULL DEFAULT '',
  risk_severity VARCHAR(32) NOT NULL DEFAULT 'moderate',
  recommended_resolution_path JSONB NOT NULL DEFAULT '[]'::jsonb,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_policy_compliance_reviews_subject ON policy_compliance_reviews(subject_name);
