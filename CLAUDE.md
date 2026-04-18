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

- **Before anything:** verify RTK is active on the dev laptop: `rtk --version && rtk gain`
  - RTK is the token-saving CLI proxy — all Bash commands route through it automatically via hook
  - If missing: see `~/.claude/RTK.md` for install instructions
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

## Core Coding Principles (Karpathy-inspired)

These 4 principles apply to EVERY coding task. They are not optional.

1. **Think Before Coding** — State assumptions explicitly. Surface tradeoffs. Don't hide confusion — ask before implementing.
2. **Simplicity First** — Minimum code solving the problem. No speculative features. Ask: "Would a senior engineer say this is overcomplicated?"
3. **Surgical Changes** — Touch only what you must. Match existing style. No drive-by refactoring. Every changed line traces to the request.
4. **Goal-Driven Execution** — Define verifiable success criteria before starting. "Fix bug" → "Write failing test, make it pass." Loop until verified.

> **Full rationale and examples:** See [`instruction/reference/CODING_PRINCIPLES.md`](instruction/reference/CODING_PRINCIPLES.md)

---

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

> **Full reference:** [`instruction/reference/PYTHON_STYLE.md`](instruction/reference/PYTHON_STYLE.md)

**Enforced rules (summary):**
- `snake_case` functions/vars, `PascalCase` classes, `CONSTANT_CASE` module constants, `_private` prefix for internal
- Relative imports within the same directory; absolute imports across modules; no `from ..` parent-relative imports
- All imports at file top — no lazy, no wildcard, no `from __future__ import annotations`, no `if TYPE_CHECKING:` blocks
- Every `__init__` parameter and attribute must be type-annotated; return type `-> None`
- No module-level *mutable service instances* (DB clients, API clients, etc.); module constants (`ROOT = Path(...)`, `logger = getLogger(...)`) and `app = create_app()` for ASGI are permitted
- Prefer `@dataclass` for data structures; `TypedDict` for JSON shapes (all fields key-required, `X | None` for nullable)
- `typing.Protocol` for interfaces, not ABCs
- `async`/`await` for all I/O; `asyncio.sleep()` not `time.sleep()`
- `logging` not `print()`; never silent `except Exception`; catch specific exceptions
- Ruff: `select = ["E","W","F","I","B","C4","UP","ARG","SIM","TID","N","RUF","ASYNC","TRY","BLE","RET","LOG","DTZ"]`, `ignore = ["E501","TRY003"]`

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

## Refactor Discipline — Mandatory

A refactor is a change that preserves behavior while improving a measurable property (LOC, complexity, type safety, test coverage, performance). These rules exist because **"simpler" is a claim that must be backed by evidence**, not a vibe.

### Pin the contract before refactoring

Before any refactor that touches a consumed surface — public API, CLI, exit codes, return shapes, stderr text, external message formats, anything a caller branches on — write functional tests that capture the **current observed behavior**, not the intended behavior. Land them as a separate commit BEFORE touching the code under refactor.

```bash
# Step 0 of every refactor: pin the contract
git checkout -b refactor/foo
# Write contract tests that pin observed behavior
just test   # all green
git commit -m "test: pin <surface> contract"
# Only NOW start the actual refactor
```

Every iteration's verification gate runs the contract tests. A refactor that breaks a contract test is rejected on the spot, not justified with a prose explanation.

### Measure the metric you're selling

If a refactor is sold as "simpler", "smaller", "faster", or "more maintainable", measure that metric at **every iteration**, not just at the end.

```bash
wc -l src/**/*.py            # before any iteration
wc -l src/**/*.py            # after each iteration — compare to baseline
```

If the metric moves the wrong direction, **name the trade-off upfront** and get explicit sign-off before continuing. A refactor that silently grows LOC by 30 % while the author talks about "cleaner structure" is a process failure, even if every individual change is defensible. When growing LOC is the correct call (e.g. trading brevity for type safety), say so in the commit message: `+N lines, traded brevity for X`.

### Extract only when the helper is smaller than the duplication

Before extracting a shared helper, compute the ROI:

```
helper_size_lines  <  per_site_duplication_lines  ×  number_of_sites
```

