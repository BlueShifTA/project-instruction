#!/bin/bash
# Post-create hook for VS Code Dev Container

set -e

echo "📦 Installing Python dependencies..."
curl -sSL https://sh.rustup.rs | sh -s -- -y
source "$HOME/.cargo/env"
pip install --upgrade pip uv
uv sync --all-packages --all-groups

echo "🔗 Installing pre-commit hooks..."
uv run pre-commit install --config devops/.pre-commit-config.yaml

echo "📚 Installing frontend dependencies..."
cd projects/frontend
npm ci
cd ../..

echo "✅ Dev container ready!"
echo ""
echo "Quick commands:"
echo "  just install      # Full install (if needed)"
echo "  just run-backend  # Start FastAPI on port 8000"
echo "  just run-frontend # Start Next.js on port 3000"
echo "  just test         # Run pytest"
echo "  just lint         # Run all linters"
echo ""
echo "Services: PostgreSQL (5432) and Redis (6379) available via docker-compose"
