CREATE TABLE IF NOT EXISTS operational_reviews (
  id SERIAL PRIMARY KEY,
  review_type VARCHAR(120) NOT NULL,
  review_window VARCHAR(80) NOT NULL DEFAULT 'this week',
  urgency DOUBLE PRECISION NOT NULL DEFAULT 0,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_operational_reviews_type ON operational_reviews(review_type);

CREATE TABLE IF NOT EXISTS deferred_actions (
  id SERIAL PRIMARY KEY,
  reason_deferred TEXT NOT NULL DEFAULT '',
  review_date VARCHAR(80) NOT NULL DEFAULT 'in 7 days',
  risk_of_delay DOUBLE PRECISION NOT NULL DEFAULT 0,
  dependencies JSONB NOT NULL DEFAULT '[]'::jsonb,
  escalation_trigger TEXT NOT NULL DEFAULT '',
  retirement_eligibility BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_deferred_actions_review_date ON deferred_actions(review_date);

CREATE TABLE IF NOT EXISTS maintenance_cycles (
  id SERIAL PRIMARY KEY,
  maintenance_plan JSONB NOT NULL DEFAULT '[]'::jsonb,
  overdue_work JSONB NOT NULL DEFAULT '[]'::jsonb,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_maintenance_cycles_created_at ON maintenance_cycles(created_at);
