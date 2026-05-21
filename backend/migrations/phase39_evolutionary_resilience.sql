CREATE TABLE IF NOT EXISTS evolution_transition_assessments (
  id SERIAL PRIMARY KEY,
  transition_readiness_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  continuity_preservation_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  migration_risk_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  rollback_readiness_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  institutional_memory_safety_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  operator_disruption_risk_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  mission_continuity_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  explainability_preservation_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_evolution_transition_assessments_created_at ON evolution_transition_assessments(created_at);

CREATE TABLE IF NOT EXISTS continuity_preservation_plans (
  id SERIAL PRIMARY KEY,
  affected_systems JSONB NOT NULL DEFAULT '[]'::jsonb,
  continuity_risks JSONB NOT NULL DEFAULT '[]'::jsonb,
  preservation_actions JSONB NOT NULL DEFAULT '[]'::jsonb,
  validation_checks JSONB NOT NULL DEFAULT '[]'::jsonb,
  rollback_notes JSONB NOT NULL DEFAULT '[]'::jsonb,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_continuity_preservation_plans_created_at ON continuity_preservation_plans(created_at);

CREATE TABLE IF NOT EXISTS rollback_readiness_plans (
  id SERIAL PRIMARY KEY,
  rollback_feasibility VARCHAR(64) NOT NULL DEFAULT 'moderate_to_high',
  reversible_changes JSONB NOT NULL DEFAULT '[]'::jsonb,
  irreversible_changes JSONB NOT NULL DEFAULT '[]'::jsonb,
  migration_checkpoints JSONB NOT NULL DEFAULT '[]'::jsonb,
  backup_requirements JSONB NOT NULL DEFAULT '[]'::jsonb,
  compatibility_risks JSONB NOT NULL DEFAULT '[]'::jsonb,
  data_loss_risks JSONB NOT NULL DEFAULT '[]'::jsonb,
  operator_review_gates JSONB NOT NULL DEFAULT '[]'::jsonb,
  rollback_readiness_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_rollback_readiness_plans_created_at ON rollback_readiness_plans(created_at);
