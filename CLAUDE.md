# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

If presenting me with questions, use the AskUserQuestion tool.  When developing features/functionality within the DevForgeAI Spec Driven framework, use the AskUserQuestion tool for feedback witin the "human in the middle".

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

**For detailed guidance, see:**

- **Skills:** @.claude/memory/skills-reference.md
- **Subagents:** @.claude/memory/subagents-reference.md
- **Slash Commands:** @.claude/memory/commands-reference.md
- **QA Automation:** @.claude/memory/qa-automation.md
- **Context Files:** @.claude/memory/context-files-guide.md
- **UI Generator:** @.claude/memory/ui-generator-guide.md
- **Token Efficiency:** @.claude/memory/token-efficiency.md
- **Epic Creation:** @.claude/memory/epic-creation-guide.md
- **Lean Orchestration:** @.devforgeai/protocols/lean-orchestration-pattern.md (core principles)
  - Case Studies: @.devforgeai/protocols/refactoring-case-studies.md
  - Budget Reference: @.devforgeai/protocols/command-budget-reference.md

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

**See:** @.claude/memory/commands-reference.md for complete command documentation.

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

- **Skills:** 9 (8 DevForgeAI + 1 infrastructure: ideation, architecture, orchestration, story-creation, ui-generator, development, qa, release, **claude-code-terminal-expert**)
- **Subagents:** 21 (includes deferral-validator, technical-debt-analyzer, tech-stack-detector, git-validator, qa-result-interpreter, ui-spec-formatter, sprint-planner, **story-requirements-analyst** NEW - RCA-007 Phase 3)
- **Commands:** 11 (7 refactored to lean orchestration: /dev, /qa, /ideate, /create-story, /create-sprint, /create-epic, /orchestrate; 1 new: /audit-budget)
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

**Progressive disclosure references:**
- @.claude/memory/skills-reference.md
- @.claude/memory/subagents-reference.md
- @.claude/memory/commands-reference.md
- @.claude/memory/qa-automation.md
- @.claude/memory/context-files-guide.md
- @.claude/memory/ui-generator-guide.md
- @.claude/memory/token-efficiency.md
- @.claude/memory/token-budget-guidelines.md

**Framework protocols:**
- @.devforgeai/protocols/lean-orchestration-pattern.md - Command architecture and refactoring

---

**The framework exists to prevent technical debt through explicit constraints and automated validation. When in doubt, ask the user—never make assumptions.**
