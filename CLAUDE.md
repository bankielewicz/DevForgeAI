# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is **DevForgeAI**, a spec-driven development framework designed to enable AI-assisted software development with zero technical debt. The framework enforces architectural constraints, prevents anti-patterns, and maintains quality through automated validation.

---

## Core Philosophy

**Spec-Driven Development with AI Enforcement:**
- Immutable context files define architectural boundaries (tech-stack, source-tree, dependencies)
- AI agents MUST follow constraints; ambiguities trigger explicit user questions
- Quality gates enforce standards at every workflow stage
- Test-Driven Development (TDD) workflow: Red → Green → Refactor

**Constitution:** Evidence-based only. All patterns backed by research, official documentation, or proven practices. No aspirational content.

---

## Critical Rules - ALWAYS Follow

### 1. Technology Decisions

**ALWAYS check tech-stack.md before suggesting technologies.**

If spec requires technology not in tech-stack.md → STOP and use AskUserQuestion:
```
Question: "Spec requires [X], but tech-stack.md specifies [Y]. Which is correct?"
Options:
  - Use spec requirement [X] (update tech-stack.md + create ADR)
  - Use existing standard [Y] (spec is incorrect)
```

### 2. File Operations (CRITICAL for Token Efficiency)

**Use native tools (40-73% token savings vs Bash):**

✅ **CORRECT:**
- `Read(file_path="...")` NOT `cat`
- `Edit(...)` NOT `sed`
- `Write(...)` NOT `echo >` or `cat <<EOF`
- `Glob(pattern="...")` NOT `find`
- `Grep(pattern="...")` NOT `grep` command

❌ **FORBIDDEN:**
- Bash for file reading/editing/searching
- Only use Bash for: tests, builds, git, package managers

### 3. Ambiguity Resolution

**Use AskUserQuestion for ALL ambiguities:**
- Technology not specified in context files
- Multiple valid implementation approaches
- Conflicting requirements (spec vs context)
- Security-sensitive decisions
- Performance targets unclear ("fast", "scalable" without metrics)

### 4. Context Files Are Immutable

Never violate:
- `tech-stack.md` (locked technologies)
- `source-tree.md` (file structure rules)
- `dependencies.md` (approved packages)
- `coding-standards.md` (code patterns)
- `architecture-constraints.md` (layer boundaries)
- `anti-patterns.md` (forbidden patterns)

Changes require Architecture Decision Records (ADRs).

### 5. TDD Is Mandatory

Tests before implementation, always:
- Red phase: Write failing tests
- Green phase: Minimal code to pass
- Refactor phase: Improve while keeping tests green

### 6. Quality Gates Are Strict

Critical/High violations **block progression**:
- Light QA blocks immediately during development
- Deep QA blocks before release
- Coverage thresholds enforced: 95%/85%/80%

### 7. No Library Substitution

Technologies in tech-stack.md are **locked**. Cannot swap without:
1. User approval via AskUserQuestion
2. Creating ADR documenting decision
3. Updating tech-stack.md

### 8. Anti-Patterns Are Forbidden

Check anti-patterns.md before suggesting:
- God Objects (classes >500 lines)
- Direct instantiation (use DI)
- SQL concatenation (use parameterized queries)
- Hardcoded secrets (use environment variables)

### 9. Document All Decisions

Architecture decisions require ADRs in `.devforgeai/adrs/`:
- Technology selections
- Framework choices
- Design pattern decisions
- Structure changes

### 10. Ask, Don't Assume

When in doubt → **HALT and use AskUserQuestion**. Never make assumptions about:
- Technology preferences
- Architecture patterns
- Security requirements
- Performance targets

---

## Quick Reference - Progressive Disclosure

**For detailed guidance, see:**

- **Skills:** @.claude/memory/skills-reference.md
- **Subagents:** @.claude/memory/subagents-reference.md
- **Slash Commands:** @.claude/memory/commands-reference.md
- **QA Automation:** @.claude/memory/qa-automation.md
- **Context Files:** @.claude/memory/context-files-guide.md
- **UI Generator:** @.claude/memory/ui-generator-guide.md
- **Token Efficiency:** @.claude/memory/token-efficiency.md

