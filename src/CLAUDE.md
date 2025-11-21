<!-- TEMPLATE: This is the source template. Installer merges this with user's CLAUDE.md -->
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview
Use native tools over bash.

Halt! if using Bash.

If presenting me with questions, use the AskUserQuestion tool.  When developing features/functionality within the DevForgeAI Spec Driven framework, use the AskUserQuestion tool for feedback witin the "human in the middle".
Deferals are not acceptable!

HALT! on deferals of implementation.  Use AskUserQuestion tool to see if user is ok with deferal.  Provide reasoning for deferal.

HALT! on commit with --no-verify
HALT! on modification of the pre-comit hook! 

When I pass a command to you, create the todo list, then execute it sequentially. Report progress as you complete each major section. 
HALT if you need clarification on any requirement or detect any ambiguity.

There are no time constraints and your context window is plenty big!

Claude skills do not run asynchonously or in the background.

This is **DevForgeAI**, a spec-driven development framework designed to enable AI-assisted software development with zero technical debt. The framework enforces architectural constraints, prevents anti-patterns, and maintains quality through automated validation.

● Bash(chmod +x /c/Users/bryan/bin/python3 && which python3)
  ⎿  /c/Users/bryan/bin/python3

● Perfect! Now python3 is available. Let me test it:

● Bash(python3 --version)
  ⎿  Python 3.10.11

---

## CRITICAL: How Skills Work

**Skills are INLINE PROMPT EXPANSIONS, not background processes.**

When you invoke a skill:
1. `Skill(command="devforgeai-development")` ← You invoke
2. System message: `"The 'devforgeai-development' skill is running"` ← Confirmation only
3. **Skill's SKILL.md content expands INLINE** ← This is the key
4. **YOU execute the skill's instructions** ← Your responsibility
5. You produce output following skill workflow ← Not waiting for external result

### Mental Model

**✅ CORRECT:** "Load additional instructions file and execute it"
**❌ WRONG:** "Launch separate process and wait for result"

### Comparison: Skills vs Subagents

| Aspect | Skills (Skill tool) | Subagents (Task tool) |
|--------|--------------------|-----------------------|
| **Execution** | You execute instructions inline | Separate agent executes in isolated context |
| **Who produces output** | You | Agent |
| **Where execution happens** | Current conversation | Isolated context |
| **When to wait** | ❌ NEVER - You execute | ✅ YES - Agent executes |

### When Skill Invoked

**What you SHOULD do:**
1. Read the skill's SKILL.md content (now in conversation)
2. Follow the skill's workflow phases
3. Execute each phase's instructions
4. Produce output as you work
5. Complete with skill's success criteria

**What you should NOT do:**
1. ❌ Wait for skill to "return results"
2. ❌ Assume skill is executing elsewhere
3. ❌ Stop workflow and wait passively

### Example

```
User: /dev STORY-001
You: Skill(command="devforgeai-development")
System: "The devforgeai-development skill is running"
```

**✅ Correct action:**
```
You: [Read skill's Phase 0 instructions]
You: [Execute Phase 0: Git validation, context checks]
You: [Display Phase 0 results]
You: [Continue to Phase 1: Red phase]
You: [Invoke test-automator subagent]
You: [Wait for subagent result]
You: [Continue to Phase 2...]
... [Complete all phases]
You: [Display final completion report]
```

**❌ Incorrect action:**
```
You: "The skill is running, I'll wait for it to complete"
You: [Stops and waits passively] ← THIS IS WRONG
```

### Understanding System Messages

When you see:
```
<command-message>The "devforgeai-development" skill is running</command-message>
```

**This message means:**
- ✅ Skill invocation successful
- ✅ Skill's SKILL.md content is now in conversation
- ✅ **You must now execute the skill's instructions**

**This message does NOT mean:**
- ❌ Skill is executing elsewhere
- ❌ Wait for skill to return results
- ❌ Skill is running in background

**Immediately after seeing this message:**
1. Locate the skill's SKILL.md content in conversation
2. Read Phase 0 instructions
3. Begin executing Phase 0
4. Continue through all phases

### Emergency Recovery

**If you've already stopped and are reading this:**
1. Apologize to user: "I incorrectly stopped after skill invocation"
2. Explain: "Skills expand inline - I should have executed the instructions"
3. Resume: "Let me now execute the skill's workflow starting from Phase 0"
4. Continue: Execute all phases to completion
5. Learn: Remember this for future skill invocations

