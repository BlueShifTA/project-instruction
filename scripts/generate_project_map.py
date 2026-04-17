import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]


def _detect_backend_package() -> str:
    backend = ROOT / "projects" / "backend"
    for candidate in sorted(backend.iterdir()):
        if candidate.is_dir() and (candidate / "main.py").exists():
            return candidate.name
    return "package"


def _detect_project_slug() -> str:
    pyproject = ROOT / "pyproject.toml"
    if pyproject.exists():
        for line in pyproject.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("name") and "=" in line:
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ROOT.name


def main() -> int:
    slug = _detect_project_slug()
    pkg = _detect_backend_package()

    content = f"""# ProjectMap

Fast search map for `{slug}`.

## Top-Level Map

```text
{slug}/
├── CLAUDE.md                  # Enforced coding rules entrypoint
├── ProjectMap.md
├── justfile
├── pyproject.toml
├── devops/
├── docs/
├── instruction/               # Instructional documentation
│   ├── profiles/              # Personal + generic coding profiles
│   ├── templates/             # 8 role-based engineering templates
│   ├── guides/                # Workflow playbooks
│   └── reference/             # Checklists, security, architecture
├── projects/
│   ├── backend/
│   │   ├── {pkg}/
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

- Backend app: `projects/backend/{pkg}/main.py`
- Frontend app page: `projects/frontend/src/app/page.tsx`
- Frontend providers: `projects/frontend/src/components/layout/AppProviders.tsx`
- Root commands: `justfile`

## Key Config

- Root Python/tooling: `pyproject.toml`
- Backend package config: `projects/backend/pyproject.toml`
- Backend settings: `projects/backend/{pkg}/core/config.py`
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

- Find API routes: `rg -n "APIRouter|@router" projects/backend/{pkg}`
- Find settings/env: `rg -n "BaseSettings|env" projects/backend/{pkg}`
- Find tests by feature: `rg -n "test_" projects/backend/tests`
- Find frontend entrypoints: `rg -n "export default" projects/frontend/src/app`
- Find frontend providers/theme: `rg -n "ThemeProvider|QueryClientProvider|appTheme" projects/frontend/src`
- Find generated hooks usage: `rg -n "use[A-Z].*Get|use[A-Z].*Mutation" projects/frontend/src`
- Find OpenAPI/orval config: `rg -n "orval|openapi.json|update-api-schema" projects/frontend`
- Find template placeholders: `rg -n "Project Template|project-template|package" .`
"""

    (ROOT / "ProjectMap.md").write_text(content, encoding="utf-8")
    print(f"Updated ProjectMap.md (project={slug!r}, backend_pkg={pkg!r})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
