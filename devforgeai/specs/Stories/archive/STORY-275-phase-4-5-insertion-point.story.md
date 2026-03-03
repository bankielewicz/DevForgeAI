---
id: STORY-275
title: Phase 4.5 Insertion Point for AC Verification
type: feature
epic: EPIC-046
sprint: SPRINT-8
status: QA Approved
points: 2
depends_on: ["STORY-274"]
priority: High
assigned_to: Unassigned
created: 2026-01-19
format_version: "2.5"
---

# Story: Phase 4.5 Insertion Point for AC Verification

## Description

**As a** framework developer,
**I want** AC verification to run after TDD refactor phase,
**so that** compliance issues are caught before integration tests.

## Acceptance Criteria

### AC#1: Phase Positioning

**Given** the devforgeai-development SKILL.md workflow,
**When** Phase 4.5 is added,
**Then** it is positioned between Phase 04 (Refactor) and Phase 05 (Integration).

---

### AC#2: Subagent Invocation

**Given** Phase 4.5 execution begins,
**When** the skill invokes ac-compliance-verifier,
**Then** it uses Task() with subagent_type="ac-compliance-verifier" and passes story ID.

---

### AC#3: Context Passing

**Given** the subagent is invoked,
**When** the prompt is constructed,
**Then** it includes story file path and technique instructions (fresh-context, one-by-one, source inspection).

---

### AC#4: Synchronous Execution

**Given** Phase 4.5 begins,
**When** the subagent executes,
**Then** the workflow waits for verification to complete before proceeding to Phase 05.

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "Phase 4.5 Definition"
      file_path: "src/claude/skills/devforgeai-development/SKILL.md"
      required_keys:
        - key: "phase_number"
          type: "string"
          example: "4.5"
          required: true
          validation: "Must be between Phase 04 and Phase 05"
          test_requirement: "Test: Verify phase ordering in SKILL.md"
        - key: "phase_name"
          type: "string"
          example: "AC Compliance Verification (Post-Refactor)"
          required: true
          validation: "Descriptive name"
          test_requirement: "Test: Verify phase has clear name"

    - type: "Configuration"
      name: "Subagent Invocation Pattern"
      file_path: "src/claude/skills/devforgeai-development/SKILL.md"
      required_keys:
        - key: "invocation_pattern"
          type: "code_block"
          example: "Task(subagent_type='ac-compliance-verifier', ...)"
          required: true
          validation: "Valid Task() invocation"
          test_requirement: "Test: Verify Task() syntax is correct"

  business_rules:
    - id: "BR-001"
      rule: "Phase 4.5 must block until verification completes"
      trigger: "During workflow execution"
      validation: "No parallel execution, synchronous wait"
      error_handling: "Timeout after 5 minutes"
      test_requirement: "Test: Verify synchronous execution"
      priority: "Critical"
    - id: "BR-002"
      rule: "Phase 4.5 runs after every refactor, not optionally"
      trigger: "During Phase 04 completion"
      validation: "Always transitions to Phase 4.5"
      error_handling: "N/A - mandatory"
      test_requirement: "Test: Verify mandatory execution"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Phase 4.5 verification"
      metric: "60-120 seconds acceptable (quality > speed)"
      test_requirement: "Test: Verify phase completes within 2 minutes"
      priority: "Medium"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- Phase 4.5 total: 60-120 seconds (acceptable per requirements)
- Timeout: 5 minutes maximum

### Reliability

**Error Handling:**
- Subagent failure: Retry once, then HALT
- Timeout: HALT with timeout message

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-274:** JSON Report Generation
  - **Why:** Phase 4.5 invokes the complete verification subagent
  - **Status:** Backlog

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+

**Test Scenarios:**
1. **Happy Path:** Phase 4.5 executes between Phase 04 and 05
2. **Edge Cases:**
   - Verification takes full 2 minutes
   - Story with many ACs (20)
3. **Error Cases:**
   - Subagent invocation fails
   - Verification times out

---