**See also:** `.claude/memory/skill-execution-troubleshooting.md` for detailed recovery procedures

---

## Core Philosophy

**Spec-Driven Development with AI Enforcement:**
- Immutable context files define architectural boundaries (tech-stack, source-tree, dependencies)
- AI agents MUST follow constraints; ambiguities trigger explicit user questions
- Quality gates enforce standards at every workflow stage
- Test-Driven Development (TDD) workflow: Red → Green → Refactor

**Constitution:** Evidence-based only. All patterns backed by research, official documentation, or proven practices. No aspirational content.

---

## Prerequisites

### Git Repository Requirement

DevForgeAI workflows require Git initialization for version control and change tracking.

**Initialize Git:**
```bash
git init
git add .
git commit -m "Initial commit"
```

**Commands requiring Git:**
- `/dev` - Development workflow (TDD cycle)
- `/qa` - Quality assurance (validation)
- `/release` - Deployment (production)
- `/orchestrate` - Full lifecycle (dev → qa → release)

**Commands Git-independent:**
- `/ideate` - Requirements gathering
- `/create-context` - Architecture setup (auto-initializes Git if empty repo)
- `/create-story` - Story generation
- `/create-epic` - Epic planning
- `/create-sprint` - Sprint planning

**File-Based Fallback:**

If Git is not available, DevForgeAI automatically uses file-based change tracking:
- Changes documented in `.devforgeai/stories/{STORY-ID}/changes/`
- Manual file organization required
- Full version control features disabled
- Recommended: Initialize Git for best experience

**Error Prevention:**

The `/dev` command checks `<env>` context for Git availability before execution:
- If Git missing → Clear error message with resolution steps
- If Git available → Full TDD workflow with version control
- No cryptic Git errors exposed to users

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

### 11. Git Operations Require User Approval (RCA-008)

**NEVER execute git commands autonomously that:**
- Stash files (especially with `--include-untracked`)
- Reset uncommitted changes (`git reset --hard`)
- Delete branches (`git branch -D`)
- Force push (`git push --force`)
- Amend commits not created in current session (`git commit --amend`)
- Affect >10 files without user knowledge

**ALWAYS use AskUserQuestion before git operations that:**
- Hide files from filesystem
- Permanently delete uncommitted work
- Modify git history
- Affect user-created files outside current story

**Required approval pattern:**
```
AskUserQuestion(
    questions=[{
        question: "Git operation will affect {N} files. How should we proceed?",
        header: "Git Action",
        multiSelect: false,
        options: [
            {
                label: "Show me the files first",
                description: "Display file list before deciding."
            },
            {
                label: "Proceed (I understand the consequences)",
                description: "[Clear explanation of what will happen]"
            },
            {
                label: "Cancel (use alternative approach)",
                description: "[What alternative will be used instead]"
            }
        ]
    }]
)
```

**Exceptions (NO user approval needed):**
- `git status` (read-only)
- `git diff` (read-only)
- `git log` (read-only)
- `git add` for current story files (≤5 files created in this session)
- `git commit` for current story implementation (TDD workflow)

**File-Based Fallback:**
When git operations are declined or unavailable:
- Use `.devforgeai/stories/{STORY-ID}/changes/` directory
- Document changes in `changes-manifest.md`
- Preserve all user files (nothing hidden)

**Rationale:** RCA-008 incident (2025-11-13) showed autonomous `git stash --include-untracked` hid 21 user-created story files without consent, causing confusion and workflow disruption. User approval prevents data loss and maintains trust.

**See also:**
- `.devforgeai/RCA/RCA-008-autonomous-git-stashing.md` (full incident analysis)
- `.claude/skills/devforgeai-development/references/git-workflow-conventions.md` (stash safety protocol)
- `.claude/skills/devforgeai-development/references/preflight-validation.md` (Steps 0.1.5 and 0.1.6)

---

## Quick Reference - Progressive Disclosure

**For detailed guidance, load reference files as needed using the Read tool:**

```
Read(file_path=".claude/memory/skills-reference.md")
Read(file_path=".claude/memory/subagents-reference.md")
Read(file_path=".claude/memory/commands-reference.md")
Read(file_path=".claude/memory/documentation-command-guide.md")
```

