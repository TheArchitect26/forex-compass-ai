CREATE TABLE IF NOT EXISTS ecosystem_dependencies (
  id SERIAL PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  dependency_type VARCHAR(80) NOT NULL,
  criticality VARCHAR(24) NOT NULL DEFAULT 'medium',
  current_health VARCHAR(24) NOT NULL DEFAULT 'unknown',
  fallback_availability VARCHAR(24) NOT NULL DEFAULT 'unknown',
  concentration_risk VARCHAR(24) NOT NULL DEFAULT 'medium',
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_ecosystem_dependencies_name ON ecosystem_dependencies(name);

CREATE TABLE IF NOT EXISTS ecosystem_risk_assessments (
  id SERIAL PRIMARY KEY,
  scores JSONB NOT NULL DEFAULT '{}'::jsonb,
  uncertainty_notes JSONB NOT NULL DEFAULT '[]'::jsonb,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_ecosystem_risk_assessments_created_at ON ecosystem_risk_assessments(created_at);

CREATE TABLE IF NOT EXISTS fallback_plans (
  id SERIAL PRIMARY KEY,
  outage_type VARCHAR(120) NOT NULL,
  affected_systems JSONB NOT NULL DEFAULT '[]'::jsonb,
  temporary_workaround TEXT NOT NULL DEFAULT '',
  operator_action_required TEXT NOT NULL DEFAULT '',
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_fallback_plans_outage_type ON fallback_plans(outage_type);
