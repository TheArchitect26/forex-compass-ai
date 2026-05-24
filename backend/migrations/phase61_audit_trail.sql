CREATE TABLE IF NOT EXISTS institutional_audit_events (
  id SERIAL PRIMARY KEY,
  what_decided_or_recommended TEXT NOT NULL DEFAULT '',
  why_produced TEXT NOT NULL DEFAULT '',
  source_systems JSONB NOT NULL DEFAULT '[]'::jsonb,
  evidence_used JSONB NOT NULL DEFAULT '[]'::jsonb,
  assumptions JSONB NOT NULL DEFAULT '[]'::jsonb,
  policy_references JSONB NOT NULL DEFAULT '[]'::jsonb,
  related_phase VARCHAR(32) NOT NULL DEFAULT '',
  affected_capability VARCHAR(128) NOT NULL DEFAULT '',
  human_reviewer_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_institutional_audit_events_phase ON institutional_audit_events(related_phase);

CREATE TABLE IF NOT EXISTS decision_provenance_records (
  id SERIAL PRIMARY KEY,
  decision_id VARCHAR(128) NOT NULL,
  recommendation_source JSONB NOT NULL DEFAULT '[]'::jsonb,
  review_inputs JSONB NOT NULL DEFAULT '[]'::jsonb,
  scorecard_evidence JSONB NOT NULL DEFAULT '[]'::jsonb,
  change_control_rationale TEXT NOT NULL DEFAULT '',
  post_implementation_lessons JSONB NOT NULL DEFAULT '[]'::jsonb,
  approval_assumptions JSONB NOT NULL DEFAULT '[]'::jsonb,
  governance_conflicts JSONB NOT NULL DEFAULT '[]'::jsonb,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_decision_provenance_records_decision_id ON decision_provenance_records(decision_id);

CREATE TABLE IF NOT EXISTS governance_lineage_records (
  id SERIAL PRIMARY KEY,
  lineage_summary TEXT NOT NULL DEFAULT '',
  policy_references JSONB NOT NULL DEFAULT '[]'::jsonb,
  related_reviews JSONB NOT NULL DEFAULT '[]'::jsonb,
  conflict_visibility VARCHAR(32) NOT NULL DEFAULT 'visible',
  human_review_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_governance_lineage_records_created_at ON governance_lineage_records(created_at);
