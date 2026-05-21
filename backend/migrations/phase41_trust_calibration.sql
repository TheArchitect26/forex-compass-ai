CREATE TABLE IF NOT EXISTS trust_calibration_audits (
  id SERIAL PRIMARY KEY,
  institutional_credibility_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  recommendation_legitimacy_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  uncertainty_transparency_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  confidence_calibration_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  usefulness_credibility_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  overreach_risk_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  operator_trust_pressure_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  humility_integrity_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_trust_calibration_audits_created_at ON trust_calibration_audits(created_at);

CREATE TABLE IF NOT EXISTS recommendation_legitimacy_reviews (
  id SERIAL PRIMARY KEY,
  evidence_strength VARCHAR(40) NOT NULL DEFAULT 'moderate',
  uncertainty_clarity VARCHAR(80) NOT NULL DEFAULT 'clear',
  actionability VARCHAR(40) NOT NULL DEFAULT 'medium',
  proportionality VARCHAR(40) NOT NULL DEFAULT 'medium',
  reversibility VARCHAR(40) NOT NULL DEFAULT 'high',
  historical_usefulness VARCHAR(80) NOT NULL DEFAULT 'mixed',
  operator_burden VARCHAR(40) NOT NULL DEFAULT 'medium',
  risk_of_overreach VARCHAR(40) NOT NULL DEFAULT 'medium',
  human_review_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_recommendation_legitimacy_reviews_created_at ON recommendation_legitimacy_reviews(created_at);

CREATE TABLE IF NOT EXISTS credibility_incidents (
  id SERIAL PRIMARY KEY,
  incident_type VARCHAR(120) NOT NULL,
  severity VARCHAR(24) NOT NULL DEFAULT 'medium',
  description TEXT NOT NULL DEFAULT '',
  affected_recommendation_area VARCHAR(120) NOT NULL DEFAULT '',
  corrective_guidance TEXT NOT NULL DEFAULT '',
  human_review_required BOOLEAN NOT NULL DEFAULT TRUE,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_credibility_incidents_type ON credibility_incidents(incident_type);
