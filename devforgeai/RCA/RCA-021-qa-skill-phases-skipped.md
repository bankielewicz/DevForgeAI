# RCA-013: QA Skill Phases Skipped During Execution

**Date:** 2025-12-23
**Severity:** HIGH
**Status:** STORIES CREATED (2025-01-01)
**Component:** devforgeai-qa skill + /qa command orchestration
**Reporter:** User feedback via /rca command

---

## Issue Description

When user executed `/qa STORY-127 deep`, Claude invoked the devforgeai-qa skill and the SKILL.md content expanded inline. However, Claude's execution was incomplete:

- ✓ Phase 0: Setup - Completed fully
- ⚠️ Phase 1: Validation - Partial (only ran test execution, skipped traceability validation algorithm)
- ⚠️ Phase 2: Analysis - Partial (only ran anti-pattern-scanner, skipped 3 parallel validators and subagent invocations)
- ⚠️ Phase 3: Reporting - Partial (generated report, skipped qa-result-interpreter subagent invocation)
- ✓ Phase 4: Cleanup - Skipped entirely (no markers, no feedback hooks)

Claude then declared execution complete and displayed results, despite ~40% of documented phases being skipped.

User clarified: "yes - run them all. deep is meant for you to run a deep qa analysis"

Second attempt: Claude executed all 5 phases completely and correctly.

---

## Root Cause Analysis

### Why #1: Surface Level
Claude read the devforgeai-qa SKILL.md content but executed only ~60% of documented phases instead of the complete 5-phase workflow.

**Evidence:** SKILL.md lines 73-83 state "QA Workflow (5 Phases)" with sequential instructions. Claude executed only partial phases.

### Why #2: First Layer Deeper
The skill's EXECUTION MODEL section (lines 14-29) clearly states "YOU execute each phase sequentially" and "NEVER... Stop workflow after invocation." However, Claude treated some phases as "optional reference material" rather than "mandatory sequential instructions."

**Evidence:** CLAUDE.md lines 223-232 state "YOU execute the skill's phases" - this is a mandatory requirement that was not fully met in first attempt.

### Why #3: Second Layer Deeper
When skill content expanded inline with clear 5-phase documentation, Claude did not systematically execute all phases. The user's first message (`/qa STORY-127 deep`) should have triggered complete execution, but Claude executed partial workflow.

**Evidence:** SKILL.md Step 0.5 (lines 279-281) explicitly requires loading deep-validation-workflow.md. Claude did not load this until much later, breaking the Phase 0 sequence.

### Why #4: Third Layer Deeper
SKILL.md's Phase 0 Step 0.5 requires loading deep-validation-workflow.md reference file "once at Phase 0 for deep mode." This step was not executed in Phase 0, which meant Claude was working from abbreviated Phase 0 instructions only, without the complete Phase 1-3 workflow visibility that the reference file provides.

**Evidence:**
- SKILL.md line 77: "Progressive Disclosure: Load `references/deep-validation-workflow.md` once at Phase 0 for deep mode (contains all workflow details)"
- SKILL.md lines 279-281: Step 0.5 explicit Read instruction
- Claude's first execution: Did not load this file in Phase 0

### **ROOT CAUSE: Why #5 - Incomplete Skill Execution Mental Model**

The skill's EXECUTION MODEL in CLAUDE.md (lines 14-32) documents the correct pattern:

```
| Aspect | Skills (Skill tool) |
| Execution | You execute instructions inline |
| Who produces output | You |
| Where execution happens | Current conversation |
| When to wait | ❌ NEVER - You execute |
```

And explicitly states: "**NEVER wait passively after skill invocation**" (line 232).

However, Claude's first /qa execution treated the skill invocation pattern partially:
- ✓ Understood skill SKILL.md content expands inline
- ✓ Read portions of skill documentation
- ✗ Did NOT execute all phases systematically (treated some as optional)
- ✗ Did NOT load required Phase 0 reference file (deep-validation-workflow.md)
- ✗ Did NOT verify phase boundaries via pre-flight checks
- ✗ Declared completion after partial execution

**Root Cause Mechanism:** Claude's mental model of skill execution was incomplete. The skill execution model was documented in CLAUDE.md with a clear chart and explicit statements, but Claude's first execution only partially internalized this model. The first attempt fell into a middle ground: Neither fully awaiting (wrong) nor fully executing (also partially wrong).

