CREATE TABLE IF NOT EXISTS institutional_lessons (
  id SERIAL PRIMARY KEY,
  lesson TEXT NOT NULL DEFAULT '',
  evidence JSONB NOT NULL DEFAULT '[]'::jsonb,
  confidence DOUBLE PRECISION NOT NULL DEFAULT 0,
  affected_systems JSONB NOT NULL DEFAULT '[]'::jsonb,
  limitations JSONB NOT NULL DEFAULT '[]'::jsonb,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_institutional_lessons_created_at ON institutional_lessons(created_at);

CREATE TABLE IF NOT EXISTS intervention_reviews (
  id SERIAL PRIMARY KEY,
  intervention VARCHAR(180) NOT NULL,
  effectiveness_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  operator_burden DOUBLE PRECISION NOT NULL DEFAULT 0,
  confidence_in_lesson DOUBLE PRECISION NOT NULL DEFAULT 0,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_intervention_reviews_intervention ON intervention_reviews(intervention);

CREATE TABLE IF NOT EXISTS forecast_reviews (
  id SERIAL PRIMARY KEY,
  predicted TEXT NOT NULL DEFAULT '',
  actual TEXT NOT NULL DEFAULT '',
  accuracy_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  miss_reason TEXT NOT NULL DEFAULT '',
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_forecast_reviews_created_at ON forecast_reviews(created_at);

CREATE TABLE IF NOT EXISTS assumption_learning_reviews (
  id SERIAL PRIMARY KEY,
  assumption TEXT NOT NULL DEFAULT '',
  status VARCHAR(24) NOT NULL DEFAULT 'review',
  confidence DOUBLE PRECISION NOT NULL DEFAULT 0,
  evidence JSONB NOT NULL DEFAULT '[]'::jsonb,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_assumption_learning_reviews_status ON assumption_learning_reviews(status);
