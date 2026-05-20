CREATE TABLE IF NOT EXISTS strategic_briefings (
  id SERIAL PRIMARY KEY,
  title VARCHAR(160) NOT NULL,
  severity VARCHAR(16) NOT NULL DEFAULT 'normal',
  summary TEXT NOT NULL DEFAULT '',
  supporting_evidence JSONB NOT NULL DEFAULT '[]'::jsonb,
  affected_systems JSONB NOT NULL DEFAULT '[]'::jsonb,
  confidence DOUBLE PRECISION NOT NULL DEFAULT 0,
  recommended_actions JSONB NOT NULL DEFAULT '[]'::jsonb,
  reproducibility_refs JSONB NOT NULL DEFAULT '[]'::jsonb,
  generated_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS strategic_memory_events (
  id SERIAL PRIMARY KEY,
  event_type VARCHAR(64) NOT NULL,
  title VARCHAR(160) NOT NULL,
  details JSONB NOT NULL DEFAULT '{}'::jsonb,
  anomaly_timeline JSONB NOT NULL DEFAULT '[]'::jsonb,
  repeated_pattern_key VARCHAR(128) NOT NULL DEFAULT '',
  successful_mitigation TEXT NOT NULL DEFAULT '',
  created_at TIMESTAMP NOT NULL DEFAULT now()
);