**Available reference files:**
- **Skills:** `.claude/memory/skills-reference.md`
- **Subagents:** `.claude/memory/subagents-reference.md`
- **Slash Commands:** `.claude/memory/commands-reference.md`
- **Documentation Command:** `.claude/memory/documentation-command-guide.md`
- **QA Automation:** `.claude/memory/qa-automation.md`
- **Context Files:** `.claude/memory/context-files-guide.md`
- **UI Generator:** `.claude/memory/ui-generator-guide.md`
- **Token Efficiency:** `.claude/memory/token-efficiency.md`
- **Epic Creation:** `.claude/memory/epic-creation-guide.md`
- **Token Budgets:** `.claude/memory/token-budget-guidelines.md`
- **Lean Orchestration:** `.devforgeai/protocols/lean-orchestration-pattern.md`
  - Case Studies: `.devforgeai/protocols/refactoring-case-studies.md`
  - Budget Reference: `.devforgeai/protocols/command-budget-reference.md`

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

3.5. STORY CREATION (devforgeai-story-creation) [AS NEEDED]
   ↓ Generates complete stories with AC, tech/UI specs, self-validation

4. UI GENERATION (devforgeai-ui-generator) [OPTIONAL]
   ↓ Generates UI specifications and code

5. DEVELOPMENT (devforgeai-development)
   ↓ TDD implementation: Write tests → Implement → Refactor

6. QA (devforgeai-qa)
   ↓ Light validation (during dev) + Deep validation (after)

6.5. DOCUMENTATION (devforgeai-documentation) [AFTER QA]
   ↓ Generate/update docs, diagrams, coverage validation (≥80%)

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

## DevForgeAI-CLI Validators

**Purpose:** Automated workflow validation to prevent autonomous deferrals and enforce quality gates.

### Installation

```bash
# Install CLI package
pip install --break-system-packages -e .claude/scripts/

# Install pre-commit hooks
bash .claude/scripts/install_hooks.sh

# Verify
devforgeai --version
```

### Commands

**validate-dod** - Validate Definition of Done completion
```bash
devforgeai validate-dod .ai_docs/Stories/STORY-001.story.md
```
- Detects autonomous deferrals (DoD [x] but Impl [ ] without approval)
- Validates user approval markers for all deferred items
- Checks story/ADR references exist
- **Blocks git commits via pre-commit hook**

**check-git** - Validate Git availability
```bash
devforgeai check-git
```
- Checks if directory is Git repository
- Prevents RCA-006 errors
- Can be called from slash commands

**validate-context** - Validate context files
```bash
devforgeai validate-context
```
- Ensures all 6 context files exist
- Quality gate before development
- Validates non-empty content

### Pre-Commit Hook

Automatically installed via `install_hooks.sh`:
- Runs `validate-dod` on all staged `.story.md` files
- Blocks commits with autonomous deferrals
- Requires user approval markers for all deferrals
- Exit code 1 = commit blocked

**Three-Layer Validation:**
1. **Layer 1:** CLI validators (fast, <100ms, deterministic) ← NEW
2. **Layer 2:** AskUserQuestion (interactive, mandatory user approval)
3. **Layer 3:** AI subagents (comprehensive, semantic analysis)

Combined: 99% violation detection, zero autonomous deferrals.

**Documentation:** `.claude/scripts/devforgeai_cli/README.md`

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

DevForgeAI provides **11 slash commands** for common tasks:

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
- `/create-agent [name] [options]` - Create framework-aware subagent (NEW)

### Story Development
- `/create-story [description]` - Generate story with acceptance criteria
- `/create-ui [STORY-ID]` - Generate UI components
- `/dev [STORY-ID]` - Execute TDD cycle

### Validation & Release
- `/qa [STORY-ID] [mode]` - Run quality validation (mode: deep or light)
- `/release [STORY-ID] [environment]` - Deploy to staging/production
- `/orchestrate [STORY-ID]` - Full lifecycle (dev → qa → release)

### Framework Maintenance
- `/audit-deferrals` - Audit all stories for deferral violations
- `/audit-budget` - Audit commands for character budget compliance

**See:** `.claude/memory/commands-reference.md` for complete command documentation (load with Read tool).

---

## Framework Status

**Last Review:** 2025-11-04
**Version:** 1.0.1
**Status:** 🟢 **PRODUCTION READY** (Phase 3 Complete + RCA-006 Enhancements)

### Implementation Progress

**Phase 1: Core Skills** ✅ Enhanced (2025-11-05)
- 8 skills implemented (devforgeai-ideation, architecture, orchestration, story-creation, ui-generator, development, qa, release)
- New: devforgeai-story-creation (complete story generation with self-validation)

