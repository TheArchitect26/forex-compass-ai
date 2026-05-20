CREATE TABLE IF NOT EXISTS evolution_lineage (
  id SERIAL PRIMARY KEY,
  changed_component VARCHAR(120) NOT NULL,
  why TEXT NOT NULL DEFAULT '',
  expected_impact TEXT NOT NULL DEFAULT '',
  affected_assumptions JSONB NOT NULL DEFAULT '[]'::jsonb,
  affected_narratives JSONB NOT NULL DEFAULT '[]'::jsonb,
  affected_replay_validity JSONB NOT NULL DEFAULT '[]'::jsonb,
  compatibility_notes TEXT NOT NULL DEFAULT '',
  created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS institutional_migrations (
  id SERIAL PRIMARY KEY,
  target VARCHAR(80) NOT NULL,
  plan JSONB NOT NULL DEFAULT '{}'::jsonb,
  reversible BOOLEAN NOT NULL DEFAULT TRUE,
  operator_approved BOOLEAN NOT NULL DEFAULT FALSE,
  status VARCHAR(32) NOT NULL DEFAULT 'pending_approval',
  created_at TIMESTAMP NOT NULL DEFAULT now()
);
