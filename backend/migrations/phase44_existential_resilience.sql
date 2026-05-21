CREATE TABLE IF NOT EXISTS crisis_resilience_audits (
  id SERIAL PRIMARY KEY,
  existential_resilience_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  crisis_continuity_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  shock_absorption_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  mission_survival_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  governance_continuity_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  operator_sustainability_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  data_survivability_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  recovery_readiness_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_crisis_resilience_audits_created_at ON crisis_resilience_audits(created_at);

CREATE TABLE IF NOT EXISTS continuity_crisis_plans (
  id SERIAL PRIMARY KEY,
  crisis_type VARCHAR(120) NOT NULL DEFAULT '',
  affected_systems JSONB NOT NULL DEFAULT '[]'::jsonb,
  critical_systems_to_preserve JSONB NOT NULL DEFAULT '[]'::jsonb,
  systems_to_pause JSONB NOT NULL DEFAULT '[]'::jsonb,
  minimum_viable_operating_mode JSONB NOT NULL DEFAULT '[]'::jsonb,
  recovery_sequence JSONB NOT NULL DEFAULT '[]'::jsonb,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_continuity_crisis_plans_created_at ON continuity_crisis_plans(created_at);

CREATE TABLE IF NOT EXISTS black_swan_reviews (
  id SERIAL PRIMARY KEY,
  assumptions_invalidated_by_shock JSONB NOT NULL DEFAULT '[]'::jsonb,
  overreliance_on_normal_conditions JSONB NOT NULL DEFAULT '[]'::jsonb,
  false_certainty_under_extreme_uncertainty JSONB NOT NULL DEFAULT '[]'::jsonb,
  fragile_dependencies JSONB NOT NULL DEFAULT '[]'::jsonb,
  crisis_time_governance_contradictions JSONB NOT NULL DEFAULT '[]'::jsonb,
  crisis_alert_overload JSONB NOT NULL DEFAULT '[]'::jsonb,
  loss_of_operator_clarity JSONB NOT NULL DEFAULT '[]'::jsonb,
  risk_of_overreaction JSONB NOT NULL DEFAULT '[]'::jsonb,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_black_swan_reviews_created_at ON black_swan_reviews(created_at);
