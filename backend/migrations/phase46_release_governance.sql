CREATE TABLE IF NOT EXISTS release_readiness_audits (
  id SERIAL PRIMARY KEY,
  release_readiness_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  build_confidence_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  deployment_risk_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  rollback_readiness_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  migration_risk_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  environment_readiness_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  post_release_monitoring_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  production_suitability_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_release_readiness_audits_created_at ON release_readiness_audits(created_at);

CREATE TABLE IF NOT EXISTS deployment_risk_assessments (
  id SERIAL PRIMARY KEY,
  unresolved_dependency_versions JSONB NOT NULL DEFAULT '[]'::jsonb,
  deprecated_nextjs_warnings JSONB NOT NULL DEFAULT '[]'::jsonb,
  frontend_backend_api_mismatch JSONB NOT NULL DEFAULT '[]'::jsonb,
  migration_drift JSONB NOT NULL DEFAULT '[]'::jsonb,
  missing_production_env_vars JSONB NOT NULL DEFAULT '[]'::jsonb,
  unsafe_fallback_assumptions JSONB NOT NULL DEFAULT '[]'::jsonb,
  test_gaps_new_routers JSONB NOT NULL DEFAULT '[]'::jsonb,
  deployment_risk_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_deployment_risk_assessments_created_at ON deployment_risk_assessments(created_at);

CREATE TABLE IF NOT EXISTS rollback_plan_reviews (
  id SERIAL PRIMARY KEY,
  rollback_steps JSONB NOT NULL DEFAULT '[]'::jsonb,
  database_rollback_warning TEXT NOT NULL DEFAULT '',
  migration_caution TEXT NOT NULL DEFAULT '',
  post_rollback_validation JSONB NOT NULL DEFAULT '[]'::jsonb,
  rollback_readiness_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_rollback_plan_reviews_created_at ON rollback_plan_reviews(created_at);
