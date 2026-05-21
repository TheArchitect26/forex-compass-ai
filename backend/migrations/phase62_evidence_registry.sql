CREATE TABLE IF NOT EXISTS evidence_records (
  id SERIAL PRIMARY KEY,
  evidence_id VARCHAR(128) NOT NULL UNIQUE,
  evidence_type VARCHAR(64) NOT NULL,
  title VARCHAR(255) NOT NULL DEFAULT '',
  source_system VARCHAR(128) NOT NULL DEFAULT '',
  source_file_or_endpoint VARCHAR(255) NOT NULL DEFAULT '',
  related_policy VARCHAR(128) NOT NULL DEFAULT '',
  related_control VARCHAR(128) NOT NULL DEFAULT '',
  related_phase VARCHAR(32) NOT NULL DEFAULT '',
  related_change VARCHAR(128) NOT NULL DEFAULT '',
  related_audit_event VARCHAR(128) NOT NULL DEFAULT '',
  timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
  owner VARCHAR(128) NOT NULL DEFAULT '',
  evidence_summary TEXT NOT NULL DEFAULT '',
  confidence VARCHAR(32) NOT NULL DEFAULT 'moderate',
  freshness_status VARCHAR(32) NOT NULL DEFAULT 'fresh',
  human_review_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_evidence_records_type ON evidence_records(evidence_type);
CREATE INDEX IF NOT EXISTS idx_evidence_records_phase ON evidence_records(related_phase);

CREATE TABLE IF NOT EXISTS control_mappings (
  id SERIAL PRIMARY KEY,
  risk_to_control JSONB NOT NULL DEFAULT '[]'::jsonb,
  control_to_evidence JSONB NOT NULL DEFAULT '[]'::jsonb,
  evidence_to_policy JSONB NOT NULL DEFAULT '[]'::jsonb,
  policy_to_audit_event JSONB NOT NULL DEFAULT '[]'::jsonb,
  change_to_validation_evidence JSONB NOT NULL DEFAULT '[]'::jsonb,
  release_to_runtime_evidence JSONB NOT NULL DEFAULT '[]'::jsonb,
  pir_to_lesson_evidence JSONB NOT NULL DEFAULT '[]'::jsonb,
  human_review_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_control_mappings_created_at ON control_mappings(created_at);

CREATE TABLE IF NOT EXISTS evidence_chain_of_custody (
  id SERIAL PRIMARY KEY,
  source_origin TEXT NOT NULL DEFAULT '',
  evidence_path JSONB NOT NULL DEFAULT '[]'::jsonb,
  linked_decisions JSONB NOT NULL DEFAULT '[]'::jsonb,
  linked_policies JSONB NOT NULL DEFAULT '[]'::jsonb,
  linked_controls JSONB NOT NULL DEFAULT '[]'::jsonb,
  linked_reviews JSONB NOT NULL DEFAULT '[]'::jsonb,
  timestamp_trail JSONB NOT NULL DEFAULT '[]'::jsonb,
  gaps JSONB NOT NULL DEFAULT '[]'::jsonb,
  weak_links JSONB NOT NULL DEFAULT '[]'::jsonb,
  human_review_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_evidence_chain_of_custody_created_at ON evidence_chain_of_custody(created_at);
