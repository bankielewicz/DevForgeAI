---
id: STORY-169
title: "RCA-013 Phase Validation Checkpoint"
type: enhancement
priority: High
points: 3
status: QA Approved
epic: N/A
sprint: N/A
created: 2025-12-31
source_rca: RCA-013
source_recommendation: REC-3
tags: [rca-013, tdd-enforcement, phase-validation, mandatory-subagents]
---

# STORY-169: RCA-013 Phase Validation Checkpoint

## User Story

**As a** DevForgeAI framework user,
**I want** each TDD phase to validate that all mandatory subagents were invoked before proceeding,
**So that** phases are truly complete and not just marked as such without proper execution.

## Background

RCA-013 REC-3 addresses the related RCA-009/RCA-011 issue where Claude skips mandatory subagents within phases. This adds explicit validation checkpoints at the END of each phase that verify all mandatory subagents were invoked before allowing phase progression.

This complements REC-1 (phase resumption) by ensuring each iteration is complete.

## Acceptance Criteria

### AC#1: Phase 2 Validation Checkpoint
**Given** Phase 2 (Implementation/Green) is about to be marked complete
**When** the validation checkpoint executes
**Then** it should verify:
- [ ] backend-architect OR frontend-developer invoked (check for Task() call)
- [ ] context-validator invoked (check for Task() call)
And HALT if any check fails

### AC#2: Phase 3 Validation Checkpoint
**Given** Phase 3 (Refactoring) is about to be marked complete
**When** the validation checkpoint executes
**Then** it should verify:
- [ ] refactoring-specialist invoked
- [ ] code-reviewer invoked
- [ ] Light QA executed (devforgeai-qa --mode=light)
And HALT if any check fails

### AC#3: Phase 4 Validation Checkpoint
**Given** Phase 4 (Integration Testing) is about to be marked complete
**When** the validation checkpoint executes
**Then** it should verify:
- [ ] integration-tester invoked
And HALT if any check fails

### AC#4: HALT Behavior
**Given** a validation checkpoint fails
**When** mandatory subagent not invoked
**Then** display:
- Error message listing missing items
- "Complete missing items before proceeding"
- Do NOT proceed to next phase

### AC#5: PASS Behavior
**Given** all mandatory subagents verified
**When** checkpoint passes
**Then** display:
- "Phase X validation passed - all mandatory steps completed"
- Proceed to next phase

## Technical Specification

### File to Modify

**`.claude/skills/devforgeai-development/SKILL.md`**

### Checkpoint Template

At end of each phase (2, 3, 4), add:

```markdown
### Phase X Validation Checkpoint

Before marking Phase X complete, verify:
- [ ] {Subagent 1} invoked (check for Task() call in conversation)
- [ ] {Subagent 2} invoked (check for Task() call in conversation)

IF any check fails:
  Display: "Phase X incomplete: {missing items}"
  HALT (do not proceed to Phase X+1)
  Prompt: "Complete missing items before proceeding"

IF all checks pass:
  Display: "Phase X validation passed - all mandatory steps completed"
  Proceed to Phase X+1
```

### Subagent Verification Logic

```
# Check conversation for evidence of subagent invocation
FOR required_subagent in phase_required_subagents:
  IF conversation contains Task(subagent_type="{required_subagent}"):
    mark_verified(required_subagent)
  ELSE:
    add_to_missing(required_subagent)
```

## Definition of Done

### Implementation
- [x] Phase 2 validation checkpoint added (backend/frontend-architect, context-validator) - Phase 03 in workflow
- [x] Phase 3 validation checkpoint added (refactoring-specialist, code-reviewer, Light QA) - Phase 04 in workflow
- [x] Phase 4 validation checkpoint added (integration-tester) - Phase 05 in workflow
- [x] HALT behavior implemented for failed checks
- [x] PASS behavior implemented for successful checks
- [x] Both .claude/ and src/claude/ versions updated

### Testing
- [x] Test Phase 2 checkpoint catches missing backend-architect - test-ac1-phase03-validation-checkpoint.sh
- [x] Test Phase 2 checkpoint catches missing context-validator - test-ac1-phase03-validation-checkpoint.sh
- [x] Test Phase 3 checkpoint catches missing refactoring-specialist - test-ac2-phase04-validation-checkpoint.sh
- [x] Test checkpoint PASS when all subagents invoked - test-ac5-pass-behavior.sh
- [x] Verify HALT prevents phase progression - test-ac4-halt-behavior.sh

