CREATE TABLE IF NOT EXISTS strategic_assumptions (
  id SERIAL PRIMARY KEY,
  assumption_text TEXT NOT NULL,
  supporting_evidence JSONB NOT NULL DEFAULT '[]'::jsonb,
  contradictory_evidence JSONB NOT NULL DEFAULT '[]'::jsonb,
  historical_confidence DOUBLE PRECISION NOT NULL DEFAULT 0.7,
  last_validation_date TIMESTAMP NOT NULL DEFAULT now(),
  replay_coverage DOUBLE PRECISION NOT NULL DEFAULT 0.5,
  regimes_affected JSONB NOT NULL DEFAULT '[]'::jsonb,
  active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS contradiction_workflows (
  id SERIAL PRIMARY KEY,
  workflow_kind VARCHAR(64) NOT NULL DEFAULT 'contradiction_review',
  state VARCHAR(32) NOT NULL DEFAULT 'open',
  linked_assumption_id INTEGER NULL REFERENCES strategic_assumptions(id),
  evidence_arbitration_notes TEXT NOT NULL DEFAULT '',
  recommendation_deprecation_candidates JSONB NOT NULL DEFAULT '[]'::jsonb,
  stale_strategy_retirement_candidates JSONB NOT NULL DEFAULT '[]'::jsonb,
  review_history JSONB NOT NULL DEFAULT '[]'::jsonb,
  created_at TIMESTAMP NOT NULL DEFAULT now()
);
