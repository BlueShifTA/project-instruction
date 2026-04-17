---
name: dev-cycle
description: Full development cycle — audit, plan, parallel fix, test, critic review. Use when user says "dev cycle", "fix cycle", or "audit and fix".
allowed-tools: Bash, Read, Grep, Glob, Agent, Write, Edit
argument-hint: [target-path]
---

Run a complete development cycle: audit the codebase, plan fixes, execute in parallel, verify, and re-review.

Target path: `$ARGUMENTS` (defaults to project root)

## Phase 1: Audit (Critic Review)

Spawn a **critic agent** (`subagent_type: read-only`, `model: sonnet`) to review the target path:

- Scan for bugs, code smells, type errors, security issues, dead code
- Classify each issue: **P0** (breaks functionality), **P1** (significant bug/smell), **P2** (minor improvement), **P3** (nit/style)
- Output a structured issues list with file paths, line numbers, and descriptions
- Save the audit report to a temporary file for Phase 2

## Phase 2: Plan (Group into Workstreams)

Analyze the audit report and group issues into **workstreams by file overlap**:

- Each workstream owns a **disjoint set of files** — zero overlap between workstreams
- If two issues touch the same file, they must be in the same workstream
- Assign a clear description and issue list to each workstream
- Limit to 4-5 parallel workstreams maximum

## Phase 3: Parallel Fix

Spawn one **fix agent per workstream** (`subagent_type: general`, `model: sonnet`, `bypassPermissions: true`):

- Each agent receives: its workstream description, issue list, and the exact files it owns
- Each agent fixes all issues in its workstream, editing only its assigned files
- Agents must NOT touch files outside their workstream
- `bypassPermissions` is required so agents can edit files without approval prompts

Wait for all fix agents to complete before proceeding.

## Phase 4: Verify

Run the full verification suite:

```bash
just test
just lint
just typecheck
```

If any check fails:
- Identify which workstream's changes caused the failure
- Spawn a targeted fix agent for those files only
- Re-run verification until all checks pass

## Phase 5: Final Critic Review

Spawn a fresh **critic agent** (`subagent_type: read-only`, `model: sonnet`) to re-review:

- Review all changes made during Phase 3 (use `git diff` to scope the review)
- Apply the same P0-P3 classification
- If **any P0 issues** are found, loop back to Phase 3 with a new workstream for those issues
- P1-P3 issues are noted in the report but do not block completion

## Phase 6: Report

Produce a summary report:

| Metric | Value |
|--------|-------|
| Issues found (audit) | count by severity |
| Issues fixed | count |
| Tests before/after | pass/fail counts |
| Remaining P1+ issues | list if any |
| Files modified | list |

## Rules

- **Zero file overlap** between parallel agents is mandatory — violations cause merge conflicts
- **Always run verification** after fixes — never skip Phase 4
- **P0 in final review triggers re-fix** — the cycle does not complete with P0s outstanding
- **Do not modify test files** unless the issue is specifically about broken tests
- **Preserve existing code style** — match indentation, naming conventions, import patterns
