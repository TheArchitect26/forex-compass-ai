CREATE TABLE IF NOT EXISTS constitutional_rules (
  id SERIAL PRIMARY KEY,
  rule_key VARCHAR(80) NOT NULL UNIQUE,
  rule_text TEXT NOT NULL,
  enabled BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS governance_incidents (
  id SERIAL PRIMARY KEY,
  incident_type VARCHAR(80) NOT NULL,
  severity VARCHAR(32) NOT NULL,
  details JSONB NOT NULL DEFAULT '{}'::jsonb,
  resolved BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS recommendation_lifecycle (
  id SERIAL PRIMARY KEY,
  recommendation_key VARCHAR(120) NOT NULL,
  state VARCHAR(32) NOT NULL DEFAULT 'active',
  evidence_strength DOUBLE PRECISION NOT NULL DEFAULT 0.7,
  contradicted BOOLEAN NOT NULL DEFAULT FALSE,
  governance_concern BOOLEAN NOT NULL DEFAULT FALSE,
  changes JSONB NOT NULL DEFAULT '[]'::jsonb,
  created_at TIMESTAMP NOT NULL DEFAULT now(),
  updated_at TIMESTAMP NOT NULL DEFAULT now()
);
