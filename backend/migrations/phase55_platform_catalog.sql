CREATE TABLE IF NOT EXISTS platform_catalog_entities (
  id SERIAL PRIMARY KEY,
  entity_name VARCHAR(128) NOT NULL,
  entity_type VARCHAR(32) NOT NULL,
  lifecycle_state VARCHAR(32) NOT NULL,
  owner VARCHAR(128) NOT NULL DEFAULT '',
  description TEXT NOT NULL DEFAULT '',
  related_phase VARCHAR(32) NOT NULL DEFAULT '',
  related_files JSONB NOT NULL DEFAULT '[]'::jsonb,
  related_apis JSONB NOT NULL DEFAULT '[]'::jsonb,
  related_frontend_page VARCHAR(128) NOT NULL DEFAULT '',
  dependencies JSONB NOT NULL DEFAULT '[]'::jsonb,
  operational_importance VARCHAR(32) NOT NULL DEFAULT 'medium',
  documentation_status VARCHAR(32) NOT NULL DEFAULT 'partial',
  human_review_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_platform_catalog_entities_name ON platform_catalog_entities(entity_name);
CREATE INDEX IF NOT EXISTS idx_platform_catalog_entities_type ON platform_catalog_entities(entity_type);
CREATE INDEX IF NOT EXISTS idx_platform_catalog_entities_lifecycle ON platform_catalog_entities(lifecycle_state);

CREATE TABLE IF NOT EXISTS capability_ownership_records (
  id SERIAL PRIMARY KEY,
  capability_name VARCHAR(128) NOT NULL,
  owner VARCHAR(128) NOT NULL DEFAULT '',
  lifecycle_state VARCHAR(32) NOT NULL DEFAULT 'active',
  ownership_status VARCHAR(32) NOT NULL DEFAULT 'clear',
  notes TEXT NOT NULL DEFAULT '',
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_capability_ownership_records_name ON capability_ownership_records(capability_name);

CREATE TABLE IF NOT EXISTS golden_path_definitions (
  id SERIAL PRIMARY KEY,
  path_name VARCHAR(128) NOT NULL,
  required_files JSONB NOT NULL DEFAULT '[]'::jsonb,
  required_tests JSONB NOT NULL DEFAULT '[]'::jsonb,
  required_readme_update BOOLEAN NOT NULL DEFAULT TRUE,
  required_router_registration BOOLEAN NOT NULL DEFAULT FALSE,
  required_migration_when_applicable BOOLEAN NOT NULL DEFAULT TRUE,
  validation_commands JSONB NOT NULL DEFAULT '[]'::jsonb,
  rollback_notes TEXT NOT NULL DEFAULT '',
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_golden_path_definitions_name ON golden_path_definitions(path_name);
