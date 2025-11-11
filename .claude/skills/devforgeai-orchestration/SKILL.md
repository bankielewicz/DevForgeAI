---
name: devforgeai-orchestration
description: Coordinates spec-driven development workflow from Epic → Sprint → Story → Architecture → Development → QA → Release. Manages story lifecycle, enforces quality gates, and orchestrates skill invocation. Use when starting epics/sprints, creating stories, managing workflow progression, or enforcing quality checkpoints.
model: claude-sonnet-4-5-20250929
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Skill
  - Task
---

# DevForgeAI Orchestration Skill

Coordinate the complete spec-driven development lifecycle with automated skill orchestration and quality gate enforcement.

---

## ⚠️ EXECUTION MODEL: This Skill Expands Inline

**After invocation, YOU (Claude) execute these instructions phase by phase.**

**When you invoke this skill:**
1. This SKILL.md content is now in your conversation
2. You execute each phase sequentially
3. You display results as you work through phases
4. You complete with success/failure report

**Do NOT:**
- ❌ Wait passively for skill to "return results"
- ❌ Assume skill is executing elsewhere
- ❌ Stop workflow after invocation

**Proceed to "Purpose" section below and begin execution.**

---

## Purpose

This skill is the **workflow coordinator** for the entire spec-driven development framework. It manages the progression of work from high-level business initiatives (Epics) through implementation (Stories) to production release.

### Core Responsibilities

1. **Project Management Integration** - Support Epic → Sprint → Story hierarchy with stories as atomic work units
2. **Skill Coordination** - Auto-invoke architecture, development, QA, and release skills at appropriate workflow stages
3. **State Management** - Track and validate story status across 11 workflow states with sequential progression
4. **Quality Gate Enforcement** - Block transitions when quality standards not met (context validation, test passing, QA approval, release readiness)

### Philosophy

- **Epic → Sprint → Story decomposition** - Break large initiatives into manageable stories
- **Story is atomic unit** - Each story is independently deliverable
- **Quality over speed** - Never skip quality gates
- **No workflow shortcuts** - Every stage must complete successfully
- **Automated orchestration** - Skills invoke each other automatically
- **Transparency** - Complete workflow history in story documents

---

## When to Use This Skill

**Use this skill when:**
- Starting a new epic or sprint
- Creating stories from requirements
- Managing story workflow progression
- Checking story status
- Enforcing quality gates
- Coordinating multi-story releases
- Tracking deferred work (RCA-006 enhanced)
- Analyzing technical debt

**Entry point:**
```
Skill(command="devforgeai-orchestration")
```

**Context markers determine mode:**
- `**Command:** create-epic` + `**Epic name:** {name}` → Epic Creation Mode
- `**Command:** create-sprint` + `**Sprint Name:** {name}` → Sprint Planning Mode
- `**Story ID:** STORY-NNN` → Story Management Mode (default)

---

## Mode Detection

This skill operates in **4 modes** based on conversation context markers.

**See `references/mode-detection.md` for complete detection logic.**

### Supported Modes

1. **Epic Creation Mode** - Phase 4A workflow (8-phase comprehensive process)
2. **Sprint Planning Mode** - Phase 3 workflow (capacity validation, story selection)
3. **Story Management Mode** - Complete story lifecycle orchestration (default)
4. **Default Mode** - Analyze context to infer operation OR HALT if ambiguous

**Mode priority:** Epic > Sprint > Story > Default

---

## Workflow States

**⚠️ EXECUTION STARTS HERE - You are now executing the skill's workflow.**

Stories progress through **11 sequential states:**

```
Backlog → Architecture → Ready for Dev → In Development → Dev Complete →
QA In Progress → [QA Approved | QA Failed] → Releasing → Released
```

**See `references/workflow-states.md` for complete state definitions.**
**See `references/state-transitions.md` for valid transitions and prerequisites.**

---

## Orchestration Phases

This skill executes workflows in **distinct phases**. Each phase loads its reference file on-demand for detailed implementation logic.

### Phase 0: Checkpoint Detection
**Purpose:** Resume interrupted workflows from last successful checkpoint
**Reference:** `checkpoint-detection.md`
**Checkpoints:** DEV_COMPLETE, QA_APPROVED, STAGING_COMPLETE, PRODUCTION_COMPLETE

### Phase 1: Story Validation
**Purpose:** Load and validate story file before execution
**Reference:** `story-validation.md`
**Validates:** File exists, status valid, prerequisites met, quality gates allow progression

### Phase 2: Skill Invocation
**Purpose:** Coordinate automatic invocation of other skills
**Reference:** `skill-invocation.md`
**Skills invoked:** devforgeai-architecture, development, qa, release (based on status)

### Phase 3: Sprint Planning
**Purpose:** Create sprints with capacity validation
**Reference:** `sprint-planning-guide.md`
**Subagent:** sprint-planner (document generation, story updates)

### Phase 3A: Story Status Update
**Purpose:** Update story status and workflow history
**Reference:** `story-status-update.md`
**Updates:** Status, timestamps, checkboxes, history entries

