set dotenv-load
set quiet := false

ROOT := justfile_directory()
BACKEND := ROOT / "projects" / "backend"
FRONTEND := ROOT / "projects" / "frontend"
DEVOPS := ROOT / "devops"
SCRIPTS := ROOT / "scripts"

default:
  @just --list

# ──────────────────────────────────────────────────────────────
# 📦 INSTALL: Dependency Management
# ──────────────────────────────────────────────────────────────

[group('install')]
[doc("Full installation: Python + Node + pre-commit hooks")]
install:
  @echo "📦 Installing all dependencies..."
  cd {{ROOT}} && uv sync --all-packages --all-groups
  cd {{ROOT}} && uv run pre-commit install --config {{DEVOPS}}/.pre-commit-config.yaml
  cd {{FRONTEND}} && pnpm install --frozen-lockfile
  @echo "✅ Installation complete"

[group('install')]
[doc("Install Python backend dependencies only")]
install-backend:
  @echo "📦 Installing backend dependencies..."
  cd {{ROOT}} && uv sync --all-packages --all-groups
  cd {{ROOT}} && uv run pre-commit install --config {{DEVOPS}}/.pre-commit-config.yaml
  @echo "✅ Backend ready"

[group('install')]
[doc("Install frontend (Node.js) dependencies only")]
install-frontend:
  @echo "📦 Installing frontend dependencies..."
  cd {{FRONTEND}} && pnpm install --frozen-lockfile
  @echo "✅ Frontend ready"

[group('install')]
[doc("Update all dependencies")]
update-deps:
  @echo "🔄 Updating Python + Node dependencies..."
  cd {{ROOT}} && uv lock --upgrade
  cd {{FRONTEND}} && pnpm update
  @echo "✅ Updated"

# ──────────────────────────────────────────────────────────────
# 🚀 RUN: Development Servers
# ──────────────────────────────────────────────────────────────

[group('run')]
[doc("Start FastAPI backend (http://localhost:8000)")]
run-backend:
  cd {{ROOT}} && PYTHONPATH={{BACKEND}} uv run uvicorn package.main:app --reload --host 127.0.0.1 --port 8000

[group('run')]
[doc("Start Next.js frontend dev server (http://localhost:3000)")]
run-frontend:
  cd {{FRONTEND}} && pnpm run dev

[group('run')]
[doc("⚠️  Run both backend & frontend (use separate terminals with: just run-backend & just run-frontend)")]
run-all:
  @echo "ℹ️  Backend: just run-backend"
  @echo "ℹ️  Frontend: just run-frontend"
  @echo ""
  @echo "Or run both in background:"
  @echo "  (just run-backend &) && (just run-frontend &)"

# ──────────────────────────────────────────────────────────────
# 🧪 TEST: Testing & Coverage
# ──────────────────────────────────────────────────────────────

[group('test')]
[doc("Run backend tests")]
test:
  cd {{ROOT}} && PYTHONPATH={{BACKEND}} uv run pytest {{BACKEND}}/tests -v

[group('test')]
[doc("Run tests with coverage report (threshold: 80%)")]
test-cov threshold="80":
  cd {{ROOT}} && PYTHONPATH={{BACKEND}} uv run pytest {{BACKEND}}/tests \
    --cov={{BACKEND}}/package \
    --cov-report term-missing \
    --cov-report xml:{{ROOT}}/coverage.xml \
    --cov-fail-under={{threshold}}

[group('test')]
[doc("Run tests in watch mode (requires pytest-watch)")]
test-watch:
  cd {{ROOT}} && PYTHONPATH={{BACKEND}} uv run ptw {{BACKEND}}/tests

[group('test')]
[doc("Run full CI-equivalent checks locally")]
run-ci:
  @echo "🔄 Running full CI pipeline..."
  cd {{ROOT}} && uv sync --all-groups --all-packages
  @echo "  → Testing..."
  cd {{ROOT}} && PYTHONPATH={{BACKEND}} uv run pytest {{BACKEND}}/tests \
    --cov={{BACKEND}}/package \
    --cov-report=term-missing \
    --cov-report=xml:{{ROOT}}/coverage.xml \
    --cov-fail-under=80
  @echo "  → Type checking Python..."
  cd {{ROOT}} && PYTHONPATH={{BACKEND}} uv run mypy {{BACKEND}}/package
  cd {{ROOT}} && uv run pyright {{BACKEND}}/package
  @echo "  → Linting Python..."
  cd {{ROOT}} && uv run ruff format --check {{BACKEND}}
  cd {{ROOT}} && uv run ruff check {{BACKEND}}
  cd {{ROOT}} && uv run python {{SCRIPTS}}/check_no_sys_path_mutation.py
  @echo "  → Building frontend..."
  cd {{FRONTEND}} && pnpm install --frozen-lockfile && pnpm run prettier:check && pnpm run lint && pnpm run typecheck && NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000 pnpm run build
  @echo "✅ CI checks passed!"