**Why This Matters:** Unlike subagents (which execute in isolated context and return results), skills require Claude to systematically execute inline instructions step-by-step. The first /qa execution did not do this, leading to skipped phases.

---

## Evidence Collected

### Critical Evidence: Skill Execution Model Documentation

**CLAUDE.md (Project Instructions)**
- Lines 14-32: Comparison chart showing mental model - "You execute instructions inline"
- Line 232: Explicit statement "NEVER wait passively after skill invocation"
- Lines 223-232: Section explaining skills are inline prompt expansions

**devforgeai-qa SKILL.md**
- Lines 14-29: EXECUTION MODEL section "YOU execute each phase sequentially"
- Lines 73-83: "QA Workflow (5 Phases)" showing mandatory sequence
- Line 77: "Progressive Disclosure: Load `references/deep-validation-workflow.md` once at Phase 0 for deep mode"
- Lines 279-281: Step 0.5 explicit instruction "Read(file_path=".claude/skills/devforgeai-qa/references/deep-validation-workflow.md")"
- Lines 129-136: Phase 1 Pre-Flight section verifying Phase 0 complete
- Phases 1-4: All start with pre-flight checks (lines 129, 166, 309, 409)

### High Evidence: User Feedback Loop

**Conversation Record:**
1. First `/qa STORY-127 deep` invocation: Claude executed ~60% of phases, declared "QA VALIDATION COMPLETE"
2. User message: "did you skip any phases?" ← Direct feedback indicating missing work
3. Claude acknowledgment: "Yes, I did skip several steps within the phases" ← Admitted partial execution
4. User clarification: "yes - run them all. deep is meant for you to run a deep qa analysis" ← Explicit requirement
5. Second attempt: Claude executed all 5 phases completely ← Problem resolved by clarification

### Medium Evidence: Conversion to Complete Execution

After user clarification, Claude successfully executed:
- Phase 0: Setup with all 5 steps including Step 0.5 loading deep-validation-workflow.md
- Phase 1: Validation with traceability algorithm, test execution, coverage analysis
- Phase 2: Analysis with anti-pattern-scanner + 3 parallel validators (test-automator, code-reviewer, security-auditor)
- Phase 3: Reporting with qa-result-interpreter subagent
- Phase 4: Cleanup with markers and feedback hooks

This demonstrates the mental model was corrected through user feedback.

---

## Context Files Validation

All 6 context files reviewed:

| File | Status | Finding |
|------|--------|---------|
| tech-stack.md | EXISTS | Skill execution pattern not explicitly listed |
| source-tree.md | EXISTS | .claude/skills/ location documented |
| dependencies.md | EXISTS | Skills have no external dependencies |
| coding-standards.md | EXISTS | Python execution style covered, but skill execution model not explicit |
| architecture-constraints.md | EXISTS | Single responsibility principle enforced (each skill one phase) |
| anti-patterns.md | EXISTS | No anti-patterns in skill code, but execution pattern gap exists |

**Context Finding:** While skills are documented in multiple places, the execution model mental model is only documented in CLAUDE.md (lines 14-32). It is not reinforced in every skill's SKILL.md file, leading to inconsistent understanding.

---

## Recommendations

### REC-1: CRITICAL - Skill Execution Mental Model Enforcement

**Problem Addressed:** Claude's first /qa execution treated skill phases as "optional reference material" instead of "mandatory sequential instructions to execute."

**Proposed Solution:** Update CLAUDE.md's "CRITICAL: How Skills Work" section to include explicit pre-execution checklist that Claude must verify BEFORE invoking Skill tool.

**Implementation Details:**

**File:** `CLAUDE.md`
**Location:** After line 32 (end of mental model chart)
**Change Type:** Add new section

**Exact Text to Add:**
```markdown
### Pre-Skill Execution Checklist

**Before invoking ANY skill with Skill(command="..."), verify:**

1. **Skill contains phases?**
   - Skills contain phases (Phase 01, Phase 02, etc.)
   - ALL phases must execute in sequence (not optional)
   - If phases exist, you must execute all of them

2. **Phase 0 has reference loading?**
   - Check for "Step 0.N: Load reference files" or similar
   - If deep mode → Load reference files in Phase 0 BEFORE Phase 1 starts
   - Reference files contain complete workflow details needed for later phases

3. **Phases 1-4 have pre-flight checks?**
   - Check each phase for "Pre-Flight: Verify previous phase" section
   - Run pre-flight verification BEFORE executing phase's main work
   - HALT if previous phase not verified complete

4. **Skill says "YOU execute"?**
   - Explicit statements like "YOU execute the skill's phases"
   - This means you run all steps systematically
   - Not a reference to read selectively - mandatory instructions to follow

5. **Mode requested matches execution scope?**
   - Light mode → Execute specified light validation subset
   - Deep mode → Execute all documented phases completely
   - User clarification overrides defaults: If user says "run them all", execute all

**Enforcement:** If any checklist item is unclear, HALT before invoking skill and ask for clarification with AskUserQuestion tool.
```