**Phase 2: Subagents** ✅ Enhanced (2025-11-05)
- 20 specialized subagents created (14 original + 2 from RCA-006 + 2 from /dev refactoring + 1 from /qa refactoring + 1 from /create-ui refactoring)
- New: tech-stack-detector, git-validator, qa-result-interpreter, ui-spec-formatter
- Context isolation verified
- Parallel execution tested
- Framework-aware subagents (prevent silos)

**Phase 3: Slash Commands** ✅ Enhanced (2025-11-05)
- 9 user-facing commands in `.claude/commands/`
- /dev refactored: 860 → 513 lines (40% reduction, lean orchestration)
- All optimized for character budget (~16K, close to 15K limit)
- All integrate with skills via Skill tool
- Clear separation: commands delegate to skills, skills delegate to subagents

**RCA-006: Deferral Validation** ✅ Phase 1 & Original Phase 2 Complete (2025-11-06)
- **Phase 1 (CRITICAL):** Phase 4.5 Deferral Challenge Checkpoint prevents autonomous deferrals
  - All deferrals (pre-existing + new) require user approval
  - deferral-validator subagent checks blocker validity
  - Timestamp all approvals for audit trail
  - "Attempt First, Defer Only If Blocked" pattern enforced
- **Original Phase 2 (HIGH):** Quality improvements and proactive monitoring
  - Deferral budget limits (max 3, max 20% of DoD items) enforced in Phase 5 Step 1.6
  - Enhanced /audit-deferrals with blocker validation (dependency, toolchain, artifact, ADR checks)
  - Auto-invoke /audit-deferrals at sprint retrospective with debt reduction sprint creation
  - Actionable insights (resolvable vs valid deferrals with specific commands)
  - Technical debt metrics (age tracking, trend analysis, stale deferral detection)
- **Story template guidance:** Anti-pattern documentation prevents pre-deferrals
- **Three-layer validation:** Python format check + Interactive checkpoint + AI subagent
- **See:** `.devforgeai/RCA/RCA-006-autonomous-deferrals.md` for complete analysis

**RCA-006: Structured Technical Specifications (Phase 2 - NEW Phasing)** 🟢 Weeks 2-3/4 Complete (2025-11-07)
- **Purpose:** Machine-readable tech specs for deterministic parsing and automated validation
- **Status:** Weeks 2-3 implementation complete (code ready), Weeks 4-5 testing pending
- **Phase 2 New Implementation (4-week plan):**
  - **Week 2 ✅ COMPLETE:** Structured YAML format v2.0 defined (7 component types: Service, Worker, Configuration, Logging, Repository, API, DataModel)
  - **Week 2 ✅ COMPLETE:** Validation library created (validate_tech_spec.py - 235 lines)
  - **Week 2 ✅ COMPLETE:** Basic migration script (migrate_story_v1_to_v2.py - 165 lines, 60-70% accuracy)
  - **Week 2 ✅ COMPLETE:** Story template updated to v2.0 (YAML code blocks, test requirements)
  - **Week 2 ✅ COMPLETE:** Dual format detection in /dev (Step 4.1 parses v1.0 or v2.0)
  - **Week 3 ✅ CODE COMPLETE:** AI-assisted migration enhancement (migrate_story_v1_to_v2.py enhanced to 659 lines)
    - AIConverter class with Claude API integration (+100 lines)
    - Conversion prompt template (660 lines with examples, quality standards)
    - Hybrid strategy (AI 95%+ → Pattern matching 60-70% fallback)
    - 27 test fixtures (5 test stories + ground truth, 12 validator tests)
    - Accuracy measurement script (measure_accuracy.py - 141 lines)
    - Automated test runner (run_all_tests.sh)
    - Requires: ANTHROPIC_API_KEY for AI mode, works without (fallback)
  - **Week 3 ⏳ TESTING PENDING:** External validation with Claude API key (expected 95%+ accuracy)
  - **Week 4 ⏳ PENDING:** Pilot migration (10 stories), manual review, GO/NO-GO decision
  - **Week 5 ⏳ PENDING:** Full migration (all stories), Decision Point 2
