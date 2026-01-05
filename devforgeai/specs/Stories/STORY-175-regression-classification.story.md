---
id: STORY-175
title: Add Regression vs Pre-existing Classification to QA Validation
type: feature
epic: EPIC-033
priority: HIGH
points: 3
status: Dev Complete
created: 2025-12-31
source: STORY-144 framework enhancement analysis
---

# STORY-175: Add Regression vs Pre-existing Classification to QA Validation

## User Story

**As a** DevForgeAI developer,
**I want** QA validation to distinguish between regressions and pre-existing issues,
**So that** I can focus on issues introduced by my current story without being blocked by legacy violations.

## Acceptance Criteria

### AC#1: Identify Files Changed by Current Story
**Given** QA validation is running
**When** deep validation begins
**Then** system uses `git diff --name-only HEAD~1` to identify changed files

### AC#2: Classify Violations
**Given** violations are detected
**When** classifying each violation
**Then** violations in changed files are `REGRESSION`, others are `PRE_EXISTING`

### AC#3: REGRESSION Violations Block QA
**Given** violations classified
**Then** `REGRESSION` violations block QA (blocking=true)
**And** `PRE_EXISTING` violations are warnings only (blocking=false)

### AC#4: Display Classification Breakdown
**Given** violations counted
**When** generating QA report
**Then** display: `Regressions: {count} | Pre-existing: {count}`

### AC#5: Document Classification Logic
**Given** implementation complete
**Then** Step 2.1.5 added to deep-validation-workflow.md

## Technical Specification

### Files to Modify
- `.claude/skills/devforgeai-qa/references/deep-validation-workflow.md`

### Implementation
```
changed_files = Bash(command="git diff --name-only HEAD~1")

FOR each violation:
    IF violation.file in changed_files:
        violation.classification = "REGRESSION"
        violation.blocking = true
    ELSE:
        violation.classification = "PRE_EXISTING"
        violation.blocking = false
```

## Edge Cases
1. **No git repository:** Fallback to all REGRESSION (blocking)
2. **First commit:** Use `git diff --name-only origin/main...HEAD`
3. **Empty changed files:** All PRE_EXISTING (non-blocking)

## Definition of Done

- [x] Git diff integration to identify changed files
- [x] Violation classification field added
- [x] Blocking logic updated based on classification
- [x] QA report template updated
- [x] Step 2.1.5 documented in deep-validation-workflow.md
- [x] Edge cases handled

## Effort Estimate
- **Points:** 3
- **Estimated Hours:** 2-3 hours

## Implementation Notes

- [x] Git diff integration to identify changed files
- [x] Violation classification field added
- [x] Blocking logic updated based on classification
- [x] QA report template updated
- [x] Step 2.1.5 documented in deep-validation-workflow.md
- [x] Edge cases handled

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-01-05

### Files Created/Modified
- `devforgeai/qa/__init__.py` - Package init with exports
- `devforgeai/qa/regression_classifier.py` - Main implementation (19 functions, 340 lines)
- `.claude/skills/devforgeai-qa/references/deep-validation-workflow.md` - Added Step 2.1.5

### Test Coverage
- 68 tests passing (100% pass rate)
- 92% code coverage
- All 5 ACs validated
- All 3 edge cases covered

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | claude/opus | Story created from STORY-144 framework enhancement |
| 2026-01-05 | claude/test-automator | Red (Phase 02): Generated 68 failing tests |
| 2026-01-05 | claude/backend-architect | Green (Phase 03): Implemented regression_classifier.py |
| 2026-01-05 | claude/refactoring-specialist | Refactor (Phase 04): Extracted helper functions, DRY improvements |
| 2026-01-05 | claude/opus | Dev Complete: All 6 DoD items completed |
