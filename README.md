# Project Instruction

Single source of truth for starting new projects with selected agents and project architectures. Combines a runnable full-stack template with instructional documentation for teams.

## What's Included

- **Runnable template:** FastAPI backend + Next.js frontend with CI, pre-commit, and dev tooling
- **Instructional docs:** Role-based templates, coding profiles, workflow guides, and reference materials (`instruction/`)
- **Unified coding rules:** `CLAUDE.md` as the enforced-rules entrypoint, with detailed references in `instruction/reference/`

## Project Structure

```text
project-instruction/
├── CLAUDE.md                     # Enforced coding rules entrypoint (links to instruction/reference/ for detail)
├── ProjectMap.md                 # Generated fast search map
├── justfile                      # Root automation commands
├── pyproject.toml                # Python workspace config
├── projects/
│   ├── backend/                  # FastAPI app (example endpoints, tests)
│   └── frontend/                 # Next.js app (MUI, React Query, Orval)
├── instruction/                  # Instructional documentation
│   ├── templates/                # 8 role-based engineering templates
│   ├── profiles/                 # Coding profiles (generic + personal examples)
│   ├── guides/                   # Workflow playbooks and scenarios
│   └── reference/                # Checklists, security patterns, architecture guides
├── .github/workflows/ci.yml     # GitHub Actions CI
├── .claude/                      # Claude Code skills and agents
├── devops/                       # Pre-commit hooks, Docker
├── docs/                         # Sphinx documentation
└── scripts/                      # Bootstrap, cleanup, project map
```

## Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv)
- [just](https://github.com/casey/just)
- Node.js 20+
- Docker (optional)

## Quick Start

```bash
just install        # Install all dependencies
just run-backend    # Start FastAPI on :8000
just run-frontend   # Start Next.js on :3000 (new terminal)
```

Open `http://localhost:3000`

## Common Commands

| Command | Description |
|---------|-------------|
| `just install` | Install Python + Node + pre-commit |
| `just run-backend` | Start FastAPI dev server |
| `just run-frontend` | Start Next.js dev server |
| `just test` | Run pytest with coverage |
| `just lint` | Run ruff lint checks |
| `just format` | Run ruff format |
| `just typecheck` | Run pyright + mypy |
| `just run-ci` | Full CI pipeline locally |
| `just generate-frontend-types` | Regenerate Orval API client |
| `just bootstrap` | Rename template placeholders |
| `just template-clean` | Remove example code after first build |
| `just project-map` | Regenerate ProjectMap.md |

## API Contract (FastAPI -> OpenAPI -> Orval -> Frontend)

1. FastAPI serves OpenAPI at `http://127.0.0.1:8000/openapi.json`
2. Frontend downloads it into `projects/frontend/openapi.json`
3. Orval generates typed models + React Query hooks into `projects/frontend/src/lib/generated/`

Regenerate after backend API changes:

```bash
just run-backend
just generate-frontend-types
```

## Template Demo Surface (Replace After Bootstrap)

Example pieces included to prove the stack works:

- Backend: `GET /health`, `GET /ready`, `POST /api/example/echo`
- Frontend: health widget, setup form on home page

After first successful build:
1. Run `just template-clean`
2. Replace template endpoints/components
3. Update `CLAUDE.md` and `ProjectMap.md` for your project

## Instructional Documentation

See `instruction/README.md` for navigation. Highlights:

- **Role templates** for systems architect, backend/frontend engineer, DevOps, PM, and more
- **Coding profiles** with domain-specific patterns and examples
- **Workflow guides** with 5 scenario playbooks (solo founder to scaling teams)
- **Reference materials** including security patterns, agentic AI architectures, and team audit checklists

## Documentation

- Coding rules: `CLAUDE.md`
- Search map: `ProjectMap.md` (regenerate with `just project-map`)
- Instructional docs: `instruction/README.md`
- Sphinx docs: `docs/` (build with `cd docs && sphinx-build -b html . _build/html`)

## License

Template scaffold provided as-is for reuse and modification.
