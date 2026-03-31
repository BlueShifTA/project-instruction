# Project Instruction

Single source of truth for coding rules, project structure, and development workflow.

## What This Repo Is

Combined project scaffold and instructional documentation:
- FastAPI backend (`projects/backend/package`) + Next.js frontend (`projects/frontend`)
- MUI theme layer + React Query + Orval-generated API client
- Root `just` automation, pre-commit hooks, GitHub Actions CI
- Instructional docs: role templates, coding profiles, guides, reference materials (`instruction/`)
- AI-friendly docs (`CLAUDE.md`, generated `ProjectMap.md`)

## Runtime Layout

- Backend entrypoint: `projects/backend/package/main.py`
- Backend routers: `projects/backend/package/api/`
- Backend settings: `projects/backend/package/core/config.py`
- Frontend app router: `projects/frontend/src/app/`
- Frontend providers (MUI + React Query): `projects/frontend/src/components/layout/AppProviders.tsx`
- Frontend generated client: `projects/frontend/src/lib/generated/`
- Frontend Orval config: `projects/frontend/orval.config.ts`
- Frontend rewrites: `projects/frontend/next.config.ts`
- Root automation: `justfile`
- Instructional docs: `instruction/`

## Standard Commands

- `just install`
- `just run-backend`
- `just run-frontend`
- `just generate-frontend-types`
- `just test`
- `just lint`
- `just format`
- `just typecheck`
- `just frontend-build`
- `just frontend-typecheck`
- `just project-map`
- `just run-ci`
- `just bootstrap`
- `just template-clean`

## Template Bootstrap Flow

- Run `just bootstrap` to rename template placeholders and backend package.
- Prefer explicit args in automation:
  - `uv run python scripts/bootstrap.py --project-name "My App" --project-slug my-app --python-package my_app --non-interactive`
- Regenerate frontend API types after backend API changes:
  - `just run-backend`
  - `just generate-frontend-types`

## Template Demo Surface (Expected to Be Replaced)

- Backend example route: `POST /api/example/echo`
- Health routes: `GET /health`, `GET /ready`
- Frontend demo homepage sections in `projects/frontend/src/app/page.tsx`
- Generated client demo usage in `projects/frontend/src/components/demo/BackendHealthSection.tsx`

## Post-First-Build Cleanup (Required)

After the first successful build and smoke test:
1. Run `just template-clean`
2. Remove or replace example routes/components/tests/docs not used by the real project
3. Update `CLAUDE.md` and `ProjectMap.md` so they describe the real project (not the template)

## Development Workflow

Follow these phases for every change:

1. **Research** — identify affected files, understand dependencies (`rg`, `git log`)
2. **Plan** — outline approach before writing code
3. **Execute** — write code following this guide, format with `uv run ruff format .`
4. **QA** — `just lint && just typecheck && just test` must pass before commit

## Validation Flow

- `just test`
- `just lint`
- `just typecheck`
- `just run-ci`

## Fast Search

- Backend routes: `rg -n "APIRouter|@router" projects/backend/package`
- Backend settings/env: `rg -n "BaseSettings|SettingsConfigDict|env" projects/backend/package`
- Frontend pages: `rg -n "export default" projects/frontend/src/app`
- Frontend providers/theme: `rg -n "ThemeProvider|QueryClientProvider|appTheme" projects/frontend/src`
- Generated hook usage: `rg -n "use[A-Z].*Get|use[A-Z].*Mutation" projects/frontend/src`
- Orval config / schema flow: `rg -n "orval|openapi.json|update-api-schema" projects/frontend`
- Next rewrites: `rg -n "rewrites\\(" projects/frontend/next.config.ts`

## Python Code Style Rules

### Naming conventions

```python
snake_case          # Functions, variables, methods
_private_method     # Internal methods (prefix with _)
CONSTANT_CASE       # Module constants, enum values
PascalCase          # Classes, protocols, exceptions
_PrivateClass       # Internal implementation classes
snake_case.py       # Module names
```

### Import rules: relative within same directory, absolute across modules

