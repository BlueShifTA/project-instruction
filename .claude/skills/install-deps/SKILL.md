---
name: install-deps
description: Install project dependencies. Use when setting up the project, after pulling changes, when dependencies change, or when imports fail.
disable-model-invocation: true
allowed-tools: Bash
argument-hint: [backend|frontend|all]
---

Install project dependencies using the project's package managers.

Scope defaults to `all` unless specified: `$ARGUMENTS`

## Steps

1. **Determine scope** from arguments:
   - `backend` → `just install-backend`
   - `frontend` → `just install-frontend`
   - `all` or empty → `just install`

2. Run the appropriate install command.

3. If install fails, read the error and suggest fixes (e.g., missing system deps, node version mismatch, lockfile conflicts).

4. Report success with a brief summary.
