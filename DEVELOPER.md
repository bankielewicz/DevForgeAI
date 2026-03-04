# DevForgeAI Developer Guide

A comprehensive guide for contributors to the DevForgeAI spec-driven development meta-framework.

## Table of Contents

- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [TDD Workflow](#tdd-workflow)
- [Adding Skills](#adding-skills)
- [Adding Subagents](#adding-subagents)
- [Adding Slash Commands](#adding-slash-commands)
- [Testing](#testing)
- [Code Standards](#code-standards)
- [Context Files](#context-files)
- [ADR Process](#adr-process)

---

## Development Setup

### Prerequisites

- **Node.js** 18+ and npm 8+
- **Python** 3.8+ (3.10+ recommended for CLI tools)
- **Git**
- **Claude Code Terminal** 1.0+
- **WSL** (if developing on Windows)

### Initial Setup

```bash
# Clone the repository
git clone https://github.com/bankielewicz/DevForgeAI.git
cd DevForgeAI

# Install Node.js dependencies
npm install

# Install Python CLI in development mode
pip install -e .claude/scripts/

# Verify Python CLI installation
devforgeai-validate --help
```

### WSL Environment Configuration

DevForgeAI runs on WSL. Always use Unix-style paths with the `/mnt/c/` prefix.

```bash
# Navigate to project root
cd /mnt/c/Projects/DevForgeAI

# Set PYTHONPATH (required for pytest module discovery)
export PYTHONPATH=".:$PYTHONPATH"
```

| Path Style | Correct |
|------------|---------|
| `/mnt/c/Projects/DevForgeAI/src/` | Yes |
| `C:\Projects\DevForgeAI\src\` | No |

### Verify Your Environment

```bash
# Confirm project root
ls CLAUDE.md  # Must succeed

# Confirm Python CLI
devforgeai-validate --help

# Confirm Node.js
npm test
```

---

## Project Structure

DevForgeAI uses a **dual-path architecture**: `src/` for source code and `.claude/` for operational runtime files.

```
DevForgeAI/
├── .claude/                     # OPERATIONAL - do not modify directly
│   ├── agents/                  # Subagent definitions (44 agents)
│   ├── commands/                # Slash commands
│   ├── hooks/                   # Workflow event hooks (*.sh)
│   ├── memory/                  # Framework memory files
│   ├── plans/                   # Plan files for active work
│   ├── rules/                   # Modular rules (core, workflow, security, conditional)
│   ├── scripts/                 # Python CLI (devforgeai-validate)
│   │   └── devforgeai_cli/      # CLI source and tests
│   └── skills/                  # Framework skills (26 skills)
│       └── [skill-name]/
│           ├── SKILL.md         # Main skill file (500-800 lines)
│           └── references/      # Deep documentation (loaded on demand)
│
├── src/                         # SOURCE CODE - modify this tree
│   └── claude/                  # Mirrored structure for development
│       └── skills/
│           └── implementing-stories/
│               └── phases/      # Phase reference files
│
├── tests/                       # All test files reside here
│   └── [STORY-ID]/              # Tests organized by story
│
├── devforgeai/                  # Framework specifications
│   ├── specs/
│   │   ├── adrs/                # Architecture Decision Records
│   │   ├── context/             # 6 IMMUTABLE context files
│   │   ├── Epics/               # Epic specifications
│   │   └── Stories/             # Story specifications
│   ├── config/                  # Framework configuration
│   ├── feedback/                # AI analysis and observations
│   ├── RCA/                     # Root Cause Analyses
│   └── workflows/               # Phase state tracking JSON
│
├── docs/                        # Framework documentation
│   ├── api/                     # API specifications
│   ├── architecture/            # Architecture docs and diagrams
│   └── guides/                  # User and developer guides
│
├── CLAUDE.md                    # Master orchestrator instructions
├── DEVELOPER.md                 # This file
└── package.json                 # Node.js package definition
```

### Key Rule: Dual-Path Separation

- **Development work** (implementations, source code) goes in `src/`
- **Operational configs** (skills, agents, commands) stay in `.claude/`
- Never replace operational paths with `src/` paths or vice versa
- Always run tests against `src/` tree, not operational folders

---

## TDD Workflow

TDD is **mandatory** for all development. The workflow follows Red, Green, Refactor with additional verification phases.

### Phase Overview

| Phase | Name | Purpose |
|-------|------|---------|
| 01 | Pre-Flight Validation | Context files, git status, story validation |
| 02 | Test-First Design (RED) | Write failing tests before implementation |
| 03 | Implementation (GREEN) | Write minimum code to pass tests |
| 04 | Refactoring | Improve code without changing behavior |
| 04.5 | AC Compliance Verify | Verify acceptance criteria after refactor |
| 05 | Integration & Validation | Cross-component integration tests |
| 05.5 | AC Compliance Verify | Verify acceptance criteria after integration |
| 06 | Deferral Challenge | Challenge any deferred items |
| 07 | DoD Update | Update Definition of Done in story file |
| 08 | Git Workflow | Commit with conventional format |
| 09 | Feedback Hook | Extract observations for framework learning |
| 10 | Result Interpretation | Final status determination |

### Red Phase Rules

- Tests **must fail** before any implementation begins
- Test naming: `test_<function>_<scenario>_<expected>`
- One assertion per test (generally)
- Mock external dependencies

### Green Phase Rules

- Write **only** the code needed to make tests pass
- No premature optimization
- No features beyond test scope

### Refactor Phase Rules

- All tests must remain passing throughout
- Reduce cyclomatic complexity if > 10
- Extract methods for reuse

### Phase Execution

Phases execute sequentially. You cannot skip phases. Every validation checkpoint must pass before proceeding. Only the user can authorize skipping a phase via explicit instruction.

### Coverage Thresholds

| Layer | Minimum |
|-------|---------|
| Business Logic | 95% |
| Application | 85% |
| Infrastructure | 80% |

Coverage gaps are **CRITICAL blockers**, not warnings. They block QA approval.

---

## Adding Skills

Skills are the primary units of framework functionality. They use gerund naming (verb + -ing) per ADR-017.

### Naming Convention

- Use gerund form: `implementing-stories`, `discovering-requirements`
- No framework prefix: `designing-systems` not `devforgeai-designing-systems`
- Existing skills with the `devforgeai-` prefix are legacy (pre-ADR-017)

### Directory Structure

```
.claude/skills/[skill-name]/
├── SKILL.md                # Main skill file (500-800 lines target, 1000 max)
├── references/             # Deep documentation loaded on demand
│   ├── workflow-detail.md
│   └── validation-rules.md
└── assets/
    └── templates/          # Output templates
```

### SKILL.md Requirements

1. YAML frontmatter with `name`, `description`, optional `tools` and `model`
2. Purpose statement
3. When to Use section
4. Numbered workflow phases
5. Reference file links
6. Success criteria

```yaml
---
name: [skill-name]
description: Brief description of when to use this skill
tools: Read, Write, Edit, Bash
model: inherit
---
```

### Size Limits

- **Target**: 500-800 lines (~20,000-30,000 characters)
- **Maximum**: 1,000 lines (~40,000 characters)
- If exceeding target, extract detail into `references/` subdirectory (progressive disclosure)

### Prohibited Patterns

- Skills without a SKILL.md file
- Hardcoding logic (use AskUserQuestion for decisions)
- Language-specific skills (must be framework-agnostic)
- Circular skill dependencies

---

## Adding Subagents

Subagents are single-responsibility agents invoked by skills via `Task()`.

### File Location

```
.claude/agents/[agent-name].md
```

### Requirements

1. YAML frontmatter with `name`, `description`, `tools`, `model`
2. System prompt focused on a single responsibility
3. Tool restrictions following principle of least privilege

```yaml
---
name: agent-name
description: What this agent does
tools: Read, Grep, Glob
model: sonnet
---
```

### Size Limits

- **Target**: 100-300 lines (~4,000-12,000 characters)
- **Maximum**: 500 lines (~20,000 characters)

### Naming Convention

- Format: `[domain]-[role]` (e.g., `code-reviewer`, `backend-architect`)
- Lowercase with hyphens

### Prohibited Patterns

- Subagents with multiple responsibilities
- Overlapping functionality with existing agents
- Agents without tool restrictions

---

## Adding Slash Commands

Slash commands are user-facing entry points invoked with `/command-name` in Claude Code Terminal.

### File Location

```
.claude/commands/[command-name].md
```

### Requirements

1. YAML frontmatter with `description` and `argument-hint`
2. Instructions using `$ARGUMENTS` placeholder
3. Under 500 lines (<20,000 characters)

```yaml
---
description: Brief description shown in command list
argument-hint: STORY-ID or parameter description
---
```

### Prohibited Patterns

- Commands exceeding 500 lines (extract to skills instead)
- Commands without argument hints
- Commands that duplicate skill functionality

---

## Testing

### Python Tests (pytest)

Tests for the Python CLI live in `.claude/scripts/devforgeai_cli/tests/`.

```bash
# Set environment
cd /mnt/c/Projects/DevForgeAI
export PYTHONPATH=".:$PYTHONPATH"

# Run all Python tests
pytest .claude/scripts/devforgeai_cli/tests/

# Run specific module
pytest .claude/scripts/devforgeai_cli/tests/test_phase_commands.py

# Run single test
pytest .claude/scripts/devforgeai_cli/tests/test_phase_commands.py::test_specific_function -v

# Run with coverage
pytest .claude/scripts/devforgeai_cli/tests/ --cov=devforgeai_cli
```

### Node.js Tests (Jest)

```bash
# Run all tests
npm test

# Run unit tests only
npm run test:unit

# Run integration tests only
npm run test:integration

# Run with coverage
npm run test:coverage
```

### Shell Script Testing

Always run shell scripts with explicit `bash` on WSL:

```bash
# Correct
bash path/to/test.sh

# Wrong - may fail due to WSL permission issues
./path/to/test.sh
```

Fix line endings before running:

```bash
dos2unix path/to/test.sh && bash path/to/test.sh
```

### Test File Organization

- All tests reside under `tests/`
- Story-specific tests go in `tests/[STORY-ID]/`
- Never write tests to `/tmp/` -- use `{project-root}/tests/{story-id}/`
- Always test against `src/` tree, not operational `.claude/` folders

### Test File Write Protection

Test files are write-protected by phase:

| Agent | Authorized Phase |
|-------|-----------------|
| test-automator | Phase 02 (Red) only |
| integration-tester | Phase 05 (Integration) only |
| All other agents | Require explicit user approval |

### Common WSL Issues

| Issue | Fix |
|-------|-----|
| Module not found | `export PYTHONPATH=".:$PYTHONPATH"` |
| Permission denied on .sh | `chmod +x script.sh` or use `bash script.sh` |
| `$'\r': command not found` | `dos2unix script.sh` |
| pytest not found | `pip install pytest` |

---

## Code Standards

### File Operations

Use native Claude Code tools, never Bash for file operations:

| Operation | Correct | Prohibited |
|-----------|---------|-----------|
| Read file | `Read(file_path="...")` | `Bash(command="cat ...")` |
| Write file | `Write(file_path="...")` | `Bash(command="echo ... > ...")` |
| Edit file | `Edit(file_path="...", ...)` | `Bash(command="sed ...")` |
| Find files | `Glob(pattern="...")` | `Bash(command="find ...")` |
| Search content | `Grep(pattern="...")` | `Bash(command="grep ...")` |

**Exception**: Bash is required for running tests, builds, git operations, and package managers.

### Markdown Documentation Style

Write direct instructions, not narrative prose:

```markdown
## Phase 1: Context Validation

Read context files in PARALLEL:
- Read(file_path="devforgeai/specs/context/tech-stack.md")
- Read(file_path="devforgeai/specs/context/source-tree.md")

HALT if ANY file missing: "Context files incomplete"
```

### Naming Conventions

| Component | Convention | Example |
|-----------|-----------|---------|
| Files | lowercase-with-hyphens.md | `phase-01-preflight.md` |
| Skills | gerund-phrase | `implementing-stories` |
| Subagents | domain-role | `code-reviewer` |
| Commands | action or action-object | `create-story` |
| Test functions | `test_<func>_<scenario>_<expected>` | `test_validate_dod_missing_items_returns_error` |

### Component Size Limits

| Component | Target Lines | Maximum Lines |
|-----------|-------------|---------------|
| Skills | 500-800 | 1,000 |
| Slash Commands | 200-400 | 500 |
| Subagents | 100-300 | 500 |
| Context Files | 200-400 | 600 |

When exceeding targets, extract to `references/` subdirectory using progressive disclosure.

### Commit Format

Use conventional commit format:

```
feat(STORY-XXX): Add feature description
fix(STORY-XXX): Fix bug description
docs(STORY-XXX): Update documentation
refactor(STORY-XXX): Refactor component
```

---

## Context Files

Six immutable context files define the framework's constitutional constraints. They live in `devforgeai/specs/context/`.

| File | Purpose |
|------|---------|
| `tech-stack.md` | Approved technologies and tool constraints |
| `source-tree.md` | Directory structure and file location rules |
| `dependencies.md` | Dependency management rules |
| `coding-standards.md` | Code style, naming, and documentation standards |
| `architecture-constraints.md` | Architectural principles and boundaries |
| `anti-patterns.md` | Forbidden patterns with detection rules |

### Immutability Rules

- **Never** call `Edit()` or `Write()` on these files directly
- Changes require an approved Architecture Decision Record (ADR)
- After ADR approval, use the `/create-context` workflow to apply changes
- When two layers contradict, immutable context files take precedence

### Citation Requirements

When making technology or architecture recommendations, you must cite the relevant context file:

```
TypeScript is required for all new code
(Source: devforgeai/specs/context/tech-stack.md, lines 12-14)
```

Follow the Read-Quote-Cite-Verify protocol:
1. **Read** the source file
2. **Quote** the exact passage (minimum 2 lines)
3. **Cite** with file path and line numbers
4. **Verify** the recommendation matches the quote

---

## ADR Process

Architecture Decision Records document significant framework decisions. They are **append-only** -- never edit an existing ADR; create a new one to supersede it.

### Location

```
devforgeai/specs/adrs/ADR-NNN-short-description.md
```

### When to Create an ADR

- Introducing technology not in `tech-stack.md`
- Changing architectural constraints
- Modifying context file contents
- Swapping or adding libraries
- Changing workflow phases or skill interfaces

### ADR Template

```markdown
# ADR-NNN: Title

**Status**: Proposed | Accepted | Superseded by ADR-XXX
**Date**: YYYY-MM-DD
**Decision Makers**: [names]

## Context

What situation prompted this decision?

## Decision

What was decided and why?

## Consequences

### Positive
- Benefit 1
- Benefit 2

### Negative
- Tradeoff 1

### Neutral
- Side effect 1

## References

- Related ADRs
- External documentation
```

### ADR Propagation

After an ADR is accepted, its decisions must be propagated to all affected layers:

1. Update CLAUDE.md references if needed
2. Update rule files for enforcement
3. Run `/audit-alignment` to detect drift
4. Unpropagated ADRs are flagged as "adr_drift" by the alignment-auditor

### Layer Mutability Summary

| Layer | Mutability | Edit Protocol |
|-------|-----------|---------------|
| CLAUDE.md | Mutable | User approval via AskUserQuestion |
| Context Files (6) | Immutable | ADR + `/create-context` workflow |
| Rules (`.claude/rules/`) | Mutable | User approval via AskUserQuestion |
| ADRs | Append-only | Create new ADR to supersede |

---

## Quick Reference

| Topic | File |
|-------|------|
| Master Instructions | `CLAUDE.md` |
| Critical Rules | `.claude/rules/core/critical-rules.md` |
| Skills Reference | `.claude/memory/skills-reference.md` |
| Commands Reference | `.claude/memory/commands-reference.md` |
| Git Policy | `.claude/rules/core/git-operations.md` |
| Quality Gates | `.claude/rules/core/quality-gates.md` |
| Tech Stack | `devforgeai/specs/context/tech-stack.md` |
| Source Tree | `devforgeai/specs/context/source-tree.md` |
| Framework Status | `devforgeai/FRAMEWORK-STATUS.md` |
| Parallel Guide | `docs/guides/parallel-orchestration-guide.md` |
