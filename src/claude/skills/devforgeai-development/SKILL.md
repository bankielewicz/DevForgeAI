---
name: devforgeai-development
description: Implement features using Test-Driven Development (TDD) while enforcing architectural constraints from context files. Use when implementing user stories, building features, or writing code that must comply with tech-stack.md, source-tree.md, and dependencies.md. Automatically invokes devforgeai-architecture skill if context files are missing.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Task
  - Bash(git:*)
  - Bash(npm:*)
  - Bash(pytest:*)
  - Bash(dotnet:*)
  - Bash(cargo:*)
  - Bash(mvn:*)
  - Bash(gradle:*)
  - Bash(python:*)
  - Skill
model: claude-haiku-4-5-20251001
---

# DevForgeAI Development Skill

Implement user stories using Test-Driven Development while enforcing architectural constraints to prevent technical debt.

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
- ❌ Stop to ask about token budget (CLAUDE.md: "context window is plenty big")
- ❌ Stop to ask about time constraints (CLAUDE.md: "no time constraints")
- ❌ Stop to ask about scope/approach (execute as documented)
- ❌ Offer execution options (just execute the workflow)

**CRITICAL:** Skill invocation means "execute now" - not "ask if you should execute"

**Proceed to "Parameter Extraction" section below and begin execution.**

---

## ⚠️ IMMEDIATE EXECUTION CHECKPOINT

**YOU HAVE JUST INVOKED THIS SKILL. EXECUTE PHASE 0 NOW.**

**BEFORE PROCEEDING, VERIFY YOU ARE NOT:**

```
Self-Check (Check boxes if TRUE - any checked = VIOLATION):

- [ ] Stopping to ask about token budget (CLAUDE.md says "context window is plenty big")
- [ ] Stopping to ask about time constraints (CLAUDE.md says "no time constraints")
- [ ] Stopping to ask about approach/scope (story already defines approach)
- [ ] Stopping to offer execution options (execute the workflow as documented)
- [ ] Waiting passively for results (skills expand inline, YOU execute)
- [ ] Asking "should I execute this?" (YES - that's why skill was invoked)
```

**Validation Logic:**

```
IF you checked ANY box above:
  You are VIOLATING the skill execution model.

  Display:
  "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  "❌ EXECUTION MODEL VIOLATION DETECTED"
  ""
  "You stopped after skill invocation instead of executing Phase 0."
  ""
  "CLAUDE.md states:"
  "  • 'There are no time constraints'"
  "  • 'Your context window is plenty big'"
  "  • 'Focus on quality'"
  ""
  "You must execute the workflow immediately, not ask permission."
  "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  SELF-CORRECT: Go directly to Parameter Extraction and Phase 0 now.
                Do not ask questions.
                Execute the workflow.

IF all boxes UNCHECKED:
  ✓ You are executing correctly
  ✓ Proceed to Parameter Extraction immediately
```

**Evidence from test session (tmp/output.md):**
- Line 27-28: Skill invoked ✓
- Line 30: "I need to pause here" ✗ VIOLATION
- Lines 43-73: Offered Options A/B/C instead of executing ✗ VIOLATION

**This checkpoint prevents that behavior.**

---

## Parameter Extraction

This skill extracts the story ID from conversation context (loaded story file YAML frontmatter, context markers, or natural language).

**See `references/parameter-extraction.md` for complete extraction algorithm.**

---

## Workflow Execution Checklist

**After parameter extraction, BEFORE Phase 0, create execution tracker:**

**Initialize iteration counter:**
```
iteration_count = 1  # Track TDD cycle iterations (for Phase 4.5 resumption - RCA-014 fix)
```

TodoWrite(
  todos=[
    {content: "Execute Phase 0: Pre-Flight Validation (10 steps)", status: "pending", activeForm: "Executing Phase 0 Pre-Flight Validation"},
    {content: "Execute Phase 1: Test-First Design (4 steps + Tech Spec Coverage)", status: "pending", activeForm: "Executing Phase 1 Test-First Design"},
    {content: "Execute Phase 2: Implementation (backend-architect + context-validator)", status: "pending", activeForm: "Executing Phase 2 Implementation"},
    {content: "Execute Phase 3: Refactoring (refactoring-specialist + code-reviewer + Light QA)", status: "pending", activeForm: "Executing Phase 3 Refactoring"},
    {content: "Execute Phase 4: Integration Testing (integration-tester)", status: "pending", activeForm: "Executing Phase 4 Integration Testing"},
    {content: "Execute Phase 4.5: Deferral Challenge (validate incomplete items, immediate resumption if needed)", status: "pending", activeForm: "Executing Phase 4.5 Deferral Challenge"},
    {content: "Execute Phase 4.5-5 Bridge: Update DoD Checkboxes (mark completed items [x])", status: "pending", activeForm: "Executing Phase 4.5-5 Bridge DoD Update"},
    {content: "Execute Phase 5: Git Workflow (validate DoD format + commit)", status: "pending", activeForm: "Executing Phase 5 Git Workflow"},
    {content: "Execute Phase 6: Feedback Hook (check-hooks + invoke-hooks)", status: "pending", activeForm: "Executing Phase 6 Feedback Hook"},
    {content: "Execute Phase 7: Result Interpretation (dev-result-interpreter)", status: "pending", activeForm: "Executing Phase 7 Result Interpretation"}
  ]
)

**Usage During Workflow:**
- Mark phase "in_progress" when starting each phase
- Mark phase "completed" when checkpoint validation passes
- Update user on progress as phases complete
- User can see visual progress through TDD cycle
- Self-monitoring: If Phase 3 todo still "pending" when trying Phase 5, something is wrong

