CREATE TABLE IF NOT EXISTS architecture_audits (
  id SERIAL PRIMARY KEY,
  audit_label VARCHAR(120) NOT NULL DEFAULT 'phase37_baseline_audit',
  subsystem_coherence DOUBLE PRECISION NOT NULL DEFAULT 0,
  api_clarity DOUBLE PRECISION NOT NULL DEFAULT 0,
  model_uniqueness DOUBLE PRECISION NOT NULL DEFAULT 0,
  terminology_consistency DOUBLE PRECISION NOT NULL DEFAULT 0,
  frontend_navigation_clarity DOUBLE PRECISION NOT NULL DEFAULT 0,
  architectural_simplicity DOUBLE PRECISION NOT NULL DEFAULT 0,
  maintenance_burden DOUBLE PRECISION NOT NULL DEFAULT 0,
  consolidation_opportunity DOUBLE PRECISION NOT NULL DEFAULT 0,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_architecture_audits_created_at ON architecture_audits(created_at);

CREATE TABLE IF NOT EXISTS subsystem_overlaps (
  id SERIAL PRIMARY KEY,
  duplicated_engine_responsibilities JSONB NOT NULL DEFAULT '[]'::jsonb,
  overlapping_apis JSONB NOT NULL DEFAULT '[]'::jsonb,
  repeated_governance_logic JSONB NOT NULL DEFAULT '[]'::jsonb,
  similar_scoring_systems JSONB NOT NULL DEFAULT '[]'::jsonb,
  stale_consoles JSONB NOT NULL DEFAULT '[]'::jsonb,
  unused_workflows JSONB NOT NULL DEFAULT '[]'::jsonb,
  fragmented_terminology JSONB NOT NULL DEFAULT '[]'::jsonb,
  model_table_overlap JSONB NOT NULL DEFAULT '[]'::jsonb,
  redundant_memory_systems JSONB NOT NULL DEFAULT '[]'::jsonb,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_subsystem_overlaps_created_at ON subsystem_overlaps(created_at);

CREATE TABLE IF NOT EXISTS consolidation_proposals (
  id SERIAL PRIMARY KEY,
  benefits JSONB NOT NULL DEFAULT '[]'::jsonb,
  risks JSONB NOT NULL DEFAULT '[]'::jsonb,
  migration_needs JSONB NOT NULL DEFAULT '[]'::jsonb,
  reversibility VARCHAR(80) NOT NULL DEFAULT 'high with phased rollout',
  affected_files JSONB NOT NULL DEFAULT '[]'::jsonb,
  proposals JSONB NOT NULL DEFAULT '[]'::jsonb,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_consolidation_proposals_created_at ON consolidation_proposals(created_at);
