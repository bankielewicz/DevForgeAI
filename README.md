# DevForgeAI - Spec-Driven Development Framework

> **Transform vague business ideas into production-ready code with zero technical debt.**

An intelligent, constraint-enforced software development framework for Claude Code Terminal that orchestrates the entire development lifecycle—from ideation through production deployment—while maintaining strict quality standards and respecting user authority.

---

## What is DevForgeAI?

DevForgeAI is a **meta-framework that teaches AI how to build software systematically**. It solves a critical problem: unguided AI development leads to chaos—autonomous decisions, technical debt, and architectural violations.

DevForgeAI fixes this through:
- **Constitutional Guardrails** — 6 immutable context files govern ALL development
- **Spec-Driven Development** — Requirements are the law; code follows specs exactly
- **TDD Mandatory** — Tests BEFORE implementation (Red → Green → Refactor)
- **User Authority** — No autonomous decisions on important matters
- **Quality Gates** — Strict validation at each workflow transition
- **Zero Autonomous Deferrals** — No work deferred without user approval

**Current Status:** Production Ready (v1.0.1)

---

## Installation

Install DevForgeAI globally via npm:

```bash
npm install -g devforgeai
```

Then install the framework in your project:

```bash
devforgeai install .
```

### Requirements

- **Node.js 18+** - [Download Node.js](https://nodejs.org/)
- **npm 8+** - Included with Node.js
- **Python 3.10+** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Download Git](https://git-scm.com/downloads)
- **Claude Code Terminal 0.8.0+** - [Install Claude Code](https://code.claude.com/)

### Quick Start

```bash
# Install framework to current directory
devforgeai install .

# Or specify a target directory
devforgeai install /path/to/project

# Check installed version
devforgeai --version

# View help and available commands
devforgeai --help
```

### Offline Installation (Air-Gapped Networks)

DevForgeAI supports installation in environments with no internet connectivity.

**How It Works:**

1. **Download Once:** `npm pack devforgeai` on a machine with internet access
2. **Transfer:** Copy the `.tgz` file to the air-gapped machine
3. **Install Offline:** `npm install -g devforgeai-1.0.0.tgz`
4. **Run Installer:** `devforgeai install .` (no network required)

**What's Bundled:**
- All `.claude/` framework files (skills, agents, commands, memory)
- All `devforgeai/` templates (context, protocols, specs)
- Python CLI wheel files (installed with `pip --no-index`)
- SHA256 checksums for integrity verification

**Bundle Integrity:**
- Checksums stored in `bundled/checksums.json`
- Installation halts if 3+ checksum mismatches detected
- Bundle size: ~3 MB compressed, ~14 MB uncompressed

### Troubleshooting

**"Python 3.10+ required" error:**
- Ensure Python 3.10+ is installed: `python3 --version`
- On Windows: Use `python` instead of `python3`

**"command not found: devforgeai":**
- Verify installation: `npm list -g devforgeai`
- Check npm global bin is in PATH: `npm config get prefix`

**Permission denied on macOS/Linux:**
- Use: `npm install -g devforgeai --unsafe-perm`
- Or use nvm to manage Node.js versions without sudo

For more troubleshooting, see [installer/TROUBLESHOOTING.md](installer/TROUBLESHOOTING.md) or [docs/offline-installation.md](docs/offline-installation.md).

---

## 30-Second Quick Start

```bash
# 1. Start with your idea
claude
> /ideate "Build a task management app with user authentication"

# 2. Generate architectural constraints
> /create-context my-project

# 3. Create and implement a story
> /create-story "User can register with email and password"
> /dev STORY-001

# 4. Validate and release
> /qa STORY-001 deep
> /release STORY-001 production
```

---

## Core Philosophy

| Principle | Description |
|-----------|-------------|
| **Spec-Driven Development** | Requirements captured upfront in structured documents. Code never proceeds beyond what's specified. |
| **Test-Driven Development** | Tests written BEFORE implementation. Red → Green → Refactor cycle enforced. |
| **Constitutional Constraints** | 6 immutable context files define the law. Deviation requires Architecture Decision Records (ADRs). |
| **User Authority** | Mandatory approval for state-changing operations. No autonomous decisions. |
| **Quality Gates** | 4 strict gates block progression until standards met (95%/85%/80% coverage). |
| **Zero Autonomous Deferrals** | Every deferral requires explicit user approval with technical justification. |

---

## Development Workflow

```
┌─────────────────┐
│   /brainstorm   │  Vague problems → Structured discovery
└────────┬────────┘
         ↓
┌─────────────────┐
│    /ideate      │  Business idea → Epic requirements
└────────┬────────┘
         ↓
┌─────────────────┐
│ /create-context │  Generate 6 immutable context files
└────────┬────────┘
         ↓
┌─────────────────┐
│  /create-epic   │  Epic with feature decomposition
└────────┬────────┘
         ↓
┌─────────────────┐
│  /create-story  │  Stories with AC + technical specs
└────────┬────────┘
         ↓
┌─────────────────┐
│     /dev        │  TDD Implementation (10 phases)
└────────┬────────┘
         ↓
┌─────────────────┐
│      /qa        │  Quality validation (95%/85%/80% coverage)
└────────┬────────┘
         ↓
┌─────────────────┐
│    /release     │  Staging → Production deployment
└─────────────────┘
```

**Workflow States:**
```
Backlog → Architecture → Ready for Dev → In Development → Dev Complete →
QA In Progress → QA Approved → Releasing → Released
```

---

## The 6 Constitutional Context Files

These files are **immutable constraints** that all AI agents must follow:

| File | Controls | Prevents |
|------|----------|----------|
| `tech-stack.md` | Approved technologies | Technology sprawl, library substitution |
| `source-tree.md` | Directory structure | File chaos, wrong component locations |
| `dependencies.md` | Allowed packages | Dependency bloat, version conflicts |
| `coding-standards.md` | Code patterns | Inconsistency, style violations |
| `architecture-constraints.md` | Layer boundaries | Circular dependencies, coupling |
| `anti-patterns.md` | Forbidden patterns | God objects, hardcoded secrets, SQL injection |

**Location:** `devforgeai/specs/context/`

**Key Rule:** Any technology/pattern not in these files → **HALT** and ask user.

---

## Slash Commands Reference

### Planning & Setup

| Command | Purpose |
|---------|---------|
| `/brainstorm [topic]` | Transform vague problems into structured discovery |
| `/ideate [business-idea]` | Business idea → requirements + epic (6-phase workflow) |
| `/create-context [project-name]` | Generate the 6 immutable context files |
| `/create-epic [epic-name]` | Create epic with feature decomposition |
| `/create-sprint [sprint-name]` | Sprint planning with story selection |

### Story Development

| Command | Purpose |
|---------|---------|
| `/create-story [feature]` | Generate complete user stories with AC + specs |
| `/create-ui [STORY-ID]` | Generate UI component specifications |
| `/dev [STORY-ID]` | Execute TDD development (10-phase workflow) |

### Validation & Release

| Command | Purpose |
|---------|---------|
| `/qa [STORY-ID] [light\|deep]` | Quality validation with coverage thresholds |
| `/release [STORY-ID] [env]` | Deploy to staging/production |
| `/orchestrate [STORY-ID]` | Full lifecycle end-to-end (dev→qa→release) |

### Framework Maintenance

| Command | Purpose |
|---------|---------|
| `/audit-deferrals` | Audit technical debt and deferral chains |
| `/rca [issue] [severity]` | Root Cause Analysis with 5 Whys |
| `/chat-search [keywords]` | Find and resume previous sessions |
| `/recommendations-triage` | Convert AI-generated framework recommendations to stories |

---

## Key Capabilities

### TDD Enforcement (`/dev`)

The development skill enforces 10 strict phases:

```
01-Preflight → 02-Red → 03-Green → 04-Refactor → 05-Integration →
06-Deferral → 07-DoD-Update → 08-Git → 09-Feedback → 10-Result
```

- Tests written BEFORE implementation
- Coverage thresholds: 95% (business), 85% (application), 80% (infrastructure)
- All deferrals require user approval (Phase 6)
- **Observation capture** during phases 01-08 feeds AI analysis at Phase 09
- Framework improvement recommendations auto-generated via `framework-analyst` subagent

### Quality Gates

4 strict gates block progression:

| Gate | Transition | Requirements |
|------|------------|--------------|
| **Gate 1** | Architecture → Ready | All 6 context files present and valid |
| **Gate 2** | Dev Complete → QA | Tests pass, coverage met, no critical violations |
| **Gate 3** | QA → Releasing | All acceptance criteria verified, deferrals justified |
| **Gate 4** | Releasing → Released | Smoke tests pass, rollback plan ready |

### 27 Specialized Subagents

Domain experts auto-invoked by skills:

**Development:** `test-automator`, `backend-architect`, `frontend-developer`, `integration-tester`, `refactoring-specialist`, `code-reviewer`

**Architecture:** `requirements-analyst`, `architect-reviewer`, `api-designer`, `dependency-graph-analyzer`, `anti-pattern-scanner`

**Quality:** `deferral-validator`, `coverage-analyzer`, `code-quality-auditor`, `security-auditor`, `context-validator`

**Operations:** `git-validator`, `git-worktree-manager`, `deployment-engineer`, `documentation-writer`

**Research:** `internet-sleuth`, `tech-stack-detector`, `stakeholder-analyst`

**Analysis:** `framework-analyst` (synthesizes workflow observations into improvement recommendations)

**Utilities:** `agent-generator`, `dev-result-interpreter`, `qa-result-interpreter`, `ui-spec-formatter`

### Parallel Execution

35-40% time reduction through:
- Multiple subagents in parallel (4-6 recommended, 10 max)
- Background shell tasks (3-4 concurrent)
- Parallel tool invocations (Read, Grep, Glob)

---

## How To Use DevForgeAI

### New Project (Greenfield)

```bash
# 1. Start with your business idea
/ideate "Build a task management app with user authentication"

# 2. Generate architectural constraints
/create-context my-project

# 3. Create epic and stories
/create-epic "Task Management MVP"
/create-story EPIC-001

# 4. Develop with TDD
/dev STORY-001

# 5. Validate and release
/qa STORY-001 deep
/release STORY-001 production
```

### Existing Project (Brownfield)

```bash
# 1. Generate context files for existing project
/create-context my-existing-project --brownfield

# 2. Create stories for new features
/create-story "Add dark mode toggle"

# 3. Continue with TDD workflow
/dev STORY-042
```

### Full Automation

```bash
# Complete lifecycle in one command
/orchestrate STORY-001
# (Internally: /dev → /qa deep → /release staging → /release production)
```

---

## Architecture

DevForgeAI implements a **three-layer architecture** optimized for Claude Code Terminal:

### Layer 1: Skills (15 Workflow Skills)

Autonomous, model-invoked capabilities for each development phase:

**Core Workflow (9):**
- `devforgeai-brainstorming` - Vague problems → structured discovery
- `devforgeai-ideation` - Business idea → epic requirements
- `devforgeai-architecture` - Context files + ADRs
- `devforgeai-orchestration` - Epic/sprint/story lifecycle management
- `devforgeai-story-creation` - Complete story generation
- `devforgeai-ui-generator` - UI component specifications
- `devforgeai-development` - TDD implementation (10 phases)
- `devforgeai-qa` - Hybrid validation (light/deep)
- `devforgeai-release` - Production deployment

**Infrastructure (6):**
- `devforgeai-documentation` - README, API docs, architecture diagrams
- `devforgeai-feedback` - Retrospective insights collection
- `devforgeai-rca` - Root Cause Analysis with 5 Whys
- `devforgeai-mcp-cli-converter` - MCP → CLI conversion
- `devforgeai-subagent-creation` - Custom subagent generation
- `devforgeai-github-actions` - CI/CD workflow generation

### Layer 2: Subagents (26 Specialized Workers)

AI workers with separate context windows for concurrent execution. See [Key Capabilities](#26-specialized-subagents) for complete list.

### Layer 3: Slash Commands (13+ User Workflows)

User-invoked, parameterized workflows. See [Slash Commands Reference](#slash-commands-reference) for complete list.

---

## Project Structure

```
.claude/
├── skills/              # Framework skills (15 skills)
│   ├── devforgeai-ideation/
│   ├── devforgeai-architecture/
│   ├── devforgeai-orchestration/
│   ├── devforgeai-story-creation/
│   ├── devforgeai-ui-generator/
│   ├── devforgeai-development/
│   ├── devforgeai-qa/
│   ├── devforgeai-release/
│   └── ...
│
├── agents/              # Specialized subagents (26 agents)
│   ├── test-automator.md
│   ├── backend-architect.md
│   ├── code-reviewer.md
│   ├── deferral-validator.md
│   └── ...
│
├── commands/            # Slash commands (13+ commands)
│   ├── ideate.md
│   ├── create-context.md
│   ├── dev.md
│   ├── qa.md
│   └── ...
│
├── memory/              # Reference documentation
│   ├── skills-reference.md
│   └── commands-reference.md
│
└── rules/               # Framework rules
    ├── core/
    ├── workflow/
    └── security/

devforgeai/
├── specs/
│   ├── context/         # 6 immutable context files
│   │   ├── tech-stack.md
│   │   ├── source-tree.md
│   │   ├── dependencies.md
│   │   ├── coding-standards.md
│   │   ├── architecture-constraints.md
│   │   └── anti-patterns.md
│   │
│   ├── Stories/         # User story definitions
│   ├── Epics/           # Epic definitions
│   └── adrs/            # Architecture Decision Records
│
├── qa/                  # QA validation outputs
├── RCA/                 # Root Cause Analysis documents
├── workflows/           # Workflow state checkpoints
└── feedback/            # Retrospective sessions

docs/
├── guides/              # How-to guides
├── architecture/        # Design decisions
└── installer/           # Installation docs
```

---

## Version Management

DevForgeAI follows [Semantic Versioning](https://semver.org/).

### Version Format

```
v{major}.{minor}.{patch}[-prerelease]

Examples:
- v1.0.0        (stable release)
- v1.1.0        (new features, backward compatible)
- v1.0.1        (bug fixes)
- v1.1.0-beta.1 (beta pre-release)
```

### Installing Specific Versions

```bash
# Latest stable
npm install -g devforgeai

# Specific version
npm install -g devforgeai@1.0.0

# Pre-release
npm install -g devforgeai@beta
```

### Updating

```bash
# Update to latest stable
npm update -g devforgeai

# Check current version
devforgeai --version

# View available versions
npm view devforgeai versions
```

### Release Channels

| Channel | Description |
|---------|-------------|
| **Stable** (`latest`) | Fully tested, production-ready |
| **Beta** (`beta`) | Preview features, generally stable |
| **RC** (`rc`) | Final testing before stable |

### Provenance and Security

All packages include **provenance attestations** for supply chain security:

```bash
npm view devforgeai
# Look for "publishConfig.provenance: true"
```

---

## Advanced Installation

### Development Installation

For contributing to DevForgeAI:

```bash
# 1. Clone the repository
git clone https://github.com/bankielewicz/DevForgeAI.git
cd DevForgeAI

# 2. Install Node.js dependencies
npm install

# 3. Install Node.js CLI globally (optional - for testing)
npm install -g .

# 4. Install Python CLI in editable mode
pip install --break-system-packages -e .claude/scripts/

# 5. Verify installation
devforgeai --version                     # Node.js CLI
devforgeai validate-dod --help           # Python CLI

# 6. Run tests
npm test                                 # Node.js tests

# 7. Build offline bundle (optional)
bash scripts/build-offline-bundle.sh
```

For detailed setup instructions, see **[docs/DEVELOPER-SETUP.md](docs/DEVELOPER-SETUP.md)**.
For CLI build documentation, see **[docs/BUILD.md](docs/BUILD.md)**.

### Migration Guide

If upgrading from v1.0.0, see **[MIGRATION-GUIDE.md](MIGRATION-GUIDE.md)**.

For detailed troubleshooting, see **[installer/INSTALL.md](installer/INSTALL.md)**.

---

## Technical Stack

Framework-agnostic design supports:

| Category | Supported |
|----------|-----------|
| **Languages** | Node.js, Python, C#, Go, Java, Rust, etc. |
| **Testing** | Jest, pytest, xUnit, Go test, JUnit, etc. |
| **Deployment** | Kubernetes, AWS, Azure, Docker, VPS |
| **CI/CD** | GitHub Actions, GitLab CI, Azure DevOps |

---

## Benefits

### For Developers
- Systematic TDD workflow with automated test generation
- Architectural constraints prevent common mistakes
- One-command deployment reduces manual effort

### For Teams
- Consistent development patterns across projects
- Quality gates ensure code review standards
- Audit trails track all workflow transitions

### For Organizations
- Zero technical debt through constraint enforcement
- Predictable delivery with story-based estimation
- Knowledge preservation through ADRs

---

## Research Foundation

DevForgeAI is built on proven patterns from:
- **Official Claude Code Documentation** (docs.claude.com)
- **Production Implementations** (Pimzino's spec-workflow, OneRedOak's dual-loop)
- **Token Efficiency Research** (40-73% savings with native tools vs Bash)

All patterns are evidence-based. No aspirational content.

---

## Contributing

1. Follow spec-driven development workflow
2. All changes must pass quality gates
3. Context files are immutable (require ADR for changes)
4. Test coverage requirements: 95%/85%/80% by layer
5. Document all architectural decisions

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## License

MIT License - See [LICENSE](LICENSE) for details.

---

## Support

- **Issues**: [GitHub Issues](https://github.com/bankielewicz/DevForgeAI/issues)
- **Discussions**: [GitHub Discussions](https://github.com/bankielewicz/DevForgeAI/discussions)
- **Documentation**: [docs/](docs/)

---

**Built with Claude Code Terminal** — Leveraging Skills, Subagents, and Slash Commands for systematic, constraint-enforced development.
