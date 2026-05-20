CREATE TABLE IF NOT EXISTS research_tasks (
  id SERIAL PRIMARY KEY,
  task_type VARCHAR(64) NOT NULL,
  status VARCHAR(16) NOT NULL DEFAULT 'pending',
  priority VARCHAR(16) NOT NULL DEFAULT 'normal',
  triggered_by VARCHAR(64) NOT NULL DEFAULT 'manual',
  linked_datasets JSONB NOT NULL DEFAULT '[]'::jsonb,
  linked_experiments JSONB NOT NULL DEFAULT '[]'::jsonb,
  linked_replay_sessions JSONB NOT NULL DEFAULT '[]'::jsonb,
  findings_summary TEXT NOT NULL DEFAULT '',
  warnings JSONB NOT NULL DEFAULT '[]'::jsonb,
  recommendations JSONB NOT NULL DEFAULT '[]'::jsonb,
  evidence JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMP NOT NULL DEFAULT now(),
  completed_at TIMESTAMP NULL
);

CREATE TABLE IF NOT EXISTS research_findings (
  id SERIAL PRIMARY KEY,
  message TEXT NOT NULL,
  confidence DOUBLE PRECISION NOT NULL DEFAULT 0,
  affected_regimes JSONB NOT NULL DEFAULT '[]'::jsonb,
  affected_profiles JSONB NOT NULL DEFAULT '[]'::jsonb,
  evidence_refs JSONB NOT NULL DEFAULT '[]'::jsonb,
  reproducible BOOLEAN NOT NULL DEFAULT TRUE,
  triggered_by_task_id INTEGER NULL REFERENCES research_tasks(id),
  created_at TIMESTAMP NOT NULL DEFAULT now()
);
