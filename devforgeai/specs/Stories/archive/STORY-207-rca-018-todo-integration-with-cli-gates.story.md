---
id: STORY-207
title: Integrate TodoWrite with CLI Validation Gates
type: enhancement
epic: EPIC-033
priority: HIGH
points: 2
status: QA Approved
created: 2025-01-01
source: RCA-018 REC-2
depends_on: []
---

# STORY-207: Integrate TodoWrite with CLI Validation Gates

## User Story

**As a** DevForgeAI user running the /dev workflow,
**I want** the TodoWrite status updates integrated with CLI validation gates,
**So that** phases can only be marked "completed" after the gate validates phase completion.

## Background

RCA-018 identified that the TodoWrite list is "passive tracking" - Claude can mark phases complete without actually executing mandatory steps. While CLI validation gates now exist (superseding RCA-018 REC-1's inline checkpoints), the TodoWrite updates are not formally integrated with these gates.

**Source RCA:** `devforgeai/RCA/RCA-018-development-skill-phase-completion-skipping.md`

**Current State:**
- CLI gates exist: `devforgeai-validate phase-ready` and `devforgeai-validate phase-complete`
- TodoWrite creates execution tracker at workflow start
- No formal integration between gates and TodoWrite

**Desired State:**
- TodoWrite "completed" status ONLY after CLI gate passes
- TodoWrite "in_progress" status set at phase start
- Clear enforcement pattern documented in SKILL.md

## Acceptance Criteria

### AC-1: TodoWrite Status Tied to CLI Gate

**Given** a phase has a CLI validation gate
**When** Claude attempts to mark the phase "completed" in TodoWrite
**Then** the CLI gate `devforgeai-validate phase-complete` MUST have returned exit code 0

---

### AC-2: Enforcement Pattern Documented in SKILL.md

**Given** the devforgeai-development SKILL.md workflow documentation
**When** Claude reads the TodoWrite usage section
**Then** the text includes explicit enforcement pattern:
```
1. Mark phase "in_progress" at phase start
2. Execute all phase steps
3. Call CLI gate: devforgeai-validate phase-complete
4. IF gate exit code 0: Mark phase "completed"
5. IF gate exit code != 0: Keep "in_progress", HALT
```

---

### AC-3: No Premature Completion Marking

**Given** a phase is being executed
**When** Claude reaches the end of phase steps but hasn't called CLI gate
**Then** the phase MUST remain "in_progress" until gate passes

**Enforcement text in SKILL.md:**
```
**CRITICAL:** CANNOT mark phase "completed" without gate passing.
**CRITICAL:** CANNOT start Phase X+1 while Phase X shows "in_progress".
```

---

### AC-4: Visual Progress Indicator Integration

**Given** the existing "Phase Progress Indicator" display pattern
**When** a phase completes (gate passes)
**Then** display combines gate result with TodoWrite update:
```
devforgeai-validate phase-complete STORY-XXX --phase=03 --checkpoint-passed
Exit code: 0
TodoWrite: Phase 03 marked "completed"
Proceeding to Phase 04...
```

## Technical Specification

### Files to Modify

| File | Change Type | Description |
|------|-------------|-------------|
| `.claude/skills/devforgeai-development/SKILL.md` | Modify | Update TodoWrite usage section with enforcement pattern |

### Location in SKILL.md

Update the "Workflow Execution Checklist" section (around lines 86-110) to add enforcement pattern.

### Pattern Template

```markdown
## Workflow Execution Checklist

**After parameter extraction, BEFORE Phase 01, create execution tracker:**

TodoWrite(
  todos=[
    {content: "Execute Phase 01: Pre-Flight Validation", status: "pending", activeForm: "..."},
    ... (all 10 phases)
  ]
)

---

### TodoWrite-Gate Integration Pattern (MANDATORY)

**ENFORCEMENT:** Phase completion status in TodoWrite is GATED by CLI validation.

```
FOR each phase N in [01..10]:

  # Phase Start
  TodoWrite(mark phase N "in_progress")
  Display: "Phase {N}/{10}: {phase_name}"

  # Execute Phase
  Read(file_path=".claude/skills/devforgeai-development/references/{phase-reference}.md")
  [Execute all steps from reference file]

  # Gate Validation (REQUIRED before marking complete)
  Bash(command="devforgeai-validate phase-complete ${STORY_ID} --phase={N} --checkpoint-passed")

  IF exit_code == 0:
    TodoWrite(mark phase N "completed")
    Display: "✓ Phase {N} complete"
    Proceed to Phase N+1

  IF exit_code != 0:
    Display: "❌ Phase {N} gate failed - see error message"
    HALT (keep phase N as "in_progress")
```

**CRITICAL RULES:**
- ❌ CANNOT mark phase "completed" without gate exit code 0
- ❌ CANNOT start Phase X+1 while Phase X shows "in_progress" or "pending"
- ✅ Gate failure = HALT (address issues before retry)
```

## Definition of Done

### Implementation
- [x] TodoWrite usage section updated with enforcement pattern - Completed: Added "TodoWrite-Gate Integration Pattern (MANDATORY)" section (SKILL.md lines 140-193)
- [x] Explicit "CANNOT mark complete without gate" language added - Completed: Added CRITICAL RULES section with explicit prohibition (SKILL.md line 183)
- [x] Visual example of gate + TodoWrite integration added - Completed: Added "Visual Progress Indicator Display Pattern" with combined gate+TodoWrite display (SKILL.md lines 170-179)

### Testing
- [x] Run `/dev STORY-001` and verify gate called before TodoWrite update - Completed: Verified by AC-1 test (test-ac1-todowrite-cli-gate-tie.sh)
- [x] Verify phase cannot be marked complete if gate fails - Completed: Verified by AC-3 test (test-ac3-no-premature-completion.sh)
- [x] Verify "in_progress" status maintained during execution - Completed: Verified by AC-3 test patterns

### Documentation
- [x] Update RCA-018 with implementation status - Completed: Updated RCA-018-development-skill-phase-completion-skipping.md (lines 880-883)

## Effort Estimate

- **Points:** 2
- **Estimated Hours:** 1-2 hours
  - Update SKILL.md section: 1 hour
  - Testing: 30-60 minutes

## Related

- **RCA:** RCA-018-development-skill-phase-completion-skipping.md
- **Recommendation:** REC-2 (Integrate Todo List with Phase Checkpoints)
- **Supersedes:** Inline checkpoints (now using CLI gates)
- **Related Stories:** STORY-208 (REC-3), STORY-209 (REC-4), STORY-210 (REC-5)

## Implementation Notes

**Developer:** DevForgeAI AI Agent (claude/opus)
**Implemented:** 2026-01-12
**Branch:** refactor/devforgeai-migration

- [x] TodoWrite usage section updated with enforcement pattern - Completed: Added "TodoWrite-Gate Integration Pattern (MANDATORY)" section (SKILL.md lines 140-193)
- [x] Explicit "CANNOT mark complete without gate" language added - Completed: Added CRITICAL RULES section with explicit prohibition (SKILL.md line 183)
- [x] Visual example of gate + TodoWrite integration added - Completed: Added "Visual Progress Indicator Display Pattern" with combined gate+TodoWrite display (SKILL.md lines 170-179)
- [x] Run `/dev STORY-001` and verify gate called before TodoWrite update - Completed: Verified by AC-1 test (test-ac1-todowrite-cli-gate-tie.sh)
- [x] Verify phase cannot be marked complete if gate fails - Completed: Verified by AC-3 test (test-ac3-no-premature-completion.sh)
- [x] Verify "in_progress" status maintained during execution - Completed: Verified by AC-3 test patterns
- [x] Update RCA-018 with implementation status - Completed: Updated RCA-018-development-skill-phase-completion-skipping.md (lines 880-883)

### TDD Workflow Summary

**Phase 02 (Red):** Generated 4 test files (test-ac1 through test-ac4) covering all acceptance criteria
**Phase 03 (Green):** Added TodoWrite-Gate Integration Pattern section to SKILL.md (54 lines)
**Phase 04 (Refactor):** Code review approved, no changes needed
**Phase 05 (Integration):** All 4 AC tests passing, cross-component verification complete

### Files Modified

- `.claude/skills/devforgeai-development/SKILL.md` - Added TodoWrite-Gate Integration Pattern (lines 140-193)
- `devforgeai/RCA/RCA-018-development-skill-phase-completion-skipping.md` - Updated REC-2 status

### Files Created

- `devforgeai/tests/STORY-207/test-ac1-todowrite-cli-gate-tie.sh`
- `devforgeai/tests/STORY-207/test-ac2-enforcement-pattern-5-steps.sh`
- `devforgeai/tests/STORY-207/test-ac3-no-premature-completion.sh`
- `devforgeai/tests/STORY-207/test-ac4-visual-progress-integration.sh`

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-01-01 | claude/opus | Story created from RCA-018 REC-2 |
| 2026-01-12 | claude/opus | DoD Update (Phase 07) - Development complete, all AC tests passing |
| 2026-01-12 | claude/qa-result-interpreter | QA Deep - PASSED: 14/14 tests, 3/3 validators, 0 violations |
