---
id: STORY-170
title: "RCA-013 Visual Iteration Counter"
type: enhancement
priority: Medium
points: 2
status: Backlog
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
- [ ] Phase headers updated to include iteration counter
- [ ] Counter increments when Phase 4.5-R triggers resumption
- [ ] Warning displayed at iteration 4/5
- [ ] Counter persisted in story workflow section
- [ ] Both .claude/ and src/claude/ versions updated

### Testing
- [ ] Test counter displays in phase headers
- [ ] Test counter increments on resumption
- [ ] Test warning appears at 4/5
- [ ] Test persistence across sessions with /resume-dev

### Documentation
- [ ] RCA-013 updated with implementation status

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
<!-- Filled in by devforgeai-development skill -->
*To be completed during development*

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | /create-stories-from-rca | Story created from RCA-013 REC-4 |
