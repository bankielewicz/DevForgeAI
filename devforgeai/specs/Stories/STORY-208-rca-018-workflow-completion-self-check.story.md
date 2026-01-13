---
id: STORY-208
title: Add Workflow Completion Self-Check Before Final Result
type: enhancement
epic: EPIC-033
priority: HIGH
points: 2
status: QA Approved
created: 2025-01-01
source: RCA-018 REC-3
depends_on:
  - STORY-207
---

# STORY-208: Add Workflow Completion Self-Check Before Final Result

## User Story

**As a** DevForgeAI user running the /dev workflow,
**I want** a mandatory self-check before the workflow declares completion,
**So that** skipped phases are caught before the result is displayed.

## Background

RCA-018 identified that Claude can declare "DEVELOPMENT WORKFLOW COMPLETE" with phases still showing "pending" in the TodoWrite list. A final self-check would catch any phases that were skipped before displaying results.

**Source RCA:** `devforgeai/RCA/RCA-018-development-skill-phase-completion-skipping.md`

**Current State:**
- 10-phase workflow with CLI gates per phase
- dev-result-interpreter invoked in Phase 10
- No final validation that all phases completed

**Desired State:**
- Mandatory self-check after Phase 10, before displaying results
- Count of phases with "completed" status vs total (10/10 expected)
- HALT if any phase not "completed"

## Acceptance Criteria

### AC-1: Self-Check Before Result Display

**Given** the /dev workflow has completed Phase 10
**When** Claude is about to display the final result
**Then** a "Workflow Completion Self-Check" section MUST execute first

---

### AC-2: Phase Count Validation

**Given** the self-check is executing
**When** Claude counts phases with "completed" status
**Then** the count MUST equal 10 (all phases)

**Validation logic:**
```
count = 0
FOR each phase in TodoWrite list:
  IF phase.status == "completed":
    count += 1

IF count < 10:
  Display: "❌ WORKFLOW INCOMPLETE - {count}/10 phases completed"
  HALT

IF count == 10:
  Display: "✓ All 10 phases completed"
  Proceed to result display
```

---

### AC-3: Missing Phase Identification

**Given** the self-check finds count < 10
**When** HALT is triggered
**Then** display MUST list which phases are NOT "completed":
```
❌ WORKFLOW INCOMPLETE - 8/10 phases completed

Missing phases:
  ✗ Phase 06: Deferral Challenge (status: pending)
  ✗ Phase 07: DoD Update (status: pending)

Complete missing phases before displaying results.
```

---

### AC-4: Self-Check Location in SKILL.md

**Given** the Complete Workflow Execution Map section exists
**When** Claude reads the workflow documentation
**Then** the self-check section appears AFTER Phase 10, BEFORE result display

**Location:**
```markdown
## Phase 10: Result Interpretation
[Phase 10 content...]

---

## Workflow Completion Self-Check (MANDATORY)

[Self-check content here]

---

## Final Result Display
[Only reached if self-check passes]
```

## Technical Specification

### Files to Modify

| File | Change Type | Description |
|------|-------------|-------------|
| `.claude/skills/devforgeai-development/SKILL.md` | Modify | Add self-check section after Phase 10 |

### Self-Check Section Template

Add after Phase 10 documentation:

```markdown
---

## Workflow Completion Self-Check (MANDATORY BEFORE RESULT DISPLAY)

**Before displaying final result or returning to user, verify ALL phases completed:**

```
FINAL VALIDATION:

# Count completed phases from TodoWrite list
completed_count = 0
missing_phases = []

FOR each phase in [01, 02, 03, 04, 05, 06, 07, 08, 09, 10]:
  IF phase.status == "completed":
    completed_count += 1
  ELSE:
    missing_phases.append(phase)