[group('test')]
[doc("Mirror GitHub Actions CI exactly (same steps, same order)")]
run-ci-local:
  @echo "🔄 Running GitHub CI pipeline locally..."
  @echo ""
  @echo "═══ Frontend Job ═══"
  @echo "  → pnpm install --frozen-lockfile..."
  cd {{FRONTEND}} && pnpm install --frozen-lockfile
  @echo "  → Prettier check..."
  cd {{FRONTEND}} && pnpm run prettier:check
  @echo "  → ESLint..."
  cd {{FRONTEND}} && pnpm run lint
  @echo "  → Typecheck..."
  cd {{FRONTEND}} && pnpm run typecheck
  @echo "  → Build..."
  cd {{FRONTEND}} && NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000 pnpm run build
  @echo ""
  @echo "═══ Backend Job ═══"
  @echo "  → Sync dependencies..."
  cd {{ROOT}} && uv sync --all-groups --all-packages
  @echo "  → Ruff linting..."
  cd {{ROOT}} && uv run ruff check {{BACKEND}}
  @echo "  → Ruff format check..."
  cd {{ROOT}} && uv run ruff format --check {{BACKEND}}
  @echo "  → sys.path mutation check..."
  cd {{ROOT}} && uv run python {{SCRIPTS}}/check_no_sys_path_mutation.py
  @echo "  → Pyright..."
  cd {{ROOT}} && uv run pyright {{BACKEND}}/package
  @echo "  → Mypy..."
  cd {{ROOT}} && PYTHONPATH={{BACKEND}} uv run mypy {{BACKEND}}/package
  @echo "  → Tests..."
  cd {{ROOT}} && PYTHONPATH={{BACKEND}} uv run pytest {{BACKEND}}/tests -v --tb=short
  @echo "  → Tests with coverage..."
  cd {{ROOT}} && PYTHONPATH={{BACKEND}} uv run pytest {{BACKEND}}/tests \
    --cov={{BACKEND}}/package \
    --cov-report=term \
    --cov-report=xml:{{ROOT}}/coverage.xml \
    --cov-fail-under=80
  @echo ""
  @echo "✅ GitHub CI pipeline passed locally!"

# ──────────────────────────────────────────────────────────────
# 🔍 LINT: Code Quality, Formatting, Type Checking
# ──────────────────────────────────────────────────────────────

[group('lint')]
[doc("Run all linters (ruff + mypy + pyright + prettier + eslint)")]
lint:
  cd {{ROOT}} && uv run pre-commit run --config {{DEVOPS}}/.pre-commit-config.yaml --all-files

[group('lint')]
[doc("Format code (ruff + prettier)")]
format:
  @echo "📝 Formatting Python..."
  cd {{ROOT}} && uv run ruff check --fix {{BACKEND}}
  cd {{ROOT}} && uv run ruff format {{BACKEND}}
  @echo "📝 Formatting JavaScript/TypeScript..."
  cd {{FRONTEND}} && pnpm run prettier:write && pnpm run lint:fix
  @echo "✅ Formatting complete"

[group('lint')]
[doc("Format check only (no modifications)")]
format-check:
  @echo "🔍 Checking format..."
  cd {{ROOT}} && uv run ruff format --check {{BACKEND}}
  cd {{FRONTEND}} && pnpm run prettier:check

[group('lint')]
[doc("Type check Python code (mypy + pyright)")]
typecheck-python:
  @echo "🔍 Type checking Python..."
  cd {{ROOT}} && PYTHONPATH={{BACKEND}} uv run mypy {{BACKEND}}/package
  cd {{ROOT}} && uv run pyright {{BACKEND}}/package

[group('lint')]
[doc("Type check TypeScript/JavaScript")]
typecheck-frontend:
  @echo "🔍 Type checking TypeScript..."
  cd {{FRONTEND}} && pnpm run typecheck

[group('lint')]
[doc("Type check all (Python + TypeScript)")]
typecheck: typecheck-python typecheck-frontend

