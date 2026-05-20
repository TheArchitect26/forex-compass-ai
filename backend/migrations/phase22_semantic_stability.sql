CREATE TABLE IF NOT EXISTS glossary_terms (
  id SERIAL PRIMARY KEY,
  term VARCHAR(120) NOT NULL,
  canonical_definition TEXT NOT NULL DEFAULT '',
  deprecated BOOLEAN NOT NULL DEFAULT FALSE,
  related_concepts JSONB NOT NULL DEFAULT '[]'::jsonb,
  historical_meanings JSONB NOT NULL DEFAULT '[]'::jsonb,
  replay_version_relevance JSONB NOT NULL DEFAULT '[]'::jsonb,
  governance_impact TEXT NOT NULL DEFAULT '',
  created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS concept_lineage (
  id SERIAL PRIMARY KEY,
  concept VARCHAR(140) NOT NULL,
  origin TEXT NOT NULL DEFAULT '',
  revisions JSONB NOT NULL DEFAULT '[]'::jsonb,
  contradictions JSONB NOT NULL DEFAULT '[]'::jsonb,
  retired_meanings JSONB NOT NULL DEFAULT '[]'::jsonb,
  successor_concepts JSONB NOT NULL DEFAULT '[]'::jsonb,
  confidence_evolution JSONB NOT NULL DEFAULT '[]'::jsonb,
  created_at TIMESTAMP NOT NULL DEFAULT now()
);
