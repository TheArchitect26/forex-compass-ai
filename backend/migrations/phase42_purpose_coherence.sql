CREATE TABLE IF NOT EXISTS purpose_coherence_audits (
  id SERIAL PRIMARY KEY,
  purpose_coherence_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  mission_alignment_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  meaning_preservation_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  anti_hollowing_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  usefulness_to_complexity_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  operator_purpose_alignment_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  doctrine_embodiment_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  strategic_authenticity_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_purpose_coherence_audits_created_at ON purpose_coherence_audits(created_at);

CREATE TABLE IF NOT EXISTS meaning_drift_signals (
  id SERIAL PRIMARY KEY,
  signal_type VARCHAR(120) NOT NULL,
  signal_description TEXT NOT NULL DEFAULT '',
  affected_systems JSONB NOT NULL DEFAULT '[]'::jsonb,
  drift_severity VARCHAR(24) NOT NULL DEFAULT 'medium',
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_meaning_drift_signals_type ON meaning_drift_signals(signal_type);

CREATE TABLE IF NOT EXISTS mission_alignment_reviews (
  id SERIAL PRIMARY KEY,
  stated_doctrine JSONB NOT NULL DEFAULT '[]'::jsonb,
  actual_recommendations JSONB NOT NULL DEFAULT '[]'::jsonb,
  frontend_console_behavior JSONB NOT NULL DEFAULT '[]'::jsonb,
  api_safeguards JSONB NOT NULL DEFAULT '[]'::jsonb,
  readme_claims JSONB NOT NULL DEFAULT '[]'::jsonb,
  tests_safeguards JSONB NOT NULL DEFAULT '[]'::jsonb,
  doctrine_embodiment_check JSONB NOT NULL DEFAULT '[]'::jsonb,
  mission_alignment_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_mission_alignment_reviews_created_at ON mission_alignment_reviews(created_at);
