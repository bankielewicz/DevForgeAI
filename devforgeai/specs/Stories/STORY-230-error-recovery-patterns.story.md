---
id: STORY-230
title: Track Error Recovery Patterns
type: feature
epic: EPIC-034
sprint: Backlog
status: Dev Complete
points: 3
depends_on: ["STORY-229"]
priority: Medium
assigned_to: TBD
created: 2025-01-02
format_version: "2.5"
---

# Story: Track Error Recovery Patterns

## Description

**As a** Framework Analyst,
**I want** to analyze how developers recover from errors,
**so that** I can improve error handling and recovery guidance.

## Acceptance Criteria

### AC#1: Recovery Action Identification

**Given** an error entry,
**When** analyzing subsequent commands,
**Then** recovery actions are identified: retry, manual-fix, skip, escalate.

---

### AC#2: Recovery Success Tracking

**Given** recovery actions,
**When** measuring success,
**Then** success rate is calculated: did next attempt succeed?

---

### AC#3: Best Recovery Per Error Type

**Given** recovery patterns,
**When** correlating with error types,
**Then** most effective recovery action is identified per error category.

---

## Definition of Done

### Implementation
- [x] Recovery action detection
- [x] Success rate calculation
- [x] Error-recovery correlation

### Quality
- [x] All 3 acceptance criteria verified
- [x] Recovery chains complete

---

## Implementation Notes

- [x] Recovery action detection - AC#1 implemented with 4 action types (retry, manual-fix, skip, escalate)
- [x] Success rate calculation - AC#2 implemented with per-action success rates
- [x] Error-recovery correlation - AC#3 implemented with best recovery per error category
- [x] All 3 acceptance criteria verified - Tests: 18 assertions, 3/3 passing
- [x] Recovery chains complete - Pipeline: SessionEntry → ErrorEntry → RecoveryEntry

**Developer:** claude/opus
**Implemented:** 2026-01-05

### TDD Workflow Summary

- **Phase 02 (Red):** Generated 3 test files with 18 assertions
- **Phase 03 (Green):** Implemented Error Recovery Patterns section (~540 lines)
- **Phase 04 (Refactor):** Fixed unreachable code in determine_recovery_success()
- **Phase 05 (Integration):** Validated STORY-229 integration and data model compatibility

### Files Modified

- `src/claude/agents/session-miner.md` - Added Error Recovery Patterns section (lines 999-1540)
- `tests/results/STORY-230/` - Test suite (3 files, 18 assertions)

---

## Change Log

**Current Status:** Dev Complete

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2025-01-02 | claude/story-creation-skill | Created | Story created for EPIC-034 Feature 4 | STORY-230-error-recovery-patterns.story.md |
| 2026-01-05 | claude/test-automator | Red (Phase 02) | Generated 3 test files with 18 assertions | tests/results/STORY-230/*.sh |
| 2026-01-05 | claude/backend-architect | Green (Phase 03) | Implemented Error Recovery Patterns section | src/claude/agents/session-miner.md |
| 2026-01-05 | claude/refactoring-specialist | Refactor (Phase 04) | Fixed unreachable code in determine_recovery_success | src/claude/agents/session-miner.md |
| 2026-01-05 | claude/opus | DoD Update (Phase 07) | Marked DoD complete, updated Implementation Notes | STORY-230-error-recovery-patterns.story.md |
