CREATE TABLE IF NOT EXISTS institutional_workflows (
  id SERIAL PRIMARY KEY,
  workflow_type VARCHAR(64) NOT NULL,
  owner_operator VARCHAR(128) NOT NULL DEFAULT 'operator',
  state VARCHAR(32) NOT NULL DEFAULT 'open',
  linked_findings JSONB NOT NULL DEFAULT '[]'::jsonb,
  linked_evidence JSONB NOT NULL DEFAULT '[]'::jsonb,
  recommended_actions JSONB NOT NULL DEFAULT '[]'::jsonb,
  review_history JSONB NOT NULL DEFAULT '[]'::jsonb,
  created_at TIMESTAMP NOT NULL DEFAULT now(),
  updated_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS institutional_archives (
  id SERIAL PRIMARY KEY,
  archive_type VARCHAR(64) NOT NULL,
  title VARCHAR(180) NOT NULL,
  summary TEXT NOT NULL DEFAULT '',
  tags JSONB NOT NULL DEFAULT '[]'::jsonb,
  evidence_refs JSONB NOT NULL DEFAULT '[]'::jsonb,
  confidence DOUBLE PRECISION NOT NULL DEFAULT 0,
  created_at TIMESTAMP NOT NULL DEFAULT now()
);
