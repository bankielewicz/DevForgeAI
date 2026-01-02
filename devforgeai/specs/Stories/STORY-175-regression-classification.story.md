---
id: STORY-175
title: Add Regression vs Pre-existing Classification to QA Validation
type: feature
epic: EPIC-033
priority: HIGH
points: 3
status: Backlog
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

- [ ] Git diff integration to identify changed files
- [ ] Violation classification field added
- [ ] Blocking logic updated based on classification
- [ ] QA report template updated
- [ ] Step 2.1.5 documented in deep-validation-workflow.md
- [ ] Edge cases handled

## Effort Estimate
- **Points:** 3
- **Estimated Hours:** 2-3 hours

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | claude/opus | Story created from STORY-144 framework enhancement |