Example: three call sites each duplicate 5 lines = 15 lines of duplication. A 40-line shared helper is a **25-line loss** even though it "removes duplication". Keep the duplication unless the helper pays for itself at today's call-site count — not at hypothetical future call sites.

### Preserve defensive fallbacks

When the old code has a defensive branch (`if isinstance(x, int) else fallback`, `.get(key) or default`, `try/except SpecificError: return sentinel`), preserve **every branch** in the refactor — not just the happy path.

```python
# WRONG — "equivalent" refactor collapses the fallback
def _extract_total(body: Response) -> int:
    return body["meta"]["page"]["total_count"]   # KeyErrors on real wire data

# CORRECT — every old branch survives
def _extract_total(body: Response, fallback: int) -> int:
    meta = body.get("meta")
    if meta is None:
        return fallback
    page = meta.get("page")
    if page is None:
        return fallback
    total = page.get("total_count")
    if total is None:
        return fallback
    return total
```

The old fallbacks exist for reasons you cannot see from inside the refactor. Adversarial review (next rule) is the backup when you're wrong about which branches are unreachable.

### Adversarial review per iteration, not once at the end

After every iteration's verification gate passes, run an adversarial review from an agent that did NOT write the code — Codex, a second Claude session, or a human reviewer. Findings are to-fix items, not suggestions. Ignore only with a written reason in the commit message.

Reviewing once at the end misses regressions that stacked across iterations. Per-iteration review catches them while the change is still small enough to revert cheaply.

### Never skip the verification gate

`just lint && just typecheck && just test` must all pass on the current working tree before every commit. **Never** use `--no-verify`, `git commit --no-verify`, `SKIP=<hook>`, or any other bypass. If a pre-commit hook fails, fix the root cause — don't route around it.

### Present alternatives at the plan stage

When a refactor has two reasonable directions (e.g. "shared helper vs. inline at each site", "TypedDict vs. Protocol", "per-kind union vs. single shape"), present BOTH at the plan stage and let the user pick. Don't commit to a direction unilaterally. Guessing costs 30 minutes of rework when the user disagrees; asking costs 10 seconds.

## Code Review Checklist

Before submitting a PR, verify:
- No unused functions or dead code
- All function signatures have type annotations (no `Any` unless justified)
- Internal methods prefixed with `_`
- No `print()` statements (use logging)
- All imports at module level, no unused imports, no `from foo import *`, no `from __future__ import annotations`, no `if TYPE_CHECKING:` blocks
- Regression test included for bug fixes
- Pre-commit hooks pass: `uv run pre-commit run --all-files` (no `--no-verify`, no `SKIP=<hook>`)
- SOLID compliance (see "SOLID Principles — Mandatory" section): SRP, OCP, LSP, ISP, DIP all checked
- **TypedDict discipline** — no `dict[str, object]` / `dict[str, Any]` / `Mapping[str, object]`, no `NotRequired[X]`, no `total=False`, no `cast(Type, {...})`; JSON casts at the seam with bare type names
- **Test construction** — no tautological tests (isinstance-after-construction, callable-on-def, parametrize-over-self, `inspect.signature` existence checks); CLI tests go through `CliRunner.invoke`
- **Refactor discipline** — contract tests pinned before any public-surface change; LOC / complexity measured before and after; helper-extraction ROI verified (helper_size < duplication × sites); defensive fallbacks preserved from the old code

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

## Project Skills & Agents

Local skills live in `.claude/skills/<name>/SKILL.md`; local agents in `.claude/agents/<name>.md`. The harness surfaces them at session start — use this table as the routing map when a task matches.

**Always prefer an existing skill or `just` recipe over open-coding the equivalent commands.** If the task has a skill, call it instead of retyping the Bash.

### Skills (invoke with `/<name>`)

