CREATE TABLE IF NOT EXISTS wisdom_audits (
  id SERIAL PRIMARY KEY,
  wisdom_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  prudence_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  restraint_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  ambiguity_tolerance_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  uncertainty_integrity_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  long_term_judgment_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  overreaction_risk_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  strategic_patience_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_wisdom_audits_created_at ON wisdom_audits(created_at);

CREATE TABLE IF NOT EXISTS ambiguity_reviews (
  id SERIAL PRIMARY KEY,
  knowns JSONB NOT NULL DEFAULT '[]'::jsonb,
  uncertain JSONB NOT NULL DEFAULT '[]'::jsonb,
  assumed JSONB NOT NULL DEFAULT '[]'::jsonb,
  needs_review JSONB NOT NULL DEFAULT '[]'::jsonb,
  what_not_to_conclude_yet JSONB NOT NULL DEFAULT '[]'::jsonb,
  human_review_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_ambiguity_reviews_created_at ON ambiguity_reviews(created_at);

CREATE TABLE IF NOT EXISTS judgment_discipline_reviews (
  id SERIAL PRIMARY KEY,
  reflective_reasoning TEXT NOT NULL DEFAULT '',
  historical_experience TEXT NOT NULL DEFAULT '',
  long_term_well_being TEXT NOT NULL DEFAULT '',
  moderation VARCHAR(40) NOT NULL DEFAULT 'moderate',
  reversibility VARCHAR(40) NOT NULL DEFAULT 'high',
  proportionality VARCHAR(40) NOT NULL DEFAULT 'medium',
  operator_burden VARCHAR(40) NOT NULL DEFAULT 'medium',
  mission_alignment TEXT NOT NULL DEFAULT '',
  human_review_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_judgment_discipline_reviews_created_at ON judgment_discipline_reviews(created_at);
