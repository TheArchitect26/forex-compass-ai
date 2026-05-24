CREATE TABLE IF NOT EXISTS feature_flag_audits (
  id SERIAL PRIMARY KEY,
  audit_name VARCHAR(128) NOT NULL DEFAULT 'phase54_feature_flag_governance',
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_feature_flag_audits_created_at ON feature_flag_audits(created_at);

CREATE TABLE IF NOT EXISTS feature_flag_registry_items (
  id SERIAL PRIMARY KEY,
  flag_name VARCHAR(128) NOT NULL,
  lifecycle_state VARCHAR(32) NOT NULL,
  capability_controlled VARCHAR(255) NOT NULL DEFAULT '',
  owner VARCHAR(128) NOT NULL DEFAULT '',
  intended_lifespan_days INTEGER NOT NULL DEFAULT 30,
  cleanup_due_at TIMESTAMP NULL,
  affected_systems JSONB NOT NULL DEFAULT '[]'::jsonb,
  default_state VARCHAR(16) NOT NULL DEFAULT 'off',
  rollback_role VARCHAR(255) NOT NULL DEFAULT '',
  operator_visibility VARCHAR(32) NOT NULL DEFAULT 'medium',
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_feature_flag_registry_items_flag_name ON feature_flag_registry_items(flag_name);
CREATE INDEX IF NOT EXISTS idx_feature_flag_registry_items_lifecycle_state ON feature_flag_registry_items(lifecycle_state);
CREATE INDEX IF NOT EXISTS idx_feature_flag_registry_items_cleanup_due_at ON feature_flag_registry_items(cleanup_due_at);

CREATE TABLE IF NOT EXISTS feature_flag_cleanup_plans (
  id SERIAL PRIMARY KEY,
  flag_name VARCHAR(128) NOT NULL,
  lifecycle_state VARCHAR(32) NOT NULL,
  capability_controlled VARCHAR(255) NOT NULL DEFAULT '',
  owner VARCHAR(128) NOT NULL DEFAULT '',
  intended_lifespan_days INTEGER NOT NULL DEFAULT 30,
  cleanup_due_at TIMESTAMP NULL,
  affected_systems JSONB NOT NULL DEFAULT '[]'::jsonb,
  default_state VARCHAR(16) NOT NULL DEFAULT 'off',
  rollback_role VARCHAR(255) NOT NULL DEFAULT '',
  operator_visibility VARCHAR(32) NOT NULL DEFAULT 'medium',
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_feature_flag_cleanup_plans_flag_name ON feature_flag_cleanup_plans(flag_name);
CREATE INDEX IF NOT EXISTS idx_feature_flag_cleanup_plans_lifecycle_state ON feature_flag_cleanup_plans(lifecycle_state);
CREATE INDEX IF NOT EXISTS idx_feature_flag_cleanup_plans_cleanup_due_at ON feature_flag_cleanup_plans(cleanup_due_at);
