# To install just use `uv tool install rust-just`

set dotenv-load

_default:
  @just --list

[group('install')]
install:
  uv sync --all-packages --all-groups
  uv run pre-commit install --config devops/.pre-commit-config.yaml
  cd projects/frontend && pnpm install --frozen-lockfile

[group('run')]
run-backend:
  PYTHONPATH=projects/backend uv run uvicorn package.main:app --reload --host 127.0.0.1 --port 8000

[group('run')]
run-frontend:
  cd projects/frontend && pnpm run dev

[doc("Make sure the backend is running before generating")]
[group('generate')]
generate-frontend-types:
  cd projects/frontend && pnpm run api

[group('test')]
test: test-backend test-frontend

[group('test')]
test-backend *args:
  PYTHONPATH=projects/backend uv run pytest projects/backend/tests {{args}}

[group('test')]
test-frontend:
  cd projects/frontend && pnpm run test

[doc("Whole-repo pre-commit run: format, lint, typecheck, custom checks")]
[group('lint')]
lint:
  uv run pre-commit run --config devops/.pre-commit-config.yaml --all-files

[group('lint')]
format:
  uv run ruff check --fix projects/backend
  uv run ruff format projects/backend
  cd projects/frontend && pnpm run prettify && pnpm run lint:fix

[group('lint')]
typecheck:
  PYTHONPATH=projects/backend uv run mypy projects/backend/package
  uv run pyright projects/backend/package
  cd projects/frontend && pnpm run typecheck

[doc("Mirror GitHub Actions CI: lint, typecheck, tests with coverage, frontend build")]
[group('test')]
run-ci:
  uv sync --all-packages --all-groups
  uv run ruff check projects/backend
  uv run ruff format --check projects/backend
  uv run python devops/check_no_sys_path_mutation.py
  uv run python devops/check_no_future_annotations.py
  uv run python devops/check_no_type_checking.py
  PYTHONPATH=projects/backend uv run mypy projects/backend/package
  uv run pyright projects/backend/package
  PYTHONPATH=projects/backend uv run pytest projects/backend/tests --cov=projects/backend/package --cov-report=term-missing --cov-fail-under=80
  cd projects/frontend && pnpm install --frozen-lockfile && pnpm run prettier:check && pnpm run lint && pnpm run typecheck && pnpm run test && NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000 pnpm run build

[doc("Rename template placeholders. Explicit args: --project-name ... --project-slug ... --python-package ... --non-interactive")]
[group('template')]
bootstrap *args:
  uv run python devops/bootstrap.py {{args}}

[doc("Mark template cleanup done after first build; prints manual follow-ups")]
[group('template')]
template-clean:
  uv run python devops/template_clean.py

[doc("Tag a new version: just tag [patch|minor|major]")]
[group('release')]
tag bump="patch":
  #!/usr/bin/env bash
  set -euo pipefail
  CURRENT=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
  VERSION="${CURRENT#v}"
  IFS='.' read -r MAJOR MINOR PATCH <<< "$VERSION"
  case "{{bump}}" in
    major) MAJOR=$((MAJOR + 1)); MINOR=0; PATCH=0 ;;
    minor) MINOR=$((MINOR + 1)); PATCH=0 ;;
    patch) PATCH=$((PATCH + 1)) ;;
    *) echo "Invalid bump type: {{bump}} (use patch, minor, or major)"; exit 1 ;;
  esac
  NEW="v${MAJOR}.${MINOR}.${PATCH}"
  echo "${CURRENT} -> ${NEW}"
  git tag -a "$NEW" -m "Release $NEW"
  echo "Tagged $NEW (run 'git push --tags' to publish)"
