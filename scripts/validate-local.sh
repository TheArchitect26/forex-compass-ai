#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

python -m compileall backend/app
PYTHONPATH=.:backend pytest -q backend/tests/test_critical_stabilization_patch.py backend/tests/test_environment_smoke.py
