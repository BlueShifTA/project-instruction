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

## Development Workflow — Test-Driven Development (TDD)

Every code change follows the TDD cycle: **Red → Green → Refactor**.

Follow these phases for every change:

1. **Research** — identify affected files, understand dependencies (`rg`, `git log`)
2. **Plan** — outline approach, identify edge cases and error paths
3. **Test first** — write failing tests that define expected behavior → run → confirm RED
4. **Implement** — write minimum code to pass tests → run → confirm GREEN
5. **Refactor** — clean up implementation while tests stay green
6. **Validate** — `just lint && just typecheck && just test` must all pass before commit

**Never write implementation code before the test exists.** If you can't test it, redesign it until you can.

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

## SOLID Principles — Mandatory

All production code must satisfy SOLID. These are not suggestions — violations are architecture drift.

> **Extended examples, frontend patterns, and testing guidance:** See [`instruction/reference/SOLID_PRINCIPLES.md`](instruction/reference/SOLID_PRINCIPLES.md)

### S — Single Responsibility Principle

A class or module has exactly one reason to change. One job per unit.

```python
# WRONG — UserService does auth, email, and DB in one class
class UserService:
    def authenticate(self, token: str) -> bool: ...
    def send_welcome_email(self, user_id: int) -> None: ...
    def save_to_db(self, user: User) -> None: ...

# CORRECT — split into focused units
class AuthService:
    def authenticate(self, token: str) -> bool: ...

class EmailService:
    def send_welcome(self, user_id: int) -> None: ...

class UserRepository:
    def save(self, user: User) -> None: ...
```

**Anti-patterns:** God classes, "Manager" or "Util" blobs, modules importing from five unrelated domains.

### O — Open/Closed Principle

Open for extension, closed for modification. Add new behavior via composition or strategy — never by editing core logic.

```python
import typing as tp

class MetricExporter(tp.Protocol):
    def export(self, metrics: dict[str, float]) -> None: ...

# New backends added without touching existing code
class PrometheusExporter:
    def export(self, metrics: dict[str, float]) -> None: ...

class DatadogExporter:
    def export(self, metrics: dict[str, float]) -> None: ...

class MetricsPipeline:
    def __init__(self, exporter: MetricExporter) -> None:
        self.exporter: MetricExporter = exporter

    def flush(self, metrics: dict[str, float]) -> None:
        self.exporter.export(metrics)
```

**Anti-patterns:** `if isinstance(x, TypeA): ... elif isinstance(x, TypeB): ...` chains that grow with every new type. Editing a core class every time a new variant is needed.

### L — Liskov Substitution Principle

Subtypes must be fully substitutable for their base type without breaking behavior. If `B` extends `A`, code using `A` must work unchanged with `B`.

```python
import typing as tp

class StorageBackend(tp.Protocol):
    async def read(self, key: str) -> bytes: ...
    async def write(self, key: str, data: bytes) -> None: ...

# Both satisfy the contract — callers don't care which one they get
class S3Backend:
    async def read(self, key: str) -> bytes: ...
    async def write(self, key: str, data: bytes) -> None: ...

class LocalBackend:
    async def read(self, key: str) -> bytes: ...
    async def write(self, key: str, data: bytes) -> None: ...
```

**Anti-patterns:** Subclass raises `NotImplementedError` for a parent method. Subclass silently narrows accepted input types. Subclass returns `None` where base returns a value.

### I — Interface Segregation Principle

Many small, specific interfaces beat one fat interface. Clients should only depend on methods they actually use.