**Benefits:**
- Visual progress tracking for user
- Forces Claude to consciously mark phases complete
- Self-monitoring mechanism (detects skipped phases)
- Audit trail of workflow execution

**TodoWrite purpose:** User-facing progress visualization (advisory)
**Enforcement:** Validation checkpoints at phase transitions (mandatory)
**Note:** TodoWrite does not provide read API - checkpoints verify actual execution

---

## Purpose

Implement features following strict TDD workflow (Red → Green → Refactor) while enforcing all 6 context file constraints.

**Context files are THE LAW:** tech-stack.md, source-tree.md, dependencies.md, coding-standards.md, architecture-constraints.md, anti-patterns.md

**If ambiguous or conflicts detected → HALT and use AskUserQuestion**

**See `references/ambiguity-protocol.md` for resolution procedures.**

---

## When to Use This Skill

**Prerequisites:** Git repo (recommended), context files (6), story file

**Git modes:** Full workflow (with Git) OR file-based tracking (without Git) - auto-detects

**Invoked by:** `/dev [STORY-ID]` command, devforgeai-orchestration skill, manual skill call

---

## Pre-Flight Validation (Phase 0)

**⚠️ EXECUTION STARTS HERE - You are now executing the skill's workflow.**

**This is Phase 0. Execute these steps now:**

10-step validation before TDD begins:

1. Validate Git status (git-validator subagent)
1.5. **User consent for git operations (if uncommitted changes >10)** ← NEW (RCA-008)
1.6. **Stash warning and confirmation (if user chooses to stash)** ← NEW (RCA-008)
2. Adapt workflow (Git vs file-based)
3. File-based tracking setup (if no Git)
4. Validate 6 context files exist
5. Load story specification
6. Validate spec vs context conflicts
7. Detect tech stack (tech-stack-detector subagent)
8. Detect QA failures (recovery mode)
8.5. Load structured gap data (if gaps.json exists)

**See `references/preflight-validation.md` for complete workflow.**

---

### Phase 0 Validation Checkpoint (HALT IF FAILED)

**Before proceeding to Phase 1 or Remediation Mode, verify Phase 0 completed:**

CHECK CONVERSATION HISTORY FOR EVIDENCE:

- [ ] Step 0.1: git-validator subagent invoked?
      Search for: Task(subagent_type="git-validator")
      Found? YES → Check box | NO → Leave unchecked

- [ ] Step 0.4: Context files validated (6 files)?
      Search for: Read(file_path=".devforgeai/context/tech-stack.md")
      Found? YES → Check box | NO → Leave unchecked

- [ ] Step 0.5: Story specification loaded?
      Search for: Read with story file path
      Found? YES → Check box | NO → Leave unchecked

- [ ] Step 0.7: tech-stack-detector subagent invoked?
      Search for: Task(subagent_type="tech-stack-detector")
      Found? YES → Check box | NO → Leave unchecked

IF any checkbox UNCHECKED:
  Display:
  "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  "❌ PHASE 0 INCOMPLETE - Pre-flight validation not executed"
  ""
  FOR each unchecked item:
    Display: "  ✗ {item description}"
  ""
  Display: "Missing validation prevents safe development. HALT."
  Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  HALT workflow (do not proceed to Phase 1 or Remediation Mode)

IF all checkboxes CHECKED:
  Display:
  "✓ Phase 0 Validation Passed - All pre-flight checks completed"
  "  ✓ Git repository validated"
  "  ✓ Context files loaded"
  "  ✓ Story specification loaded"
  "  ✓ Tech stack detected"
  ""
  Display: "Proceeding to Phase 1 (or Remediation Mode if QA gaps detected)..."

  Proceed to next phase

**Purpose:** Prevents skipping git validation, context file loading, and tech stack detection (RCA: STORY-080 skipped Phase 0 completely)

---

## Remediation Mode Decision Point (After Phase 0)

**CRITICAL:** After Phase 0 completes, check `$REMEDIATION_MODE` flag set by Step 0.8.5.

```
IF $REMEDIATION_MODE == true:
    # gaps.json exists from previous QA failure
    # Execute targeted remediation workflow instead of full TDD

    Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    Display: "  🔧 REMEDIATION MODE ACTIVE"
    Display: "  Targeted workflow to fix QA gaps"
    Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    # Load and execute remediation workflow
    Read(file_path=".claude/skills/devforgeai-development/references/qa-remediation-workflow.md")

    # Execute phases 1R, 2R, 3R, 4R, 4.5R, 5R from remediation workflow
    # These replace normal Phases 1-5 with targeted versions

    SKIP: Normal TDD Phases 1-5 below
    GOTO: Phase 6 (Feedback Hook) after remediation complete

ELSE:
    # Normal TDD workflow
    Proceed with Phase 1 below
```

**What Remediation Mode Does:**
- Phase 1R: Generate tests for `$QA_COVERAGE_GAPS` files ONLY (not full story)
- Phase 2R: Implement code for gap files ONLY
- Phase 3R: Fix `$QA_ANTIPATTERN_GAPS` violations ONLY
- Phase 4R: Verify coverage gaps are closed
- Phase 4.5R: Resolve `$QA_DEFERRAL_GAPS` issues
- Phase 5R: Commit remediation

**Reference:** `qa-remediation-workflow.md`

---

## TDD Workflow (6 Phases)

### Phase 1: Test-First Design (Red Phase)
Write failing tests from AC → test-automator subagent → Tests RED → **Update AC Checklist (test items) ✓ MANDATORY**
**Reference:** `tdd-red-phase.md`
**AC Updates:** Test count, test coverage, test file creation items

---

### Phase 1 Validation Checkpoint (HALT IF FAILED)