- **Impact (projected):** Coverage gap detection 85% → 95%+, enables Phase 3 implementation validation
- **Backward compatibility:** v1.0 freeform stories still supported (dual format)
- **Migration:** Optional (gradual path), AI-assisted tool ready for use
- **See:** `.devforgeai/specs/STRUCTURED-FORMAT-SPECIFICATION.md`, `AI-ASSISTED-MIGRATION-GUIDE.md`, `PHASE2-WEEK3-DELIVERY-PACKAGE.md`

**RCA-007: Multi-File Story Creation** ✅ Complete (2025-11-06 - All 3 Phases)
- **Phase 1 (HIGH):** Enhanced subagent prompts with 4-section template
  - Pre-Flight Briefing explains workflow context
  - Critical Output Constraints prohibit file creation
  - Prohibited Actions list (8 forbidden operations)
  - Expected Output Format with examples
  - Validation checkpoint (Step 2.1.5) detects file creation attempts
  - Automatic recovery (re-invoke with STRICT MODE)
- **Phase 2 (MEDIUM):** Contract-based validation and file system monitoring
  - YAML contracts (requirements-analyst-contract.yaml, api-designer-contract.yaml)
  - Contract validation (Step 2.2.5, Step 3.2.5)
  - File system diff check (Steps 2.0, 2.2.7, 3.0, 3.2.7)
  - Validation script (validate_contract.py) with test fixtures
  - 4-layer defense in depth (prompt → output → contract → file system)
- **Phase 3 (MEDIUM):** Skill-specific subagent creation
  - story-requirements-analyst subagent (21st subagent)
  - No Write/Edit tools (file creation impossible by design)
  - Tight coupling to devforgeai-story-creation workflow
  - Content-only output (returns markdown for assembly)
  - 99.9% violation prevention (architectural constraint)
- **Result:** Single-file design enforced, zero extra files (SUMMARY.md, QUICK-START.md, etc.)
- **See:** `.devforgeai/RCA/RCA-007-multi-file-story-creation.md` for complete analysis

**Phase 4: Real Project Validation** ⏳ Ready to Begin
- Framework complete and ready for production testing

### Component Summary

- **Skills:** 15 functional + 1 incomplete (16 total directories)
  - **Core Workflow (9):** ideation, architecture, orchestration, story-creation, ui-generator, development, qa, release, rca
  - **DevForgeAI Infrastructure (4):** documentation, feedback, mcp-cli-converter, subagent-creation
  - **Claude Code Infrastructure (2):** claude-code-terminal-expert, skill-creator
  - **Incomplete (1):** internet-sleuth-integration (missing SKILL.md, use internet-sleuth subagent instead)
  - **EPIC-010 Will Add (1):** github (GitHub Actions CI/CD)
- **Subagents:** 26 (includes deferral-validator, technical-debt-analyzer, tech-stack-detector, git-validator, qa-result-interpreter, ui-spec-formatter, sprint-planner, story-requirements-analyst, code-analyzer, **internet-sleuth**, pattern-compliance-auditor, dev-result-interpreter)
- **Commands:** 23 total
  - **Core Workflow (11):** ideate, create-context, create-epic, create-sprint, create-story, create-ui, dev, qa, release, orchestrate, create-agent
  - **Feedback System (7):** feedback, feedback-config, feedback-search, feedback-reindex, feedback-export-data, export-feedback, import-feedback
  - **Framework Maintenance (4):** audit-deferrals, audit-budget, audit-hooks, rca
  - **Documentation (1):** document
  - **EPIC-010 Will Add (2):** worktrees, setup-github-actions
- **Context Files:** 6 (immutable constraints)
- **Quality Gates:** 4 (Gate 3 enhanced with deferral validation)
- **Protocols:** 1 (lean-orchestration-pattern.md - defines command architecture)

---

## Project Structure