## Acceptance Criteria Verification Checklist

### AC#1: Phase Positioning

- [x] Phase 4.5 in SKILL.md - **Phase:** 3 - **Evidence:** Line 515 "## Phase 04.5"
- [x] Between Phase 04 and 05 - **Phase:** 3 - **Evidence:** Lines 511-540

### AC#2: Subagent Invocation

- [x] Task() call present - **Phase:** 3 - **Evidence:** Lines 520-537
- [x] Correct subagent_type - **Phase:** 3 - **Evidence:** Line 521 "ac-compliance-verifier"

### AC#3: Context Passing

- [x] Story file path passed - **Phase:** 3 - **Evidence:** Line 531 "${STORY_ID}*.story.md"
- [x] Technique instructions included - **Phase:** 3 - **Evidence:** Lines 526-529

### AC#4: Synchronous Execution

- [x] No parallel execution - **Phase:** 3 - **Evidence:** No run_in_background parameter
- [x] Waits for completion - **Phase:** 3 - **Evidence:** Lines 536-537 comment

---

**Checklist Progress:** 8/8 items complete (100%)

---

## Definition of Done

### Implementation
- [x] Phase 4.5 added to SKILL.md
- [x] Task() invocation correct
- [x] Context passed correctly
- [x] Synchronous execution enforced

### Quality
- [x] All 4 acceptance criteria have passing tests (34/34)
- [x] Phase ordering verified
- [x] Error handling implemented

### Testing
- [x] Unit tests for phase positioning (4 test suites, 34 tests - GREEN)
- [x] Integration test for subagent invocation

### Documentation
- [x] Phase 4.5 documented in SKILL.md
- [x] Reference file created (phase-04.5-ac-verification.md)

---

## Implementation Notes

- **Phase 02 (TDD Red):** 4 test suites generated covering all 4 ACs (34 tests total)
  - AC#1: 8 tests for phase positioning (6 failing)
  - AC#2: 7 tests for subagent invocation (4 failing)
  - AC#3: 10 tests for context passing (4 failing)
  - AC#4: 9 tests for synchronous execution (4 failing)
- Test files: `devforgeai/tests/STORY-275/test-ac{1-4}-*.sh`
- **Phase 03 (TDD Green):** Implementation complete in src/ tree
  - Added Phase 04.5 section to SKILL.md (between Phase 04 and 05)
  - Created `phase-04.5-ac-verification.md` phase file
  - Updated Required Subagents table with ac-compliance-verifier
  - Added phase transitions (04→4.5, 4.5→05)
  - Updated phase-05-integration.md entry gate to check from 4.5
  - All 34 tests now PASSING
- Implementation location: `src/claude/skills/devforgeai-development/` (user will copy to operational `.claude/skills/`)
- **Manual Deployment Required:** Copy src/ files to .claude/skills/ operational directory

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-19 15:00 | claude/devforgeai-story-creation | Created | Story created from EPIC-046 Feature 2.1 | STORY-275.story.md |
| 2026-01-19 | claude/test-automator | Red (Phase 02) | Tests generated (34 tests, 4 suites) | devforgeai/tests/STORY-275/*.sh |
| 2026-01-20 | claude/backend-architect | Green (Phase 03) | Phase 4.5 implemented in src/ tree | src/claude/skills/devforgeai-development/SKILL.md, phases/phase-04.5-ac-verification.md |
| 2026-01-20 | claude/opus | DoD (Phase 07) | All DoD items marked complete, status→Dev Complete | STORY-275.story.md |
| 2026-01-20 | claude/qa-result-interpreter | QA Deep | PASSED: Coverage 100%, 0 violations | devforgeai/qa/reports/STORY-275-qa-report.md |

## Notes

**Design Decisions:**
- Phase 4.5 (not 5) to run BEFORE integration tests
- Synchronous (blocking) to ensure verification completes
- 60-120s acceptable per user preference (quality > speed)

**References:**
- EPIC-046: AC Compliance Verification System
- US-2.1 from requirements specification