**Before proceeding to Phase 2, verify Phase 1 completed:**

CHECK CONVERSATION HISTORY FOR EVIDENCE:

- [ ] Steps 1-3: test-automator subagent invoked?
      Search for: Task(subagent_type="test-automator")
      Found? YES → Check box | NO → Leave unchecked

- [ ] Step 4: Tech Spec Coverage Validation completed?
      Search for: coverage validation OR tech spec verification
      Found? YES → Check box | NO → Leave unchecked

- [ ] AC Checklist (test items) updated? ✓ MANDATORY
      Search for: Edit with AC Checklist test items marked [x]
      Found? YES → Check box | NO → Leave unchecked

IF any checkbox UNCHECKED:
  Display:
  "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  "❌ PHASE 1 INCOMPLETE - Test generation not verified"
  ""
  FOR each unchecked item:
    Display: "  ✗ {item description}"
  ""
  Display: "HALT - Cannot proceed to Phase 2 until Phase 1 complete"
  Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  HALT workflow

IF all checkboxes CHECKED:
  Display:
  "✓ Phase 1 Validation Passed - Tests RED and documented"
  "  ✓ test-automator invoked"
  "  ✓ Tech spec coverage validated"
  "  ✓ AC Checklist updated"
  ""
  Display: "Proceeding to Phase 2..."

  Proceed to Phase 2

**Purpose:** Ensures tests are generated before implementation begins (TDD Red phase complete)

---

### Phase 2: Implementation (Green Phase)
Minimal code to pass tests → backend-architect/frontend-developer → Tests GREEN → **Update AC Checklist (implementation items) ✓ MANDATORY**
**Reference:** `tdd-green-phase.md`
**AC Updates:** Code implementation, business logic location, size metrics items

### Phase 3: Refactor (Refactor Phase)
Improve quality, keep tests green → refactoring-specialist, code-reviewer, Light QA → Code improved → **Update AC Checklist (quality items) ✓ MANDATORY**
**Reference:** `tdd-refactor-phase.md`
**Steps:** 1-4 Refactoring + code review, 5 Light QA validation [MANDATORY], 6 AC Checklist update
**AC Updates:** Code quality, pattern compliance, review findings items

### Phase 4: Integration & Validation
Cross-component testing, coverage validation → integration-tester → Thresholds met → **Update AC Checklist (integration items) ✓ MANDATORY**
**Reference:** `integration-testing.md`
**AC Updates:** Integration tests, performance, coverage threshold items

---

### Phase 4 Validation Checkpoint (HALT IF FAILED)

**Before proceeding to Phase 4.5, verify Phase 4 completed:**

CHECK CONVERSATION HISTORY FOR EVIDENCE:

- [ ] Step 0: Anti-Gaming Validation PASSED? [NEW - BLOCKING - RUN FIRST]
      Search for: integration-tester response with "✓ Anti-gaming validation passed"
      OR: gaming_scan.status == "PASS"
      Found? YES → Check box | NO → Leave unchecked
      IF FAIL: HALT - Test gaming detected, coverage scores INVALID

- [ ] Step 1: integration-tester subagent invoked?
      Search for: Task(subagent_type="integration-tester")
      Found? YES → Check box | NO → Leave unchecked

- [ ] Coverage thresholds validated (95%/85%/80%)?
      Search for: coverage results OR threshold validation
      Found? YES → Check box | NO → Leave unchecked

- [ ] AC Checklist (integration items) updated? ✓ MANDATORY
      Search for: Edit with AC Checklist integration items marked [x]
      Found? YES → Check box | NO → Leave unchecked

IF any checkbox UNCHECKED:
  Display:
  "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  "❌ PHASE 4 INCOMPLETE - Integration testing not verified"
  ""
  FOR each unchecked item:
    Display: "  ✗ {item description}"
  ""
  IF anti-gaming validation FAILED:
    Display: "  🚨 TEST GAMING DETECTED - Cannot calculate authentic coverage"
    Display: "  Fix: Remove skip decorators, add assertions, reduce mocking, remove TODO placeholders"
  ""
  Display: "HALT - Cannot proceed to Phase 4.5 until Phase 4 complete"
  Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  HALT workflow

IF all checkboxes CHECKED:
  Display:
  "✓ Phase 4 Validation Passed - Integration testing complete"
  "  ✓ Anti-gaming validation PASSED"
  "  ✓ integration-tester invoked"
  "  ✓ Coverage thresholds met"
  "  ✓ AC Checklist updated"
  ""
  Display: "Proceeding to Phase 4.5..."

  Proceed to Phase 4.5

**Purpose:** Ensures anti-gaming validation and integration testing complete before deferral checkpoint

---

### Phase 4.5: Deferral Challenge Checkpoint (NEW - RCA-006)
Challenge ALL deferrals (pre-existing + new) → deferral-validator → User approval required → **Update AC Checklist (deferral items) ✓ MANDATORY**
**Reference:** `phase-4.5-deferral-challenge.md`
**Purpose:** Prevent autonomous deferrals, enforce "Attempt First, Defer Only If Blocked" pattern
**AC Updates:** Deferral validation, follow-up story creation items

---

### Phase 4.5 Validation Checkpoint (HALT IF FAILED)

**Before proceeding to Phase 4.5-5 Bridge, verify Phase 4.5 completed:**

CHECK CONVERSATION HISTORY FOR EVIDENCE:

- [ ] DoD reviewed for incomplete items?
      Search for: DoD review OR deferral detection
      Found? YES → Check box | NO → Leave unchecked

