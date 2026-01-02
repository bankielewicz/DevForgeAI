---
id: STORY-182
title: Add Documentation Accuracy Validation to QA Deep Mode
type: feature
epic: EPIC-033
priority: MEDIUM
points: 2
status: Backlog
created: 2025-12-31
source: STORY-144 framework enhancement analysis
---

# STORY-182: Add Documentation Accuracy Validation to QA Deep Mode

## User Story

**As a** DevForgeAI framework maintainer,
**I want** QA to validate documentation accuracy claims,
**So that** SKILL.md file counts match actual filesystem state.

## Background

SKILL.md can claim "18 reference files" when directory contains 22 files.

## Acceptance Criteria

### AC-1: Step Added to Deep Validation
**Given** deep-validation-workflow.md
**Then** Step 1.X: Documentation Accuracy Validation added

### AC-2: File Count Claims Validated
**Given** SKILL.md with "Total: N reference files"
**Then** Glob count compared to claimed count

### AC-3: Discrepancies Reported
**Then** MEDIUM severity violations for discrepancies

### AC-4: All Claim Types Validated
**Then** file count, line count, section claims validated

### AC-5: Violation Message Clear
**Then** message: "Claims {claimed} files, found {actual}"

## Technical Specification

### Files to Modify
- `.claude/skills/devforgeai-qa/references/deep-validation-workflow.md`

### Implementation
```
FOR each SKILL.md containing "Total: N reference files":
    claimed_count = extract_number("Total: (\d+) reference files")
    actual_count = Glob(pattern="references/*.md").count()

    IF claimed_count != actual_count:
        violations.append({
            severity: "MEDIUM",
            type: "documentation_drift",
            message: "Claims {claimed_count} files, found {actual_count}"
        })
```

## Definition of Done

- [ ] Step 1.X added to deep-validation-workflow.md
- [ ] File count validation implemented
- [ ] MEDIUM severity violations reported
- [ ] Clear violation messages

## Effort Estimate
- **Points:** 2
- **Estimated Hours:** 1-2 hours

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | claude/opus | Story created from STORY-144 framework enhancement |