Files in the **same directory** must use relative imports (`from .`).
Files importing from a **different directory** (parent or sibling module) must use absolute imports.
Never use parent-relative imports (`from ..`).

```python
# Same directory: use relative imports
from .example import router          # CORRECT
from package.api.example import router  # WRONG — same directory, use relative

# Different directory: use absolute imports
from package.domain.models import MyModel  # CORRECT
from ..domain.models import MyModel        # WRONG — never use parent-relative (..)
```

### No lazy imports

All imports must be at the top of the file. Never import inside functions, methods, `if` blocks, or any other conditional/deferred context.

### Always type-annotate class `__init__` attributes

Every `__init__` parameter and every instance attribute assignment must have explicit type annotations. The return type must be `-> None`. Use modern union syntax: `list[str] | None` (Python 3.10+). Avoid `Any` unless truly necessary.

```python
# CORRECT
class Foo:
    def __init__(self, num: int, name: str) -> None:
        self.num: int = num
        self.name: str = name

# WRONG — missing attribute annotations and return type
class Foo:
    def __init__(self, num, name):
        self.num = num
        self.name = name
```

### No module-level global instances

Never instantiate a class at module level. Instantiate inside other classes, functions, or use a singleton pattern if truly needed.

**Exception:** FastAPI `app = create_app()` at module level is permitted as it is required by ASGI servers.

```python
foo = Foo()  # WRONG — module-level global

class Boo:
    def __init__(self) -> None:
        self.foo: Foo = Foo()  # CORRECT — inside a class

def main() -> None:
    foo = Foo()  # CORRECT — inside a function
```

### Dataclass-first design

Prefer `@dataclasses.dataclass` for data structures. Use frozen dataclasses when immutable. Validate in `__post_init__`. Group related constants in a dataclass instead of scattering magic numbers.

```python
import dataclasses as dc

@dc.dataclass(frozen=True)
class AppConfig:
    host: str = "127.0.0.1"
    port: int = 8000
    max_retries: int = 3
    retry_delay: float = 1.0

@dc.dataclass
class ProcessResult:
    value: float
    status: str

    def __post_init__(self) -> None:
        assert self.value >= 0
```

### Protocol-based polymorphism

Use `typing.Protocol` for interfaces instead of abstract base classes. This provides type safety without tight coupling.

```python
import typing as tp

class StorageBackend(tp.Protocol):
    async def read(self, key: str) -> bytes: ...
    async def write(self, key: str, data: bytes) -> None: ...

def process_data(storage: StorageBackend) -> None:
    # Any class implementing read/write will satisfy this
    ...
```

### Async-first for I/O

Use `async`/`await` for all I/O operations (network, file, database). Use `asyncio.sleep()` for delays, never blocking `time.sleep()`. Use context managers for resource cleanup.

```python
async def fetch_data(url: str) -> dict[str, str]:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
```

### Retry pattern for unreliable operations

Wrap network calls and external API interactions with retry logic using exponential backoff.

```python
import asyncio
import logging

logger = logging.getLogger(__name__)

async def fetch_with_retry(
    url: str,
    max_attempts: int = 3,
    base_delay: float = 1.0,
) -> dict[str, str]:
    for attempt in range(1, max_attempts + 1):
        try:
            return await fetch_data(url)
        except (TimeoutError, ConnectionError) as exc:
            if attempt == max_attempts:
                raise
            delay = base_delay * (2 ** (attempt - 1))
            logger.warning("Attempt %d/%d failed: %s, retrying in %.1fs", attempt, max_attempts, exc, delay)
            await asyncio.sleep(delay)
    raise RuntimeError("Unreachable")
```

### Logging over print

Never use `print()` in production code. Use the `logging` module. Log with `exc_info=True` when catching exceptions.

```python
import logging

logger = logging.getLogger(__name__)

logger.info("Processing request %s", request_id)
logger.warning("Slow response: %.2fs", elapsed)
logger.error("Failed to connect", exc_info=True)
```

### Exception handling: no blind except, log before swallowing

Never catch `Exception` or `BaseException` silently. Allowed patterns:

