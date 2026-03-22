# TEMPLATE REGISTRY

**Last Updated:** 2026-03-22
**Location:** Part of [project-instruction](../../README.md)

---

## 📚 AVAILABLE TEMPLATES

### 1. project-template

**Path:** `~/Project/project-template`  
**Type:** Full-stack monorepo  
**Best For:** Web applications with comprehensive documentation needs

**Stack:**
- **Backend:** FastAPI (Python 3.13+)
- **Frontend:** Next.js + React
- **Testing:** pytest, pytest-cov
- **Docs:** Sphinx with RTD theme
- **CI/CD:** GitHub Actions (test + docs deployment)

**Key Features:**
- ✅ Monorepo structure (`projects/backend/`, `projects/frontend/`)
- ✅ Sphinx documentation with GitHub Pages workflow
- ✅ GitHub Copilot instructions
- ✅ Comprehensive README with setup guides
- ✅ Multi-stage Docker build

**Project Structure:**
```
project-template/
├── projects/
│   ├── backend/          # FastAPI app
│   │   ├── api/
│   │   ├── package/
│   │   └── tests/
│   └── frontend/         # Next.js app
├── docs/                 # Sphinx documentation
├── devops/
│   ├── ci/
│   │   └── Dockerfile
│   └── .pre-commit-config.yaml
├── .github/
│   ├── workflows/
│   │   ├── ci.yml
│   │   └── docs.yml
│   └── copilot-instructions.md
├── pyproject.toml
├── justfile
└── README.md
```

**Unique Justfile Recipes:**
- `export-openapi` - Generate OpenAPI schema
- Documentation build commands (via Sphinx)

**When to Use:**
- New web projects requiring both API and UI
- Projects that need comprehensive documentation
- Team projects with multiple contributors

---

### 2. fastapi-nextjs-template

**Path:** `~/Project/fastapi-nextjs-template`  
**Type:** Full-stack dual-repo  
**Best For:** Simpler web apps without monorepo complexity

**Stack:**
- **Backend:** FastAPI (Python 3.13+)
- **Frontend:** Next.js + React
- **Testing:** pytest, pytest-cov
- **CI/CD:** GitHub Actions (test + build + deploy to GHCR)

**Key Features:**
- ✅ Flat structure (backend/, frontend/ at root)
- ✅ Docker Compose for local dev + production
- ✅ AGENTS.md for AI coding assistance
- ✅ Tag-based releases with `just tag`
- ✅ Separate Dockerfiles for backend/frontend

**Project Structure:**
```
fastapi-nextjs-template/
├── backend/
│   ├── app_template/     # Main package
│   │   ├── main.py
│   │   ├── api/
│   │   ├── services/
│   │   ├── domain/
│   │   └── core/
│   └── tests/
├── frontend/
│   └── app/              # Next.js App Router
├── devops/
│   ├── backend.dockerfile
│   ├── frontend.dockerfile
│   └── .pre-commit-config.yaml
├── .github/
│   └── workflows/
│       └── ci.yml
├── docker-compose.yml
├── docker-compose.prod.yml
├── AGENTS.md
├── pyproject.toml
├── justfile
└── README.md
```

**Unique Justfile Recipes:**
- `run-ci` / `ci-local` - Run full CI pipeline locally
- `docker-prod` - Production deployment
- `tag [version]` - Create and push version tags

**When to Use:**
- Straightforward web apps
- Projects prioritizing simplicity over monorepo structure
- When you want separate backend/frontend deployment

---

### 3. spinnaker-pyside-template

**Path:** `~/Project/spinnaker-pyside-template`  
**Type:** Desktop application  
**Best For:** Camera/hardware control GUIs

**Stack:**
- **UI:** PySide6 (Qt for Python)
- **Python:** 3.10 (Spinnaker SDK compatibility)
- **Hardware:** FLIR Spinnaker SDK
- **Testing:** pytest + pytest-qt
- **Deployment:** PyInstaller standalone executables

**Key Features:**
- ✅ Hardware abstraction (CameraProtocol interface)
- ✅ Mock camera for development without hardware
- ✅ Hardware-specific test markers (`@pytest.mark.hardware`)
- ✅ Auto-detection of Spinnaker SDK paths
- ✅ System service installation scripts
- ✅ Cross-platform support (macOS arm64/x86_64, Linux x86_64/aarch64)

