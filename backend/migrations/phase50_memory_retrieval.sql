CREATE TABLE IF NOT EXISTS memory_index_entries (
  id SERIAL PRIMARY KEY,
  entry_key VARCHAR(120) NOT NULL UNIQUE,
  category VARCHAR(40) NOT NULL,
  title VARCHAR(255) NOT NULL DEFAULT '',
  tags JSONB NOT NULL DEFAULT '[]'::jsonb,
  summary TEXT NOT NULL DEFAULT '',
  source_module VARCHAR(120) NOT NULL DEFAULT '',
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_memory_index_entries_category ON memory_index_entries(category);

CREATE TABLE IF NOT EXISTS memory_retrieval_queries (
  id SERIAL PRIMARY KEY,
  query_text TEXT NOT NULL DEFAULT '',
  context TEXT NOT NULL DEFAULT '',
  relevance_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  confidence_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  usefulness_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  staleness_risk_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_memory_retrieval_queries_created_at ON memory_retrieval_queries(created_at);

CREATE TABLE IF NOT EXISTS contextual_recall_results (
  id SERIAL PRIMARY KEY,
  query_ref VARCHAR(120) NOT NULL DEFAULT '',
  related_lessons JSONB NOT NULL DEFAULT '[]'::jsonb,
  related_decisions JSONB NOT NULL DEFAULT '[]'::jsonb,
  related_incidents JSONB NOT NULL DEFAULT '[]'::jsonb,
  related_assumptions JSONB NOT NULL DEFAULT '[]'::jsonb,
  related_warnings JSONB NOT NULL DEFAULT '[]'::jsonb,
  related_phases JSONB NOT NULL DEFAULT '[]'::jsonb,
  stale_knowledge_risks JSONB NOT NULL DEFAULT '[]'::jsonb,
  recommended_human_review TEXT NOT NULL DEFAULT '',
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_contextual_recall_results_created_at ON contextual_recall_results(created_at);
