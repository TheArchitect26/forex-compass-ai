CREATE TABLE IF NOT EXISTS mission_anchors (
  id SERIAL PRIMARY KEY,
  operator_note TEXT NOT NULL DEFAULT '',
  mission_reaffirmation TEXT NOT NULL DEFAULT '',
  long_horizon_intent TEXT NOT NULL DEFAULT '',
  reset_intent TEXT NOT NULL DEFAULT '',
  anti_drift_confirmation BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS mission_timeline_events (
  id SERIAL PRIMARY KEY,
  event_type VARCHAR(80) NOT NULL,
  details JSONB NOT NULL DEFAULT '{}'::jsonb,
  severity VARCHAR(32) NOT NULL DEFAULT 'info',
  created_at TIMESTAMP NOT NULL DEFAULT now()
);