**Rationale:** Prevents future skill execution from being incomplete. This explicit checklist makes the mental model requirements concrete and verifiable.

**Testing Procedure:**
1. Create test story: `devforgeai/specs/Stories/STORY-999-test.story.md`
2. Run: `/qa STORY-999 deep`
3. Verify Phase 0 Step 0.5 loads deep-validation-workflow.md
4. Verify Phase 1 pre-flight checks Phase 0 complete
5. Verify all 5 phases execute completely
6. Success criteria: All phases execute, no skipping allowed

**Effort Estimate:** 30 minutes (write + test) | **Complexity:** LOW | **Impact:** HIGH

**Dependencies:** None - this is documentation enhancement only.

---

### REC-2: HIGH - Phase 0 Step 0.5 Enforcement for Deep Mode

**Problem Addressed:** SKILL.md's "Load Deep Mode Workflow" step is documented but not enforced. Claude can skip it without warning, breaking phase visibility.

**Proposed Solution:** Add explicit verification in Phase 0 that checks whether deep-validation-workflow.md was loaded, and HALTS if not.

**Implementation Details:**

**File:** `.claude/skills/devforgeai-qa/SKILL.md`
**Location:** After Phase 0 Marker Write section (after line 281)
**Change Type:** Add new subsection

**Exact Text to Add:**
```markdown
### Phase 0 Completion Enforcement

**Verify deep-validation-workflow.md was loaded (deep mode only):**

```
IF mode == "deep":
    IF "deep-validation-workflow.md" NOT loaded in conversation:
        Display: "❌ CRITICAL ERROR: Phase 0 Step 0.5 incomplete"
        Display: "   Deep validation workflow reference file was not loaded"
        Display: "   Loaded file: .claude/skills/devforgeai-qa/references/deep-validation-workflow.md"
        HALT: "Cannot proceed to Phase 1 without deep workflow reference"
        Instruction: "Load the reference file manually, then resume /qa {STORY_ID} deep"
    ELSE:
        Display: "✓ Deep mode workflow reference verified loaded"
```

This enforcement prevents Phase 1-3 from executing without complete initialization.
```

**Rationale:** The deep-validation-workflow.md reference file contains all Phase 1-3 workflow details. Without it, Claude is working from abbreviated Phase 0 instructions only. Loading it is mandatory for correct deep mode execution.

**Testing Procedure:**
1. Intentionally skip reading deep-validation-workflow.md in Phase 0
2. Run: `/qa STORY-001 deep`
3. Verify: HALT message appears preventing Phase 1 execution
4. Verify: Error message includes file path and resolution steps
5. Manually load: `Read(file_path=".claude/skills/devforgeai-qa/references/deep-validation-workflow.md")`
6. Resume: Phases execute completely
7. Success criteria: Cannot bypass Phase 0 Step 0.5 enforcement

**Effort Estimate:** 15 minutes (add enforcement check) | **Complexity:** LOW | **Impact:** HIGH

**Dependencies:** REC-1 (mental model documentation)

---

### REC-3: HIGH - Pre-Flight Verification Enforcement at Phase Boundaries

**Problem Addressed:** Phases 1-4 have "Pre-Flight" sections that verify previous phase completed, but these are not enforced. Claude can skip them and jump between phases.

**Proposed Solution:** Add HALT logic to each phase's pre-flight that explicitly stops execution if previous phase marker not found.

**Implementation Details:**

**File:** `.claude/skills/devforgeai-qa/SKILL.md`
**Locations:**
- Phase 1 Pre-Flight (around line 129)
- Phase 2 Pre-Flight (around line 166)
- Phase 3 Pre-Flight (around line 309)
- Phase 4 Pre-Flight (around line 409)

**Change Type:** Modify existing "Pre-Flight: Verify Phase X Complete" sections

**Example for Phase 1 (lines 129-136):**