### Documentation
- [x] RCA-013 updated with implementation status
- [x] Related RCA-009, RCA-011 cross-referenced

## Non-Functional Requirements

### Reliability
- Checkpoint must accurately detect subagent invocation
- False positives (blocking when subagent was invoked) must be avoided

### Performance
- Checkpoint validation should be fast (<1 second)

## Effort Estimate

- **Story Points:** 3 (1 SP = 4 hours)
- **Estimated Hours:** 2 hours
- **Complexity:** Medium (applies pattern to 3 phases)

## Dependencies

- Related to STORY-161 (RCA-011 Immediate Execution Checkpoint) - similar pattern

## References

- Source RCA: `devforgeai/RCA/RCA-013-development-workflow-stops-before-completion-despite-no-deferrals.md`
- REC-3 Section: Lines 593-624
- Related: RCA-009 (mandatory subagent skipping), RCA-011 (phase skipping)

---

## Implementation Notes

- [x] Phase 2 validation checkpoint added (backend/frontend-architect, context-validator) - Phase 03 in workflow - Completed: Added Phase 03 Validation Checkpoint section to phase-03-implementation.md with subagent verification for backend-architect/frontend-developer and context-validator
- [x] Phase 3 validation checkpoint added (refactoring-specialist, code-reviewer, Light QA) - Phase 04 in workflow - Completed: Added Phase 04 Validation Checkpoint section to phase-04-refactoring.md with subagent verification for refactoring-specialist, code-reviewer, and Light QA
- [x] Phase 4 validation checkpoint added (integration-tester) - Phase 05 in workflow - Completed: Added Phase 05 Validation Checkpoint section to phase-05-integration.md with subagent verification for integration-tester
- [x] HALT behavior implemented for failed checks - Completed: Added HALT logic with "Phase X incomplete: {missing items}" and "Complete missing items before proceeding" messages
- [x] PASS behavior implemented for successful checks - Completed: Added PASS logic with "Phase X validation passed - all mandatory steps completed" message and proceed instruction
- [x] Both .claude/ and src/claude/ versions updated - Completed: Synced all 4 files (SKILL.md + 3 phase files) to src/claude/skills/devforgeai-development/
- [x] Test Phase 2 checkpoint catches missing backend-architect - Completed: test-ac1-phase03-validation-checkpoint.sh Test 3 and Test 6
- [x] Test Phase 2 checkpoint catches missing context-validator - Completed: test-ac1-phase03-validation-checkpoint.sh Test 4
- [x] Test Phase 3 checkpoint catches missing refactoring-specialist - Completed: test-ac2-phase04-validation-checkpoint.sh Test 3
- [x] Test checkpoint PASS when all subagents invoked - Completed: test-ac5-pass-behavior.sh (6 tests)
- [x] Verify HALT prevents phase progression - Completed: test-ac4-halt-behavior.sh (6 tests)
- [x] RCA-013 updated with implementation status - Completed: Updated RCA-013 "Next Sprint" section marking REC-3 complete via STORY-169
- [x] Related RCA-009, RCA-011 cross-referenced - Completed: RCA-013 already references these; marked as "addressed by REC-3"

**Files Modified:**
- `.claude/skills/devforgeai-development/SKILL.md` (lines 499-527) - Phase Validation Checkpoint Template
- `.claude/skills/devforgeai-development/phases/phase-03-implementation.md` - Phase 03 Validation Checkpoint
- `.claude/skills/devforgeai-development/phases/phase-04-refactoring.md` - Phase 04 Validation Checkpoint
- `.claude/skills/devforgeai-development/phases/phase-05-integration.md` - Phase 05 Validation Checkpoint
- `src/claude/skills/devforgeai-development/` - Distribution copies

**Test Coverage:** 36 tests in `tests/STORY-169/` (100% pass rate)

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | /create-stories-from-rca | Story created from RCA-013 REC-3 |
| 2025-01-04 | claude/opus | Implemented via /dev - TDD workflow complete, 36 tests passing |
| 2025-01-04 | claude/qa-result-interpreter | QA Deep | PASSED: Coverage 100%, 0 violations, 3/3 validators passed | qa-report.md |
