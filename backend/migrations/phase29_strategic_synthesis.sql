CREATE TABLE IF NOT EXISTS synthesis_snapshots (
  id SERIAL PRIMARY KEY,
  summary JSONB NOT NULL DEFAULT '{}'::jsonb,
  top_priorities JSONB NOT NULL DEFAULT '[]'::jsonb,
  suppressed_noise JSONB NOT NULL DEFAULT '[]'::jsonb,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_synthesis_snapshots_created_at ON synthesis_snapshots(created_at);

CREATE TABLE IF NOT EXISTS synthesis_conflicts (
  id SERIAL PRIMARY KEY,
  conflict_type VARCHAR(120) NOT NULL,
  details JSONB NOT NULL DEFAULT '{}'::jsonb,
  severity VARCHAR(32) NOT NULL DEFAULT 'warning',
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_synthesis_conflicts_type ON synthesis_conflicts(conflict_type);

CREATE TABLE IF NOT EXISTS strategic_focus_decisions (
  id SERIAL PRIMARY KEY,
  focus_mode VARCHAR(80) NOT NULL,
  review_window VARCHAR(80) NOT NULL DEFAULT 'within 24 hours',
  rationale TEXT NOT NULL DEFAULT '',
  operator_approved BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_focus_decisions_mode ON strategic_focus_decisions(focus_mode);
