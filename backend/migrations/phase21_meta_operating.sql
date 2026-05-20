CREATE TABLE IF NOT EXISTS meta_coordination_events (
  id SERIAL PRIMARY KEY,
  event_type VARCHAR(80) NOT NULL,
  details JSONB NOT NULL DEFAULT '{}'::jsonb,
  severity VARCHAR(32) NOT NULL DEFAULT 'info',
  created_at TIMESTAMP NOT NULL DEFAULT now()
);
