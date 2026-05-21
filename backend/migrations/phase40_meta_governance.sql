CREATE TABLE IF NOT EXISTS governance_policy_audits (
  id SERIAL PRIMARY KEY,
  governance_alignment_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  safeguard_consistency_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  policy_clarity_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  escalation_coherence_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  human_review_consistency_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  advisory_boundary_integrity_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  auditability_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  doctrine_drift_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_governance_policy_audits_created_at ON governance_policy_audits(created_at);

CREATE TABLE IF NOT EXISTS policy_conflicts (
  id SERIAL PRIMARY KEY,
  conflict_source VARCHAR(200) NOT NULL,
  contradiction TEXT NOT NULL DEFAULT '',
  affected_systems JSONB NOT NULL DEFAULT '[]'::jsonb,
  risk_if_unresolved TEXT NOT NULL DEFAULT '',
  escalation_level VARCHAR(32) NOT NULL DEFAULT 'medium',
  operator_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_policy_conflicts_source ON policy_conflicts(conflict_source);

CREATE TABLE IF NOT EXISTS safeguard_harmonization_plans (
  id SERIAL PRIMARY KEY,
  conflict_source VARCHAR(200) NOT NULL DEFAULT '',
  proposed_resolution TEXT NOT NULL DEFAULT '',
  affected_systems JSONB NOT NULL DEFAULT '[]'::jsonb,
  risk_if_unresolved TEXT NOT NULL DEFAULT '',
  reversibility VARCHAR(64) NOT NULL DEFAULT 'high',
  operator_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_safeguard_harmonization_plans_created_at ON safeguard_harmonization_plans(created_at);
