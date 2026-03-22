# Project Maintainer

Agent for maintaining the project-instruction repository (merged template + instructional docs).

## Quick Start

Use root `just` commands:
- `just install` — install all dependencies
- `just lint` — run ruff lint
- `just test` — run pytest with coverage
- `just typecheck` — run pyright + mypy
- `just run-ci` — full CI pipeline locally

## Key Files (read in order)

1. `CLAUDE.md` — single source of truth for coding rules
2. `ProjectMap.md` — fast search map
3. `justfile` — all automation recipes
4. `instruction/README.md` — instructional docs navigation

## Repository Structure

This repo combines two concerns:
- **Runnable template** (`projects/backend/`, `projects/frontend/`) — FastAPI + Next.js scaffold
- **Instructional docs** (`instruction/`) — role templates, coding profiles, guides, reference materials

## Maintenance Rules

- When coding rules change in `CLAUDE.md`, update the code examples in `projects/` for consistency
- When adding new patterns to the template, document them in `CLAUDE.md`
- Keep `instruction/` docs generic — personal/domain-specific content goes in `instruction/profiles/[name]/`
- Run `just project-map` after structural changes to regenerate `ProjectMap.md`

## Template Lifecycle

- Customize with `just bootstrap` (renames placeholders)
- After first successful build: `just template-clean` (removes example code)
- Update `CLAUDE.md` and `ProjectMap.md` to describe the real project
