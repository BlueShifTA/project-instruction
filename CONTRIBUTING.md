# Contributing

Project Template — FastAPI + Next.js. Coding rules, workflow, and review checklist live in [CLAUDE.md](CLAUDE.md). Read it before opening a PR.

## Quick start

```bash
just install       # install backend (uv) + frontend (pnpm) + pre-commit hooks
just run-backend   # FastAPI on :8000
just run-frontend  # Next.js on :3000
```

## Before every commit

```bash
just lint && just typecheck && just test
```

All three must pass. Pre-commit hooks run these automatically — **never** use `--no-verify` or `SKIP=<hook>`.

## Pull request checklist

See [CLAUDE.md § Code Review Checklist](CLAUDE.md#code-review-checklist).

Key items:

- TDD followed (test committed before implementation)
- No `print()`, no wildcard imports, no `from __future__ import annotations`, no `if TYPE_CHECKING:` blocks
- SOLID compliance (see [`instruction/reference/SOLID_PRINCIPLES.md`](instruction/reference/SOLID_PRINCIPLES.md))
- Regression test included for bug fixes
- `just run-ci` passes locally

## Where things live

- Backend routes: `projects/backend/package/api/`
- Backend services: `projects/backend/package/services/`
- Frontend pages: `projects/frontend/src/app/`
- Frontend components: `projects/frontend/src/components/`
- Instructional docs: `instruction/` (see [`instruction/README.md`](instruction/README.md))
- Reusable coding principles and patterns: `instruction/reference/`

## Reporting issues

Use the GitHub issue tracker. Include:
- What you did
- What you expected
- What happened (stack trace, screenshot, logs)
- Environment (OS, Python/Node versions)