```
.claude/
├── skills/              # 9 skills (8 DevForgeAI + 1 infrastructure)
│   ├── devforgeai-ideation/
│   ├── devforgeai-architecture/
│   ├── devforgeai-orchestration/
│   ├── devforgeai-story-creation/
│   ├── devforgeai-ui-generator/
│   ├── devforgeai-development/
│   ├── devforgeai-qa/
│   ├── devforgeai-release/
│   └── claude-code-terminal-expert/  # Claude Code Terminal knowledge
│
├── agents/              # 20 specialized subagents
│   └── [20 .md files]
│
├── commands/            # 11 slash commands
│   └── [11 .md files]
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
├── protocols/           # Framework protocols and patterns
│   └── lean-orchestration-pattern.md
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

## Root Cause Analysis Protocol

When you encounter a framework breakdown, use the RCA capability to systematically analyze and prevent recurrence.

### Trigger Command

```bash
/rca [issue-description] [severity]
```

**Examples:**
- `/rca "devforgeai-development didn't validate context files" CRITICAL`
- `/rca "QA skill accepted pre-existing deferrals without challenge" HIGH`
- `/rca "orchestration skill skipped checkpoint detection" MEDIUM`
- `/rca "/dev command contains business logic"`

### What Happens

**8-Phase RCA Workflow:**

1. **Auto-Read Files** - Relevant skills, commands, subagents, context files
2. **5 Whys Analysis** - Progressive questioning to root cause
3. **Evidence Collection** - File excerpts, line numbers, quotes
4. **Recommendations** - Exact implementation (CRITICAL → LOW priority)
5. **RCA Document** - Created in `.devforgeai/RCA/RCA-XXX-title.md`
6. **Validation** - Self-check for completeness
7. **Completion Report** - Summary with next steps

### Output Format

**RCA document includes:**
- Issue description and metadata (date, component, severity)
- 5 Whys analysis with evidence backing each answer
- Files examined (comprehensive excerpts with line numbers)
- Recommendations by priority (CRITICAL/HIGH/MEDIUM/LOW)
- Exact implementation code/text (copy-paste ready)
- Testing procedures for each recommendation
- Implementation checklist
- Prevention strategy (short-term and long-term)
- Related RCAs

### Protocol Rules

**Evidence-Based Only:**
- No aspirational recommendations
- All solutions backed by file evidence
- Works within Claude Code Terminal capabilities
- References actual files examined during analysis

**Framework-Aware:**
- Respects 6 immutable context files
- Understands quality gates and workflow states
- Applies lean orchestration pattern
- References existing RCA patterns (RCA-006, RCA-007, RCA-008, RCA-009)

**Actionable:**
- Exact file paths and sections (Phase X, Step Y)
- Copy-paste ready implementation
- Clear testing procedures (3+ verification steps)
- Effort estimates (time and complexity)

**User Preferences (Confirmed):**
- ✅ Auto-read relevant files during RCA
- ✅ Create RCA document automatically
- ✅ Comprehensive evidence with file excerpts
- ✅ Include exact implementation code/text

### When to Trigger RCA

**Strong indicators:**
- Process failures (skill/command didn't work as intended)
- Workflow violations (quality gate bypassed, state incorrect)
- Constraint violations (context files ignored)
- Autonomous operations (without user approval)
- Recurrent issues (happened before)

**Examples from existing RCAs:**
- RCA-006: Autonomous deferrals without user approval
- RCA-007: Subagent created multiple files (should return content only)
- RCA-008: Autonomous git stashing without user consent
- RCA-009: Skill invoked but workflow stopped prematurely

---

## Story Progress Tracking (NEW - RCA-011)

**DevForgeAI provides three complementary progress tracking mechanisms during TDD implementation:**

### 1. TodoWrite (Phase-Level Tracking)
**Purpose:** AI self-monitoring - tracks which TDD phase is executing
**Updated:** Real-time as phases start/complete
**Granularity:** Phase-level (8 phases: Phase 0, 1, 2, 3, 4, 4.5, 4.5-5 Bridge, 5, 6)
**Visible to:** User sees visual progress bars in terminal
**Example:** "✓ Execute Phase 2: Implementation (pending → completed)"

### 2. AC Verification Checklist (Sub-Item Tracking)
**Purpose:** User visibility into AC completion progress
**Updated:** End of each TDD phase (batch update Phase 1-5 items)
**Granularity:** AC sub-item level (20-50 items per story, mapped to phases)
**Visible to:** User in story file's "Acceptance Criteria Verification Checklist" section
**Example:** "✓ Character count ≤15,000 - Phase: 2 - Evidence: wc -c"

**When items are checked:**
- Phase 1: Test generation items (test count, coverage, file creation)
- Phase 2: Implementation items (code written, business logic location, metrics)
- Phase 3: Quality items (complexity, patterns, code review)
- Phase 4: Integration items (scenarios, performance, coverage thresholds)
- Phase 4.5: Deferral items (validations, approvals)
- Phase 5: Deployment items (commit, status, backward compatibility)

### 3. Definition of Done (Official Completion Record)
**Purpose:** Quality gate validation - official record of what's complete
**Updated:** Phase 4.5-5 Bridge (after deferrals validated, before git commit)
**Granularity:** DoD item level (30-40 items per story, categorized)
**Visible to:** User in story file's "Definition of Done" section + "Implementation Notes"
**Example:** "- [x] All tests passing - Completed: Phase 4, 165/168 tests (98.2%)"

### Why All Three?

**TodoWrite** → AI knows where it is (prevents skipped phases)
**AC Checklist** → User sees granular progress (transparency)
**Definition of Done** → Framework validates completion (quality gate)

Each serves a distinct purpose. Together they provide comprehensive progress visibility and prevent autonomous deferrals.

**See:** `.claude/skills/devforgeai-development/references/ac-checklist-update-workflow.md` for AC Checklist implementation details

---

## Acceptance Criteria vs. Tracking Mechanisms (RCA-012 Clarification)

**IMPORTANT:** Stories contain both AC **definitions** and AC **tracking**. Understanding the distinction eliminates confusion about unchecked checkboxes.

### Three Tracking Mechanisms Comparison

| Element | Purpose | Checkbox Behavior | Updated When | Source of Truth |
|---------|---------|-------------------|--------------|-----------------|
| **AC Headers** (e.g., `### AC#1: Title`) | **Define what to test** (immutable specification) | **Never marked** (no checkboxes as of v2.1) | Never (definitions are static) | Story creation |
| **AC Verification Checklist** | **Track granular progress** (real-time sub-items) | Marked `[x]` during TDD phases | End of each TDD phase (1-5) | TDD execution |
| **Definition of Done** | **Official completion record** (quality gate) | Marked `[x]` in Phase 4.5-5 Bridge | After deferrals validated, before commit | Quality gate validation |

