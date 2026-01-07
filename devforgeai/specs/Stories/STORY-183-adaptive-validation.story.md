---
id: STORY-183
title: Add Adaptive Parallel Validation Based on Story Type
type: feature
epic: EPIC-033
priority: MEDIUM
points: 2
status: Dev Complete
created: 2025-12-31
source: STORY-144 framework enhancement analysis
---

# STORY-183: Add Adaptive Parallel Validation Based on Story Type

## User Story

**As a** DevForgeAI developer,
**I want** QA to select validators based on story type,
**So that** documentation stories don't waste tokens on code validators.

## Acceptance Criteria

### AC-1: Story Type Extracted in Phase 0
**Given** QA validation starts
**Then** story type extracted from YAML frontmatter

### AC-2: Documentation Stories Use Fewer Validators
**Given** story type is "documentation"
**Then** only code-reviewer runs (no test-automator, no security-auditor)

### AC-3: Refactor Stories Skip Test-Automator
**Given** story type is "refactor"
**Then** test-automator skipped (tests exist)

### AC-4: Feature/Bugfix Use All Validators
**Given** story type is "feature" or "bugfix"
**Then** all 3 validators run

### AC-5: Success Threshold Adjusted
**Then** threshold adjusted based on validator count

## Technical Specification

### Files to Modify
- `.claude/skills/devforgeai-qa/SKILL.md`
- `.claude/skills/devforgeai-qa/references/parallel-validation.md`

### Implementation
```
IF story_type == "documentation":
    validators = ["code-reviewer"]
    success_threshold = 1
ELIF story_type == "refactor":
    validators = ["code-reviewer", "security-auditor"]
    success_threshold = 1
ELSE:
    validators = ["test-automator", "code-reviewer", "security-auditor"]
    success_threshold = 2
```

## Definition of Done

- [x] Story type detection in Phase 0
- [x] Adaptive validator selection implemented
- [x] Success threshold calculation updated
- [x] Rationale documented in parallel-validation.md

## Implementation Notes

- [x] Story type detection in Phase 0 - Completed: Step 0.6 added to SKILL.md (lines 233-263) extracts type from YAML frontmatter
- [x] Adaptive validator selection implemented - Completed: Adaptive Validator Selection section in parallel-validation.md (lines 51-113)
- [x] Success threshold calculation updated - Completed: Threshold formula and rationale tables in parallel-validation.md (lines 189-240)
- [x] Rationale documented in parallel-validation.md - Completed: Rationale by Story Type section (lines 96-111)
- Validator mapping: documentation=1, refactor=2, feature/bugfix=3 validators
- Success thresholds: documentation=1/1, refactor=1/2, feature/bugfix=2/3
- Token savings: ~6K for documentation stories, ~3K for refactor stories
- All 15 tests pass (100% coverage of acceptance criteria)
- Test file: tests/STORY-183/test-adaptive-validation.sh

## Effort Estimate
- **Points:** 2
- **Estimated Hours:** 1-2 hours

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | claude/opus | Story created from STORY-144 framework enhancement |
| 2026-01-06 | claude/test-automator | Red (Phase 02): 15 failing tests generated |
| 2026-01-06 | claude/backend-architect | Green (Phase 03): Implementation complete - all tests pass |
| 2026-01-06 | claude/refactoring-specialist | Refactor (Phase 04): Added validator preview display |
| 2026-01-06 | claude/opus | DoD Update (Phase 07): All checkboxes marked complete |
