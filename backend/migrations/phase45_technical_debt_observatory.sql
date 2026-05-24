CREATE TABLE IF NOT EXISTS technical_debt_audits (
  id SERIAL PRIMARY KEY,
  technical_debt_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  maintainability_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  build_fragility_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  dependency_risk_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  migration_burden_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  test_confidence_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  refactor_urgency_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  debt_paydown_priority_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_technical_debt_audits_created_at ON technical_debt_audits(created_at);

CREATE TABLE IF NOT EXISTS debt_items (
  id SERIAL PRIMARY KEY,
  category VARCHAR(40) NOT NULL,
  severity VARCHAR(24) NOT NULL DEFAULT 'medium',
  affected_files JSONB NOT NULL DEFAULT '[]'::jsonb,
  impact TEXT NOT NULL DEFAULT '',
  estimated_effort VARCHAR(24) NOT NULL DEFAULT 'medium',
  risk_if_ignored TEXT NOT NULL DEFAULT '',
  recommended_owner_action TEXT NOT NULL DEFAULT '',
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_debt_items_category ON debt_items(category);

CREATE TABLE IF NOT EXISTS debt_paydown_plans (
  id SERIAL PRIMARY KEY,
  paydown_actions JSONB NOT NULL DEFAULT '[]'::jsonb,
  recommended_timeline JSONB NOT NULL DEFAULT '[]'::jsonb,
  owners JSONB NOT NULL DEFAULT '[]'::jsonb,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_debt_paydown_plans_created_at ON debt_paydown_plans(created_at);
