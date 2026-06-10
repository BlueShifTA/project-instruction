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

[doc("The CI pipeline (GitHub Actions runs exactly this): pre-commit gate + tests + frontend build")]
[group('test')]
run-ci:
  uv sync --locked --all-packages --all-groups
  cd projects/frontend && pnpm install --frozen-lockfile
  just lint
  just test
  cd projects/frontend && NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000 pnpm run build

[doc("One-shot project scaffold: bootstrap rename + install + de-templating checklist")]
[group('template')]
setup *args:
  uv run python devops/bootstrap.py {{args}}
  just install
  @uv run python devops/template_check.py || true
  @echo ""
  @echo "Scaffold ready. Next: just run-backend + just run-frontend, then work through the checklist above."

[doc("Rename template placeholders. Explicit args: --project-name ... --project-slug ... --python-package ... --non-interactive")]
[group('template')]
bootstrap *args:
  uv run python devops/bootstrap.py {{args}}

[doc("List remaining template remnants (brand strings + demo surface). Exit 0 when fully de-templated")]
[group('template')]
template-check:
  uv run python devops/template_check.py

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
