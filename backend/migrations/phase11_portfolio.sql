CREATE TABLE IF NOT EXISTS portfolio_replay_sessions (
  id SERIAL PRIMARY KEY,
  name VARCHAR(64) NOT NULL DEFAULT 'portfolio-lab',
  pair VARCHAR(16) NOT NULL,
  timeframe VARCHAR(8) NOT NULL,
  strategy_profile VARCHAR(32) NOT NULL DEFAULT 'intraday',
  sizing_mode VARCHAR(32) NOT NULL DEFAULT 'fixed_risk',
  balance DOUBLE PRECISION NOT NULL DEFAULT 10000,
  equity_curve JSONB NOT NULL DEFAULT '[]'::jsonb,
  open_positions JSONB NOT NULL DEFAULT '[]'::jsonb,
  closed_positions JSONB NOT NULL DEFAULT '[]'::jsonb,
  exposure_state JSONB NOT NULL DEFAULT '{}'::jsonb,
  risk_state JSONB NOT NULL DEFAULT '{}'::jsonb,
  replay_session_id INTEGER NULL REFERENCES replay_sessions(id),
  status VARCHAR(16) NOT NULL DEFAULT 'running',
  created_at TIMESTAMP NOT NULL DEFAULT now()
);
