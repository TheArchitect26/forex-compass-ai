CREATE TABLE IF NOT EXISTS entropy_audits (
  id SERIAL PRIMARY KEY,
  entropy_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  coupling_risk_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  maintainability_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  refactor_priority_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  subsystem_drift_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  architectural_recovery_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  simplification_opportunity_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_entropy_audits_created_at ON entropy_audits(created_at);

CREATE TABLE IF NOT EXISTS refactor_recommendations (
  id SERIAL PRIMARY KEY,
  action VARCHAR(160) NOT NULL,
  expected_benefit TEXT NOT NULL DEFAULT '',
  risk_level VARCHAR(24) NOT NULL DEFAULT 'medium',
  reversibility VARCHAR(80) NOT NULL DEFAULT 'high',
  estimated_complexity VARCHAR(24) NOT NULL DEFAULT 'medium',
  affected_subsystems JSONB NOT NULL DEFAULT '[]'::jsonb,
  migration_guidance JSONB NOT NULL DEFAULT '[]'::jsonb,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_refactor_recommendations_action ON refactor_recommendations(action);

CREATE TABLE IF NOT EXISTS architectural_recovery_plans (
  id SERIAL PRIMARY KEY,
  facade_candidates JSONB NOT NULL DEFAULT '[]'::jsonb,
  consolidation_targets JSONB NOT NULL DEFAULT '[]'::jsonb,
  layering_inconsistencies JSONB NOT NULL DEFAULT '[]'::jsonb,
  unclear_boundaries JSONB NOT NULL DEFAULT '[]'::jsonb,
  maintenance_hotspots JSONB NOT NULL DEFAULT '[]'::jsonb,
  simplification_opportunities JSONB NOT NULL DEFAULT '[]'::jsonb,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_architectural_recovery_plans_created_at ON architectural_recovery_plans(created_at);