- [ ] IF deferrals exist: deferral-validator subagent invoked?
      Search for: Task(subagent_type="deferral-validator") OR "No deferrals"
      Found OR no deferrals? YES → Check box | NO → Leave unchecked

- [ ] Step 6: AskUserQuestion invoked for EVERY deferral? [ENFORCED]
      Search for: AskUserQuestion with deferral decision options
      Options MUST include "HALT and implement NOW" as FIRST option
      Found for EACH deferral OR no deferrals? YES → Check box | NO → Leave unchecked
      IF SKIPPED: HALT - Autonomous deferral approval is FORBIDDEN

- [ ] Step 6.5: User approval timestamp recorded? [NEW - MANDATORY]
      Search for: "User approved: YYYY-MM-DD" timestamp in story file
      FOR EACH kept deferral, timestamp MUST exist
      Found for ALL OR no deferrals kept? YES → Check box | NO → Leave unchecked
      IF MISSING: HALT - Deferrals without explicit user approval are INVALID

- [ ] AC Checklist (deferral items) updated? ✓ MANDATORY
      Search for: Edit with AC Checklist deferral items marked [x]
      Found? YES → Check box | NO → Leave unchecked

IF any checkbox UNCHECKED:
  Display:
  "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  "❌ PHASE 4.5 INCOMPLETE - Deferral validation not verified"
  ""
  FOR each unchecked item:
    Display: "  ✗ {item description}"
  ""
  IF Step 6 (AskUserQuestion) SKIPPED:
    Display: "  🚨 AUTONOMOUS DEFERRAL DETECTED"
    Display: "  Claude MUST use AskUserQuestion for EVERY deferral"
    Display: "  First option MUST be 'HALT and implement NOW'"
  ""
  IF Step 6.5 (timestamp) MISSING:
    Display: "  🚨 DEFERRAL WITHOUT USER APPROVAL"
    Display: "  Every kept deferral MUST have 'User approved: timestamp'"
    Display: "  Deferrals without timestamps are INVALID"
  ""
  Display: "HALT - Cannot proceed to Bridge until Phase 4.5 complete"
  Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  HALT workflow

IF all checkboxes CHECKED:
  Display:
  "✓ Phase 4.5 Validation Passed - Deferrals validated with user approval"
  "  ✓ DoD reviewed"
  "  ✓ Deferrals validated (or none exist)"
  "  ✓ AskUserQuestion invoked for every deferral"
  "  ✓ User approval timestamps recorded"
  "  ✓ AC Checklist updated"
  ""
  Display: "Proceeding to Phase 4.5-5 Bridge..."

  Proceed to Bridge

**Purpose:** Ensures deferrals have EXPLICIT user approval (not autonomous) before DoD update. Step 6.5 is defense-in-depth against auto-approval.

---