### Phase 3.5: QA Retry Loop
**Purpose:** Manage QA failure recovery (max 3 attempts)
**Reference:** `qa-retry-workflow.md`
**Logic:** Attempt tracking, deferral handling, loop prevention, automatic retry

### Phase 4A: Epic Creation
**Purpose:** Generate epics from requirements (8-phase workflow)
**References:** `epic-management.md`, `feature-decomposition-patterns.md`, `technical-assessment-guide.md`, `epic-validation-checklist.md`
**Subagents:** requirements-analyst (feature decomposition), architect-reviewer (technical assessment)

### Phase 4.5: Deferred Work Tracking
**Purpose:** Track and validate deferred DoD items
**Reference:** `deferred-tracking.md`
**Subagent:** technical-debt-analyzer (debt trend analysis, circular detection)

### Phase 5: Next Action Determination
**Purpose:** Recommend next steps based on current state
**Reference:** `next-action-determination.md`
**Output:** Recommended actions, manual commands, workflow guidance

### Phase 6: Orchestration Finalization
**Purpose:** Generate completion summary and finalize workflow
**Reference:** `orchestration-finalization.md`
**Output:** Timeline, phases executed, quality gates passed, metrics summary

### Phase 7: Sprint Retrospective (RCA-006 Phase 2 - NEW)
**Purpose:** Auto-audit technical debt at sprint completion, create debt reduction sprints
**Reference:** `sprint-retrospective.md`
**Trigger:** Last story in sprint reaches "Released" status
**Output:** Sprint metrics, resolvable deferrals, debt reduction recommendations

---

## Quality Gate Enforcement

**Four gates block workflow progression** when requirements not met:

1. **Gate 1: Context Validation** (Architecture → Ready for Dev)
2. **Gate 2: Test Passing** (Dev Complete → QA In Progress)
3. **Gate 3: QA Approval** (QA Approved → Releasing)
4. **Gate 4: Release Readiness** (Releasing → Released)

**See `references/quality-gates.md` for complete gate requirements and enforcement logic.**

---

## Subagent Coordination

This skill delegates specialized tasks to **4 subagents:**

- **requirements-analyst** - Epic feature decomposition, requirements spec generation
- **architect-reviewer** - Epic technical assessment, complexity scoring (0-10)
- **sprint-planner** - Sprint creation, capacity validation, story status updates
- **technical-debt-analyzer** - Deferred work analysis, debt trend reporting, circular deferral detection

**See `references/skill-invocation.md` for subagent coordination patterns.**

---

## Reference Files

**Load these on-demand during workflow execution:**

### Core Workflow (9 files)
- `mode-detection.md` - Mode detection logic and context markers (329 lines)
- `checkpoint-detection.md` - Checkpoint recovery workflow (474 lines)
- `story-validation.md` - Story file validation procedures (345 lines)
- `skill-invocation.md` - Skill coordination patterns (509 lines)
- `story-status-update.md` - Status update and history procedures (278 lines)
- `qa-retry-workflow.md` - QA failure recovery with max 3 attempts (919 lines)
- `deferred-tracking.md` - Technical debt tracking and analysis (714 lines)
- `next-action-determination.md` - Next step recommendations (287 lines)
- `orchestration-finalization.md` - Completion summary generation (513 lines)

### Epic Management (4 files)
- `epic-management.md` - Epic creation phases 1-2 (496 lines)
- `feature-decomposition-patterns.md` - Phase 3 patterns by domain (903 lines)
- `technical-assessment-guide.md` - Phase 4 complexity scoring (914 lines)
- `epic-validation-checklist.md` - Phase 7 validation and self-healing (760 lines)

### Sprint Management (2 files)
- `sprint-planning-guide.md` - Sprint creation and capacity (631 lines)
- `sprint-retrospective.md` - Sprint retrospective and debt audit (390 lines - RCA-006 Phase 2)

### State Management (2 files)
- `workflow-states.md` - 11 state definitions (585 lines)
- `state-transitions.md` - Valid transitions and rules (1,105 lines)

### Supporting Files (4 files)
- `quality-gates.md` - 4 gate requirements and enforcement (1,017 lines)
- `story-management.md` - Story lifecycle procedures (633 lines)
- `user-interaction-patterns.md` - AskUserQuestion templates (513 lines)
- `troubleshooting.md` - Common issues and solutions (935 lines)

**Total reference content:** 20 files, ~11,660 lines (loaded progressively as needed)

---

## Common Issues

**Top 5 issues and quick solutions:**

1. **Mode detection fails** → Check context markers (see `mode-detection.md`)
2. **Checkpoint not detected** → Verify Status History format (see `checkpoint-detection.md`)
3. **Quality gate blocks** → Review gate requirements (see `quality-gates.md`)
4. **QA retry exceeds 3** → Address root cause or split story (see `qa-retry-workflow.md`)
5. **Sprint capacity exceeded** → Remove lower-priority stories (see `sprint-planning-guide.md`)

**See `references/troubleshooting.md` for complete troubleshooting guide with 13 common issues.**

---

**The orchestration skill ensures every story follows the same high-quality workflow: Architecture → Development → QA → Release, with no shortcuts and complete transparency.**
