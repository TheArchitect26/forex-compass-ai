CREATE TABLE IF NOT EXISTS institutional_evaluations (
  id SERIAL PRIMARY KEY,
  institutional_maturity_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  usability_maturity_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  release_maturity_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  runtime_maturity_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  governance_maturity_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  memory_maturity_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  strategic_usefulness_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  maintainability_maturity_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  operator_clarity_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_institutional_evaluations_created_at ON institutional_evaluations(created_at);

CREATE TABLE IF NOT EXISTS maturity_benchmarks (
  id SERIAL PRIMARY KEY,
  category VARCHAR(80) NOT NULL,
  current_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  target_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  evidence JSONB NOT NULL DEFAULT '[]'::jsonb,
  trend VARCHAR(24) NOT NULL DEFAULT 'stable',
  maturity_level VARCHAR(24) NOT NULL DEFAULT 'developing',
  recommended_improvement TEXT NOT NULL DEFAULT '',
  human_review_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_maturity_benchmarks_category ON maturity_benchmarks(category);

CREATE TABLE IF NOT EXISTS improvement_plans (
  id SERIAL PRIMARY KEY,
  plan_items JSONB NOT NULL DEFAULT '[]'::jsonb,
  priority_order JSONB NOT NULL DEFAULT '[]'::jsonb,
  human_review_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_improvement_plans_created_at ON improvement_plans(created_at);
