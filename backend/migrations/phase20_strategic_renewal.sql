CREATE TABLE IF NOT EXISTS evolution_plans (
  id SERIAL PRIMARY KEY,
  proposed_evolution VARCHAR(180) NOT NULL,
  rationale TEXT NOT NULL DEFAULT '',
  affected_systems JSONB NOT NULL DEFAULT '[]'::jsonb,
  compatibility_impact VARCHAR(32) NOT NULL DEFAULT 'low',
  replay_impact VARCHAR(32) NOT NULL DEFAULT 'low',
  governance_impact VARCHAR(32) NOT NULL DEFAULT 'medium',
  survivability_impact VARCHAR(32) NOT NULL DEFAULT 'medium',
  rollback_strategy TEXT NOT NULL DEFAULT '',
  operator_review_required BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS renewal_workflows (
  id SERIAL PRIMARY KEY,
  workflow_type VARCHAR(80) NOT NULL,
  status VARCHAR(32) NOT NULL DEFAULT 'pending_review',
  operator_reviewed BOOLEAN NOT NULL DEFAULT FALSE,
  auditable BOOLEAN NOT NULL DEFAULT TRUE,
  reproducible BOOLEAN NOT NULL DEFAULT TRUE,
  reversible BOOLEAN NOT NULL DEFAULT TRUE,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMP NOT NULL DEFAULT now()
);