### Why AC Headers Have No Checkboxes (Template v2.1+)

**AC headers are specifications, not progress trackers.**

Acceptance Criteria define **WHAT needs to be tested/implemented**. They are static requirements that remain valid throughout the story lifecycle. Marking an AC header "complete" would incorrectly imply the requirement is no longer relevant.

**Progress tracking happens in two places:**
1. **AC Verification Checklist** - Granular sub-item tracking (20-50 items per story, updated during TDD phases)
2. **Definition of Done** - Official completion tracking (30-40 items per story, updated in Phase 4.5-5 Bridge)

**Example (STORY-052 - Documentation Story):**

**AC Header (Definition - Never Marked):**
```markdown
### AC#1: Document Completeness - Core Content Coverage

**Given** the effective prompting guide exists
**When** a user reads the guide
**Then** the document contains:
- Introduction explaining why clear input matters (≥200 words)
- Command-specific guidance for 11 commands
- 20-30 before/after examples
```
↑ This is a **specification** - defines what success looks like

**DoD Items (Completion Tracker - Marked When Complete):**
```markdown
### Implementation
- [x] Document includes introduction (648 words explaining purpose and value)
- [x] All 11 commands have dedicated guidance sections
- [x] 24 before/after examples included with explanations
```
↑ These are **completion records** - marked [x] when work is done

**The Distinction:**
- **AC Header:** "Document must have ≥200 word introduction" (requirement definition)
- **DoD Item:** "Document includes introduction (648 words)" (completion evidence)

### For Older Stories (Template v2.0 and Earlier)

**Template Evolution Timeline:**
- **v1.0 stories:** AC headers have `### 1. [ ]` checkbox syntax (vestigial)
- **v2.0 stories:** AC headers have `### 1. [ ]` checkbox syntax (vestigial)
- **v2.1 stories:** AC headers have `### AC#1:` format (no checkboxes) ← NEW (as of 2025-01-21)

**Important:** In v1.0/v2.0 stories, AC header checkboxes may or may not be marked:
- **20% of stories (e.g., STORY-007):** AC headers marked `[x]` when DoD 100% complete
- **80% of stories (e.g., STORY-014, STORY-023, STORY-030, STORY-052):** AC headers left `[ ]` regardless of completion

**No documented convention existed** for v1.0/v2.0 templates, leading to framework-wide inconsistency discovered in RCA-012.

### How to Determine Story Completion Status

**Single Source of Truth: Definition of Done Section**

**❌ Do NOT rely on AC header checkboxes** in v1.0/v2.0 stories - they don't reliably indicate completion

