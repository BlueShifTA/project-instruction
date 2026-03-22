# Instructional Documentation

Reusable workflow templates, role-based guidance, and decision frameworks for building software teams.

For coding rules enforced in this repo, see the root [CLAUDE.md](../CLAUDE.md).

---

## Quick Start

| Goal | File | Time |
|------|------|------|
| Role clarity | `templates/[role].md` | 15 min |
| Code examples | `profiles/coding-profiles/[role].md` | 20 min |
| Team workflow | `guides/SOLO_WORKFLOW.md` | 30 min |
| Quick audit | `reference/CHECKLIST.md` | 10 min |
| Example profile | `profiles/surapat/PROFILE.md` | 20 min |
| Decision rules | `profiles/surapat/DECISIONS.md` | 15 min |
| Team scenarios | `guides/0-getting-started.md` | 45 min |

---

## By Role

### Individual Contributors

| Role | Template | Coding Profile |
|------|----------|----------------|
| Backend Engineer | `templates/3-backend-engineer.md` | `profiles/coding-profiles/data-engineer.md` |
| Frontend Engineer | `templates/4-frontend-engineer.md` | `profiles/coding-profiles/frontend-engineer.md` |
| Frontend (Next.js) | `templates/4-frontend-engineer.md` | `profiles/coding-profiles/frontend-nextjs.md` |
| Systems Engineer | `templates/2-workflow-orchestration.md` | `profiles/coding-profiles/systems-engineer.md` |
| DevOps / Reliability | `templates/6-devops-deployment.md` | `profiles/coding-profiles/reliability-engineer.md` |

### Leadership

| Role | Primary File | Secondary |
|------|-------------|-----------|
| Systems Architect | `templates/1-systems-architect.md` | `reference/TECH_DECISIONS.md` |
| Engineering Manager | `templates/8-communication-decision-making.md` | `guides/0-getting-started.md` |
| Product Manager | `templates/7-product-manager.md` | `guides/WORK_CYCLE.md` |
| Tech Lead | `templates/5-code-review-standards.md` | `profiles/surapat/PROFILE.md` |

---

## By Goal

### Starting a Project

- **Solo (1-2 people):** `guides/0-getting-started.md` (Scenario 1) + `guides/SOLO_WORKFLOW.md`
- **Small team (3-5):** `guides/0-getting-started.md` (Scenario 2) + pick 3-4 role `templates/`
- **Scaling (5-10):** `guides/0-getting-started.md` (Scenario 3) + all `templates/` + `reference/CHECKLIST.md`

### Fixing a Problem

| Problem | File | Time |
|---------|------|------|
| Slow code reviews | `templates/5-code-review-standards.md` | 2 hours |
| Team not aligned | `templates/8-communication-decision-making.md` | 1 week |
| Code quality issues | `guides/PHASE_5_AUTO_QUALITY.md` | 2 days |
| Security gaps | `reference/SECURITY_PATTERNS.md` | 4 hours |
| Bad architecture decisions | `profiles/surapat/DECISIONS.md` + `reference/TECH_DECISIONS.md` | 3 days |

---

## By Topic

- **Architecture & Design:** `templates/1-systems-architect.md`, `reference/TECH_DECISIONS.md`, `reference/AGENTIC_AI_ARCHITECTURES.md`
- **Security:** `reference/SECURITY_PATTERNS.md`, `profiles/coding-profiles/systems-engineer.md`, `profiles/coding-profiles/reliability-engineer.md`
- **Code Quality:** `templates/5-code-review-standards.md`, `guides/PHASE_5_AUTO_QUALITY.md`, `reference/CODE_STYLE_ANALYSIS.md`
- **Team Management:** `templates/8-communication-decision-making.md`, `guides/WORK_CYCLE.md`, `reference/CHECKLIST.md`
- **Deployment & Operations:** `templates/6-devops-deployment.md`, `profiles/coding-profiles/reliability-engineer.md`