---

## Development Workflow Overview

### Complete Lifecycle

```
1. IDEATION (devforgeai-ideation)
   ↓ Transforms business ideas → structured requirements

2. ARCHITECTURE (devforgeai-architecture)
   ↓ Creates 6 immutable context files

3. ORCHESTRATION (devforgeai-orchestration)
   ↓ Manages story lifecycle through 11 workflow states

4. UI GENERATION (devforgeai-ui-generator) [OPTIONAL]
   ↓ Generates UI specifications and code

5. DEVELOPMENT (devforgeai-development)
   ↓ TDD implementation: Write tests → Implement → Refactor

6. QA (devforgeai-qa)
   ↓ Light validation (during dev) + Deep validation (after)

7. RELEASE (devforgeai-release)
   ↓ Automated deployment with smoke tests and rollback
```

### Story Workflow States

Stories progress through **11 sequential states**:
```
Backlog → Architecture → Ready for Dev → In Development → Dev Complete →
QA In Progress → [QA Approved | QA Failed] → Releasing → Released
```

### Quality Gates

**Gate 1: Context Validation** (Architecture → Ready for Dev)
- All 6 context files exist and non-empty
- No placeholder content (TODO, TBD)

**Gate 2: Test Passing** (Dev Complete → QA In Progress)
- Build succeeds
- All tests pass (100% pass rate)
- Light validation passed

**Gate 3: QA Approval** (QA Approved → Releasing)
- Deep validation PASSED
- Coverage meets thresholds (95%/85%/80%)
- Zero CRITICAL violations
- Zero HIGH violations (or approved exceptions)

**Gate 4: Release Readiness** (Releasing → Released)
- QA approved
- All workflow checkboxes complete
- No blocking dependencies

---

## Common Commands

### Testing

```bash
# .NET
dotnet test
dotnet test --collect:"XPlat Code Coverage"

# Python
pytest
pytest --cov=src --cov-report=term

# JavaScript
npm test
npm test -- --coverage
```

### Building

```bash
# .NET
dotnet build
dotnet restore

# JavaScript
npm install
npm run build

# Python
pip install -r requirements.txt
```

### Linting and Formatting

```bash
# .NET
dotnet format
dotnet format --verify-no-changes

# Python
black src/
pylint src/

# JavaScript
npm run lint
prettier --write src/
```

### Git Workflow

```bash
git status
git diff
git add [files]
git commit -m "$(cat <<'EOF'
[type]: [brief description]

- Implemented [feature] following TDD
- Tests: [description]
- Compliance: tech-stack.md, coding-standards.md
- Coverage: [percentage]

Closes #[issue-number]
EOF
)"
git push origin [branch]
```

---

## CRITICAL: Skill Invocation Constraints

**Skills CANNOT accept parameters at invocation time.**

From official Claude documentation:
> "Skills CANNOT accept command-line style parameters. All parameters are conveyed through natural language in the conversation."

### ❌ WRONG - Skills with Parameters
```
Skill(command="devforgeai-qa --mode=deep --story=STORY-001")
Skill(command="devforgeai-development --story=STORY-001")
Skill(command="devforgeai-release --env=production")
```

### ✅ CORRECT - Context-Based Invocation
```
# Step 1: Load story content into conversation
@.ai_docs/Stories/STORY-001.story.md

# Step 2: Set context with explicit statements
**Story ID:** STORY-001
**Validation Mode:** deep
**Environment:** staging

# Step 3: Invoke skill WITHOUT arguments
Skill(command="devforgeai-qa")

# Skill extracts story ID from YAML frontmatter in loaded story file
# Skill extracts mode/environment from explicit statements in conversation
```

### Why This Works

1. **@file loads content** - Story YAML frontmatter becomes part of conversation
2. **Explicit statements provide context** - Skills search for patterns like "Mode: deep"
3. **Skills read conversation** - Extract information using pattern matching on conversation
4. **No parameter mechanism** - Skills operate purely on available conversation context

---

## Slash Commands (User-Facing Workflows)