| Skill | Use when | Under the hood |
|-------|----------|----------------|
| `/install-deps` | Setting up, after pulling, imports fail | `just install` |
| `/run-dev` | Start backend/frontend servers | `just run-backend` / `run-frontend` |
| `/generate-types` | After changing backend API shape | `just generate-frontend-types` |
| `/format-code` | Before commit, after writing code, lint fails | `just format` |
| `/verify` | Confirm tests + types + lint pass | `just test` + `typecheck` + `lint` |
| `/ci` | Final check before PR | `just run-ci` |
| `/karpathy-check` | Catch over-engineering, drive-by edits, untested claims | `git diff` + `rg` (review-only) |
| `/simplify` | Kill dead code, DRY violations, quality issues | git + Edit, per-file lint, then `just test` + `typecheck` + `lint` |
| `/brutal-critic` | Adversarial review (`code`, `ux`, `architecture`, `security`) | spawns `read-only` agent; `ux` also calls `/screenshot` |
| `/dev-cycle` | Full audit → fix → verify → critic pass | chains `code-fixer` agents + Codex |
| `/research` | Deep source-backed doc on a topic | `WebFetch` (prefer) / `WebSearch` |
| `/autoresearch` | Bounded goal-directed iteration (≤20 rounds) | git branch + per-iteration verify |
| `/screenshot` | Visual QA or before UX review | Playwright (desktop + mobile) |
| `/seed-data` | Populate a fresh DB for testing/demo | OpenAPI + `curl` |

### Agents (spawn via `Agent(subagent_type=…)`)

| Agent | Purpose |
|-------|---------|
| `code-fixer` | Fix one disjoint workstream from a dev-cycle audit — edits only its assigned files. |
| `template-maintainer` | Maintain the template scaffold (bootstrap, cleanup, docs sync). |

### Routing shortcuts

- **Bug fix** → write failing test → fix → `/verify` → `/karpathy-check` (triage drift)
- **New feature** → TDD → `/verify` → `/format-code` → `/ci`
- **Cleanup sweep** → `/simplify` (already chains `/format-code` + `/verify`)
- **Before PR** → `/ci`
- **After backend API change** → `/generate-types`
- **Second opinion** → `/brutal-critic` or Codex (`~/node_modules/.bin/codex exec review --uncommitted ...`)

## Architecture & Scaling Patterns

> **Full reference:** [`instruction/reference/FASTAPI_PATTERNS.md`](instruction/reference/FASTAPI_PATTERNS.md)

**Enforced patterns (summary):**
- Middleware registers outermost-first: `RequestIDMiddleware` → `RequestSizeLimitMiddleware` → `CORSMiddleware` (runs innermost-first at request time)
- Use FastAPI `lifespan` for startup/shutdown resources (DB pools, thread executors, caches)
- Bounded `ThreadPoolExecutor` via lifespan: `min(32, cpu_count + 4)` — prevents unbounded thread spawning
- Layer pattern: `api/` (thin handlers) → `services/` (business logic) → `domain/` (Pydantic models) → `core/` (config, middleware)
- All CLIs use a shared `run_cli(fn, handlers)` error boundary — no per-CLI `try/except` ladders; exit codes are public contract

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

**Functional tests only.** Every test must exercise a real code path through its public interface and assert on observable behavior (return value, HTTP response, rendered DOM text, exit code, side effect). Tests of structure — "component is a function", "class has method X", "the signature accepts parameter Y" — are banned (see "Banned test shapes" below). If a test fails, production code must have broken; if renaming a type can break the test, the test is structural, not functional.

- **Backend** — call the endpoint/function and assert on the response body, status code, or observable side effect (e.g. row in DB, log line, event emitted). Prefer `TestClient` / `CliRunner` / real function invocation over poking internals.
- **Frontend** — render the component with its real providers (React Query, theme) and assert on the user-facing DOM (text, roles, aria labels). Never assert on state hooks, prop types, or implementation details.

**Test priority order:**
1. Error paths and edge cases FIRST (these break in production)
2. Happy path second
3. Regression test required for every bug fix

**Coverage targets:**
- Core business logic: 95%+ (CRUD, auth, domain models)
- API routes: 90%+ (all status codes, validation errors, edge cases)
- Services: 85%+ (including failure modes)
- Frontend components: cover each rendered state (loading, error, success, empty) via DOM assertions
- **Minimum floor: 80%** — no PR merges below this

