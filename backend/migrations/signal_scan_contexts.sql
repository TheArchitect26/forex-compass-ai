CREATE TABLE IF NOT EXISTS signal_scan_contexts (
  id SERIAL PRIMARY KEY,
  signal_id INTEGER UNIQUE REFERENCES signals(id),
  symbol VARCHAR(16) NOT NULL,
  interval VARCHAR(8) NOT NULL,
  signal_timestamp TIMESTAMP NOT NULL,
  direction VARCHAR(8) NOT NULL,
  confidence FLOAT NOT NULL,
  entry_price FLOAT NOT NULL,
  data_mode VARCHAR(32) NOT NULL DEFAULT 'synthetic_demo',
  provider_name VARCHAR(32) NOT NULL DEFAULT 'synthetic',
  demo_only BOOLEAN NOT NULL DEFAULT TRUE,
  candle_snapshot JSON DEFAULT '{}',
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_signal_scan_contexts_signal_id ON signal_scan_contexts(signal_id);
CREATE INDEX IF NOT EXISTS ix_signal_scan_contexts_symbol ON signal_scan_contexts(symbol);
CREATE INDEX IF NOT EXISTS ix_signal_scan_contexts_interval ON signal_scan_contexts(interval);
CREATE INDEX IF NOT EXISTS ix_signal_scan_contexts_signal_timestamp ON signal_scan_contexts(signal_timestamp);
CREATE INDEX IF NOT EXISTS ix_signal_scan_contexts_data_mode ON signal_scan_contexts(data_mode);
CREATE INDEX IF NOT EXISTS ix_signal_scan_contexts_demo_only ON signal_scan_contexts(demo_only);