---

## By Audience

- **Solo founders (2 hours):** `guides/0-getting-started.md` (Scenario 1) -> `guides/SOLO_WORKFLOW.md` -> `guides/PROJECT_QUICKSTART.md`
- **Engineering managers (4 hours):** `guides/0-getting-started.md` (Scenario 3) -> all `templates/` -> `reference/CHECKLIST.md` monthly
- **New team members (1 week):** `guides/0-getting-started.md` (Scenario 2) -> your role template -> your coding profile
- **Architects (8 hours):** `templates/1-systems-architect.md` -> `reference/TECH_DECISIONS.md` -> `reference/AGENTIC_AI_ARCHITECTURES.md`
- **Code reviewers (3 hours):** `templates/5-code-review-standards.md` -> all `profiles/coding-profiles/` -> `reference/CODE_STYLE_ANALYSIS.md`

---

## Search by Keyword

| Keyword | Files |
|---------|-------|
| Agentic AI / Frameworks | `reference/AGENTIC_AI_ARCHITECTURES.md` |
| API design | `templates/3-backend-engineer.md`, `profiles/coding-profiles/data-engineer.md` |
| Code review | `templates/5-code-review-standards.md`, `reference/CODE_STYLE_ANALYSIS.md` |
| Security | `reference/SECURITY_PATTERNS.md`, `profiles/coding-profiles/systems-engineer.md` |
| CI/CD | `templates/6-devops-deployment.md`, `guides/PHASE_5_AUTO_QUALITY.md` |
| Database | `profiles/coding-profiles/data-engineer.md`, `profiles/surapat/DECISIONS.md` |
| Frontend | `templates/4-frontend-engineer.md`, `profiles/coding-profiles/frontend-engineer.md` |
| Scaling | `guides/0-getting-started.md`, `templates/1-systems-architect.md` |
| Testing | `templates/4-frontend-engineer.md`, `guides/PHASE_5_AUTO_QUALITY.md` |

---

## Directory Structure

```
instruction/
├── profiles/
│   ├── surapat/                   # Example personal profile
│   │   ├── PROFILE.md             # Coding style, tools, patterns
│   │   ├── DECISIONS.md           # Tech decision rules
│   │   └── WORKFLOWS.md           # Workflow + process
│   └── coding-profiles/           # Generic engineer profiles
│       ├── data-engineer.md
│       ├── frontend-engineer.md
│       ├── frontend-nextjs.md
│       ├── fullstack-architect.md
│       ├── reliability-engineer.md
│       └── systems-engineer.md
├── templates/                     # Role-based guidance
│   ├── 1-systems-architect.md
│   ├── 2-workflow-orchestration.md
│   ├── 3-backend-engineer.md
│   ├── 4-frontend-engineer.md
│   ├── 5-code-review-standards.md
│   ├── 6-devops-deployment.md
│   ├── 7-product-manager.md
│   └── 8-communication-decision-making.md
├── guides/                        # Workflow playbooks
│   ├── 0-getting-started.md       # 5 entry scenarios
│   ├── SOLO_WORKFLOW.md
│   ├── WORK_CYCLE.md
│   ├── PHASE_5_AUTO_QUALITY.md
│   └── PROJECT_QUICKSTART.md
└── reference/                     # Checklists & standards
    ├── CHECKLIST.md
    ├── SECURITY_PATTERNS.md
    ├── AGENTIC_AI_ARCHITECTURES.md
    ├── AUDIT_TEMPLATE.md
    ├── CODE_STYLE_ANALYSIS.md
    ├── PATTERNS.md
    ├── TECH_DECISIONS.md
    └── TEMPLATE_REGISTRY.md
```

---

## Contributing

To add your personal profile:
1. Create `profiles/[your-name]/` directory
2. Add `PROFILE.md` (coding style), `DECISIONS.md` (tech decisions), `WORKFLOWS.md` (process)
3. Keep `templates/` generic for team-wide use