**Execution:**
- Fast tests (no unnecessary sleep)
- Test markers (backend): `slow`, `integration`
- Run specific tests: `uv run pytest tests -k test_name` (backend), `pnpm run test -- <pattern>` (frontend)
- Always run full suite before commit: `just test && just lint && just typecheck`
- `just test` runs both backend (`pytest`) and frontend (`vitest`) — neither is optional

### Test design rules — what a test must prove

Every test must exercise a real code path whose failure would cause a real bug. Before writing a test, answer: **what line of production code would have to break for this test to fail?** If the answer is "none, just a type rename", the test is tautological and must be deleted or rewritten.

**Banned test shapes:**

```python
# WRONG — isinstance check right after construction is trivially true
def test_foo_is_foo() -> None:
    f = Foo(x=1)
    assert isinstance(f, Foo)   # BANNED — constructor already proves this

# WRONG — callable check on a def-declared function
def test_fn_is_callable() -> None:
    assert callable(my_function)   # BANNED — def makes it callable

# WRONG — parametrize over a set and assert membership in the same set
@pytest.mark.parametrize("status", ["ok", "error"])
def test_status_in_enum(status: str) -> None:
    assert status in {"ok", "error"}   # BANNED — tautology

# WRONG — inspect.signature to check a parameter exists
def test_has_param() -> None:
    sig = inspect.signature(fn)
    assert "key" in sig.parameters   # BANNED — call fn(key=...) instead

# WRONG — assert issubclass on a dataclass hierarchy you just defined
def test_error_is_value_error() -> None:
    assert issubclass(MyError, ValueError)   # BANNED — class shape, not behavior
```

**Required test shapes:**

- **CLI tests go through the test runner.** `CliRunner.invoke` (click) or `subprocess.run`. Never bypass to internal helpers. The exit code, stdout, and stderr are the contract — only end-to-end invocation proves it.
- **Fixtures must match the real wire format** of whatever external API they simulate. Include every field the TypedDict declares (with `None` where null). A fixture that omits a required field is lying about what the cast accepts.
- **Mock objects used as context managers must configure `__enter__` / `__exit__` explicitly.** `mock.__enter__.return_value = mock` — otherwise `with fake as inner:` yields a different mock than the one the test configured.
- **Before monkeypatching, trace the execution order inside the target function.** A guard injected at call position 2 doesn't catch things that happen at position 3+. Read the source of the function under test before writing the patch.
- **Contract tests BEFORE refactor.** See the Refactor Discipline section below — before touching any code that produces exit codes, JSON shapes, stderr phrases, or error messages an external caller branches on, write functional tests that pin the CURRENT observed behavior under its own commit.

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
- **Reference** (`instruction/reference/`):
  - [`CODING_PRINCIPLES.md`](instruction/reference/CODING_PRINCIPLES.md) — Karpathy-inspired behavioral guidelines
  - [`PYTHON_STYLE.md`](instruction/reference/PYTHON_STYLE.md) — full Python style rules (naming, imports, typing, ruff)
  - [`FASTAPI_PATTERNS.md`](instruction/reference/FASTAPI_PATTERNS.md) — FastAPI middleware, lifespan, CLI patterns
  - [`SOLID_PRINCIPLES.md`](instruction/reference/SOLID_PRINCIPLES.md) — extended SOLID examples and testing guidance
  - [`SECURITY_PATTERNS.md`](instruction/reference/SECURITY_PATTERNS.md) — network, input, data, LLM, agent safety
  - [`CHECKLIST.md`](instruction/reference/CHECKLIST.md) — quarterly team audit scorecard
  - [`AGENTIC_AI_ARCHITECTURES.md`](instruction/reference/AGENTIC_AI_ARCHITECTURES.md) — multi-agent design patterns
  - [`PATTERNS.md`](instruction/reference/PATTERNS.md), [`STRUCTURE.md`](instruction/reference/STRUCTURE.md), [`AUDIT_TEMPLATE.md`](instruction/reference/AUDIT_TEMPLATE.md), [`CODE_STYLE_ANALYSIS.md`](instruction/reference/CODE_STYLE_ANALYSIS.md)
- **Example profile** (`instruction/profiles/surapat/`): Personal coding profile — **replace or delete after bootstrapping** (`just template-clean` will remind you)