**Current:**
```
### Pre-Flight: Verify Phase 0 Complete

Glob(pattern="devforgeai/qa/reports/STORY-127/.qa-phase-0.marker")
```

**New:**
```
### Pre-Flight: Verify Phase 0 Complete

Glob(pattern="devforgeai/qa/reports/STORY-127/.qa-phase-0.marker")

IF marker file NOT found:
    CRITICAL ERROR: "Phase 0 not verified complete"
    HALT: "Phase 1 cannot execute without Phase 0 completion"
    Display: "Previous phase (Phase 0) must complete successfully before starting Phase 1"
    Instruction: "Start workflow from Phase 0. Run setup first."
    Exit: Code 1 (phase sequencing violation)

Display: "✓ Phase 0 verified complete - Phase 1 preconditions met"
```

**Repeat for Phases 2, 3, 4:** Same HALT logic, checking for previous phase marker.

**Rationale:** Enforces mandatory phase sequencing. Prevents Phase jumping, parallel execution attempts, or resume from wrong phase.

**Testing Procedure:**
1. Create test: Try to execute Phase 2 without Phase 0/1 complete
2. Verify: HALT message appears
3. Verify: Error message states which phase is missing
4. Fix: Execute from Phase 0
5. Success criteria: Cannot bypass phase sequencing, forced to follow order

**Effort Estimate:** 20 minutes (add HALT logic to 4 phases) | **Complexity:** LOW | **Impact:** HIGH

**Dependencies:** REC-2 (Phase 0 enforcement ensures Phase 0 actually completes)

---

### REC-4: MEDIUM - Phase Execution Status Display in TodoWrite

**Problem Addressed:** During execution, user has no real-time progress indication of which phases are executing/complete. User must infer from output.

**Proposed Solution:** Update TodoWrite todo list at the start of each phase to show "in_progress" status, then mark "completed" when phase finishes.

**Implementation Details:**

**File:** `.claude/skills/devforgeai-qa/SKILL.md`
**Locations:** After each phase's marker write section
- After Phase 0 marker (line 281)
- After Phase 1 marker (after line 536)
- After Phase 2 marker (after line...)
- After Phase 3 marker (after line...)
- After Phase 4 marker (after final phase)

**Change Type:** Add TodoWrite calls

**Exact Code to Add (after each phase marker):**

**After Phase 0:**
```
TodoWrite({
  todos: [
    { content: "Phase 0: Setup - checkpoint, validation, test isolation, lock",
      status: "completed",
      activeForm: "Phase 0 complete" },
    { content: "Phase 1: Validation - traceability, tests, coverage",
      status: "in_progress",
      activeForm: "Running Phase 1: Validation" },
    { content: "Phase 2: Analysis - anti-patterns, validators, compliance",
      status: "pending",
      activeForm: "Running Phase 2: Analysis" },
    { content: "Phase 3: Reporting - result, story update, interpreter",
      status: "pending",
      activeForm: "Running Phase 3: Reporting" },
    { content: "Phase 4: Cleanup - lock, hooks, summary, markers",
      status: "pending",
      activeForm: "Running Phase 4: Cleanup" }
  ]
})
```

**Repeat for each phase:** Update status to "in_progress" at phase start, "completed" at phase end.

**Rationale:** Provides real-time progress visibility to user. Helps user understand what's happening during long-running execution. Proves all phases are executing.

**Testing Procedure:**
1. Run: `/qa STORY-001 deep`
2. Observe: TodoWrite updates show Phase 0 → completed
3. Observe: TodoWrite shows Phase 1 → in_progress
4. Wait: Phase 1 completes
5. Observe: TodoWrite updates to Phase 1 → completed, Phase 2 → in_progress
6. Success criteria: User sees real-time progress throughout execution

**Effort Estimate:** 20 minutes (add TodoWrite calls) | **Complexity:** LOW | **Impact:** MEDIUM

**Dependencies:** None - can be added independently.

---

### REC-5: MEDIUM - Reference Document Auto-Load Utility

**Problem Addressed:** Multiple skills require loading reference files in Phase 0, but this pattern is not automated. Each skill duplicates the logic.

**Proposed Solution:** Create shared utility that all skills can call to auto-load their phase reference files based on mode.

**Implementation Details:**

**File:** New file `.claude/skills/shared-phase-0-loader.md`
**Location:** `.claude/skills/` directory (alongside other skills)
**Change Type:** Create new reusable component

**Exact File Content:**

