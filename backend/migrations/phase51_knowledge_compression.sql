CREATE TABLE IF NOT EXISTS distilled_insights (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL DEFAULT '',
  insight_type VARCHAR(64) NOT NULL,
  summary TEXT NOT NULL DEFAULT '',
  strategic_retention_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  knowledge_durability_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_distilled_insights_type ON distilled_insights(insight_type);

CREATE TABLE IF NOT EXISTS strategic_heuristics (
  id SERIAL PRIMARY KEY,
  heuristic TEXT NOT NULL DEFAULT '',
  domain VARCHAR(64) NOT NULL DEFAULT 'general',
  usefulness_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  actionability_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_strategic_heuristics_domain ON strategic_heuristics(domain);

CREATE TABLE IF NOT EXISTS institutional_anti_patterns (
  id SERIAL PRIMARY KEY,
  anti_pattern VARCHAR(120) NOT NULL,
  recurring_context TEXT NOT NULL DEFAULT '',
  severity VARCHAR(24) NOT NULL DEFAULT 'medium',
  cognitive_cost_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  recurrence_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_institutional_anti_patterns_key ON institutional_anti_patterns(anti_pattern);