DevForgeAI provides **9 slash commands** for common tasks:

### Command Syntax

**Parameter format:**
- Use positional arguments: `/command ARG1 ARG2 ARG3`
- NOT flag syntax: `/command --flag=value` (will trigger clarification)
- Access via: `$1`, `$2`, `$3` in command definitions

**Examples:**
```
/qa STORY-001 deep        ✅ Correct
/qa STORY-001 --mode=deep ⚠️ Works but educates to use: /qa STORY-001 deep
/release STORY-001 production     ✅ Correct
/release STORY-001 --env=production ⚠️ Works but educates
```

### Planning & Setup
- `/ideate [business-idea]` - Transform idea to requirements
- `/create-context [project-name]` - Generate 6 context files
- `/create-epic [epic-name]` - Create epic document
- `/create-sprint [sprint-number]` - Plan sprint

### Story Development
- `/create-story [description]` - Generate story with acceptance criteria
- `/create-ui [STORY-ID]` - Generate UI components
- `/dev [STORY-ID]` - Execute TDD cycle

### Validation & Release
- `/qa [STORY-ID] [mode]` - Run quality validation (mode: deep or light)
- `/release [STORY-ID] [environment]` - Deploy to staging/production
- `/orchestrate [STORY-ID]` - Full lifecycle (dev → qa → release)

**See:** @.claude/memory/commands-reference.md for complete command documentation.

---

## Framework Status

**Last Review:** 2025-10-31
**Status:** 🟢 **PHASE 3 COMPLETE - PRODUCTION READY**

### Implementation Progress

**Phase 1: Core Skills** ✅ Complete (2025-10-30)
- 7 skills implemented (devforgeai-ideation, architecture, orchestration, ui-generator, development, qa, release)

**Phase 2: Subagents** ✅ Complete (2025-10-31)
- 14 specialized subagents created
- Context isolation verified
- Parallel execution tested

**Phase 3: Slash Commands** ✅ Complete (2025-10-31)
- 9 user-facing commands in `.claude/commands/`
- All optimized for character budget (<15K limit)
- All integrate with skills via Skill tool

**Phase 4: Real Project Validation** ⏳ Ready to Begin
- Framework complete and ready for production testing

### Component Summary

- **Skills:** 7
- **Subagents:** 14
- **Commands:** 9
- **Context Files:** 6 (immutable constraints)

---

## Project Structure

```
.claude/
├── skills/              # 7 framework skills
│   ├── devforgeai-ideation/
│   ├── devforgeai-architecture/
│   ├── devforgeai-orchestration/
│   ├── devforgeai-ui-generator/
│   ├── devforgeai-development/
│   ├── devforgeai-qa/
│   └── devforgeai-release/
│
├── agents/              # 14 specialized subagents
│   └── [14 .md files]
│
├── commands/            # 9 slash commands
│   └── [9 .md files]
│
└── memory/              # Progressive disclosure references
    ├── skills-reference.md
    ├── subagents-reference.md
    ├── commands-reference.md
    ├── qa-automation.md
    ├── context-files-guide.md
    ├── ui-generator-guide.md
    └── token-efficiency.md

.devforgeai/
├── context/             # 6 immutable constraint files
│   ├── tech-stack.md
│   ├── source-tree.md
│   ├── dependencies.md
│   ├── coding-standards.md
│   ├── architecture-constraints.md
│   └── anti-patterns.md
│
├── adrs/                # Architecture Decision Records
├── deployment/          # Deployment configurations
├── qa/                  # QA outputs and reports
└── specs/               # Requirements and planning docs

.ai_docs/
├── Epics/               # Business initiatives
├── Sprints/             # 2-week iterations
└── Stories/             # Work units with acceptance criteria
```

---

## What NOT to Do

### ❌ No Aspirational Content
- No features that "might be nice" without evidence
- No hypothetical benefits without research backing
- If unsure → HALT and request human approval to research

### ❌ Don't Assume Files Exist
- Research docs (`.ai_docs/research/`) show PATTERNS as examples
- Most examples are NOT actual project files
- When in doubt: Use Glob/Read to verify file existence

