CREATE TABLE IF NOT EXISTS runtime_health_audits (
  id SERIAL PRIMARY KEY,
  runtime_health_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  endpoint_reliability_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  latency_risk_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  frontend_backend_compatibility_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  error_pressure_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  deployment_regression_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  monitoring_readiness_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  recovery_visibility_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_runtime_health_audits_created_at ON runtime_health_audits(created_at);

CREATE TABLE IF NOT EXISTS endpoint_health_observations (
  id SERIAL PRIMARY KEY,
  endpoint_path VARCHAR(255) NOT NULL,
  method VARCHAR(12) NOT NULL DEFAULT 'GET',
  expected_status INTEGER NOT NULL DEFAULT 200,
  observed_status INTEGER NOT NULL DEFAULT 200,
  latency_estimate_ms DOUBLE PRECISION NOT NULL DEFAULT 0,
  error_pattern TEXT NOT NULL DEFAULT '',
  affected_subsystem VARCHAR(80) NOT NULL DEFAULT '',
  severity VARCHAR(24) NOT NULL DEFAULT 'low',
  recommended_human_review BOOLEAN NOT NULL DEFAULT FALSE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_endpoint_health_observations_path ON endpoint_health_observations(endpoint_path);

CREATE TABLE IF NOT EXISTS deployment_regression_signals (
  id SERIAL PRIMARY KEY,
  routes_failing_after_release JSONB NOT NULL DEFAULT '[]'::jsonb,
  api_base_url_mismatch JSONB NOT NULL DEFAULT '[]'::jsonb,
  vercel_backend_route_mismatch JSONB NOT NULL DEFAULT '[]'::jsonb,
  static_frontend_page_mismatch JSONB NOT NULL DEFAULT '[]'::jsonb,
  missing_env_var_runtime_errors JSONB NOT NULL DEFAULT '[]'::jsonb,
  dependency_runtime_import_failures JSONB NOT NULL DEFAULT '[]'::jsonb,
  slow_endpoints JSONB NOT NULL DEFAULT '[]'::jsonb,
  repeated_500_or_404_patterns JSONB NOT NULL DEFAULT '[]'::jsonb,
  deployment_regression_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_deployment_regression_signals_created_at ON deployment_regression_signals(created_at);