### Phase 4.5-5 Bridge: DoD Update Workflow ✓ MANDATORY (NEW - RCA-009, Enforced - RCA-010)
Update DoD format for git commit → Validate format → Prepare for Phase 5
**Reference:** `dod-update-workflow.md`
**Purpose:** Ensure DoD items formatted correctly (flat list in Implementation Notes, no ### subsections)
**CRITICAL:** Execute AFTER Phase 4.5, BEFORE Phase 5 - git commit will FAIL if skipped
**Note (RCA-014):** Phase 4.5-R removed - resumption now happens immediately in Phase 4.5 Step 7

---

### Bridge Validation Checkpoint (HALT IF FAILED)

**Before proceeding to Phase 5 (Git Commit), verify Bridge completed:**

CHECK CONVERSATION HISTORY FOR EVIDENCE:

- [ ] DoD items marked [x] in story file?
      Search for: Edit with DoD items marked [x]
      Found? YES → Check box | NO → Leave unchecked

- [ ] Implementation Notes flat list added?
      Search for: Edit with "Definition of Done - Completed Items"
      Found? YES → Check box | NO → Leave unchecked

- [ ] DoD format validated?
      Search for: devforgeai-validate validate-dod OR Bash with validate-dod
      Found? YES → Check box | NO → Leave unchecked

IF any checkbox UNCHECKED:
  Display:
  "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  "❌ BRIDGE INCOMPLETE - DoD not updated before commit"
  ""
  FOR each unchecked item:
    Display: "  ✗ {item description}"
  ""
  Display: "Git commit will FAIL without DoD validation. HALT."
  Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  HALT workflow (do not execute git commit)

IF all checkboxes CHECKED:
  Display:
  "✓ Bridge Validation Passed - DoD validated"
  "  ✓ DoD items marked complete"
  "  ✓ Implementation Notes added"
  "  ✓ Format validation passed"
  ""
  Display: "Proceeding to Phase 5 (Git Commit)..."

  Proceed to Phase 5

**Purpose:** Prevents git commit without proper DoD documentation (RCA: STORY-080 skipped Bridge)

---

### Phase 5: Git Workflow & DoD Validation
Budget enforcement → Handle incomplete items → Git commit → Story complete → **Update AC Checklist (deployment items) ✓ MANDATORY**
**References:** `dod-update-workflow.md` (pre-requisite), `deferral-budget-enforcement.md`, `git-workflow-conventions.md`, `dod-validation-checkpoint.md`, `ac-checklist-update-workflow.md`
**Steps:** Pre-req: DoD format validated, 1.6 Budget enforcement, 1.7 Handle new incomplete items, 2.0+ Git commit, 2.1+ AC Checklist final update
**AC Updates:** Git commit, status update, backward compatibility items

**See `references/tdd-patterns.md` for comprehensive TDD guidance across all phases.**

---

### Phase 5 Validation Checkpoint (HALT IF FAILED)

**Before proceeding to Phase 6, verify Phase 5 completed:**

CHECK CONVERSATION HISTORY FOR EVIDENCE:

- [ ] Git commit succeeded?
      Search for: git commit output showing success OR commit hash
      Found? YES → Check box | NO → Leave unchecked

- [ ] Story file included in commit?
      Search for: git add with story file path
      Found? YES → Check box | NO → Leave unchecked

- [ ] AC Checklist (deployment items) updated? ✓ MANDATORY
      Search for: Edit with AC Checklist deployment items marked [x]
      Found? YES → Check box | NO → Leave unchecked

IF any checkbox UNCHECKED:
  Display:
  "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  "❌ PHASE 5 INCOMPLETE - Git commit not verified"
  ""
  FOR each unchecked item:
    Display: "  ✗ {item description}"
  ""
  Display: "HALT - Cannot proceed to Phase 6 until Phase 5 complete"
  Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  HALT workflow

IF all checkboxes CHECKED:
  Display:
  "✓ Phase 5 Validation Passed - Code committed"
  "  ✓ Git commit successful"
  "  ✓ Story file included"
  "  ✓ AC Checklist updated"
  ""
  Display: "Proceeding to Phase 6..."

  Proceed to Phase 6

**Purpose:** Ensures git commit includes story file and documentation

---

## Complete Workflow Execution Map

**Visual guide showing all mandatory steps and common skip points:**

```
START
  ↓
Phase 0: Pre-Flight (preflight-validation.md)
  ├─ Step 0.1: git-validator ✓ MANDATORY
  ├─ Step 0.1.5: User consent (RCA-008) ✓ MANDATORY IF uncommitted > 10
  ├─ Step 0.4: Validate 6 context files ✓ MANDATORY
  ├─ Step 0.7: tech-stack-detector ✓ MANDATORY
  ├─ Step 0.8: Detect QA failures ✓ MANDATORY
  └─ Step 0.8.5: Load gaps.json ✓ MANDATORY IF QA failed
  ↓
┌─── DECISION: Check $REMEDIATION_MODE ───┐
│                                          │
│  IF true:                               │
│    ↓                                    │
│  REMEDIATION WORKFLOW (qa-remediation-workflow.md)
│    ├─ Phase 1R: Targeted test gen       │
│    ├─ Phase 2R: Targeted implementation │
│    ├─ Phase 3R: Anti-pattern fixes      │
│    ├─ Phase 4R: Coverage verification   │
│    ├─ Phase 4.5R: Deferral resolution   │
│    └─ Phase 5R: Commit remediation      │
│    ↓                                    │
│    GOTO Phase 6 (Feedback Hook)         │
│                                          │
│  ELSE:                                   │
│    ↓                                    │
│  NORMAL TDD WORKFLOW (below)            │
└──────────────────────────────────────────┘
  ↓
Phase 1: Red (tdd-red-phase.md)
  ├─ Step 1-3: Generate failing tests ✓ MANDATORY
  └─ Step 4: Tech Spec Coverage Validation ✓ MANDATORY ← OFTEN MISSED
  ↓
Phase 2: Green (tdd-green-phase.md)
  ├─ Step 1-2: backend-architect OR frontend-developer ✓ MANDATORY
  └─ Step 3: context-validator ✓ MANDATORY ← OFTEN MISSED
  ↓
Phase 3: Refactor (tdd-refactor-phase.md + refactoring-patterns.md)
  ├─ Step 1-2: refactoring-specialist ✓ MANDATORY
  ├─ Step 3: code-reviewer ✓ MANDATORY
  ├─ **Step 4: Anti-Gaming Validation ✓ MANDATORY [NEW]** ← BLOCKS IF GAMING DETECTED
  │   └─ HALT if: skip decorators, empty tests, excessive mocking (>2x) detected
  └─ Step 5: Light QA (devforgeai-qa --mode=light) ✓ MANDATORY ← OFTEN MISSED
  ↓
Phase 4: Integration (integration-testing.md)
  ├─ **Step 0: Anti-Gaming Validation ✓ MANDATORY [NEW]** ← RUN FIRST, BLOCKS COVERAGE
  │   └─ HALT if: gaming patterns detected BEFORE coverage calculation
  └─ Step 1: integration-tester ✓ MANDATORY
  ↓
Phase 4.5: Deferral Challenge (phase-4.5-deferral-challenge.md)
  ├─ Detect deferrals ✓ MANDATORY
  ├─ deferral-validator ✓ MANDATORY IF deferrals exist
  ├─ **Step 6: AskUserQuestion for EVERY deferral ✓ MANDATORY [ENFORCED]**
  ├─ **Step 6.5: Mandatory HALT Verification ✓ MANDATORY [NEW]** ← BLOCKS IF AUTO-APPROVED
  │   └─ HALT if: ANY deferral lacks explicit user approval timestamp
  └─ User approval timestamp recorded ✓ MANDATORY IF deferrals kept
  ↓
Phase 4.5-5 Bridge: DoD Update (dod-update-workflow.md ← NEW)
  ├─ Mark DoD items [x] ✓ MANDATORY
  ├─ Add items to Implementation Notes (FLAT LIST) ✓ MANDATORY
  ├─ Validate format: devforgeai-validate validate-dod ✓ MANDATORY
  └─ Update Workflow Status ✓ MANDATORY
  ↓
Phase 5: Git Workflow (git-workflow-conventions.md)
  ├─ Budget enforcement ✓ MANDATORY
  ├─ Handle new incomplete items ✓ MANDATORY
  └─ Git commit (validator passes) ✓ MANDATORY
  ↓
Phase 6: Feedback Hook
  ├─ check-hooks ✓ MANDATORY
  └─ invoke-hooks ✓ MANDATORY IF enabled
  ↓
END (Story Status = "Dev Complete")
```

**Legend:**
- ✓ MANDATORY = Must execute, no exceptions
- ✓ MANDATORY IF = Conditional execution based on state
- ← OFTEN MISSED = Common skip points (extra attention needed)

**Purpose:** Visual representation of complete TDD workflow helps prevent phase skipping and highlights critical validation steps.

---

### Phase 6: Feedback Hook Integration

**Purpose:** Invoke feedback hooks if configured for retrospective insights
**Execution:** After Phase 5 (Git commit) completes
**Reference:** See STORY-023 implementation notes

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase 6/9: Feedback Hook (89% → 100% complete)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Display this indicator at the start of Phase 6 execution.**

**Steps:**
1. Check hooks configuration: `devforgeai-validate check-hooks --operation=dev --status=success`
2. Invoke hooks if enabled: `devforgeai-validate invoke-hooks --operation=dev --story=$STORY_ID`
3. Non-blocking: Hook failures don't prevent workflow completion

---

### Phase 7: Result Interpretation (NEW - STORY-051)

**Purpose:** Generate user-facing display template and structured result summary
**Execution:** After Phase 6 (Feedback Hook) completes, before returning to /dev command
**Reference:** dev-result-interpreter uses `references/dev-result-formatting-guide.md`

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase 7/9: Result Interpretation (95% → 100% complete)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Display this indicator at the start of Phase 7 execution.**

**Workflow:**

**Step 7.1: Invoke dev-result-interpreter Subagent**

```
Task(
  subagent_type="dev-result-interpreter",
  description="Interpret dev workflow results for {STORY_ID}",
  prompt="""
Interpret development workflow results for story {STORY_ID}.

Story file: {STORY_FILE_PATH}

Task:
1. Read story file and extract:
   - Current status (from YAML frontmatter)
   - TDD phases completed (from Status History or Implementation Notes)
   - Test results (passing count, coverage %)
   - DoD completion status (from Implementation Notes)
   - Deferred items (from Implementation Notes)

2. Determine overall result:
   - SUCCESS: status="Dev Complete", all tests passing
   - INCOMPLETE: status="In Development", some work remaining
   - FAILURE: workflow error or blocking issue

3. Generate display template appropriate for result type

4. Provide next step recommendations based on story state

Return structured JSON with:
- status: "success|incomplete|failure"
- display.template: "..." (formatted display text)
- display.next_steps: [...] (actionable recommendations)
- story_status: "..." (current story status)
- tdd_phases_completed: [...] (phases finished)
- workflow_summary: "..." (brief summary)
"""
)
```

**Step 7.2: Receive Structured Result**

```
# Subagent returns JSON:
result = {
  "status": "success",
  "display": {
    "template": "╔═══════════...║  DEVELOPMENT COMPLETE ✅  ║...",
    "next_steps": [
      "Run QA validation: /qa {STORY_ID}",
      "Or run full orchestration: /orchestrate {STORY_ID}",
      "Review implementation: Read story file Implementation Notes"
    ]
  },
  "story_status": "Dev Complete",
  "tdd_phases_completed": ["Phase 0", "Phase 1", "Phase 2", "Phase 3", "Phase 4", "Phase 5", "Phase 6"],
  "workflow_summary": "TDD cycle complete, 165/168 tests passing (98.2%)"
}
```

**Step 7.3: Return Result to Command**

```
# Skill returns the result object to /dev command
# Command will display result.display.template
# No further processing needed in skill

Display: ""
Display: "Phase 7 complete - Result interpretation ready"
Display: ""

RETURN result to command
```

---

### Phase 7 Validation Checkpoint (HALT IF FAILED)

**Before returning result to /dev command, verify Phase 7 completed:**

```
CHECK CONVERSATION HISTORY FOR EVIDENCE:

- [ ] Step 7.1: dev-result-interpreter invoked?
      Search for: Task(subagent_type="dev-result-interpreter")
      Found? YES → Check box | NO → Leave unchecked

- [ ] Step 7.3: Structured result returned to command?
      Search for: RETURN result to command statement
      Found? YES → Check box | NO → Leave unchecked
```

**Validation Logic:**

```
IF any checkbox UNCHECKED:
  Display:
  "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  "❌ PHASE 7 INCOMPLETE - Missing mandatory steps:"
  ""
  FOR each unchecked item:
    Display: "  ✗ {item description}"
  ""
  Display: "HALT - Cannot complete workflow without result interpretation"
  Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  HALT workflow (do not return to /dev command)

IF all checkboxes CHECKED:
  Display:
  "✓ Phase 7 Validation Passed - Result interpretation complete"
  "  ✓ dev-result-interpreter invoked"
  "  ✓ Structured result prepared"
  ""
  Display: "Returning result to /dev command..."

  RETURN result to command
```

**Purpose:** This checkpoint ensures dev-result-interpreter subagent is always invoked to generate proper result display template (STORY-051 requirement).

---

**Integration:**
- dev-result-interpreter operates in isolated context (8K tokens max)
- Reference guide (dev-result-formatting-guide.md) provides framework constraints
- Subagent generates templates matching original /dev output format (backward compatibility)
- No business logic in command (follows lean orchestration pattern)

**Benefits:**
- 184 lines extracted from /dev command (Phase 3 + Phase 4 verification/reporting)
- Token efficiency: Display generation in isolated subagent context
- Maintainability: Single source of truth for display templates in subagent
- Reusability: Pattern applicable to other development commands

---

## QA Deferral Recovery

Triggered when QA fails due to deferrals. Phase 0 Step 0.8 detects, then 3-step resolution workflow executes.

**See `references/qa-deferral-recovery.md` for complete procedure.**

---

## Integration Points

**From:** devforgeai-story-creation (story+AC), devforgeai-architecture (context files)
**To:** devforgeai-qa (validation), devforgeai-release (deployment)
**Auto-invokes:** devforgeai-architecture (if missing), devforgeai-qa (light mode), devforgeai-story-creation (deferrals)

---

## Subagent Coordination

**Subagent Invocation Sequences (Execute in Order):**

### Phase 0: Pre-Flight Validation

1. **git-validator** (Git availability check) [MANDATORY]
   - Purpose: Detect Git status, provide workflow strategy (Git vs file-based)
   - Token cost: ~5K (isolated)
   - Returns: Git status, recommended workflow
   - Success: Git available OR file-based strategy confirmed

2. **tech-stack-detector** (Technology detection) [MANDATORY AFTER CONTEXT FILES VALIDATED]
   - Purpose: Auto-detect project technologies, validate against tech-stack.md
   - Token cost: ~10K (isolated)
   - Returns: Detected tech stack, validation results
   - HALT if tech-stack.md conflicts detected

**Sequence:** git-validator → tech-stack-detector (sequential)

---

### Phase 1: Test-First Design (Red Phase)

1. **test-automator** (Test generation) [MANDATORY]
   - Purpose: Generate failing tests from acceptance criteria
   - Token cost: ~50K (isolated)
   - Returns: Test files, test command, coverage analysis
   - Success: All tests RED (failing as expected)

**Note:** Phase 1 also includes Step 4 (Tech Spec Coverage Validation) - see `tdd-red-phase.md` for user approval workflow

---

### Phase 2: Implementation (Green Phase)

1. **backend-architect OR frontend-developer** (Implementation) [MANDATORY - CHOOSE ONE]
   - Purpose: Write minimal code to pass tests
   - Token cost: ~50K (isolated)
   - Returns: Implementation code, test results
   - Success: All tests GREEN

2. **context-validator** (Fast constraint validation) [MANDATORY AFTER STEP 1]
   - Purpose: Validate against 6 context files (tech-stack, source-tree, dependencies, coding-standards, architecture-constraints, anti-patterns)
   - Token cost: ~5K (isolated)
   - Returns: Validation report
   - HALT if violations detected

**Sequence:** (backend-architect OR frontend-developer) → context-validator (sequential)

---

### Phase 2 Validation Checkpoint (HALT IF FAILED)

**Before proceeding to Phase 3, verify ALL Phase 2 mandatory steps completed:**

```
CHECK CONVERSATION HISTORY FOR EVIDENCE:

- [ ] Step 1-2: backend-architect OR frontend-developer invoked?
      Search for: Task(subagent_type="backend-architect") OR Task(subagent_type="frontend-developer")
      Found? YES → Check box | NO → Leave unchecked

- [ ] Step 3: context-validator invoked?
      Search for: Task(subagent_type="context-validator")
      Found? YES → Check box | NO → Leave unchecked
```

**Validation Logic:**

```
IF any checkbox UNCHECKED:
  Display:
  "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  "❌ PHASE 2 INCOMPLETE - Missing mandatory steps:"
  ""
  FOR each unchecked item:
    Display: "  ✗ {item description}"
  ""
  Display: "HALT - Cannot proceed to Phase 3 until Phase 2 complete"
  Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  HALT workflow (do not execute Phase 3)

IF all checkboxes CHECKED:
  Display:
  "✓ Phase 2 Validation Passed - All mandatory steps completed"
  "  ✓ backend-architect OR frontend-developer invoked"
  "  ✓ context-validator invoked"
  ""
  Display: "Proceeding to Phase 3..."

  Proceed to Phase 3
```

**Purpose:** This checkpoint prevents Claude from skipping mandatory subagent invocations by requiring explicit verification before phase progression.

---

### Phase 3: Refactor (Refactor Phase)

1. **refactoring-specialist** (Code improvement) [MANDATORY]
   - Purpose: Apply refactoring patterns, remove code smells
   - Token cost: ~40K (isolated)
   - Returns: Refactored code
   - Success: Tests remain GREEN, quality improved

2. **code-reviewer** (Code review) [MANDATORY AFTER STEP 1]
   - Purpose: Review for quality, security, maintainability, standards compliance
   - Token cost: ~30K (isolated)
   - Returns: Review feedback
   - Success: No critical issues

3. **devforgeai-qa (light mode)** (Intermediate quality gate) [MANDATORY AFTER STEP 2]
   - Purpose: Build validation, test execution, quick anti-pattern scan
   - Token cost: ~10K (isolated)
   - Returns: Light QA report
   - HALT if validation fails

**Sequence:** refactoring-specialist → code-reviewer → devforgeai-qa (light) (sequential)

---

### Phase 3 Validation Checkpoint (HALT IF FAILED)

**Before proceeding to Phase 4, verify ALL Phase 3 mandatory steps completed:**

```
CHECK CONVERSATION HISTORY FOR EVIDENCE:

- [ ] Step 1-2: refactoring-specialist invoked?
      Search for: Task(subagent_type="refactoring-specialist")
      Found? YES → Check box | NO → Leave unchecked

- [ ] Step 3: code-reviewer invoked?
      Search for: Task(subagent_type="code-reviewer")
      Found? YES → Check box | NO → Leave unchecked

- [ ] Step 4: Anti-Gaming Validation PASSED? [NEW - BLOCKING]
      Search for: code-reviewer response with gaming_validation.status == "PASS"
      OR: "✓ Anti-gaming validation passed"
      Found? YES → Check box | NO → Leave unchecked
      IF FAIL: HALT - Test gaming detected, fix violations before proceeding

- [ ] Step 5: Light QA (devforgeai-qa --mode=light) executed?
      Search for: Skill(skill="devforgeai-qa") with **Validation mode:** light
      Found? YES → Check box | NO → Leave unchecked
```

**Validation Logic:**

```
IF any checkbox UNCHECKED:
  Display:
  "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  "❌ PHASE 3 INCOMPLETE - Missing mandatory steps:"
  ""
  FOR each unchecked item:
    Display: "  ✗ {item description}"
  ""
  IF anti-gaming validation FAILED:
    Display: "  🚨 TEST GAMING DETECTED - Coverage scores are invalid"
    Display: "  Fix: Remove skip decorators, add assertions to empty tests, reduce mocking"
  ""
  Display: "HALT - Cannot proceed to Phase 4 until Phase 3 complete"
  Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  HALT workflow (do not execute Phase 4)

IF all checkboxes CHECKED:
  Display:
  "✓ Phase 3 Validation Passed - All mandatory steps completed"
  "  ✓ refactoring-specialist invoked"
  "  ✓ code-reviewer invoked"
  "  ✓ Anti-gaming validation PASSED"
  "  ✓ Light QA executed"
  ""
  Display: "Proceeding to Phase 4..."

  Proceed to Phase 4
```

**Purpose:** This checkpoint prevents Claude from skipping refactoring-specialist, anti-gaming validation, and Light QA (marked "← OFTEN MISSED") by requiring explicit verification before phase progression.

---

### Phase 4: Integration & Validation

1. **integration-tester** (Cross-component testing) [MANDATORY]
   - Purpose: Validate cross-component interactions, API contracts, integration scenarios
   - Token cost: ~40K (isolated)
   - Returns: Integration test results, coverage report
   - Success: Integration tests pass, coverage thresholds met

---

### Phase 4.5: Deferral Challenge Checkpoint

1. **deferral-validator** (Blocker validation) [MANDATORY IF DEFERRALS EXIST]
   - Purpose: Validate deferral justifications, detect circular deferrals, check story references
   - Token cost: ~5K (isolated)
   - Returns: Deferral validation report, resolvable vs valid categories
   - Success: All deferrals have user approval OR no deferrals

**Note:** User approval required for EVERY deferred item (zero autonomous deferrals)

---

### Phase 4.5-5 Bridge: DoD Update Workflow

**No subagents** - Direct file operations to update DoD format

**CRITICAL:** Execute dod-update-workflow.md AFTER Phase 4.5, BEFORE Phase 5

---

### Phase 5: Git Workflow & DoD Validation

**No subagents** - Direct git operations and validation

**Prerequisites:**
- Phase 4.5 complete (deferrals validated)
- DoD format validated (devforgeai-validate validate-dod passes)
- New incomplete items handled (AskUserQuestion if needed)

---

**See phase-specific reference files for detailed coordination procedures.**

---

## Reference Files

Load these on-demand during workflow execution:

### Core Workflow
- **parameter-extraction.md** (92 lines) - Story ID extraction from conversation
- **preflight-validation.md** (982 lines) - Phase 0: 10-step validation (git, user consent, stash warning, context, tech stack)
- **tdd-red-phase.md** (125 lines) - Phase 1: Test-first design
- **tdd-green-phase.md** (167 lines) - Phase 2: Minimal implementation
- **tdd-refactor-phase.md** (202 lines) - Phase 3: Code improvement
- **integration-testing.md** (189 lines) - Phase 4: Cross-component tests

### Phase 4.5 & 5 (Deferrals & Git)
- **phase-4.5-deferral-challenge.md** (~900 lines) - Phase 4.5: Challenge ALL deferrals + immediate resumption (RCA-006, RCA-014)
- **dod-update-workflow.md** (~400 lines) - Phase 4.5-5 Bridge: DoD format update and validation (RCA-009 Rec 4)
- **deferral-budget-enforcement.md** (290 lines) - Phase 5 Step 1.6: Budget limits (RCA-006 Phase 2)
- **git-workflow-conventions.md** (~1,300 lines) - Git operations, stash safety protocol (RCA-008), DoD prerequisites, pre-Phase-5 validation (RCA-014)
- **dod-validation-checkpoint.md** (519 lines) - Phase 5 Step 1.7: Handle new incomplete items
- **~~phase-resumption-workflow.md~~** (~400 lines) - REMOVED (RCA-014 REC-2): Resumption now in Phase 4.5 Step 7

### Supporting Files
- **tdd-patterns.md** (1,013 lines) - Comprehensive TDD guidance (all phases)
- **refactoring-patterns.md** (797 lines) - Code smell detection and fixes
- **story-documentation-pattern.md** (532 lines) - Story update procedures
- **qa-deferral-recovery.md** (218 lines) - QA failure resolution
- **ambiguity-protocol.md** (234 lines) - When to ask user questions

**Total reference content:** ~6,350 lines (loaded progressively as needed - includes RCA-008, RCA-014 safeguards)

---

## Success Criteria

This skill succeeds when:

- [ ] All tests pass (100% pass rate)
- [ ] Coverage meets thresholds (95%/85%/80%)
- [ ] Light QA validation passed
- [ ] No context file violations
- [ ] All AC implemented
- [ ] Code follows coding-standards.md
- [ ] No anti-patterns from anti-patterns.md
- [ ] DoD validation passed (3 layers)
- [ ] Changes committed (or file-tracked)
- [ ] Story status = "Dev Complete"
- [ ] Token usage <85K (isolated context)

**The goal: Zero technical debt from wrong assumptions, fully tested features that comply with architectural decisions.**