[group('lint')]
[doc("Lint frontend (eslint)")]
lint-frontend:
  cd {{FRONTEND}} && pnpm run lint

# ──────────────────────────────────────────────────────────────
# 🔧 GENERATE: Code Generation
# ──────────────────────────────────────────────────────────────

[group('generate')]
[doc("Generate frontend API client types from OpenAPI schema")]
generate-frontend-types:
  @echo "📚 Generating frontend API types..."
  cd {{FRONTEND}} && pnpm run api
  @echo "✅ Types generated"

[group('generate')]
[doc("Generate OpenAPI schema from backend")]
generate-openapi:
  @echo "📚 Generating OpenAPI schema..."
  cd {{ROOT}} && PYTHONPATH={{BACKEND}} uv run python -c "from package.main import app; import json; print(json.dumps(app.openapi(), indent=2))" > {{ROOT}}/openapi.json
  @echo "✅ OpenAPI schema generated (openapi.json)"

# ──────────────────────────────────────────────────────────────
# 🎯 TEMPLATE: Template Customization
# ──────────────────────────────────────────────────────────────

[group('template')]
[doc("Bootstrap: Customize template placeholders")]
bootstrap:
  cd {{ROOT}} && uv run python {{SCRIPTS}}/bootstrap.py

[group('template')]
[doc("Clean template markers after first build")]
template-clean:
  cd {{ROOT}} && uv run python {{SCRIPTS}}/template_clean.py

[group('template')]
[doc("Regenerate ProjectMap.md for fast agent search")]
project-map:
  cd {{ROOT}} && uv run python {{SCRIPTS}}/generate_project_map.py

# ──────────────────────────────────────────────────────────────
# 🧹 UTIL: Utilities
# ──────────────────────────────────────────────────────────────

[group('util')]
[doc("Clean all build artifacts, caches, and temp files")]
clean:
  @echo "🧹 Cleaning..."
  rm -rf {{ROOT}}/.venv {{ROOT}}/.mypy_cache {{ROOT}}/.ruff_cache {{ROOT}}/.pytest_cache {{ROOT}}/.coverage {{ROOT}}/coverage.xml {{ROOT}}/htmlcov
  rm -rf {{FRONTEND}}/.next {{FRONTEND}}/node_modules {{FRONTEND}}/.eslintcache
  find {{ROOT}} -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
  find {{ROOT}} -type f -name "*.pyc" -delete
  @echo "✅ Cleaned"

[group('util')]
[doc("Reset pre-commit cache")]
clean-hooks:
  rm -rf {{ROOT}}/.git/hooks/pre-commit {{ROOT}}/.pre-commit-framework-cache
  cd {{ROOT}} && uv run pre-commit install --config {{DEVOPS}}/.pre-commit-config.yaml
  @echo "✅ Pre-commit hooks reset"

[group('util')]
[doc("Full reset: clean + reinstall everything")]
reset: clean
  @echo "🔄 Full reset..."
  just install
  @echo "✅ Reset complete"

# ──────────────────────────────────────────────────────────────
# 🏷️ RELEASE: Version Tagging
# ──────────────────────────────────────────────────────────────

[group('release')]
[doc("Tag a new version (patch/minor/major). Usage: just tag [patch|minor|major]")]
tag bump="patch":
  #!/usr/bin/env bash
  set -euo pipefail
  CURRENT=$(git -C {{ROOT}} describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
  VERSION="${CURRENT#v}"
  IFS='.' read -r MAJOR MINOR PATCH <<< "$VERSION"
  case "{{bump}}" in
    major) MAJOR=$((MAJOR + 1)); MINOR=0; PATCH=0 ;;
    minor) MINOR=$((MINOR + 1)); PATCH=0 ;;
    patch) PATCH=$((PATCH + 1)) ;;
    *) echo "❌ Invalid bump type: {{bump}} (use patch, minor, or major)"; exit 1 ;;
  esac
  NEW="v${MAJOR}.${MINOR}.${PATCH}"
  echo "🏷️  ${CURRENT} → ${NEW}"
  git -C {{ROOT}} tag -a "$NEW" -m "Release $NEW"
  echo "✅ Tagged $NEW (run 'git push --tags' to publish)"

[group('util')]
[doc("Show disk usage by directory")]
du:
  du -sh {{ROOT}} {{ROOT}}/* 2>/dev/null | sort -h

[group('util')]
[doc("List all available recipes")]
recipes:
  just --list --justfile {{justfile()}}
