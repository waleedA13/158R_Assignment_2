#!/usr/bin/env bash
# Run the same stages as CI, in the same order, and stop at the first failure.
# Usage (repo root, inside the 3.12 venv):  bash scripts/check.sh
set -euo pipefail
cd "$(dirname "$0")/.."
export DATA_DIR="${DATA_DIR:-tests/fixtures}"

step() { printf '\n== %s\n' "$1"; }

step "1 Formatting";        ruff format --check .
step "2 Linting";           ruff check .
step "3 Security audit";    pip-audit -r requirements-dev.txt
step "4 Unit tests";        pytest tests/unit --cov --cov-report=term-missing
step "5 Integration tests"; pytest tests/integration
if ls notebooks/*.ipynb >/dev/null 2>&1; then pytest --nbmake notebooks/; else echo "No notebooks yet"; fi
step "6 End-to-end";        pytest tests/e2e

printf '\nAll checks passed.\n'
