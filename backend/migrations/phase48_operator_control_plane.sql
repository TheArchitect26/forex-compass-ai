CREATE TABLE IF NOT EXISTS control_plane_snapshots (
  id SERIAL PRIMARY KEY,
  operator_clarity_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  dashboard_sprawl_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  cognitive_load_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  institutional_health_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  actionability_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  signal_to_noise_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  navigation_burden_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  consolidation_opportunity_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_control_plane_snapshots_created_at ON control_plane_snapshots(created_at);

CREATE TABLE IF NOT EXISTS operator_focus_summaries (
  id SERIAL PRIMARY KEY,
  focus_view VARCHAR(64) NOT NULL,
  top_institutional_priorities JSONB NOT NULL DEFAULT '[]'::jsonb,
  top_ignore_or_defer JSONB NOT NULL DEFAULT '[]'::jsonb,
  critical_warnings JSONB NOT NULL DEFAULT '[]'::jsonb,
  next_best_human_reviewed_action TEXT NOT NULL DEFAULT '',
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_operator_focus_summaries_view ON operator_focus_summaries(focus_view);

CREATE TABLE IF NOT EXISTS console_sprawl_audits (
  id SERIAL PRIMARY KEY,
  too_many_sidebar_items BOOLEAN NOT NULL DEFAULT FALSE,
  overlapping_frontend_pages JSONB NOT NULL DEFAULT '[]'::jsonb,
  low_value_consoles JSONB NOT NULL DEFAULT '[]'::jsonb,
  duplicated_summaries JSONB NOT NULL DEFAULT '[]'::jsonb,
  navigation_confusion JSONB NOT NULL DEFAULT '[]'::jsonb,
  excessive_context_switching JSONB NOT NULL DEFAULT '[]'::jsonb,
  dashboards_to_group JSONB NOT NULL DEFAULT '[]'::jsonb,
  advisory_only BOOLEAN NOT NULL DEFAULT TRUE,
  auto_apply BOOLEAN NOT NULL DEFAULT FALSE,
  human_approval_required BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_console_sprawl_audits_created_at ON console_sprawl_audits(created_at);