**Project Structure:**
```
spinnaker-pyside-template/
├── src/
│   ├── app/              # Application entry
│   │   └── main.py
│   ├── camera/           # Hardware interfaces
│   │   ├── protocol.py   # Abstract interface
│   │   ├── spinnaker.py  # Real camera
│   │   ├── mock.py       # Development mock
│   │   └── discover.py   # Camera discovery
│   ├── ui/               # PySide6 widgets
│   │   ├── main_window.py
│   │   ├── viewport.py
│   │   └── controls.py
│   └── core/             # Config utilities
├── tests/
├── devops/
│   ├── sdk/              # Spinnaker wheel storage
│   ├── Dockerfile
│   ├── Dockerfile.jetson
│   ├── install.sh        # System service installer
│   ├── uninstall.sh
│   └── .pre-commit-config.yaml
├── AGENTS.md
├── pyproject.toml
├── justfile
└── README.md
```

**Unique Justfile Recipes:**
- `install-spinnaker` - Auto-detect and install Spinnaker SDK
- `install-all` - Full setup including SDK
- `sync` - Re-sync deps and reinstall Spinnaker (preserves wheel)
- `run-mock` - Run with mock camera (no hardware)
- `test-hardware` - Run hardware-dependent tests
- `discover` - Camera discovery utility
- `build-exe` - Build standalone executable (PyInstaller)
- `build-docker-jetson` - Build for Jetson platform
- `deploy-install` - Install as system service

**Special Notes:**
- **NumPy < 2.0 required** (Spinnaker compiled against 1.x)
- **macOS:** Requires `ffmpeg@2.8` (`brew install ffmpeg@2.8`)
- **Always use `just sync`** instead of `uv sync` to preserve Spinnaker wheel

**When to Use:**
- Camera/vision system control interfaces
- Hardware device GUI applications
- Desktop apps requiring Qt widgets
- Projects needing mock/real hardware switching

---

## 🔍 COMPARISON MATRIX

| Feature | project-template | fastapi-nextjs | spinnaker-pyside |
|---------|------------------|----------------|------------------|
| **Primary Use Case** | Documented web apps | Simple web apps | Desktop hardware apps |
| **Python Version** | 3.13+ | 3.13+ | 3.10 (SDK compat) |
| **Frontend** | Next.js | Next.js | PySide6 |
| **Backend** | FastAPI | FastAPI | N/A |
| **Structure** | Monorepo | Flat dual-repo | Single package |
| **Documentation** | Sphinx + README | README only | README only |
| **CI/CD** | Test + Docs | Test + Deploy | Test only |
| **Docker** | Multi-stage | Compose + prod | Multi-platform |
| **Special Features** | API docs generation | Tag versioning | Hardware abstraction |
| **Deployment** | Container | Container + GHCR | Executable + service |
| **Complexity** | High | Medium | Medium |

---

## 🛠️ COMMON PATTERNS (ALL TEMPLATES)

### Universal Tools
- **Dependency Manager:** `uv` (replaces pip/poetry/pipenv)
- **Task Runner:** `just` (replaces Makefile)
- **Linter:** `ruff` (Python) + `eslint` (TypeScript)
- **Type Checker:** `pyright` or `mypy` (Python)
- **Formatter:** `ruff format` (Python) + `prettier` (JS/TS)
- **Testing:** `pytest` with coverage
- **Pre-commit:** Hooks in `devops/.pre-commit-config.yaml`

### Universal Files
```
├── pyproject.toml              # Python config (uv-based)
├── uv.lock                     # Lockfile (committed)
├── justfile                    # Task automation
├── README.md                   # Project overview
├── devops/
│   ├── .pre-commit-config.yaml
│   └── Dockerfile
├── .github/
│   └── workflows/
│       └── ci.yml
└── .gitignore
```

### Standard Justfile Groups
1. **install** - Dependency setup + pre-commit hooks
2. **run** - Application execution
3. **test** - Test execution (with/without coverage)
4. **lint** - Code quality checks
5. **docker** - Container operations
6. **util** - Utilities (clean, tag, export)