**✅ Check Definition of Done section instead:**
```markdown
## Definition of Done

### Implementation
- [x] Feature implemented  ← All items [x] = Implementation complete
- [x] Code reviewed

### Quality
- [x] Tests passing        ← All items [x] = Quality validated
- [x] Coverage met

### Testing
- [x] Unit tests           ← All items [x] = Testing complete
- [x] Integration tests

### Documentation
- [x] Docs updated          ← All items [x] = Documentation complete
```

**If DoD has unchecked items `[ ]`:**
1. Check for **"Approved Deferrals"** section in Implementation Notes
2. **If section exists** with user approval timestamp → Valid deferral (story complete per agreement)
3. **If section missing** → Story incomplete (should NOT be "QA Approved" - quality gate violation)

**Decision Tree:**
```
Want to know if story is complete?
  ↓
Check DoD section
  ├─ All items [x]? → Story 100% complete ✅
  └─ Some items [ ]?
      ↓
      Check for "Approved Deferrals" section
        ├─ Section exists with user approval timestamp?
        │   → Story complete with documented deferrals ✅
        └─ Section missing?
            → Story incomplete (quality gate violation) ❌
```

**Secondary Indicator: Workflow Status**
```markdown
## Workflow Status
- [x] Architecture phase complete
- [x] Development phase complete  ← Status "Dev Complete" matches this
- [ ] QA phase complete           ← Status "QA Approved" would mark this [x]
- [ ] Released                    ← Status "Released" would mark this [x]
```

### Quality Gate Rule (As of RCA-012 Remediation)

**QA Validation Now Enforces (Phase 0.9):**

1. **100% AC-to-DoD traceability**
   - Every AC requirement must have corresponding DoD item
   - Validated via explicit checkbox OR test validation OR metric validation

2. **Documented deferrals**
   - Any unchecked DoD item `[ ]` requires "Approved Deferrals" section
   - Section must include:
     - User approval timestamp (e.g., "2025-01-21 10:30 UTC")
     - Blocker justification (Dependency, Toolchain, Artifact, ADR, Low-Priority)
     - Follow-up reference (story ID or completion condition)

**QA Will HALT If:**
- AC requirement has no DoD coverage (traceability <100%)
- DoD has unchecked items without "Approved Deferrals" section
- Deferral section exists but missing user approval timestamp

**See:** `.claude/skills/devforgeai-qa/references/traceability-validation-algorithm.md` (created in RCA-012 Phase 2)

### Migration Guidance (Optional)

**Want to update old stories (v2.0) to new format (v2.1)?**

Use migration script:
```bash
bash .claude/skills/devforgeai-story-creation/scripts/migrate-ac-headers.sh <story-file>
```

**What it does:**
- Changes `### 1. [ ]` → `### AC#1:`
- Updates `format_version: "2.0"` → `"2.1"`
- Creates backup (`.v2.0-backup`) before changes
- Validates migration success

**When to migrate:**
- Want visual consistency across all stories
- Find checkbox syntax confusing in old stories
- Preparing stories for presentation/review

**When to skip:**
- Old format doesn't bother you
- Story is archived (no active work)
- Migration risk outweighs benefit

**See:** `.devforgeai/RCA/RCA-012/MIGRATION-SCRIPT.md` for complete migration documentation

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

### ❌ Don't Execute Destructive Git Operations Without Approval
- Never stash files without showing user what will be hidden
- Never reset uncommitted changes without confirmation
- Never force push without explicit user request
- Never amend commits not created in current session
- See Critical Rule #11 for complete git operation policy

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

**Progressive disclosure references (load as needed with Read tool):**
- `.claude/memory/skills-reference.md`
- `.claude/memory/subagents-reference.md`
- `.claude/memory/commands-reference.md`
- `.claude/memory/documentation-command-guide.md`
- `.claude/memory/qa-automation.md`
- `.claude/memory/context-files-guide.md`
- `.claude/memory/ui-generator-guide.md`
- `.claude/memory/token-efficiency.md`
- `.claude/memory/token-budget-guidelines.md`

**Framework protocols (load as needed with Read tool):**
- `.devforgeai/protocols/lean-orchestration-pattern.md` - Command architecture and refactoring
- `.devforgeai/protocols/refactoring-case-studies.md` - Detailed refactoring examples
- `.devforgeai/protocols/command-budget-reference.md` - Budget tables and monitoring

---

**The framework exists to prevent technical debt through explicit constraints and automated validation. When in doubt, ask the user—never make assumptions.**