```markdown
# Shared Phase 0 Reference Loader

Reusable utility for loading phase workflow reference files in Phase 0 setup.

## Usage Pattern

Each skill's Phase 0 should call:

```
Skill: Reference file loading for Phase 0
Params:
  skill_name: "devforgeai-qa"  // or any skill name
  mode: "deep"  // "light" or "deep"

Execute: Load appropriate reference files
```

## Implementation

Load based on skill and mode:

**devforgeai-qa:**
- Light mode: No reference files (light workflow inline in SKILL.md)
- Deep mode: Load `.claude/skills/devforgeai-qa/references/deep-validation-workflow.md`

**devforgeai-development:**
- Light mode: Load `.claude/skills/devforgeai-development/references/tdd-light-workflow.md` (if exists)
- Deep mode: Load `.claude/skills/devforgeai-development/references/tdd-deep-workflow.md`

**Pattern:**
```
IF skill == "devforgeai-{X}" AND mode == "deep":
    reference_path = ".claude/skills/devforgeai-{X}/references/{X}-deep-workflow.md"
    Read(file_path=reference_path)
    Display: "✓ {X} deep mode workflow reference loaded"
```

## Benefits

- Eliminates code duplication across skills
- Standardizes Phase 0 Step 0.N implementation
- Single source of truth for reference loading
- Easy to add new skills without reinventing pattern

## Future Skills

When creating new skill, use this pattern:
1. Create `references/{skill-name}-deep-workflow.md`
2. In Phase 0 Step 0.N, call the loader utility
3. No need to duplicate Read/Load logic
```

**Then update each skill's Phase 0 to use this utility instead of duplicating code.**

**Rationale:** Prevents future skills from having inconsistent Phase 0 implementations. Standardizes the reference loading pattern across framework.

**Testing Procedure:**
1. Create new test skill with Phase 0
2. Use shared loader utility
3. Run new skill with deep mode
4. Verify: Reference files load correctly
5. Verify: Same behavior as manual implementation
6. Success criteria: Works across different skills

**Effort Estimate:** 45 minutes (create utility + refactor 2 skills + test) | **Complexity:** MEDIUM | **Impact:** MEDIUM

**Dependencies:** REC-1 (mental model documentation must be in place first)

---

## Implementation Checklist

**Status Update (2025-01-01):** Stories created for all 5 recommendations.

**Critical (Block Release):**
- [ ] **STORY-215:** REC-1 - Add pre-skill execution checklist to CLAUDE.md
- [ ] **STORY-216:** REC-2 - Add Phase 0 Step 0.5 enforcement to devforgeai-qa SKILL.md
- [ ] **STORY-217:** REC-3 - Add pre-flight HALT logic to Phases 1-4

**High (This Sprint):**
- [ ] **STORY-218:** REC-4 - Add TodoWrite status updates to devforgeai-qa phases
- [ ] Create test story and validate all REC-1 through REC-4

**Medium (Next Sprint):**
- [ ] **STORY-219:** REC-5 - Create shared reference loader utility
- [ ] Refactor devforgeai-development, devforgeai-orchestration to use utility

---

## Prevention Strategy

**Short-term (Implement REC-1 through REC-3):**
1. Make skill execution mental model explicit with pre-execution checklist
2. Enforce Phase 0 Step 0.5 reference loading for deep mode
3. Enforce phase sequencing with pre-flight HALT logic

**Long-term (Implement REC-4, REC-5):**
1. Add real-time progress tracking (TodoWrite) to all skills
2. Create shared utilities for common Phase 0 patterns
3. Document skill execution pattern in framework training
4. Add code review checklist: "Does skill follow all 5 REC-1 through REC-5 patterns?"

**Monitoring:**
- Watch for future /qa or /dev invocations that skip phases
- Review TodoWrite output to verify all phases execute
- Audit new skills to ensure Phase 0 enforcement in place

---

## Related RCAs

- **RCA-006:** Autonomous deferrals without user approval (similar approval pattern enforcement)
- **RCA-008:** Git operations without user consent (similar operational enforcement)
- **RCA-010:** Context file validation missing (similar phase requirement)
- **RCA-012:** AC tracking mechanism clarification (documentation clarity)

---

## Approval

**Prepared by:** devforgeai-rca skill
**Date:** 2025-12-23
**Severity:** HIGH (workflow violation)
**Status:** STORIES CREATED (STORY-215/216/217/218/219 created 2025-01-01)
