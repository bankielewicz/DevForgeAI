---
id: STORY-183
title: Add Adaptive Parallel Validation Based on Story Type
type: feature
epic: EPIC-033
priority: MEDIUM
points: 2
status: Backlog
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

- [ ] Story type detection in Phase 0
- [ ] Adaptive validator selection implemented
- [ ] Success threshold calculation updated
- [ ] Rationale documented in parallel-validation.md

## Effort Estimate
- **Points:** 2
- **Estimated Hours:** 1-2 hours

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | claude/opus | Story created from STORY-144 framework enhancement |
