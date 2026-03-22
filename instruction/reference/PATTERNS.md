# PATTERNS.md — Engineering Behavioral & Technical Patterns

---

## Confirmed Patterns

### 1. Anti-Hallucination Protocol is Primary Directive
AI agents fabricate progress ("87% production-ready" with seeded data). Always validate end-to-end before signaling completion. "Code exists" ≠ "it works" — run it and prove it.

### 2. Pragmatic Solutions Beat Perfect Code
Compose working pieces rather than rebuilding from scratch. Prefer battle-tested solutions (subprocess wrappers, proven libraries) even if not custom-fit. "Compose working pieces > rebuild from scratch."

### 3. Memory Acts as Distributed State Machine
Daily logs and persistent memory enable context recovery across sessions. Without them, work duplicates and diverges. Always search memory before committing to new work.

### 4. Hardware Embodiment Unlocks New Problem Classes
Each new capability layer (move → stream → control → record → infer) introduces a new problem class. Can't reuse prior debugging patterns. Expect: safety constraints → sensor fusion → inference timing as emerging problem classes.

### 5. Cost Structure Drives Architecture Decisions
When costs become visible, they change priorities. Context-loading costs can dominate total spend (e.g., 98%+ of token cost). Make costs visible early — they shift architectural decisions.

### 6. Template-Driven Development Compresses MVP Time
Reusable templates skip scaffolding overhead and deliver working software in hours, not days. Template ROI is confirmed — TEMPLATE_REGISTRY.md is strategic.

### 7. Safety-First Testing is Non-Negotiable for Physical Systems
When controlling physical hardware via UI, write safety tests FIRST, ship AFTER all pass. The test-coverage threshold doubles when hardware actuation is involved. A UI bug that sends wrong values isn't a crash — it's broken hardware.

---

## Emerging Patterns

### 8. Sub-Agent Refactoring Works But Needs Audit
Multi-agent parallel refactoring is fast but leaves cross-cutting issues: dead code, stale references, migration order violations. Structural work happens fast; integration testing must follow.

### 9. Tracing to Data Source Beats Debugging the Pipeline
When a pipeline breaks, don't debug backwards from the sink — trace to where data ORIGINATES. The root cause is usually at the source, not in the middle.

---

## Decision-Making Template

When deciding between options:
1. Strong preference for **working pragmatic** over elegant theoretical
2. Demand for **end-to-end validation** before closure
3. Comfort with **deferral** over perfect execution
4. Reference to **memory files** before committing to new work (always search first)