### ❌ Don't Break Framework-Agnostic Principle
- Avoid language-specific recommendations in process docs
- Examples can be language-specific (mark clearly)
- Commands must work for Node.js, Python, C#, Go, Java, etc.

### ❌ Don't Violate Context Files
- Never swap locked technologies without approval + ADR
- Never put files in wrong locations
- Never add unapproved dependencies
- Never implement forbidden anti-patterns

---

## When Working in This Repository

### Starting New Work

1. **Ensure git repository initialized with commits:**
   ```bash
   git rev-list -n 1 HEAD 2>/dev/null
   # If no commits: Run /create-context (auto-creates initial commit)
   ```

2. **Check context files exist:**
   ```
   Glob(pattern=".devforgeai/context/*.md")
   # Should show 6 files
   ```

3. **If missing, create them:**
   ```
   > /create-context [project-name]
   # Also creates initial commit if repo is empty
   ```

4. **Then create story or epic:**
   ```
   > /create-story [description]
   ```

### Implementing a Story

**Option 1: Full Orchestration**
```
> /orchestrate STORY-001
# Executes: Dev → QA → Release automatically
```

**Option 2: Step-by-Step**
```
> /dev STORY-001        # Development with TDD
> /qa STORY-001         # Quality validation
> /release STORY-001    # Production deployment
```

### Adding UI Components

```
> /create-ui STORY-001
# Interactive: Choose web/GUI/terminal → Choose tech → Choose styling
# Output: UI specs and code in .devforgeai/specs/ui/
```

---

## Key File Locations

**Context Files:** `.devforgeai/context/` (6 constraint files)
**Stories:** `.ai_docs/Stories/{STORY-ID}.story.md`
**Epics:** `.ai_docs/Epics/{EPIC-ID}.epic.md`
**Sprints:** `.ai_docs/Sprints/Sprint-{N}.md`
**ADRs:** `.devforgeai/adrs/ADR-{NNN}-title.md`
**QA Reports:** `.devforgeai/qa/reports/{STORY-ID}-qa-report.md`
**Deployment:** `.devforgeai/deployment/` (platform configs)

---

## Integration Patterns

### Skills
```
Skill(command="devforgeai-architecture")
Skill(command="devforgeai-development --story=STORY-001")
Skill(command="devforgeai-qa --mode=deep --story=STORY-001")
```

### Subagents
```
Task(
  subagent_type="test-automator",
  description="Generate tests",
  prompt="Generate comprehensive tests for..."
)
```

### Commands
```
> /dev STORY-001
> /qa STORY-001
> /release STORY-001
```

---

## Security and Quality Standards

**Security:**
- No hardcoded secrets (use environment variables)
- Parameterized queries (prevent SQL injection)
- Input validation (prevent XSS)
- Strong cryptography (SHA256+, not MD5/SHA1)

**Code Quality:**
- Cyclomatic complexity <10 per method
- Maintainability index ≥70
- Code duplication <5%
- Documentation coverage ≥80% for public APIs

**Testing:**
- Test pyramid: 70% unit, 20% integration, 10% E2E
- Coverage: 95% business logic, 85% application, 80% infrastructure
- All acceptance criteria have tests
- Tests follow AAA pattern (Arrange, Act, Assert)

---

## References

**For detailed guidance:**
- Framework documentation: `ROADMAP.md`, `README.md`
- Skills: `.claude/skills/*/SKILL.md`
- Subagents: `.claude/agents/*.md`
- Commands: `.claude/commands/*.md`
- Research: `.ai_docs/` (prompt engineering, workflows, terminal best practices)

**Progressive disclosure references:**
- @.claude/memory/skills-reference.md
- @.claude/memory/subagents-reference.md
- @.claude/memory/commands-reference.md
- @.claude/memory/qa-automation.md
- @.claude/memory/context-files-guide.md
- @.claude/memory/ui-generator-guide.md
- @.claude/memory/token-efficiency.md
- @.claude/memory/token-budget-guidelines.md

---

**The framework exists to prevent technical debt through explicit constraints and automated validation. When in doubt, ask the user—never make assumptions.**