```python
import typing as tp

# WRONG — one fat protocol forces all implementors to support everything
class BigBackend(tp.Protocol):
    async def read(self, key: str) -> bytes: ...
    async def write(self, key: str, data: bytes) -> None: ...
    async def delete(self, key: str) -> None: ...
    async def list_keys(self, prefix: str) -> list[str]: ...
    async def get_metadata(self, key: str) -> dict[str, str]: ...

# CORRECT — split by usage pattern
class Readable(tp.Protocol):
    async def read(self, key: str) -> bytes: ...

class Writable(tp.Protocol):
    async def write(self, key: str, data: bytes) -> None: ...

class Listable(tp.Protocol):
    async def list_keys(self, prefix: str) -> list[str]: ...

# Combine only what a specific consumer needs
class ReadWriteBackend(Readable, Writable, tp.Protocol): ...
```

**Anti-patterns:** A Protocol with 10+ methods where most callers use 2. Forcing mock implementations to stub out irrelevant methods.

### D — Dependency Inversion Principle

High-level modules must not depend on low-level modules. Both depend on abstractions. Inject dependencies — never instantiate concrete classes inside business logic.

```python
import typing as tp

# Abstraction (Protocol) — neither side depends on the other directly
class InferenceBackend(tp.Protocol):
    async def generate(self, prompt: str) -> str: ...

# High-level service depends on the abstraction only
class PerformanceAnalyzer:
    def __init__(self, backend: InferenceBackend) -> None:
        self.backend: InferenceBackend = backend  # injected

    async def analyze(self, trace: str) -> str:
        return await self.backend.generate(f"Analyze this trace: {trace}")

# Low-level concretions — wired up at composition root, never inside PerformanceAnalyzer
class VLLMBackend:
    async def generate(self, prompt: str) -> str: ...

class OllamaBackend:
    async def generate(self, prompt: str) -> str: ...
```

**Anti-patterns:** `self.db = PostgresClient()` inside `__init__`. Importing and instantiating a concrete class at the top of a service module. Hardcoding the storage engine, HTTP client, or model provider inside business logic.

> **Note:** `Protocol`-based polymorphism (already required in this project) is the primary mechanism for DIP. See the [Protocol-based polymorphism](#protocol-based-polymorphism) section above.

### SOLID PR Checklist

Add to the standard review checklist (see "Code Review Checklist" below):

- [ ] **SRP** — does each class/module have exactly one reason to change? No god classes or "utils" blobs.
- [ ] **OCP** — can new behavior be added via extension without editing existing core logic?
- [ ] **LSP** — do all Protocol implementors honor the full contract (no silent narrowing, no surprise `NotImplementedError`)?
- [ ] **ISP** — are interfaces minimal? No client forced to depend on methods it doesn't use.
- [ ] **DIP** — do services depend on `Protocol` abstractions, with concretions injected at the composition root?

## Code Review Checklist

Before submitting a PR, verify:
- No unused functions or dead code
- All function signatures have type annotations (no `Any` unless justified)
- Internal methods prefixed with `_`
- No `print()` statements (use logging)
- All imports at module level, no unused imports
- Regression test included for bug fixes
- Pre-commit hooks pass: `uv run pre-commit run --all-files`
- SOLID compliance (see "SOLID Principles — Mandatory" section): SRP, OCP, LSP, ISP, DIP all checked

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
pnpm add -g @openai/codex

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

## Testing Philosophy — TDD First

**TDD is mandatory.** Write tests before implementation for every feature, fix, and refactor.

**Test priority order:**
1. Error paths and edge cases FIRST (these break in production)
2. Happy path second
3. Integration tests for established features, unit tests for isolated logic
4. Regression test required for every bug fix

**Coverage targets:**
- Core business logic: 95%+ (CRUD, auth, domain models)
- API routes: 90%+ (all status codes, validation errors, edge cases)
- Services: 85%+ (including failure modes)
- Frontend components: test user-facing behavior, not implementation details
- **Minimum floor: 80%** — no PR merges below this

**Execution:**
- Fast tests (no unnecessary sleep)
- Test markers: `slow`, `integration`, `unit`
- Run specific tests: `uv run pytest tests -k test_name`
- Always run full suite before commit: `just test && just lint && just typecheck`

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
