from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]


CONTENT = """# ProjectMap

Fast search map for `project-template`.

## Top-Level Map

```text
project-template/
├── CLAUDE.md
├── ProjectMap.md
├── justfile
├── pyproject.toml
├── devops/
├── docs/
├── projects/
│   ├── backend/
│   │   ├── package/
│   │   │   ├── api/
│   │   │   ├── core/
│   │   │   ├── domain/
│   │   │   └── services/
│   │   └── tests/
│   └── frontend/
│       ├── openapi.json
│       ├── orval.config.ts
│       └── src/
│           ├── app/
│           ├── components/
│           ├── lib/generated/
│           └── theme/
└── scripts/
```

## Entrypoints

- Backend app: `projects/backend/package/main.py`
- Frontend app page: `projects/frontend/src/app/page.tsx`
- Frontend providers: `projects/frontend/src/components/layout/AppProviders.tsx`
- Root commands: `justfile`

## Key Config

- Root Python/tooling: `pyproject.toml`
- Backend package config: `projects/backend/pyproject.toml`
- Backend settings: `projects/backend/package/core/config.py`
- Frontend package config: `projects/frontend/package.json`
- Frontend rewrites: `projects/frontend/next.config.ts`
- Frontend Orval config: `projects/frontend/orval.config.ts`
- Pre-commit: `devops/.pre-commit-config.yaml`
- CI: `.github/workflows/ci.yml`
- Docs deploy: `.github/workflows/docs.yml`

## Tests

- Backend tests: `projects/backend/tests/`

## Standard Commands

- `just install`
- `just run-backend`
- `just run-frontend`
- `just test`
- `just lint`
- `just typecheck`
- `just generate-frontend-types`
- `just run-ci`
- `just bootstrap`
- `just template-clean`
- `just project-map`

## Search Recipes

- Find API routes: `rg -n "APIRouter|@router" projects/backend/package`
- Find settings/env: `rg -n "BaseSettings|env" projects/backend/package`
- Find tests by feature: `rg -n "test_" projects/backend/tests`
- Find frontend entrypoints: `rg -n "export default" projects/frontend/src/app`
- Find frontend providers/theme: `rg -n "ThemeProvider|QueryClientProvider|appTheme"
  " projects/frontend/src`
- Find generated hooks usage: `rg -n "use[A-Z].*Get|use[A-Z].*Mutation" projects/frontend/src`
- Find OpenAPI/orval config: `rg -n "orval|openapi.json|update-api-schema" projects/frontend`
- Find template placeholders: `rg -n "Project Template|project-template|package" .`
"""


def main() -> int:
    (ROOT / "ProjectMap.md").write_text(CONTENT, encoding="utf-8")
    print("Updated ProjectMap.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
