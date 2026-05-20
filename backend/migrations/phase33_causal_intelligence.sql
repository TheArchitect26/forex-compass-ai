CREATE TABLE IF NOT EXISTS causal_analyses (
  id SERIAL PRIMARY KEY,
  incident_type VARCHAR(120) NOT NULL,
  root_causes JSONB NOT NULL DEFAULT '[]'::jsonb,
  confidence_level DOUBLE PRECISION NOT NULL DEFAULT 0,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_causal_analyses_incident ON causal_analyses(incident_type);

CREATE TABLE IF NOT EXISTS causal_graph_snapshots (
  id SERIAL PRIMARY KEY,
  nodes JSONB NOT NULL DEFAULT '[]'::jsonb,
  edges JSONB NOT NULL DEFAULT '[]'::jsonb,
  notes TEXT NOT NULL DEFAULT '',
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_causal_graph_snapshots_created_at ON causal_graph_snapshots(created_at);

CREATE TABLE IF NOT EXISTS intervention_effect_estimates (
  id SERIAL PRIMARY KEY,
  intervention VARCHAR(180) NOT NULL,
  likely_benefit DOUBLE PRECISION NOT NULL DEFAULT 0,
  confidence DOUBLE PRECISION NOT NULL DEFAULT 0,
  time_horizon VARCHAR(80) NOT NULL DEFAULT '1-3 weeks',
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_intervention_effect_estimates_intervention ON intervention_effect_estimates(intervention);
