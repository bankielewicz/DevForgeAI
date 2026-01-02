---
id: STORY-169
title: "RCA-013 Phase Validation Checkpoint"
type: enhancement
priority: High
points: 3
status: Backlog
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
- [ ] Phase 2 validation checkpoint added (backend/frontend-architect, context-validator)
- [ ] Phase 3 validation checkpoint added (refactoring-specialist, code-reviewer, Light QA)
- [ ] Phase 4 validation checkpoint added (integration-tester)
- [ ] HALT behavior implemented for failed checks
- [ ] PASS behavior implemented for successful checks
- [ ] Both .claude/ and src/claude/ versions updated

### Testing
- [ ] Test Phase 2 checkpoint catches missing backend-architect
- [ ] Test Phase 2 checkpoint catches missing context-validator
- [ ] Test Phase 3 checkpoint catches missing refactoring-specialist
- [ ] Test checkpoint PASS when all subagents invoked
- [ ] Verify HALT prevents phase progression

### Documentation
- [ ] RCA-013 updated with implementation status
- [ ] Related RCA-009, RCA-011 cross-referenced

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
<!-- Filled in by devforgeai-development skill -->
*To be completed during development*

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | /create-stories-from-rca | Story created from RCA-013 REC-3 |