```python
# CORRECT — re-raise after logging
try:
    result = await fetch()
except Exception:
    logger.error("Unexpected error", exc_info=True)
    raise

# CORRECT — log with exc_info=True (only when you truly need to swallow)
try:
    result = await fetch()
except Exception:
    logger.exception("Failed to fetch, continuing")

# PREFERRED — catch specific exceptions
try:
    result = await fetch()
except TimeoutError as exc:
    logger.warning("Timeout: %s", exc, exc_info=True)
    raise
```

Enforced by ruff rules `BLE001` (blind-except) and `TRY` (exception handling patterns).

### Ruff rules enforced

```
select = ["E", "W", "F", "I", "B", "C4", "UP", "ARG", "SIM", "TID", "N", "RUF",
          "ASYNC", "TRY", "BLE", "RET", "LOG", "DTZ"]
ignore = ["E501", "TRY003"]
```

Parent-relative imports (`from ..`) are banned via `ban-relative-imports = "parents"` in `[tool.ruff.lint.flake8-tidy-imports]`.

## Code Review Checklist

Before submitting a PR, verify:
- No unused functions or dead code
- All function signatures have type annotations (no `Any` unless justified)
- Internal methods prefixed with `_`
- No `print()` statements (use logging)
- All imports at module level, no unused imports
- Regression test included for bug fixes
- Pre-commit hooks pass: `uv run pre-commit run --all-files`

## Codex Policy — Claude + Codex Agent Routing

**Codex CLI** (`~/node_modules/.bin/codex`, authenticated) serves as a secondary agent for specific task types. Claude remains the primary agent for complex work.

### Agent Routing Table

| Task type | Agent | Notes |
|-----------|-------|-------|
| Adversarial review, code critique, design challenges | **Codex** | Always use Codex for reviews/critiques |
| Simple/small features, minor fixes, isolated tasks | **Codex** | 1–2 files, clear scope |
| Dev-cycle Phase 1 (audit) and Phase 6 (critic) | **Codex** | Review stages only |
| Multi-file architecture, complex features (>3 files) | **Claude** | Cross-cutting concerns |
| Research, web search, deep analysis | **Claude** | Needs tool orchestration |
| Writing (proposals, emails, documentation) | **Claude** | Needs conversation context |
| Planning, coordination (dev-cycle Phases 2–5) | **Claude** | Multi-step reasoning |
| Tasks needing MCP tools, APIs, or memory | **Claude** | Tool access required |

### Routing Decision Tree

1. Is it a review, critique, or adversarial challenge? → **Codex**
2. Is it a small, isolated change (1–2 files, clear scope)? → **Codex**
3. Does it need web search, MCP tools, or multi-step reasoning? → **Claude**
4. Does it touch >3 files or require architecture decisions? → **Claude**
5. Is it research, writing, or planning? → **Claude**
6. When in doubt → **Claude** (Codex is the secondary agent, not the default)

### How to Invoke Codex

```bash
# General task
~/node_modules/.bin/codex exec "<prompt with full context>" --dangerously-bypass-approvals-and-sandbox --ephemeral 2>&1

# Code review on uncommitted changes
~/node_modules/.bin/codex exec review --uncommitted --dangerously-bypass-approvals-and-sandbox --ephemeral 2>&1
```

Pass project-specific instructions inline or reference the project's CLAUDE.md. Codex runs in the same workspace and can read/write files.

### Installation

```bash
# Install Codex CLI
npm install -g @openai/codex

# Authenticate
codex login
# Follow browser auth flow

# Install Claude Code plugin (in Claude Code REPL)
/plugin marketplace add openai/codex-plugin-cc
/plugin install codex@openai-codex
/reload-plugins
/codex:setup
```

**Plugin skills available after install:**
- `/codex:review` — standard code review
- `/codex:adversarial-review` — challenge design decisions
- `/codex:rescue` — delegate a task to Codex in background
- `/codex:status` / `/codex:result` / `/codex:cancel` — manage Codex tasks

## Architecture & Scaling Patterns

### Middleware ordering

Middleware runs in reverse registration order. Register outermost (first-to-run) middleware first:
1. `RequestIDMiddleware` — attach request ID for log tracing
2. `RequestSizeLimitMiddleware` — reject oversized payloads before parsing
3. `CORSMiddleware` — handle cross-origin requests

