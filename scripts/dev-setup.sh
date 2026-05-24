#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env from .env.example"
fi

python -m pip install --upgrade pip
python -m pip install -r backend/requirements.txt

echo "Developer setup complete."
echo "Next: run scripts/validate-local.sh"
