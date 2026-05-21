CREATE TABLE IF NOT EXISTS temporal_events (
  id SERIAL PRIMARY KEY,
  event_type VARCHAR(80) NOT NULL,
  timing_classification VARCHAR(24) NOT NULL,
  details JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_temporal_events_event_type ON temporal_events(event_type);

CREATE TABLE IF NOT EXISTS rhythm_observations (
  id SERIAL PRIMARY KEY,
  rhythm_state VARCHAR(32) NOT NULL,
  domain VARCHAR(80) NOT NULL,
  metrics JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_rhythm_observations_state ON rhythm_observations(rhythm_state);

CREATE TABLE IF NOT EXISTS timing_decisions (
  id SERIAL PRIMARY KEY,
  subject VARCHAR(180) NOT NULL,
  recommendation VARCHAR(32) NOT NULL,
  rationale TEXT NOT NULL DEFAULT '',
  operator_approved BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_timing_decisions_reco ON timing_decisions(recommendation);