See `projects/backend/package/main.py` for the reference implementation.

### Lifespan resource management

Use FastAPI's `lifespan` context manager for startup/shutdown resources (database pools, thread executors, caches). Resources created in `yield` are cleaned up on shutdown.

### Thread pool sizing

Install a bounded `ThreadPoolExecutor` via lifespan to prevent unbounded OS thread spawning under concurrent `run_in_executor` calls. Default: `min(32, cpu_count + 4)`.

### Adding new backend modules

Follow the existing layer pattern:
- `api/` — route handlers (thin, delegate to services)
- `services/` — business logic
- `domain/` — Pydantic models and domain types
- `core/` — configuration, middleware, shared utilities

## Commit Message Format

Use imperative mood. Lead with root cause. Reference issue/PR if applicable.

```
<action> <what> [<detail>]

- problem: <root cause>
- <bullet points explaining changes>
- <impact/testing notes>
```

**Action verbs:** Fix, Add, Update, Refactor, Enable

**Example:**
```
Fix boundary propagation in data pipeline

- problem: boundaries computed but not passed to processor,
  causing fallback to default checks
- fix propagation so computed boundaries are used when available
- add regression test for the fallback scenario
```

## Versioning

Semantic versioning (`vMAJOR.MINOR.PATCH`). Tag after every commit using `just tag patch|minor|major`:
- **PATCH** — small features, bug fixes, UI tweaks
- **MINOR** — new modules, significant features, API additions
- **MAJOR** — breaking changes, architectural overhauls

**Rule: always tag immediately after committing.** Never accumulate untagged commits.

## Testing Philosophy

- Maintain **80% minimum** code coverage
- **Prefer integration tests** for established features (test real behavior)
- **Unit tests** acceptable for MVP and isolated logic
- **Regression tests required** for every bug fix
- Fast execution (no unnecessary sleep)
- Test markers: `slow`, `integration`, `unit`
- Run specific tests: `uv run pytest tests -k test_name`

## Security Patterns (Summary)

Key security measures enforced in this template:
- **Request ID middleware** for log correlation (`X-Request-ID` header)
- **Request size limits** (1MB max body)
- **CORS restrictions** (no wildcards, explicit origins only)
- **Loopback bind** by default (`127.0.0.1`, not `0.0.0.0`)

For comprehensive security patterns (network, input validation, data safety, LLM safety, agent safety, thread safety), see `instruction/reference/SECURITY_PATTERNS.md`.

## Secrets & Environment Files — STRICT RULES

**NEVER read, cat, print, log, or display the contents of `.env` files.**
- Do NOT use `cat .env`, `Read .env`, `echo $SECRET`, or any command that would expose secrets
- Do NOT include `.env` contents in code suggestions, diffs, or commit messages
- If you need to check if a variable is set, use `test -f .env && grep -c "VAR_NAME" .env` (count only, not content)
- When creating `.env` files, write them via the Write tool with placeholder values only
- `.env.example` is the ONLY env file that may be read or displayed

**Environment file rules:**
- `.env` — NEVER committed, NEVER read by agents, contains real secrets
- `.env.example` — committed, contains placeholder values only, safe to read
- `.env.test` — for test environments, no real secrets, safe to read
- `.env.local` — NEVER committed, NEVER read by agents

## Instructional Documentation

Role-based templates, coding profiles, and reference materials live in `instruction/`. See `instruction/README.md` for navigation.

- **Role templates** (`instruction/templates/`): Systems architect, backend/frontend engineer, code review, DevOps, PM, communication
- **Coding profiles** (`instruction/profiles/coding-profiles/`): Data, frontend, Next.js, fullstack, reliability, systems engineer
- **Guides** (`instruction/guides/`): Getting started scenarios, solo workflow, work cycle, quality automation, quickstart
- **Reference** (`instruction/reference/`): Checklists, security patterns, agentic AI architectures, audit templates, code style analysis
- **Example profile** (`instruction/profiles/surapat/`): Personal coding profile demonstrating how to document individual preferences
