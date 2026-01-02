---
id: STORY-164
title: "RCA-011 Self-Check Display for Phase Completion"
type: enhancement
priority: Medium
points: 2
status: Backlog
epic: N/A
sprint: N/A
created: 2025-12-31
source_rca: RCA-011
source_recommendation: REC-4
tags: [rca-011, tdd-enforcement, phase-completion, audit-trail]
---

# STORY-164: RCA-011 Self-Check Display for Phase Completion

## User Story

**As a** DevForgeAI framework user,
**I want** to see a confirmation display before each phase is marked complete,
**So that** I can verify all mandatory steps were executed and have an audit trail.

## Background

RCA-011 identified that Claude marks phases "completed" without reviewing if all mandatory steps executed. REC-4 requires Claude to display a "Mandatory Steps Completed" confirmation before marking any phase complete.

This creates:
1. Visual confirmation for user
2. Line number references for audit trail
3. Self-check mechanism forcing Claude to verify

## Acceptance Criteria

### AC-1: Phase 2 Completion Display
**Given** Claude is completing Phase 2
**When** Claude is about to mark Phase 2 as "completed"
**Then** Claude must first display:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase 2/9: Implementation - Mandatory Steps Completed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Step 1-2: backend-architect invoked (lines XXX-YYY)
✓ Step 3: context-validator invoked (lines XXX-YYY)

All Phase 2 mandatory steps completed. Proceeding to Phase 3...
```

### AC-2: Phase 3 Completion Display
**Given** Claude is completing Phase 3
**When** Claude is about to mark Phase 3 as "completed"
**Then** Claude must first display similar confirmation showing:
- refactoring-specialist invoked with line numbers
- code-reviewer invoked with line numbers
- Light QA executed with line numbers

### AC-3: Phase 7 Completion Display
**Given** Claude is completing Phase 7
**When** Claude is about to return results to command
**Then** Claude must first display confirmation showing:
- dev-result-interpreter invoked with line numbers

### AC-4: Line Number References
**Given** the self-check display
**When** showing "invoked (lines XXX-YYY)"
**Then** line numbers should reference actual conversation lines where Task/Skill was called

## Technical Specification

### File to Modify

**`.claude/skills/devforgeai-development/SKILL.md`**
- Sections: Phase 2, 3, 7 completion text
- Add: Self-check display requirements for each phase

### Example Implementation

After Phase 2 validation checkpoint, add:
```markdown
### Phase 2 Completion Display

Before marking Phase 2 complete, display:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase 2/9: Implementation - Mandatory Steps Completed ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Step 1-2: backend-architect invoked (lines XXX-YYY)
✓ Step 3: context-validator invoked (lines XXX-YYY)

All Phase 2 mandatory steps completed. Proceeding to Phase 3...
```

## Definition of Done

### Implementation
- [ ] Phase 2 self-check display added to SKILL.md
- [ ] Phase 3 self-check display added to SKILL.md
- [ ] Phase 7 self-check display added to SKILL.md
- [ ] Line number reference format documented
- [ ] Both .claude/ and src/claude/ versions updated

### Testing
- [ ] Test with `/dev STORY-XXX` and verify displays appear
- [ ] Verify line number references are accurate
- [ ] Verify displays appear BEFORE marking phase complete

### Documentation
- [ ] RCA-011 updated with implementation status

## Non-Functional Requirements

### Clarity
- Display format should be visually distinct (Unicode box-drawing)
- Line references should be specific (not ranges like "lines 100-500")

### Consistency
- All three phases use same display format
- Follows existing visual progress indicator pattern from RCA-010

## Effort Estimate

- **Story Points:** 2 (1 SP = 4 hours)
- **Estimated Hours:** 1 hour
- **Complexity:** Low-Medium (display templates and line tracking)

## Dependencies

- RCA-011 REC-1 (Phase 2/3/7 checkpoints) - ✅ IMPLEMENTED

## References

- Source RCA: `devforgeai/RCA/RCA-011-mandatory-tdd-phase-skipping.md`
- REC-4 Section: Lines 412-448

---

## Implementation Notes
<!-- Filled in by devforgeai-development skill -->
*To be completed during development*

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | /create-stories-from-rca | Story created from RCA-011 REC-4 |
