#!/usr/bin/env bash
set -euo pipefail

echo "Setting up local/Codespaces environment..."

if [ ! -f .env ] && [ -f .env.example ]; then
  cp .env.example .env
  echo "Created .env from .env.example"
fi

python -m pip install --upgrade pip
pip install -r backend/requirements.txt

echo "Setup complete."
echo "Run: bash scripts/validate-local.sh"
