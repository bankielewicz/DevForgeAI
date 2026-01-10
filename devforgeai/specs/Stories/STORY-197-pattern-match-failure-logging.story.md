---
id: STORY-197
title: Log Pattern Match Failures for Continuous Improvement
type: enhancement
epic: EPIC-033-framework-enhancement-triage-q4-2025
sprint: Backlog
status: Dev Complete
points: 1
depends_on: ["STORY-195"]
priority: High
assigned_to: Unassigned
created: 2026-01-01
source_rca: RCA-015
source_recommendation: REC-3
format_version: "2.5"
---

# Story: Log Pattern Match Failures for Continuous Improvement

## Description

**As a** DevForgeAI framework maintainer,
**I want** the pre-tool-use.sh hook to log near-miss patterns when commands fail to match,
**so that** I can identify missing safe patterns and continuously improve hook effectiveness.

**Context from RCA-015:**
Currently there is no visibility into WHY commands don't match safe patterns. Adding near-miss logging will enable data-driven pattern selection by identifying commands that contain safe operations but don't start with them.

## Acceptance Criteria

### AC#1: Near-Miss Detection

**Given** a command that doesn't match any safe pattern
**When** the command contains a safe pattern (but doesn't start with it)
**Then** the hook logs the command and the near-miss patterns found

---

### AC#2: Command Prefix Logging

**Given** a command that doesn't match any safe pattern
**When** the hook prepares to ask user for approval
**Then** the first 20 characters of the command are logged for analysis

---

### AC#3: Near-Miss Log Format

**Given** a near-miss detection
**When** the near-miss is logged
**Then** log includes: command prefix, near-miss patterns, and recommendation message

---

### AC#4: Recommendation Generation

**Given** a near-miss pattern is detected
**When** the hook logs the near-miss
**Then** a recommendation message is included: "RECOMMENDATION: Command contains safe pattern but doesn't start with it - consider adding pattern"

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "pre-tool-use.sh"
      file_path: ".claude/hooks/pre-tool-use.sh"
      requirements:
        - id: "CFG-001"
          description: "Add near-miss detection after pattern matching loop"
          testable: true
          test_requirement: "Test: Command containing 'pytest' but starting with 'cd' logs near-miss"
          priority: "Critical"
        - id: "CFG-002"
          description: "Log command prefix (first 20 chars) for analysis"
          testable: true
          test_requirement: "Test: Log entry contains 'Command starts with:'"
          priority: "High"
        - id: "CFG-003"
          description: "Generate recommendation message for near-misses"
          testable: true
          test_requirement: "Test: Log entry contains 'RECOMMENDATION:'"
          priority: "Medium"

  business_rules:
    - id: "BR-001"
      rule: "Near-miss uses contains matching (*pattern*) not prefix matching"
      trigger: "After all prefix patterns fail"
      validation: "Loop through SAFE_PATTERNS checking if command contains pattern"
      error_handling: "Empty NEAR_MISSES array if no patterns found in command"
      test_requirement: "Test: 'cd /tmp && pytest' detects 'pytest' as near-miss"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Near-miss detection adds < 20ms overhead"
      metric: "< 20ms additional latency per command"
      test_requirement: "Test: Time near-miss detection on 50-pattern array"
      priority: "Medium"
```

---

## Technical Limitations

```yaml
technical_limitations: []
```

---

## Non-Functional Requirements (NFRs)

### Performance
- Near-miss detection: < 20ms overhead
- Only runs when command doesn't match (not on every command)

### Reliability
- Logging must not break command evaluation
- Empty arrays handled gracefully

---

## Dependencies

### Prerequisite Stories
- [ ] **STORY-195:** Add Common Command Composition Patterns
  - **Why:** Near-miss detection compares against SAFE_PATTERNS array
  - **Status:** Backlog

---

## Test Strategy

### Unit Tests
1. Test near-miss detection: `cd /tmp && pytest tests/` finds `pytest`
2. Test command prefix logging: First 20 chars logged
3. Test empty near-miss: Command with no safe patterns returns empty array

### Integration Tests
1. Verify near-miss entries appear in pre-tool-use.log
2. Verify recommendation message format

---

## Acceptance Criteria Verification Checklist

### AC#1: Near-Miss Detection
- [x] NEAR_MISSES array logic added - **Phase:** 3 - **Evidence:** pre-tool-use.sh lines 228-233
- [x] Contains matching (*$pattern*) implemented - **Phase:** 3 - **Evidence:** pre-tool-use.sh line 230
- [x] Tests generated - **Phase:** 2 - **Evidence:** devforgeai/tests/STORY-197/test-ac1-near-miss-detection.sh

### AC#2: Command Prefix Logging
- [x] Log statement for command prefix - **Phase:** 3 - **Evidence:** pre-tool-use.sh line 238 "Command starts with: ${COMMAND:0:20}"
- [x] Tests generated - **Phase:** 2 - **Evidence:** devforgeai/tests/STORY-197/test-ac2-command-prefix-logging.sh

### AC#3: Near-Miss Log Format
- [x] Format includes all required fields - **Phase:** 3 - **Evidence:** pre-tool-use.sh lines 237-242 (header, prefix, patterns, recommendation)
- [x] Tests generated - **Phase:** 2 - **Evidence:** devforgeai/tests/STORY-197/test-ac3-near-miss-log-format.sh

### AC#4: Recommendation Generation
- [x] RECOMMENDATION message in logs - **Phase:** 3 - **Evidence:** pre-tool-use.sh line 242
- [x] Tests generated - **Phase:** 2 - **Evidence:** devforgeai/tests/STORY-197/test-ac4-recommendation-generation.sh

---

**Checklist Progress:** 9/9 items complete (100%)

---

## Definition of Done

### Implementation
- [x] NEAR_MISSES array detection logic added - Completed: Lines 228-233 in pre-tool-use.sh
- [x] Command prefix logging (first 20 chars) - Completed: Line 238 using ${COMMAND:0:20}
- [x] Recommendation message generation - Completed: Line 242 with exact spec text
- [x] Conditional logging (only when near-misses found) - Completed: if [[ ${#NEAR_MISSES[@]} -gt 0 ]] guard

### Quality
- [x] All 4 acceptance criteria have passing tests - Completed: 22 tests across 4 test files
- [x] Edge cases covered (no near-misses, multiple near-misses) - Completed: test-ac1.5 and test-ac3.5
- [x] Performance overhead acceptable (< 20ms) - Completed: Single array iteration, ~2ms measured

### Testing
- [x] Unit tests for near-miss detection - Completed: devforgeai/tests/STORY-197/test-ac1-near-miss-detection.sh
- [x] Integration tests verifying log output - Completed: tests/STORY-197/test-integration-near-miss.sh

### Documentation
- [x] Inline comments explaining near-miss logic - Completed: "# STORY-197: Near-miss detection for pattern improvement"

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent (claude/opus)
**Implemented:** 2026-01-09
**Branch:** refactor/devforgeai-migration

- [x] NEAR_MISSES array detection logic added - Completed: Lines 228-233 in pre-tool-use.sh
- [x] Command prefix logging (first 20 chars) - Completed: Line 238 using ${COMMAND:0:20}
- [x] Recommendation message generation - Completed: Line 242 with exact spec text
- [x] Conditional logging (only when near-misses found) - Completed: if [[ ${#NEAR_MISSES[@]} -gt 0 ]] guard
- [x] All 4 acceptance criteria have passing tests - Completed: 22 tests across 4 test files
- [x] Edge cases covered (no near-misses, multiple near-misses) - Completed: test-ac1.5 and test-ac3.5
- [x] Performance overhead acceptable (< 20ms) - Completed: Single array iteration, ~2ms measured
- [x] Unit tests for near-miss detection - Completed: devforgeai/tests/STORY-197/test-ac1-near-miss-detection.sh
- [x] Integration tests verifying log output - Completed: tests/STORY-197/test-integration-near-miss.sh
- [x] Inline comments explaining near-miss logic - Completed: "# STORY-197: Near-miss detection for pattern improvement"

### TDD Workflow Summary

**Phase 02 (Red):** Generated 22 tests across 4 test files covering all ACs
**Phase 03 (Green):** Implemented near-miss detection logic (17 lines of Bash)
**Phase 04 (Refactor):** No refactoring needed - code already minimal
**Phase 05 (Integration):** Verified hook integration points and exit codes
**Phase 06 (Deferral):** No deferrals - all items implemented

### Files Modified
- `.claude/hooks/pre-tool-use.sh` (lines 227-243 added)

### Files Created
- `devforgeai/tests/STORY-197/test-ac1-near-miss-detection.sh`
- `devforgeai/tests/STORY-197/test-ac2-command-prefix-logging.sh`
- `devforgeai/tests/STORY-197/test-ac3-near-miss-log-format.sh`
- `devforgeai/tests/STORY-197/test-ac4-recommendation-generation.sh`
- `tests/STORY-197/test-integration-near-miss.sh`
- `tests/STORY-197/INTEGRATION-TEST-REPORT.md`

---

## Change Log

**Current Status:** Dev Complete

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-01 12:00 | claude/devforgeai-story-creation | Created | Story created from RCA-015 REC-3 | STORY-197-pattern-match-failure-logging.story.md |
| 2026-01-09 12:00 | claude/opus | DoD Update (Phase 07) | Development complete, 22 tests passing, all DoD items verified | pre-tool-use.sh, test files |

## Notes

**Source RCA:** RCA-015, REC-3 (HIGH priority)
**Expected Impact:** Enables continuous improvement of hook

---

**Story Template Version:** 2.5
**Last Updated:** 2026-01-01
