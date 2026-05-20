CREATE TABLE IF NOT EXISTS research_workloads (
  id SERIAL PRIMARY KEY,
  workload_type VARCHAR(64) NOT NULL,
  status VARCHAR(16) NOT NULL DEFAULT 'queued',
  priority INTEGER NOT NULL DEFAULT 50,
  retries INTEGER NOT NULL DEFAULT 0,
  execution_duration_ms DOUBLE PRECISION NOT NULL DEFAULT 0,
  queue_name VARCHAR(32) NOT NULL DEFAULT 'research',
  worker_id VARCHAR(64) NOT NULL DEFAULT 'unassigned',
  resource_estimate JSONB NOT NULL DEFAULT '{}'::jsonb,
  checkpoint JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMP NOT NULL DEFAULT now(),
  completed_at TIMESTAMP NULL
);

CREATE TABLE IF NOT EXISTS research_graph_edges (
  id SERIAL PRIMARY KEY,
  source_type VARCHAR(32) NOT NULL,
  source_id VARCHAR(64) NOT NULL,
  target_type VARCHAR(32) NOT NULL,
  target_id VARCHAR(64) NOT NULL,
  relation VARCHAR(64) NOT NULL DEFAULT 'related_to',
  weight DOUBLE PRECISION NOT NULL DEFAULT 1,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMP NOT NULL DEFAULT now()
);
