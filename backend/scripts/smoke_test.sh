#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${1:-http://localhost:8000}"

check() {
  local path="$1"
  echo "Checking ${path}"
  curl -fsS "${BASE_URL}${path}" >/dev/null
}

check "/api/market/pairs"
check "/api/market/ohlcv?pair=EUR/USD&timeframe=1h&limit=100"
check "/api/analysis/EUR/USD"
check "/api/signals/scan"
check "/api/signals"

echo "Smoke test passed for ${BASE_URL}"
