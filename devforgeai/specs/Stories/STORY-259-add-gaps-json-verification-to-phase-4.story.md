---
id: STORY-259
title: Add gaps.json Verification to Phase 4 Execution Summary
type: feature
epic: EPIC-040
sprint: Backlog
status: Dev Complete
points: 1
depends_on: ["STORY-258"]
priority: High
assigned_to: Unassigned
created: 2026-01-15
format_version: "2.5"
source_rca: RCA-002
source_recommendation: REC-3
---

# Story: Add gaps.json Verification to Phase 4 Execution Summary

## Description

**As a** DevForgeAI framework user,
**I want** Phase 4 execution summary to verify gaps.json exists when QA failed,
**so that** the QA workflow cannot complete without the mandatory remediation file.

**Context:** RCA-002 found that gaps.json creation was documented as MANDATORY but only within workflow context. This story adds a verification checkpoint to Phase 4 to catch any edge cases where gaps.json wasn't created.

## Acceptance Criteria

### AC#1: Verification Checkpoint Addition

**Given** the Phase 4 validation checkpoint section exists,
**When** reviewing the checkpoint items,
**Then** a new item is present: "IF QA FAILED: gaps.json exists?"

---

### AC#2: gaps.json Existence Check

**Given** overall_status is "FAILED" at Phase 4,
**When** the execution summary is generated,
**Then** verify gaps.json exists at `devforgeai/qa/reports/{STORY-ID}-gaps.json`.

---

### AC#3: HALT on Missing gaps.json

**Given** overall_status is "FAILED" AND gaps.json does not exist,
**When** Phase 4 reaches the verification checkpoint,
**Then**:
- Display "❌ CRITICAL: gaps.json missing for failed QA"
- HALT with message "Create gaps.json before completing QA workflow"

---

### AC#4: Skip Verification for Passing QA

**Given** overall_status is "PASSED" or "PASS WITH WARNINGS",
**When** Phase 4 reaches the verification checkpoint,
**Then** gaps.json check is skipped (no error if file doesn't exist).

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "SKILL.md Phase 4 Step 4.3"
      file_path: ".claude/skills/devforgeai-qa/SKILL.md"
      required_keys:
        - key: "gaps.json verification checkpoint"
          type: "markdown"
          example: "- [ ] **IF QA FAILED: gaps.json exists?** [RCA-002]"
          required: true
          validation: "Checkpoint item exists in Step 4.3"
          test_requirement: "Test: Grep for 'gaps.json exists' in SKILL.md"

  business_rules:
    - id: "BR-001"
      rule: "gaps.json verification only runs when QA FAILED"
      trigger: "overall_status == FAILED"
      validation: "Glob check executed"
      error_handling: "HALT if file missing"
      test_requirement: "Test: Passing QA does not check for gaps.json"
      priority: "High"

    - id: "BR-002"
      rule: "Missing gaps.json is a blocking error"
      trigger: "FAILED status AND no gaps.json"
      validation: "HALT message displayed"
      error_handling: "Workflow stops"
      test_requirement: "Test: Missing file causes HALT"
      priority: "Critical"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Reliability"
      requirement: "Defense in depth"
      metric: "Double verification (creation in Step 3.4, check in Step 4.3)"
      test_requirement: "Test: File verified even if Step 3.4 bug exists"
      priority: "High"
```

---

## Technical Limitations

```yaml
technical_limitations: []
```

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-258:** Link gaps.json Creation to QA Failed Status Transition
  - **Why:** Creates the gaps.json file that this story verifies
  - **Status:** Backlog

---

## Test Strategy

### Unit Tests

**Test Scenarios:**
1. **Happy Path:** FAILED status + gaps.json exists → verification passes
2. **Error Case:** FAILED status + no gaps.json → HALT
3. **Skip Case:** PASSED status → no verification

---

## Acceptance Criteria Verification Checklist

### AC#1: Verification Checkpoint Addition

- [x] Checkpoint item added to Step 4.3 - **Phase:** 3 - **Evidence:** SKILL.md line 1164

### AC#2: gaps.json Existence Check

- [x] Glob check implemented - **Phase:** 3 - **Evidence:** SKILL.md lines 1168-1170

### AC#3: HALT on Missing gaps.json

- [x] CRITICAL error message - **Phase:** 3 - **Evidence:** SKILL.md line 1171
- [x] HALT behavior - **Phase:** 3 - **Evidence:** SKILL.md line 1172

### AC#4: Skip Verification for Passing QA

- [x] Conditional check implemented - **Phase:** 3 - **Evidence:** SKILL.md lines 1175-1177

---

**Checklist Progress:** 5/5 items complete (100%)

---

## Definition of Done

### Implementation
- [x] Checkpoint item added to Phase 4 Step 4.3
- [x] Conditional check for FAILED status
- [x] Glob verification for gaps.json
- [x] HALT logic on missing file
- [x] RCA-002 reference comment added

### Quality
- [x] All 4 acceptance criteria have passing tests

### Testing
- [x] Unit test for FAILED + exists scenario
- [x] Unit test for FAILED + missing scenario
- [x] Unit test for PASSED scenario (skip)

### Documentation
- [x] RCA-002 reference in checkpoint comment

---

## Change Log

**Current Status:** Dev Complete

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-15 10:00 | claude/create-stories-from-rca | Created | Story created from RCA-002 REC-3 | STORY-259.story.md |
| 2026-01-16 11:45 | claude/backend-architect | Green (Phase 03) | Added gaps.json verification to Phase 4 Step 4.3 | .claude/skills/devforgeai-qa/SKILL.md |
| 2026-01-16 11:50 | claude/opus | DoD Update (Phase 07) | Marked all DoD items complete, status Dev Complete | STORY-259.story.md |

## Implementation Notes

- [x] Checkpoint item added to Phase 4 Step 4.3 - Completed: SKILL.md line 1164
- [x] Conditional check for FAILED status - Completed: SKILL.md line 1168
- [x] Glob verification for gaps.json - Completed: SKILL.md lines 1169-1170
- [x] HALT logic on missing file - Completed: SKILL.md lines 1171-1172
- [x] RCA-002 reference comment added - Completed: SKILL.md line 1164
- [x] All 4 acceptance criteria have passing tests - Completed: 9/9 tests pass
- [x] Unit test for FAILED + exists scenario - Completed: TEST-003, TEST-004
- [x] Unit test for FAILED + missing scenario - Completed: TEST-005, TEST-006
- [x] Unit test for PASSED scenario (skip) - Completed: TEST-008
- [x] RCA-002 reference in checkpoint comment - Completed: SKILL.md line 1164 `[RCA-002]`

## Notes

**Source:**
- **RCA:** RCA-002
- **Recommendation:** REC-3

---

**Story Template Version:** 2.5
**Last Updated:** 2026-01-15
