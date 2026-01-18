---
id: STORY-258
title: Link gaps.json Creation to QA Failed Status Transition
type: feature
epic: EPIC-040
sprint: Backlog
status: QA Approved
points: 1
depends_on: []
priority: High
assigned_to: Unassigned
created: 2026-01-15
format_version: "2.5"
source_rca: RCA-002
source_recommendation: REC-2
---

# Story: Link gaps.json Creation to QA Failed Status Transition

## Description

**As a** DevForgeAI framework user,
**I want** gaps.json to be automatically created when QA status transitions to "QA Failed",
**so that** the `/dev` remediation workflow has the required gap file regardless of how the failure was detected.

**Context:** RCA-002 discovered that when a CLI failure was found post-QA workflow (through manual user challenge), the mandatory gaps.json file was not created when status changed to "QA Failed". The gaps.json creation was buried in Phase 3 logic and not tied to status transitions.

## Acceptance Criteria

### AC#1: gaps.json Creation Before Status Update

**Given** QA validation determines overall_status is "FAILED",
**When** the atomic status update protocol executes (Step 3.4),
**Then** gaps.json is created BEFORE the story status field is updated to "QA Failed".

---

### AC#2: gaps.json Contains Current Violations

**Given** gaps.json is being created during status transition,
**When** the file is written,
**Then** it contains all violations from the current QA run:
- Each violation has type, severity, message, and remediation
- File is valid JSON
- File is written to `devforgeai/qa/reports/{STORY-ID}-gaps.json`

---

### AC#3: Creation Confirmation Message

**Given** gaps.json is created during status transition,
**When** the creation completes,
**Then** display "✓ gaps.json created (required for QA Failed status)".

---

### AC#4: Idempotent Creation

**Given** gaps.json already exists for the story,
**When** status transitions to "QA Failed" again,
**Then** the existing file is overwritten with current violations (not appended).

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "SKILL.md Step 3.4"
      file_path: ".claude/skills/devforgeai-qa/SKILL.md"
      required_keys:
        - key: "gaps.json creation in Step 3.4"
          type: "markdown"
          example: "# MANDATORY: Create gaps.json BEFORE status update [RCA-002]"
          required: true
          validation: "Code block exists in Step 3.4"
          test_requirement: "Test: Grep for 'gaps.json BEFORE status' in SKILL.md"

    - type: "DataModel"
      name: "gaps.json"
      table: "N/A (file-based)"
      purpose: "Store QA violations for /dev remediation"
      fields:
        - name: "story_id"
          type: "String"
          constraints: "Required"
          description: "Story identifier"
          test_requirement: "Test: story_id field present in output"
        - name: "qa_timestamp"
          type: "DateTime"
          constraints: "Required"
          description: "When QA was run"
          test_requirement: "Test: timestamp is valid ISO 8601"
        - name: "overall_status"
          type: "String"
          constraints: "Required, enum: FAILED"
          description: "QA result status"
          test_requirement: "Test: status is always FAILED when file created"
        - name: "violations"
          type: "Array"
          constraints: "Required, min 1 item"
          description: "List of violations"
          test_requirement: "Test: violations array has at least 1 entry"

  business_rules:
    - id: "BR-001"
      rule: "gaps.json MUST be created before status changes to QA Failed"
      trigger: "overall_status == FAILED"
      validation: "File exists before Edit() call for status"
      error_handling: "HALT if file creation fails"
      test_requirement: "Test: Status update blocked until gaps.json exists"
      priority: "Critical"

    - id: "BR-002"
      rule: "gaps.json creation is idempotent"
      trigger: "Repeated QA runs on same story"
      validation: "File contains only current run violations"
      error_handling: "Overwrite existing file"
      test_requirement: "Test: Second QA run overwrites previous gaps.json"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Reliability"
      requirement: "Atomic file creation"
      metric: "File is complete or not created (no partial writes)"
      test_requirement: "Test: Interrupted write leaves no partial file"
      priority: "High"