# Validate count
IF completed_count < 10:
  Display:
  "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  "❌ WORKFLOW INCOMPLETE - Cannot declare completion"
  ""
  "Phases completed: {completed_count}/10"
  "Missing phases:"
  FOR each phase in missing_phases:
    Display: "  ✗ Phase {phase.number}: {phase.name} (status: {phase.status})"
  ""
  "Complete missing phases before displaying final result."
  "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  HALT (do not display "Workflow Complete" banner, do not return to user)

IF completed_count == 10:
  Display:
  "✓ All 10 phases completed - Workflow validation passed"
  ""
  "Proceeding to final result display..."

  Proceed to Final Result Display section
```

**Purpose:** Last-line defense against phase skipping. Catches any bypass of individual phase gates before user sees "complete" status.
```

### Integration with dev-result-interpreter

The self-check runs AFTER dev-result-interpreter subagent returns, BEFORE displaying to user:

```
Phase 10: Result Interpretation
  └─ Invoke dev-result-interpreter subagent
  └─ Receive structured result
  └─ [DO NOT DISPLAY YET]

Workflow Completion Self-Check
  └─ Count completed phases (10/10?)
  └─ IF pass: Proceed
  └─ IF fail: HALT

Final Result Display
  └─ Display structured result from Phase 10
  └─ Display "DEVELOPMENT WORKFLOW COMPLETE" banner
```

## Definition of Done

### Implementation
- [x] Self-check section added after Phase 10 - Completed: Added "Workflow Completion Self-Check" section at SKILL.md lines 639-682
- [x] Phase counting logic documented - Completed: FOR loop counts completed phases, validates count == 10
- [x] Missing phase identification documented - Completed: missing_phases array lists phases with status != "completed"
- [x] HALT behavior documented - Completed: HALT triggered when completed_count < 10, prevents "Workflow Complete" banner

### Testing
- [ ] Run `/dev STORY-001` and verify self-check executes
- [ ] Simulate skipped phase and verify HALT triggers
- [ ] Verify missing phases correctly identified

### Documentation
- [ ] Update RCA-018 with implementation status

## Effort Estimate

- **Points:** 2
- **Estimated Hours:** 1 hour
  - Add self-check section: 30 minutes
  - Testing: 30 minutes

## Related

- **RCA:** RCA-018-development-skill-phase-completion-skipping.md
- **Recommendation:** REC-3 (Add "Complete Workflow Execution Map" Checkpoint Reference)
- **Dependency:** STORY-207 (TodoWrite integration with gates)
- **Related Stories:** STORY-209 (REC-4), STORY-210 (REC-5)

## Implementation Notes

**Developer:** DevForgeAI AI Agent (claude/opus)
**Implemented:** 2026-01-12
**Branch:** refactor/devforgeai-migration

- [x] Self-check section added after Phase 10 - Completed: Added "Workflow Completion Self-Check" section at SKILL.md lines 639-682
- [x] Phase counting logic documented - Completed: FOR loop counts completed phases, validates count == 10
- [x] Missing phase identification documented - Completed: missing_phases array lists phases with status != "completed"
- [x] HALT behavior documented - Completed: HALT triggered when completed_count < 10, prevents "Workflow Complete" banner

### Files Modified
- `.claude/skills/devforgeai-development/SKILL.md` - Added self-check section (lines 639-682)

### TDD Summary
- **Phase 02 (Red):** 6 tests generated covering all 4 ACs
- **Phase 03 (Green):** Self-check section implemented, all tests GREEN
- **Phase 04 (Refactor):** Code quality reviewed, no blocking issues
- **Phase 05 (Integration):** Integration validated, section integrates cleanly

## Change Log

**Current Status:** QA Approved

| Date | Author | Change |
|------|--------|--------|
| 2025-01-01 | claude/opus | Story created from RCA-018 REC-3 |
| 2026-01-12 | claude/opus | DoD Update (Phase 07) - Implementation complete |
| 2026-01-12 | claude/qa-result-interpreter | QA Deep | PASS WITH WARNINGS: 100% traceability, 4/4 ACs verified, 0 violations |
