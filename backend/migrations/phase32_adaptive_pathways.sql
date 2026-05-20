CREATE TABLE IF NOT EXISTS adaptive_pathways (
  id SERIAL PRIMARY KEY,
  pathway_name VARCHAR(120) NOT NULL,
  trigger_conditions JSONB NOT NULL DEFAULT '{}'::jsonb,
  entry_criteria JSONB NOT NULL DEFAULT '[]'::jsonb,
  exit_criteria JSONB NOT NULL DEFAULT '[]'::jsonb,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_adaptive_pathways_name ON adaptive_pathways(pathway_name);

CREATE TABLE IF NOT EXISTS pathway_evaluations (
  id SERIAL PRIMARY KEY,
  pathway_name VARCHAR(120) NOT NULL,
  evaluation JSONB NOT NULL DEFAULT '{}'::jsonb,
  escalation_needed BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_pathway_evaluations_name ON pathway_evaluations(pathway_name);

CREATE TABLE IF NOT EXISTS pathway_decisions (
  id SERIAL PRIMARY KEY,
  recommended_pathway VARCHAR(120) NOT NULL,
  approved_by_operator BOOLEAN NOT NULL DEFAULT FALSE,
  reversibility_notes TEXT NOT NULL DEFAULT '',
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_pathway_decisions_pathway ON pathway_decisions(recommended_pathway);