```

---

## Technical Limitations

```yaml
technical_limitations: []
```

---

## Non-Functional Requirements (NFRs)

### Reliability

**File Creation:**
- Atomic write: Complete file or no file
- Valid JSON: Always parseable
- Deterministic path: `devforgeai/qa/reports/{STORY-ID}-gaps.json`

---

## Dependencies

### Prerequisite Stories

None.

### External Dependencies

None.

### Technology Dependencies

None - uses existing Write tool.

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+

**Test Scenarios:**
1. **Happy Path:** FAILED status triggers gaps.json creation
2. **Edge Cases:**
   - Multiple violations in single run
   - Second QA run overwrites existing file
3. **Error Cases:**
   - File system permission error (graceful failure)

---

## Acceptance Criteria Verification Checklist

### AC#1: gaps.json Creation Before Status Update

- [x] gaps.json created before Edit() call - **Phase:** 3 - **Evidence:** Step 3.3.5 in SKILL.md (line 791)
- [x] Order verified (file check before status) - **Phase:** 4 - **Evidence:** test_ac1_step_ordering passes

### AC#2: gaps.json Contains Current Violations

- [x] All violations included - **Phase:** 3 - **Evidence:** Step 3.3.5 JSON schema
- [x] Valid JSON format - **Phase:** 3 - **Evidence:** test_ac2_violation_fields passes
- [x] Correct file path - **Phase:** 3 - **Evidence:** test_ac2_file_path passes

### AC#3: Creation Confirmation Message

- [x] Message displayed after creation - **Phase:** 3 - **Evidence:** test_ac3_confirmation_message passes

### AC#4: Idempotent Creation

- [x] Existing file overwritten - **Phase:** 3 - **Evidence:** test_ac4_idempotent passes

---

**Checklist Progress:** 7/7 items complete (100%)

---

## Definition of Done

### Implementation
- [x] gaps.json creation added to Step 3.4 atomic protocol - Completed: Step 3.3.5 added to SKILL.md (lines 791-824)
- [x] Creation occurs BEFORE status update - Completed: Step 3.3.5 precedes Step 3.4
- [x] Violation mapping to JSON implemented - Completed: JSON schema with story_id, qa_timestamp, overall_status, violations
- [x] Confirmation message implemented - Completed: Display "✓ gaps.json created (required for QA Failed status)"
- [x] Overwrite behavior implemented - Completed: Write() tool overwrites existing file (idempotent)

### Quality
- [x] All 4 acceptance criteria have passing tests - Completed: 7 tests covering all 4 ACs (100% pass rate)
- [x] Edge cases covered - Completed: Idempotent overwrite, ordering verification
- [x] JSON output validated - Completed: test_ac2_violation_fields validates schema

### Testing
- [x] Unit test for gaps.json creation - Completed: tests/STORY-258/test_gaps_json_creation.sh
- [x] Unit test for idempotent overwrite - Completed: test_ac4_idempotent
- [x] Integration test with QA workflow - Completed: integration-tester validated Step 3.3.5 → 3.4 flow

### Documentation
- [x] RCA-002 reference in SKILL.md comments - Completed: Step 3.3.5 header includes [RCA-002] tag

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-01-16
**Branch:** refactor/devforgeai-migration

- [x] gaps.json creation added to Step 3.4 atomic protocol - Completed: Step 3.3.5 added to SKILL.md (lines 791-824)
- [x] Creation occurs BEFORE status update - Completed: Step 3.3.5 precedes Step 3.4
- [x] Violation mapping to JSON implemented - Completed: JSON schema with story_id, qa_timestamp, overall_status, violations
- [x] Confirmation message implemented - Completed: Display "✓ gaps.json created (required for QA Failed status)"
- [x] Overwrite behavior implemented - Completed: Write() tool overwrites existing file (idempotent)
- [x] All 4 acceptance criteria have passing tests - Completed: 7 tests covering all 4 ACs (100% pass rate)
- [x] Edge cases covered - Completed: Idempotent overwrite, ordering verification
- [x] JSON output validated - Completed: test_ac2_violation_fields validates schema
- [x] Unit test for gaps.json creation - Completed: tests/STORY-258/test_gaps_json_creation.sh
- [x] Unit test for idempotent overwrite - Completed: test_ac4_idempotent
- [x] Integration test with QA workflow - Completed: integration-tester validated Step 3.3.5 → 3.4 flow
- [x] RCA-002 reference in SKILL.md comments - Completed: Step 3.3.5 header includes [RCA-002] tag

### Files Modified

- `.claude/skills/devforgeai-qa/SKILL.md` - Added Step 3.3.5: MANDATORY gaps.json Creation BEFORE Status Transition [RCA-002]

### Files Created

- `tests/STORY-258/test_gaps_json_creation.sh` - 7 tests validating all 4 acceptance criteria

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-15 10:00 | claude/create-stories-from-rca | Created | Story created from RCA-002 REC-2 | STORY-258.story.md |
| 2026-01-16 10:30 | claude/test-automator | Red (Phase 02) | Tests generated | tests/STORY-258/test_gaps_json_creation.sh |
| 2026-01-16 10:45 | claude/backend-architect | Green (Phase 03) | Step 3.3.5 implemented | .claude/skills/devforgeai-qa/SKILL.md |
| 2026-01-16 11:00 | claude/opus | DoD Update (Phase 07) | Development complete, DoD validated | STORY-258.story.md |
| 2026-01-16 12:20 | claude/qa-result-interpreter | QA Deep | PASSED: Coverage 100%, 0 violations | STORY-258-qa-report.md |

## Notes

**Source:**
- **RCA:** RCA-002
- **Recommendation:** REC-2

**References:**
- `devforgeai/RCA/RCA-002-qa-cli-execution-gaps-validation.md`

---

**Story Template Version:** 2.5
**Last Updated:** 2026-01-15