### Standard Pre-commit Hooks
1. `ruff` - Python linting + auto-fix
2. `ruff-format` - Python formatting
3. `pyright` - Python type checking
4. `prettier` - JS/TS/JSON/YAML/Markdown formatting
5. `eslint` - Next.js linting (web templates only)
6. Standard hooks: trailing-whitespace, end-of-file-fixer, check-yaml, check-toml

### Coverage Standards
- **Minimum:** 80%
- **Command:** `just test-cov 80`
- **Reports:** Terminal + XML (for CI)
- **Exclusions:** Boilerplate (`__main__`, `TYPE_CHECKING`, etc.)

---

## ❌ MISSING COMPONENTS (NOT YET IMPLEMENTED)

### .claude/ Directory
**Status:** Not present in any template  
**Purpose:** Claude Code context and shortcuts  
**Planned Contents:**
- `CONTEXT.md` - Project-specific background
- `SHORTCUTS.md` - Common workflows
- `EXAMPLES.md` - Code pattern examples

### .devcontainer/ Directory
**Status:** Not present in any template  
**Purpose:** VS Code Dev Container configuration  
**Planned Contents:**
- `devcontainer.json` - Container config
- `Dockerfile` - Dev environment setup
- `docker-compose.yml` - Dev services

**Action Required:** Create standardized `.claude/` and `.devcontainer/` structures after Phase 1 completion.

---

## 📋 SELECTION GUIDE

### Choose **project-template** when:
- ✅ You need comprehensive documentation (Sphinx)
- ✅ Project will have external contributors
- ✅ You want monorepo structure
- ✅ Documentation site deployment required

### Choose **fastapi-nextjs-template** when:
- ✅ Simple web app (no complex docs)
- ✅ Prefer flat structure over monorepo
- ✅ Fast prototyping is priority
- ✅ Need Docker Compose for local dev

### Choose **spinnaker-pyside-template** when:
- ✅ Building desktop GUI application
- ✅ Working with cameras or hardware devices
- ✅ Need hardware abstraction layer
- ✅ Require offline/standalone deployment
- ✅ System service installation needed

---

## 🔄 TEMPLATE LIFECYCLE

### Creating New Project from Template

**Method 1: GitHub "Use this template"**
```bash
# 1. Click "Use this template" on GitHub
# 2. Clone your new repo
git clone git@github.com:username/new-project.git
cd new-project

# 3. Initialize
just install

# 4. Customize
# - Update pyproject.toml (name, version, description)
# - Update README.md
# - Replace placeholder names in code
# - Update AGENTS.md with project specifics
```

**Method 2: Local Copy**
```bash
# 1. Copy template
cp -r ~/Project/fastapi-nextjs-template ~/Projects/new-project
cd ~/Projects/new-project

# 2. Remove git history
rm -rf .git
git init
git add .
git commit -m "Initial commit from template"

# 3. Install and customize (same as above)
just install
```

### Maintaining Templates

**Update Protocol:**
1. Test changes in at least 2 projects
2. Document in MASTER_TEMPLATE.md
3. Apply to all templates
4. Update this registry
5. Commit with clear message: `chore: update template - <description>`

**Version Tracking:**
- Templates don't have version numbers
- Track by git commit hash + date
- Major changes → create git tag (`template-v1`, `template-v2`, etc.)

---

## 🎯 NEXT STEPS

### Phase 1 Remaining Tasks
- [ ] Complete <REPO> project analysis (Phase 1b-1c)
- [ ] Extract coding style patterns from lead engineer
- [ ] Create ARM_CODING_PROFILE.md
- [ ] Design .claude/ structure
- [ ] Design .devcontainer/ structure
- [ ] Add .claude/ and .devcontainer/ to all templates

### Future Enhancements
- [ ] Add example projects for each template
- [ ] Create template comparison tool
- [ ] Automated template sync script
- [ ] Template update changelog

---

**Owner:** Surapat Ek-In (Arm)
**Last Updated:** 2026-02-20 12:11 PM CET  
**Next Review:** After Phase 1 completion
