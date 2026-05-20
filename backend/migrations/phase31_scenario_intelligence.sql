CREATE TABLE IF NOT EXISTS scenario_runs (
  id SERIAL PRIMARY KEY,
  scenario_name VARCHAR(120) NOT NULL,
  assumptions JSONB NOT NULL DEFAULT '[]'::jsonb,
  result JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_scenario_runs_name ON scenario_runs(scenario_name);

CREATE TABLE IF NOT EXISTS scenario_comparisons (
  id SERIAL PRIMARY KEY,
  left_option VARCHAR(120) NOT NULL,
  right_option VARCHAR(120) NOT NULL,
  preferred_option VARCHAR(120) NOT NULL,
  reasoning TEXT NOT NULL DEFAULT '',
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_scenario_comparisons_preferred ON scenario_comparisons(preferred_option);

CREATE TABLE IF NOT EXISTS consequence_assessments (
  id SERIAL PRIMARY KEY,
  scenario_name VARCHAR(120) NOT NULL,
  primary_effects JSONB NOT NULL DEFAULT '[]'::jsonb,
  second_order_effects JSONB NOT NULL DEFAULT '[]'::jsonb,
  risks_introduced JSONB NOT NULL DEFAULT '[]'::jsonb,
  risks_reduced JSONB NOT NULL DEFAULT '[]'::jsonb,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_consequence_assessments_name ON consequence_assessments(scenario_name);
