CREATE TABLE IF NOT EXISTS post_implementation_reviews (
  id SERIAL PRIMARY KEY,
  change_summary TEXT NOT NULL DEFAULT '',
  planned_outcome TEXT NOT NULL DEFAULT '',
  actual_outcome TEXT NOT NULL DEFAULT '',
  deviations JSONB NOT NULL DEFAULT '[]'::jsonb,
  what_worked JSONB NOT NULL DEFAULT '[]'::jsonb,
  what_failed JSONB NOT NULL DEFAULT '[]'::jsonb,
  unexpected_impacts JSONB NOT NULL DEFAULT '[]'::jsonb,
  affected_systems JSONB NOT NULL DEFAULT '[]'::jsonb,
  rollback_status VARCHAR(32) NOT NULL DEFAULT 'not_required',
  operator_impact VARCHAR(32) NOT NULL DEFAULT 'low',
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_post_implementation_reviews_created_at ON post_implementation_reviews(created_at);

CREATE TABLE IF NOT EXISTS change_lessons_learned (
  id SERIAL PRIMARY KEY,
  lesson_category VARCHAR(64) NOT NULL,
  lesson_text TEXT NOT NULL DEFAULT '',
  reusable_heuristic TEXT NOT NULL DEFAULT '',
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_change_lessons_learned_category ON change_lessons_learned(lesson_category);

CREATE TABLE IF NOT EXISTS change_improvement_actions (
  id SERIAL PRIMARY KEY,
  action_text TEXT NOT NULL DEFAULT '',
  priority VARCHAR(32) NOT NULL DEFAULT 'medium',
  status VARCHAR(32) NOT NULL DEFAULT 'open',
  owner VARCHAR(128) NOT NULL DEFAULT '',
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_change_improvement_actions_status ON change_improvement_actions(status);
