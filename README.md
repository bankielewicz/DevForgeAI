# DevForgeAI - Spec-Driven Development Meta-Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js >= 18](https://img.shields.io/badge/Node.js-%3E%3D18-green.svg)](https://nodejs.org/)
[![Python >= 3.10](https://img.shields.io/badge/Python-%3E%3D3.10-blue.svg)](https://www.python.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Built with Claude Code](https://img.shields.io/badge/Built%20with-Claude%20Code-blueviolet.svg)](https://docs.anthropic.com/en/docs/claude-code)

> **Transform vague business ideas into production-ready code with zero technical debt.**

DevForgeAI is a **Claude Code Terminal meta-framework** that orchestrates the entire software development lifecycle -- from brainstorming through production release -- using 44 specialized subagents, 26 skills, 46 slash commands, and 6 constitutional constraint files. It works with **any technology stack**.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Competitive Analysis](#competitive-analysis)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Architecture](#architecture)
- [Commands Reference](#commands-reference)
- [Constitutional Context Files](#constitutional-context-files)
- [The /dev Workflow](#the-dev-workflow)
- [Configuration Layer Alignment Protocol](#configuration-layer-alignment-protocol)
- [Why DevForgeAI?](#why-devforgeai)
- [Contributing](#contributing)
- [Security](#security)
- [Support](#support)
- [License](#license)

---

## Overview

Unguided AI development leads to chaos: autonomous decisions, technical debt, and architectural violations. DevForgeAI solves this through a constraint-enforced, spec-driven approach where **requirements are law and code follows specs exactly**.

### Core Principles

| Principle | Description |
|-----------|-------------|
| **Immutable Context Files** | 6 constitutional files govern all development decisions. Changes require Architecture Decision Records (ADRs). |
| **TDD Mandatory** | Tests BEFORE implementation. Red, Green, Refactor -- no exceptions. |
| **Quality Gates** | 4 strict gates block progression until standards are met (95%/85%/80% coverage). |
| **User Authority** | No autonomous decisions on important matters. AI halts and asks. |
| **Zero Autonomous Deferrals** | No work deferred without explicit user approval. |
| **Spec-Driven Development** | Requirements captured upfront in structured documents. Code never proceeds beyond what is specified. |

### By the Numbers

| Component | Count |
|-----------|-------|
| Subagents | 44 |
| Skills | 26 |
| Slash Commands | 46 |
| Constitutional Files | 6 |
| Quality Gates | 4 |
| Dev Phases (TDD) | 10 |

---

## Features

- **Technology Agnostic** -- Works with any stack. Context files define your approved technologies, not the framework.
- **Full Lifecycle Orchestration** -- Brainstorm to release in one coherent workflow.
- **44 Specialized Subagents** -- Each agent has a single responsibility: backend-architect, test-automator, code-reviewer, security-auditor, diagnostic-analyst, and more.
- **26 Inline Skills** -- Skills expand as executable instructions, not background processes. Phases execute sequentially with validation checkpoints.
- **46 Slash Commands** -- From `/brainstorm` to `/release`, every workflow step has a dedicated command.
- **Constitutional Guardrails** -- 6 immutable context files prevent technology sprawl, dependency bloat, architectural violations, and anti-patterns.
- **Strict TDD Enforcement** -- 10-phase development cycle with mandatory Red-Green-Refactor.
- **Root Cause Analysis** -- Built-in `/rca` command with 5 Whys methodology and diagnostic-analyst subagent.
- **Configuration Layer Alignment Protocol (CLAP)** -- 15 validation checks detect contradictions across all configuration layers.
- **Feedback System** -- 7 commands for capturing, searching, exporting, and importing development feedback.
- **Cross-AI Collaboration** -- `/collaborate` generates portable documents for sharing issues with external LLMs.
- **Sprint Planning** -- `/create-sprint` with automated story selection and capacity planning.
- **Hook-Based Phase Enforcement** -- Step-level validation gates prevent phase skipping (EPIC-086).

---

## Competitive Analysis

DevForgeAI has been benchmarked against 10 competitors in the AI-driven development framework space. The analysis covers spec-driven enforcement, TDD methodology, quality gates, subagent architecture, and market positioning.

### How DevForgeAI Compares

| Capability | DevForgeAI | BMAD | AWS Kiro | Cursor | Cline | Tessl |
|------------|:----------:|:----:|:--------:|:------:|:-----:|:-----:|
| Mandatory TDD | ✅ | ❌ | ❌ | ❌ | ❌ | ⚠️ |
| Coverage thresholds (95/85/80%) | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Immutable constraint files | ✅ | ❌ | ❌ | ❌ | ❌ | ⚠️ |
| ADR change management | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Pre-commit enforcement | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Specialized subagents | ✅ 44 | ✅ 7+ | ⚠️ | ❌ | ⚠️ | ❌ |
| Phase-enforced workflow | ✅ 10 | ❌ | ⚠️ | ❌ | ⚠️ | ❌ |

**Key finding:** DevForgeAI occupies the only position combining full lifecycle methodology with mandatory mechanical enforcement — a quadrant currently unoccupied by any publicly available competitor.

**Full analysis:** [Comparison Tables](devforgeai/specs/research/shared/RESEARCH-001-comparison-tables.md) | [Detailed Report](devforgeai/specs/research/shared/RESEARCH-001-ai-dev-frameworks-competitive-analysis.md) | [Research Index](devforgeai/specs/research/research-index.md)

---

## Quick Start

```bash
# 1. Install DevForgeAI into your project
npx devforgeai install

# 2. Open your project in Claude Code Terminal

# 3. Generate constitutional context files for your project
/create-context my-project

# 4. Create an epic from your requirements
/create-epic user-authentication

# 5. Break the epic into implementable stories
/create-story login-endpoint

# 6. Develop with TDD enforcement
/dev STORY-001

# 7. Validate quality
/qa STORY-001 deep

# 8. Release
/release STORY-001
```

For a guided experience starting from a vague idea:

```bash
# Start with brainstorming
/brainstorm "I want to build a marketplace for local artisans"

# Refine into structured requirements
/ideate marketplace-for-artisans

# The framework guides you through the rest
```

---

## Installation

### Prerequisites

- **Node.js** >= 18.0.0
- **npm** >= 8.0.0
- **Python** >= 3.10 (optional — for CLI validation tools)
- **Git** (for version control hooks and workflow tracking)
- **Claude Code Terminal** (the runtime environment)

### Option A: Install via npx (Recommended)

The fastest way to get started. Run this from your project directory:

```bash
npx devforgeai install
```

The interactive wizard will guide you through:
1. **Directory selection** — where to install (default: current directory)
2. **Component selection** — agents, skills, commands, hooks, Python CLI, etc.
3. **Python check** — auto-detects Python 3.10+ for validation tools
4. **Project name** — used in template files

For CI/CD or scripted installs, use non-interactive mode:

```bash
npx devforgeai install --yes                    # All defaults, current directory
npx devforgeai install ./my-project --yes       # Specific directory
npx devforgeai install --yes --skip-python      # Skip Python CLI
```

### Option B: Install from Downloaded Source

If you downloaded or cloned the DevForgeAI repository:

```bash
# 1. Navigate to the DevForgeAI source directory
cd DevForgeAI

# 2. Install Node.js dependencies
npm install

# 3. Run the installer targeting your project
node bin/devforgeai.js install /path/to/your-project

# Or install to the current directory
node bin/devforgeai.js install .
```

### Option C: Global Install via npm

```bash
npm install -g devforgeai
devforgeai install
```

### What Gets Installed

The installer copies the following components into your project:

| Component | Contents | Location |
|-----------|----------|----------|
| **Core Framework** | CLAUDE.md, rules, memory files, context templates | `.claude/rules/`, `.claude/memory/`, `devforgeai/specs/context/` |
| **Agents** | 44 specialized AI subagent definitions | `.claude/agents/` |
| **Skills** | 26 inline skill workflows | `.claude/skills/` |
| **Commands** | 46 slash command definitions | `.claude/commands/` |
| **Hooks** | Workflow validation hooks | `.claude/hooks/` |
| **Python CLI** | Validation tools (`devforgeai-validate`) | `.claude/scripts/` |
| **Project Structure** | Standard directories | `src/`, `tests/`, `docs/`, `devforgeai/` |

### Post-Install Setup

After installation, customize the 6 constitutional context files for your project:

```bash
# Edit these files in devforgeai/specs/context/ to match your tech stack:
#   tech-stack.md           — Your approved technologies
#   source-tree.md          — Your directory structure
#   dependencies.md         — Your allowed packages
#   coding-standards.md     — Your code style rules
#   architecture-constraints.md — Your layer boundaries
#   anti-patterns.md        — Your forbidden patterns

# Or generate them interactively:
/create-context my-project
```

### Managing Your Installation

```bash
# Check installation status
devforgeai status

# Update framework files (preserves your context customizations)
devforgeai install          # Select "Update" when prompted

# Remove DevForgeAI (preserves your src/, tests/, docs/)
devforgeai uninstall
```

### Verify Installation

```bash
# Check Node.js CLI
devforgeai --version

# Check Python validation (if installed)
devforgeai-validate --help

# Check installation status
devforgeai status
```

---

## Usage

### Starting a New Project

```
/brainstorm [topic]          # Vague problem -> structured discovery
/ideate [business-idea]      # Business idea -> epic requirements
/create-context [project]    # Generate 6 constitutional context files
/create-epic [epic-name]     # Epic with feature decomposition
/create-story [feature]      # Stories with acceptance criteria + specs
```

### Developing a Story

```
/dev STORY-XXX               # 10-phase TDD cycle
/dev-status STORY-XXX        # Check progress without invoking workflow
/resume-dev STORY-XXX        # Resume from a specific phase
```

### Validating and Releasing

```
/qa STORY-XXX light          # Fast validation during development
/qa STORY-XXX deep           # Comprehensive analysis with coverage checks
/release STORY-XXX           # Deploy to staging/production
/orchestrate STORY-XXX       # Full lifecycle: dev -> qa -> release
```

### Framework Maintenance

```
/audit-alignment             # Detect contradictions across config layers
/audit-deferrals             # Audit deferred work for circular chains
/rca [issue]                 # Root Cause Analysis with 5 Whys
/create-stories-from-rca     # Turn RCA recommendations into stories
/review-qa-reports           # Process QA gaps into remediation stories
```

---

## Architecture

### High-Level Structure

```
DevForgeAI/
├── .claude/                    # Framework runtime (operational)
│   ├── agents/                 # 44 specialized subagents (.md files)
│   ├── skills/                 # 26 inline skills (SKILL.md per skill)
│   ├── commands/               # 46 slash command definitions
│   ├── memory/                 # Persistent reference files
│   ├── rules/                  # Modular rules (core, workflow, security)
│   └── plans/                  # Plan files for active work
│
├── devforgeai/                 # Framework specifications
│   ├── specs/
│   │   ├── context/            # 6 constitutional context files
│   │   ├── adrs/               # Architecture Decision Records
│   │   ├── epics/              # Epic specifications
│   │   └── stories/            # Story specifications
│   ├── feedback/               # AI analysis and observations
│   └── RCA/                    # Root Cause Analysis reports
│
├── src/                        # Source code (development target)
├── tests/                      # Test files (phase-restricted writes)
├── docs/                       # Documentation output
│   ├── api/                    # API documentation
│   ├── guides/                 # User guides
│   └── architecture/           # Architecture diagrams
│
├── CLAUDE.md                   # Orchestrator instructions
├── package.json                # Node.js package definition
└── README.md                   # This file
```

### Markdown-First Design

DevForgeAI is built on **Markdown files as executable specifications**:

- **Skills** are `.md` files containing phased instructions that expand inline when invoked
- **Subagents** are `.md` files defining specialized roles, constraints, and tool access
- **Commands** are `.md` files mapping slash commands to skill invocations
- **Rules** are `.md` files loaded automatically based on file path patterns
- **Context files** are `.md` files serving as constitutional constraints

No custom runtime or compilation step is required. Claude Code Terminal reads and executes these Markdown specifications directly.

### Subagent Roster (44 agents)

Subagents are specialized AI roles, each with a single responsibility:

| Category | Agents |
|----------|--------|
| **Architecture** | backend-architect, api-designer, architect-reviewer |
| **Development** | frontend-developer, test-automator, integration-tester |
| **Quality** | code-reviewer, code-analyzer, code-quality-auditor, anti-pattern-scanner, security-auditor, coverage-analyzer |
| **Analysis** | diagnostic-analyst, framework-analyst, technical-debt-analyzer, dependency-graph-analyzer, dead-code-detector |
| **Validation** | context-validator, ac-compliance-verifier, context-preservation-validator, deferral-validator, alignment-auditor |
| **Documentation** | documentation-writer |
| **Operations** | deployment-engineer, git-validator, git-worktree-manager |
| **Interpretation** | dev-result-interpreter, qa-result-interpreter, ideation-result-interpreter, epic-coverage-result-interpreter |
| **Planning** | requirements-analyst, stakeholder-analyst, story-requirements-analyst, sprint-planner, entrepreneur-assessor |
| **Infrastructure** | agent-generator, tech-stack-detector, session-miner, observation-extractor, pattern-compliance-auditor, file-overlap-detector |
| **Specialized** | refactoring-specialist, ui-spec-formatter, internet-sleuth |

### Skill Catalog (26 skills)

| Category | Skills |
|----------|--------|
| **Workflow** | brainstorming, discovering-requirements, designing-systems, devforgeai-story-creation, implementing-stories, devforgeai-qa, devforgeai-release, devforgeai-orchestration |
| **Analysis** | root-cause-diagnosis, devforgeai-rca, devforgeai-qa-remediation, validating-epic-coverage, auditing-w3-compliance, assessing-entrepreneur |
| **Maintenance** | devforgeai-feedback, devforgeai-insights, devforgeai-research, story-remediation |
| **Generation** | devforgeai-ui-generator, devforgeai-documentation, devforgeai-subagent-creation, devforgeai-github-actions |
| **Infrastructure** | claude-code-terminal-expert, skill-creator, cross-ai-collaboration, devforgeai-mcp-cli-converter |

---

## Commands Reference

### Planning and Setup (6 commands)

| Command | Purpose |
|---------|---------|
| `/brainstorm [topic]` | Transform vague problems into structured discovery documents |
| `/ideate [business-idea]` | Transform business idea to structured requirements (6-phase workflow) |
| `/create-context [project]` | Generate 6 immutable constitutional context files |
| `/create-epic [epic-name]` | Generate epic with feature decomposition |
| `/create-sprint [sprint-name]` | Plan 2-week sprint with story selection |
| `/assess-me` | Run guided self-assessment for adaptive coaching profile |

### Story Development (5 commands)

| Command | Purpose |
|---------|---------|
| `/create-story [feature]` | Generate story with acceptance criteria and technical specs |
| `/create-ui [STORY-ID]` | Generate UI component specifications (web/GUI/terminal) |
| `/dev [STORY-ID]` | Execute TDD development cycle (10 phases: Red, Green, Refactor) |
| `/dev-status [STORY-ID]` | Display development progress without invoking full workflow |
| `/resume-dev [STORY-ID]` | Resume development from a specific phase |

### Validation and Release (4 commands)

| Command | Purpose |
|---------|---------|
| `/qa [STORY-ID] [light\|deep]` | Quality validation with coverage thresholds |
| `/release [STORY-ID] [env]` | Deploy to staging and production |
| `/validate-stories` | Validate stories against constitutional context files |
| `/fix-story` | Apply automated/guided fixes to story/epic files |

### Orchestration (3 commands)

| Command | Purpose |
|---------|---------|
| `/orchestrate [STORY-ID]` | Full lifecycle: dev, qa, release |
| `/validate-epic-coverage` | Validate epic coverage and report gaps |
| `/create-missing-stories` | Create stories for detected coverage gaps |

### Framework Maintenance (11 commands)

| Command | Purpose |
|---------|---------|
| `/audit-deferrals` | Audit deferred work for circular chains and invalid references |
| `/audit-alignment` | Validate configuration layer alignment across all project layers |
| `/audit-budget` | Audit command character budgets against lean orchestration |
| `/audit-hooks` | Audit hook registry and invocation history |
| `/audit-hybrid` | Audit commands for hybrid command/skill violations |
| `/audit-orphans` | Scan for orphaned files, duplicate templates, and sync drift |
| `/audit-w3` | Audit codebase for W3 violations (auto-skill chaining) |
| `/rca [issue] [severity]` | Root Cause Analysis with 5 Whys methodology |
| `/create-stories-from-rca` | Create user stories from RCA recommendations |
| `/review-qa-reports` | Process QA gap files and create remediation stories |
| `/prompt-version` | Prompt versioning with before/after snapshots and SHA-256 verification |

### Session and History (2 commands)

| Command | Purpose |
|---------|---------|
| `/chat-search [keywords]` | Search chat history and resume previous conversations |
| `/insights` | Session data mining for workflow patterns |

### Research and Analysis (2 commands)

| Command | Purpose |
|---------|---------|
| `/research [topic]` | Capture and persist research findings across sessions |
| `/recommendations-triage` | Triage AI-generated improvement recommendations |

### Feedback System (7 commands)

| Command | Purpose |
|---------|---------|
| `/feedback` | Manual feedback trigger with context |
| `/feedback-config` | View and edit feedback system configuration |
| `/feedback-search` | Search feedback history with filters |
| `/feedback-reindex` | Rebuild feedback session index |
| `/export-feedback` | Export feedback sessions to portable ZIP |
| `/import-feedback` | Import feedback sessions from ZIP package |
| `/feedback-export-data` | Export feedback data with selection criteria |

### Collaboration (1 command)

| Command | Purpose |
|---------|---------|
| `/collaborate` | Generate cross-AI collaboration document for sharing with external LLMs |

### Infrastructure (4 commands)

| Command | Purpose |
|---------|---------|
| `/create-agent` | Create DevForgeAI-aware Claude Code subagent |
| `/document` | Generate project documentation |
| `/setup-github-actions` | Generate CI/CD workflow files |
| `/worktrees` | Manage Git worktrees for parallel development |

### Utility (2 commands)

| Command | Purpose |
|---------|---------|
| `/read-constitution` | Display constitutional context files |
| `/devforgeai-validate` | Run CLI validation commands |

---

## Constitutional Context Files

These 6 files in `devforgeai/specs/context/` are **immutable constraints** that govern all AI agent behavior:

| File | Controls | Prevents |
|------|----------|----------|
| `tech-stack.md` | Approved technologies and versions | Technology sprawl, library substitution |
| `source-tree.md` | Directory structure and file locations | File chaos, components in wrong directories |
| `dependencies.md` | Allowed packages and version ranges | Dependency bloat, version conflicts |
| `coding-standards.md` | Code patterns, naming, formatting | Inconsistency, style violations |
| `architecture-constraints.md` | Layer boundaries, coupling rules | Circular dependencies, tight coupling |
| `anti-patterns.md` | Forbidden patterns and practices | God objects, hardcoded secrets, SQL injection |

**Immutability Rule:** These files cannot be edited directly. Changes require:
1. Creating an Architecture Decision Record (ADR) with justification
2. User approval of the ADR
3. Propagation through the `/create-context` workflow

**HALT Behavior:** Any technology, pattern, or dependency not found in these files causes the AI to halt and ask the user before proceeding.

---

## The /dev Workflow

The `/dev` command executes a strict 10-phase TDD cycle:

```
Phase 01: Pre-Flight      Validate story, context files, git status
Phase 02: Red              Write failing tests (test-automator subagent)
Phase 03: Green            Implement minimum code to pass tests
Phase 04: Refactor         Improve code quality without changing behavior
Phase 04.5: AC Verify      Post-refactor acceptance criteria compliance check
Phase 05: Integration      Integration tests (integration-tester subagent)
Phase 05.5: AC Verify      Post-integration acceptance criteria compliance check
Phase 06: Deferral         Document any deferred work (requires user approval)
Phase 07: DoD Update       Update Definition of Done in story file
Phase 08: Git              Commit with validation hooks
Phase 09: Feedback         Capture observations, generate framework recommendations
Phase 10: Result           Final status report
```

### Quality Coverage Thresholds

| Layer | Minimum Coverage | Enforcement |
|-------|-----------------|-------------|
| Business Logic | 95% | CRITICAL -- blocks QA |
| Application | 85% | CRITICAL -- blocks QA |
| Infrastructure | 80% | CRITICAL -- blocks QA |

Coverage gaps are **blockers, not warnings**. QA fails if thresholds are not met.

### Test Folder Protection

Test files (`tests/**`, `*.test.*`, `*.spec.*`) are write-protected:

- **Phase 02 only:** `test-automator` subagent can write tests
- **Phase 05 only:** `integration-tester` subagent can write integration tests
- **All other phases:** Test modifications require explicit user approval

This prevents implementation agents from weakening test assertions to make failing tests pass.

---

## Configuration Layer Alignment Protocol

CLAP validates consistency across all configuration layers with **15 checks** in 3 categories:

| Category | Checks | Purpose |
|----------|--------|---------|
| Contradiction Checks | CC-01 to CC-10 | Detect conflicting instructions between layers |
| Completeness Checks | CMP-01 to CMP-04 | Find missing references and incomplete configuration |
| ADR Propagation | ADR-01 | Verify accepted ADR decisions are reflected in context files |

**Layers validated:** CLAUDE.md, System Prompt, 6 Context Files, Rules (.claude/rules/), ADRs

Run manually with `/audit-alignment` or automatically during `/create-context` Phase 5.5.

---

## Recent Development

### EPIC-086: Hook-Based Step-Level Phase Enforcement

Recent work has implemented hook-based validation gates at the step level within TDD phases:

- **STORY-525:** Hook registry and lifecycle management
- **STORY-526:** Step-level validation gate hooks
- **STORY-527:** TaskCompleted hook for step validation

This system prevents phase skipping by validating that each step within a phase completes before the next step begins.

---

## Tech Stack

DevForgeAI itself is built with:

| Component | Technology |
|-----------|-----------|
| Skills, Agents, Commands | Markdown (.md files) |
| CLI Validation | Python 3.10+ (`devforgeai-validate`) |
| Package Manager | npm (Node.js >= 18) |
| Testing | Jest (Node.js), pytest (Python) |
| Version Control | Git with pre-commit validation hooks |
| Runtime | Claude Code Terminal |

---

## Why DevForgeAI?

AI coding assistants are powerful but undisciplined. Without guardrails, they make autonomous technology decisions, skip tests, introduce dependencies, and accumulate technical debt faster than any human team could.

**DevForgeAI solves this** by treating software engineering discipline as a constraint satisfaction problem:

- **The problem:** AI agents writing code without architectural boundaries produce inconsistent, untestable, debt-laden software.
- **The solution:** Constitutional context files define what technologies, patterns, and structures are allowed. 44 specialized subagents enforce those constraints at every phase. Quality gates block progression until standards are met.
- **The result:** Every feature goes through brainstorming, requirements, architecture, TDD implementation, QA validation, and release -- with automated enforcement at each step.

DevForgeAI is not another code generator. It is a **development process enforcer** that makes it structurally impossible to ship low-quality software through AI-assisted development.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Follow the DevForgeAI workflow:
   - Create a story with `/create-story`
   - Develop with TDD using `/dev`
   - Validate with `/qa deep`
4. Commit changes (pre-commit hooks validate DoD compliance)
5. Push to your branch (`git push origin feature/your-feature`)
6. Open a Pull Request

### Development Setup

```bash
# Clone the repository
git clone https://github.com/bankielewicz/DevForgeAI.git
cd DevForgeAI

# Install Node.js dependencies
npm install

# Install Python CLI in development mode
pip install -e .claude/scripts/

# Run tests
npm test                    # Node.js tests (Jest)
pytest .claude/scripts/devforgeai_cli/tests/   # Python tests
```

### Rules for Contributors

- **Context files are immutable** -- propose changes via ADRs in `devforgeai/specs/adrs/`
- **TDD is mandatory** -- tests before implementation
- **No `--no-verify` commits** -- fix validation errors, do not bypass them
- **No `/tmp/` usage** -- use `{project-root}/tmp/{story-id}/` for temporary files
- **Native tools over Bash** -- use Read/Write/Edit/Glob/Grep instead of cat/echo/sed

---

## Support

If DevForgeAI has been useful to you, consider buying me a coffee!

<a href="https://buymeacoffee.com/devforgeai" target="_blank">
  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="50">
</a>

<img src="devforgeai/bmc_qr.png" alt="Buy Me a Coffee QR Code" width="200">

---

## Security

See [SECURITY.md](SECURITY.md) for our security policy and how to report vulnerabilities.

---

## License

MIT License -- see [LICENSE](LICENSE) for details.

---

**Built with Claude Code Terminal** -- Leveraging Skills, Subagents, and Slash Commands for systematic, constraint-enforced development.
