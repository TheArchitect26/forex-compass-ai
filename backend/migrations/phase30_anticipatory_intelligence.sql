CREATE TABLE IF NOT EXISTS foresight_warnings (
  id SERIAL PRIMARY KEY,
  warning_type VARCHAR(120) NOT NULL,
  classification VARCHAR(24) NOT NULL,
  evidence JSONB NOT NULL DEFAULT '{}'::jsonb,
  resolved BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_foresight_warnings_type ON foresight_warnings(warning_type);

CREATE TABLE IF NOT EXISTS strategic_forecasts (
  id SERIAL PRIMARY KEY,
  trajectory VARCHAR(32) NOT NULL,
  instability_probability DOUBLE PRECISION NOT NULL DEFAULT 0,
  time_to_risk_estimate_days INTEGER NOT NULL DEFAULT 14,
  details JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_strategic_forecasts_trajectory ON strategic_forecasts(trajectory);

CREATE TABLE IF NOT EXISTS intervention_plans (
  id SERIAL PRIMARY KEY,
  plan JSONB NOT NULL DEFAULT '[]'::jsonb,
  urgency DOUBLE PRECISION NOT NULL DEFAULT 0,
  operator_review_required BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_intervention_plans_created_at ON intervention_plans(created_at);
