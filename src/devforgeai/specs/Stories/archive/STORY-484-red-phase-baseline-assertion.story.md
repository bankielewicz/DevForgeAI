---
id: STORY-484
title: Add Pre-Implementation Baseline Assertion to Test-Automator RED Phase
type: feature
epic: EPIC-083
sprint: Backlog
status: QA Approved
points: 2
depends_on: []
priority: Medium
advisory: false
source_gap: null
source_story: null
assigned_to: DevForgeAI AI Agent
created: 2026-02-22
format_version: "2.9"
---

# Story: Add Pre-Implementation Baseline Assertion to Test-Automator RED Phase

## Description

**As a** developer running TDD RED phase,
**I want** the test-automator to flag tests that unexpectedly pass during the RED phase,
**so that** tests with insufficient assertions are caught before proceeding to GREEN phase.

## Provenance

```xml
<provenance>
  <origin document="REC-STORY408-001" section="recommendations-queue">
    <quote>"Flag tests that pass during RED phase as requiring tighter assertions. tdd-red-phase.md has a basic warning message but no anomaly detection, baseline tracking, or automated investigation."</quote>
    <line_reference>recommendations-queue.json, lines 55-63</line_reference>
    <quantified_impact>Prevents false GREEN transitions from weak assertions</quantified_impact>
  </origin>
</provenance>
```

## Acceptance Criteria

### AC#1: RED Phase Pass Detection

```xml
<acceptance_criteria id="AC1">
  <given>Tests are executed during TDD RED phase (before implementation)</given>
  <when>One or more tests pass unexpectedly</when>
  <then>The test-automator flags each passing test with a warning: "Test passed during RED phase - verify assertions are specific enough"</then>
  <verification>
    <source_files>
      <file hint="Test automator agent">.claude/agents/test-automator.md</file>
    </source_files>
    <test_file>src/tests/STORY-484/test_ac1_pass_detection.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

### AC#2: Anomaly Investigation Guidance

```xml
<acceptance_criteria id="AC2">
  <given>A test passes during RED phase</given>
  <when>The warning is displayed</when>
  <then>The test-automator provides investigation guidance: check if existing code already satisfies the test, verify assertion specificity, confirm test targets new (not existing) behavior</then>
  <verification>
    <source_files>
      <file hint="Test automator agent">.claude/agents/test-automator.md</file>
    </source_files>
    <test_file>src/tests/STORY-484/test_ac2_investigation_guidance.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

### AC#3: Baseline Tracking Documentation

```xml
<acceptance_criteria id="AC3">
  <given>The RED phase validation step exists in tdd-red-phase.md</given>
  <when>Baseline assertion tracking is documented</when>
  <then>Documentation specifies that pre-implementation test results should be recorded as a baseline, and any tests passing at baseline require explicit justification before proceeding</then>
  <verification>
    <source_files>
      <file hint="TDD red phase reference">.claude/skills/implementing-stories/phases/tdd-red-phase.md</file>
      <file hint="Test automator agent">.claude/agents/test-automator.md</file>
    </source_files>
    <test_file>src/tests/STORY-484/test_ac3_baseline_tracking.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "test-automator-red-phase"
      file_path: ".claude/agents/test-automator.md"
      required_keys:
        - key: "RED Phase Baseline Assertion"
          type: "string"
          required: true
          validation: "Section must include pass detection, investigation guidance, and baseline tracking"
          test_requirement: "Test: Verify baseline assertion section exists"
      requirements:
        - id: "CFG-001"
          description: "Add RED phase pass detection logic to test-automator.md"
          testable: true
          test_requirement: "Test: Grep for 'RED phase' and 'baseline' in test-automator.md"
          priority: "Critical"
        - id: "CFG-002"
          description: "Add investigation guidance for unexpectedly passing tests"
          testable: true
          test_requirement: "Test: Verify investigation steps documented"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "Tests passing during RED phase must be investigated before GREEN phase proceeds"
      trigger: "During RED phase test execution"
      validation: "All passing tests have explicit justification"
      error_handling: "Warning (non-blocking) with investigation guidance"
      test_requirement: "Test: Verify warning format and guidance content"
      priority: "Critical"

  non_functional_requirements: []
```

## Technical Limitations

```yaml
technical_limitations: []
```

## Dependencies

### Prerequisite Stories
- None

## Test Strategy

### Unit Tests
**Coverage Target:** 95%+

**Test Scenarios:**
1. **Happy Path:** Passing test during RED phase triggers warning with guidance
2. **Edge Cases:** All tests fail (no warning needed), mixed pass/fail results

## Acceptance Criteria Verification Checklist

### AC#1: Pass Detection
- [x] Warning for tests passing during RED phase - **Phase:** 3 - **Evidence:** file content

### AC#2: Investigation Guidance
- [x] Guidance steps documented - **Phase:** 3 - **Evidence:** file content

### AC#3: Baseline Tracking
- [x] Baseline recording documented in tdd-red-phase.md - **Phase:** 3 - **Evidence:** file content

---

**Checklist Progress:** 3/3 items complete (100%)

---

## Definition of Done

### Implementation
- [x] RED phase pass detection added to test-automator.md
- [x] Investigation guidance documented
- [x] Baseline tracking documented in tdd-red-phase.md

### Quality
- [x] All 3 acceptance criteria have passing tests

### Testing
- [x] Unit tests for detection and guidance content

### Documentation
- [x] test-automator.md and tdd-red-phase.md updated

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-23

- [x] RED phase pass detection added to test-automator.md - Completed: Added "RED Phase Baseline Assertion" section to src/claude/agents/test-automator.md with warning message and pass detection logic
- [x] Investigation guidance documented - Completed: Added "Investigation Steps" subsection with 3 guidance steps (check existing code, verify assertion specificity, confirm test targets new behavior)
- [x] Baseline tracking documented in tdd-red-phase.md - Completed: Added "Pre-Implementation Baseline Tracking" section to src/claude/skills/implementing-stories/references/tdd-red-phase.md with baseline recording and justification requirements
- [x] All 3 acceptance criteria have passing tests - Completed: 3 test files in tests/STORY-484/ all pass (8/8 assertions)
- [x] Unit tests for detection and guidance content - Completed: test_ac1, test_ac2, test_ac3 shell scripts validate content via grep
- [x] test-automator.md and tdd-red-phase.md updated - Completed: Both files in src/ tree updated with new sections

### TDD Workflow Summary

| Phase | Result |
|-------|--------|
| RED | 0/8 assertions passing (all tests fail as expected) |
| GREEN | 8/8 assertions passing (all tests pass) |
| REFACTOR | No changes needed (documentation story) |

### Files Modified
- `src/claude/agents/test-automator.md` - Added RED Phase Baseline Assertion section
- `src/claude/skills/implementing-stories/references/tdd-red-phase.md` - Added Pre-Implementation Baseline Tracking section

### Files Created
- `tests/STORY-484/test_ac1_red_phase_pass_detection.sh`
- `tests/STORY-484/test_ac2_anomaly_investigation_guidance.sh`
- `tests/STORY-484/test_ac3_baseline_tracking_documentation.sh`

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-22 | .claude/story-requirements-analyst | Created | Story created from REC-STORY408-001 triage | STORY-484.story.md |
| 2026-02-23 | .claude/qa-result-interpreter | QA Deep | PASSED: Coverage 100%, 0 violations | - |

## Notes

**Source:** REC-STORY408-001 from framework-analyst (STORY-408 Phase 09 consolidated analysis)

---

Story Template Version: 2.9
Last Updated: 2026-02-22
