---
id: STORY-182
title: Add Documentation Accuracy Validation to QA Deep Mode
type: feature
epic: EPIC-033
priority: MEDIUM
points: 2
status: Dev Complete
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

- [x] Step 1.X added to deep-validation-workflow.md - Completed: Section 1.3 Documentation Accuracy Validation (4 Steps) added at line 136
- [x] File count validation implemented - Completed: Step 2 uses Glob pattern comparison for reference file counting
- [x] MEDIUM severity violations reported - Completed: Step 3 generates violations with severity: "MEDIUM", type: "documentation_drift"
- [x] Clear violation messages - Completed: Message format "Claims {claimed_count} files, found {actual_count}" implemented

## Effort Estimate
- **Points:** 2
- **Estimated Hours:** 1-2 hours

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-01-06
**Branch:** refactor/devforgeai-migration

- [x] Step 1.X added to deep-validation-workflow.md - Completed: Section 1.3 Documentation Accuracy Validation (4 Steps) added at line 136
- [x] File count validation implemented - Completed: Step 2 uses Glob pattern comparison for reference file counting
- [x] MEDIUM severity violations reported - Completed: Step 3 generates violations with severity: "MEDIUM", type: "documentation_drift"
- [x] Clear violation messages - Completed: Message format "Claims {claimed_count} files, found {actual_count}" implemented

### TDD Workflow Summary

**Phase 02 (Red):** Generated 5 test files covering all 5 acceptance criteria
**Phase 03 (Green):** Added Section 1.3 to deep-validation-workflow.md (54 lines)
**Phase 04 (Refactor):** Updated Overview section, code review approved
**Phase 05 (Integration):** Cross-component integration verified, all tests passing

### Files Created/Modified

**Modified:**
- `.claude/skills/devforgeai-qa/references/deep-validation-workflow.md` (Section 1.3 added)

**Created:**
- `tests/STORY-182/test-ac1-step-added-to-deep-validation.sh`
- `tests/STORY-182/test-ac2-file-count-claims-validated.sh`
- `tests/STORY-182/test-ac3-discrepancies-reported.sh`
- `tests/STORY-182/test-ac4-all-claim-types-validated.sh`
- `tests/STORY-182/test-ac5-violation-message-clear.sh`
- `tests/STORY-182/run_all_tests.sh`

### Test Results

- **Total tests:** 5
- **Pass rate:** 100%
- **Execution time:** <1 second

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | claude/opus | Story created from STORY-144 framework enhancement |
| 2026-01-06 | claude/test-automator | Red (Phase 02) | Tests generated | tests/STORY-182/*.sh |
| 2026-01-06 | claude/backend-architect | Green (Phase 03) | Implementation complete | deep-validation-workflow.md |
| 2026-01-06 | claude/refactoring-specialist | Refactor (Phase 04) | Overview updated | deep-validation-workflow.md |
| 2026-01-06 | claude/opus | DoD Update (Phase 07) | Development complete | STORY-182 |
