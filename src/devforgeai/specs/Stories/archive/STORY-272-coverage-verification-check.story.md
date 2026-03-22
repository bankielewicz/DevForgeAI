---
id: STORY-272
title: Coverage Verification Check for AC Verification
type: feature
epic: EPIC-046
sprint: SPRINT-8
status: QA Approved
points: 2
depends_on: ["STORY-271"]
priority: High
assigned_to: Unassigned
created: 2026-01-19
format_version: "2.5"
---

# Story: Coverage Verification Check for AC Verification

## Description

**As a** verification subagent,
**I want** to verify test coverage exists for each AC,
**so that** I can confirm the AC is properly tested before marking as verified.

## Acceptance Criteria

### AC#1: Test File Location

**Given** a story ID being verified,
**When** the subagent checks for test coverage,
**Then** it locates test files in `tests/STORY-XXX/` directory.

---

### AC#2: AC-Test Mapping Verification

**Given** located test files,
**When** the subagent analyzes test naming,
**Then** it verifies tests exist following convention: `test_ac{N}_*` (e.g., `test_ac1_authentication.py`).

---

### AC#3: Test Existence Check per AC

**Given** an AC being verified,
**When** no corresponding test file exists,
**Then** the AC is flagged with: "No test found for AC#{N}".

---

### AC#4: Test Content Validation

**Given** a test file exists for an AC,
**When** the subagent inspects the test,
**Then** it verifies the test contains assertions related to the AC's Then clause.

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "DataModel"
      name: "CoverageResult"
      purpose: "Test coverage verification for AC"
      fields:
        - name: "ac_id"
          type: "String"
          constraints: "Required"
          description: "AC being checked"
          test_requirement: "Test: Verify ac_id matches source AC"
        - name: "tests_found"
          type: "Array<String>"
          constraints: "Required (may be empty)"
          description: "Test files found for this AC"
          test_requirement: "Test: Verify array contains valid file names"
        - name: "coverage_met"
          type: "Boolean"
          constraints: "Required"
          description: "Whether coverage threshold met"
          test_requirement: "Test: Verify boolean reflects test existence"
        - name: "assertions_validated"
          type: "Boolean"
          constraints: "Optional"
          description: "Whether test assertions match AC"
          test_requirement: "Test: Verify assertion validation performed"

  business_rules:
    - id: "BR-001"
      rule: "Test file naming convention: test_ac{N}_*"
      trigger: "During test discovery"
      validation: "Grep for test_ac followed by AC number"
      error_handling: "Flag AC as uncovered if no matching test"
      test_requirement: "Test: Verify naming convention enforcement"
      priority: "High"
    - id: "BR-002"
      rule: "Test directory location: tests/STORY-XXX/"
      trigger: "During test file search"
      validation: "Glob pattern matches story-scoped test directory"
      error_handling: "Check alternate locations, log if found elsewhere"
      test_requirement: "Test: Verify test directory convention"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Test discovery"
      metric: "< 2 seconds for test file discovery"
      test_requirement: "Test: Test discovery completes in 2s"
      priority: "Medium"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- Test file discovery: < 2s
- Test content validation: < 1s per file

### Reliability

**Error Handling:**
- Test directory missing: Log warning, report 0 coverage
- Malformed test file: Log warning, mark as needs review

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-271:** Source Code Inspection Workflow
  - **Why:** Coverage check follows same inspection patterns
  - **Status:** Backlog

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+

**Test Scenarios:**
1. **Happy Path:** Story with tests following naming convention
2. **Edge Cases:**
   - Story with no test directory
   - Tests in alternate naming format
   - Multiple tests per AC
3. **Error Cases:**
   - Test directory missing entirely
   - Test file exists but empty

---

## Acceptance Criteria Verification Checklist

### AC#1: Test File Location

- [x] Locates tests/STORY-XXX/ directory - **Phase:** 3 - **Evidence:** Glob result
- [x] Handles missing directory gracefully - **Phase:** 3 - **Evidence:** Error handling

### AC#2: AC-Test Mapping Verification

- [x] Identifies test_ac{N}_* pattern - **Phase:** 3 - **Evidence:** Pattern match
- [x] Maps tests to ACs correctly - **Phase:** 3 - **Evidence:** Mapping output

### AC#3: Test Existence Check

