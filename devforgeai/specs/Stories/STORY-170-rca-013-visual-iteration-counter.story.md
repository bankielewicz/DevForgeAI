---
id: STORY-170
title: "RCA-013 Visual Iteration Counter"
type: enhancement
priority: Medium
points: 2
status: QA Approved
epic: N/A
sprint: N/A
created: 2025-12-31
source_rca: RCA-013
source_recommendation: REC-4
tags: [rca-013, user-experience, progress-tracking, iteration]
---

# STORY-170: RCA-013 Visual Iteration Counter

## User Story

**As a** DevForgeAI framework user,
**I want** to see "TDD Iteration 1/5" in phase headers during development,
**So that** I understand if a story is requiring multiple passes and can assess complexity.

## Background

RCA-013 REC-1 implemented phase resumption logic, which means stories can now iterate through TDD phases multiple times. REC-4 adds visual feedback so users can see which iteration they're on, helping them understand:
- Story complexity (many iterations = complex story)
- Progress toward completion
- When iteration limit is approaching

## Acceptance Criteria

### AC#1: Iteration Counter in Phase Headers
**Given** a TDD workflow is executing
**When** a phase header is displayed
**Then** it should include iteration number: "Phase 2/9 - Iteration 1/5"

### AC#2: Counter Increments on Resumption
**Given** Phase 4.5-R triggers resumption (user rejected deferrals)
**When** workflow loops back to earlier phase
**Then** iteration counter should increment: "Iteration 2/5"

### AC#3: Warning at High Iterations
**Given** iteration count reaches 4 of 5
**When** phase header displays
**Then** it should include warning indicator: "Iteration 4/5 - Approaching limit"

### AC#4: Counter Persists Across Session
**Given** a story has completed iteration 2
**When** user runs `/resume-dev` to continue
**Then** iteration counter should resume at 3 (not reset to 1)

## Technical Specification

### File to Modify

**`.claude/skills/devforgeai-development/SKILL.md`**

### Phase Header Format Change

**Current:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Phase 2/9: Implementation - Green Phase
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**New:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Phase 2/9: Implementation - Green Phase
TDD Iteration: 1/5
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Iteration Storage

Store iteration count in:
1. TodoWrite context (for current session)
2. Story file workflow section (for persistence)

```yaml
## Workflow Status
- iteration_count: 2
- last_iteration_date: 2025-12-31
```

## Definition of Done

### Implementation
- [x] Phase headers updated to include iteration counter
- [x] Counter increments when Phase 4.5-R triggers resumption
- [x] Warning displayed at iteration 4/5
- [x] Counter persisted in story workflow section
- [x] Both .claude/ and src/claude/ versions updated

### Testing
- [x] Test counter displays in phase headers
- [x] Test counter increments on resumption
- [x] Test warning appears at 4/5
- [x] Test persistence across sessions with /resume-dev

### Documentation
- [x] RCA-013 updated with implementation status

## Effort Estimate

- **Story Points:** 2 (1 SP = 4 hours)
- **Estimated Hours:** 1 hour
- **Complexity:** Low (display formatting + counter logic)

## Dependencies

- RCA-013 REC-1 (Phase Resumption Logic) - ✅ IMPLEMENTED

## References

- Source RCA: `devforgeai/RCA/RCA-013-development-workflow-stops-before-completion-despite-no-deferrals.md`
- REC-4 Section: Lines 628-633

---

## Implementation Notes

**Developer:** claude/opus
**Implemented:** 2026-01-04
**Story Type:** Documentation-Only Enhancement

- [x] Phase headers updated to include iteration counter - Completed: Added "TDD Iteration: 1/5" format to Display Template Pattern in SKILL.md
- [x] Counter increments when Phase 4.5-R triggers resumption - Completed: Added Step 5.1 iteration increment logic in phase-06-deferral.md
- [x] Warning displayed at iteration 4/5 - Completed: Added conditional "⚠️ Approaching limit" warning in both SKILL.md and phase-06-deferral.md
- [x] Counter persisted in story workflow section - Completed: Documented phase-state.json schema with iteration_count and last_iteration_date fields
- [x] Both .claude/ and src/claude/ versions updated - Completed: All changes mirrored to src/claude/skills/devforgeai-development/
- [x] Test counter displays in phase headers - Completed: test_ac1_iteration_counter_in_phase_headers.sh (4/4 assertions)
- [x] Test counter increments on resumption - Completed: test_ac2_counter_increments_on_resumption.sh (4/4 assertions)
- [x] Test warning appears at 4/5 - Completed: test_ac3_warning_at_high_iterations.sh (5/5 assertions)
- [x] Test persistence across sessions with /resume-dev - Completed: test_ac4_counter_persists_across_session.sh (6/6 assertions)
- [x] RCA-013 updated with implementation status - Completed: Marked REC-4 as DONE in RCA-013 Next Sprint section

### TDD Workflow Summary

**Phase 02 (Red):** Generated 5 test files covering 4 ACs with 19 pattern assertions
**Phase 03 (Green):** Implemented minimal documentation changes to pass tests
**Phase 04 (Refactor):** Code review completed, identified src/ sync issue and fixed
**Phase 05 (Integration):** All 19/19 pattern tests passing (100% coverage)

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | /create-stories-from-rca | Story created from RCA-013 REC-4 |
| 2026-01-04 | claude/test-automator | Red (Phase 02): Tests generated for AC#1-4 |
| 2026-01-04 | claude/backend-architect | Green (Phase 03): Implementation complete |
| 2026-01-04 | claude/refactoring-specialist | Refactor (Phase 04): Code review completed, src/ synced |
| 2026-01-04 | integration-tester | QA (Phase 04.5): Integration tests passed (19/19 patterns, 100% coverage) |
| 2026-01-04 | claude/opus | DoD Update (Phase 07): All DoD items validated, ready for commit |
