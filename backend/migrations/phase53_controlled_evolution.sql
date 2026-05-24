CREATE TABLE IF NOT EXISTS capability_lifecycle_audits (
  id SERIAL PRIMARY KEY,
  capability VARCHAR(120) NOT NULL,
  lifecycle_state VARCHAR(40) NOT NULL,
  value_evidence TEXT NOT NULL DEFAULT '',
  maintenance_burden VARCHAR(24) NOT NULL DEFAULT 'medium',
  overlap_risk VARCHAR(24) NOT NULL DEFAULT 'medium',
  maturity_level VARCHAR(24) NOT NULL DEFAULT 'active',
  recommendation TEXT NOT NULL DEFAULT '',
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_capability_lifecycle_audits_capability ON capability_lifecycle_audits(capability);

CREATE TABLE IF NOT EXISTS capability_retirement_candidates (
  id SERIAL PRIMARY KEY,
  capability VARCHAR(120) NOT NULL,
  reason TEXT NOT NULL DEFAULT '',
  burden_without_clarity BOOLEAN NOT NULL DEFAULT FALSE,
  grouped_under_control_plane BOOLEAN NOT NULL DEFAULT FALSE,
  retire_later BOOLEAN NOT NULL DEFAULT TRUE,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_capability_retirement_candidates_capability ON capability_retirement_candidates(capability);

CREATE TABLE IF NOT EXISTS controlled_evolution_plans (
  id SERIAL PRIMARY KEY,
  what_to_evolve_next JSONB NOT NULL DEFAULT '[]'::jsonb,
  what_to_freeze JSONB NOT NULL DEFAULT '[]'::jsonb,
  what_to_consolidate JSONB NOT NULL DEFAULT '[]'::jsonb,
  what_to_monitor JSONB NOT NULL DEFAULT '[]'::jsonb,
  what_to_retire_later JSONB NOT NULL DEFAULT '[]'::jsonb,
  what_not_to_touch JSONB NOT NULL DEFAULT '[]'::jsonb,
  risk_notes JSONB NOT NULL DEFAULT '[]'::jsonb,
  reversibility_notes JSONB NOT NULL DEFAULT '[]'::jsonb,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_controlled_evolution_plans_created_at ON controlled_evolution_plans(created_at);