- [x] Detects missing tests for AC - **Phase:** 3 - **Evidence:** Flag output
- [x] Generates clear flag message - **Phase:** 3 - **Evidence:** Message content

### AC#4: Test Content Validation

- [x] Inspects test file content - **Phase:** 3 - **Evidence:** Read result
- [x] Validates assertions present - **Phase:** 3 - **Evidence:** Assertion check

---

**Checklist Progress:** 8/8 items complete (100%)

---

## Definition of Done

### Implementation
- [x] Test file location logic implemented
- [x] Naming convention verification working
- [x] Test existence flagging implemented
- [x] Test content validation implemented

### Quality
- [x] All 4 acceptance criteria have passing tests
- [x] Clear flag messages for missing tests
- [x] Handles edge cases gracefully

### Testing
- [x] Unit tests for test discovery
- [x] Unit tests for naming convention
- [x] Integration test with real test files

### Documentation
- [x] Test naming convention documented

---

## Implementation Notes

**Developer:** claude/opus
**Implemented:** 2026-01-19
**Branch:** main

- [x] Test file location logic implemented - Completed: Added Step 1 to Coverage Verification Workflow with Glob patterns for tests/STORY-XXX/
- [x] Naming convention verification working - Completed: Added Step 2-3 with test_ac{N}_* and test-ac{N}-* patterns
- [x] Test existence flagging implemented - Completed: Added Step 4 with "No test found for AC#N" flag message
- [x] Test content validation implemented - Completed: Added Step 5 with Read() and Grep() for assertion detection
- [x] All 4 acceptance criteria have passing tests - Completed: 25 tests across 4 AC files all passing
- [x] Clear flag messages for missing tests - Completed: Flag format documented in Step 4
- [x] Handles edge cases gracefully - Completed: Missing directory, empty files, malformed tests all handled
- [x] Unit tests for test discovery - Completed: test-ac1-test-file-location.sh
- [x] Unit tests for naming convention - Completed: test-ac2-ac-test-mapping-verification.sh
- [x] Integration test with real test files - Completed: run-all-tests.sh validates all ACs
- [x] Test naming convention documented - Completed: BR-001 in Coverage Verification Workflow

**Phase 02 (TDD Red) - 2026-01-19:**
- Generated 4 test files in `devforgeai/tests/STORY-272/`
- Tests validate ac-compliance-verifier.md coverage verification workflow
- All tests currently FAILING (correct RED state)
- Test files: test-ac1 through test-ac4 + run-all-tests.sh

**Phase 03 (TDD Green) - 2026-01-19:**
- Added Coverage Verification Workflow section to ac-compliance-verifier.md
- Documented all 4 ACs: test file location, AC-test mapping, existence check, content validation
- Added CoverageResult data model with ac_id, tests_found, coverage_met, assertions_validated
- Documented BR-001 (naming convention) and BR-002 (directory location)
- All 25 tests now PASSING (GREEN state)
- Context validation: PASSED (no violations)

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-19 14:45 | claude/devforgeai-story-creation | Created | Story created from EPIC-046 Feature 1.4 | STORY-272.story.md |
| 2026-01-19 | claude/test-automator | Red (Phase 02) | Generated 4 AC test files | devforgeai/tests/STORY-272/*.sh |
| 2026-01-19 | claude/backend-architect | Green (Phase 03) | Added Coverage Verification Workflow | .claude/agents/ac-compliance-verifier.md |
| 2026-01-19 | claude/refactoring-specialist | Refactor (Phase 04) | Reviewed, no major changes needed | .claude/agents/ac-compliance-verifier.md |
| 2026-01-19 | claude/integration-tester | Integration (Phase 05) | Integration tests passed | ac-compliance-verifier.md, test files |
| 2026-01-19 | claude/opus | DoD Update (Phase 07) | Development complete, DoD validated | STORY-272.story.md |
| 2026-01-19 | claude/qa-result-interpreter | QA Deep | PASSED: 25/25 tests, 100% traceability, 0 blocking violations | devforgeai/qa/reports/STORY-272-qa-report.md |

## Notes

**Design Decisions:**
- Test naming convention `test_ac{N}_*` enables automated mapping
- Story-scoped test directories (`tests/STORY-XXX/`) per existing convention
- Content validation is optional (existence check is minimum requirement)

**References:**
- EPIC-046: AC Compliance Verification System
- US-1.4 from requirements specification
- STORY-092: Story-Scoped Test Isolation (existing convention)
