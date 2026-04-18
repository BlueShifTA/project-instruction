---
name: verify
description: Run tests, linting, and type checking to verify code changes are correct. Use after writing or modifying code, before committing, or when the user asks to check if things work.
allowed-tools: Bash, Read, Grep, Glob
argument-hint: [backend|frontend|all]
---

Verify code quality by running tests, linting, and type checking.

Scope defaults to `all` unless specified: `$ARGUMENTS`

## Steps

1. **Determine scope** from arguments:
   - `backend` — Python only
   - `frontend` — TypeScript/Node only
   - `all` or empty — both

2. **Run checks in order** (stop on first failure, report clearly):

   **Backend:**
   ```bash
   just test-backend
   just typecheck-python
   just format-check
   ```

   **Frontend:**
   ```bash
   just test-frontend
   just typecheck-frontend
   just lint-frontend
   just format-check
   ```

   **All:**
   ```bash
   just test
   just typecheck
   just lint
   ```

3. **On failure:** Read the error output, identify the root cause, and report:
   - Which check failed
   - Which file(s) and line(s)
   - A short suggestion for fixing

4. **On success:** Report concisely — e.g., "All checks passed (tests, types, lint)."
