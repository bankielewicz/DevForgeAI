---
id: STORY-197
title: Log Pattern Match Failures for Continuous Improvement
type: enhancement
epic: EPIC-033-framework-enhancement-triage-q4-2025
sprint: Backlog
status: Backlog
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
- [ ] NEAR_MISSES array logic added - **Phase:** 3 - **Evidence:** pre-tool-use.sh diff
- [ ] Contains matching (*$pattern*) implemented - **Phase:** 3 - **Evidence:** code review

### AC#2: Command Prefix Logging
- [ ] Log statement for command prefix - **Phase:** 3 - **Evidence:** grep verification

### AC#3: Near-Miss Log Format
- [ ] Format includes all required fields - **Phase:** 5 - **Evidence:** log output

### AC#4: Recommendation Generation
- [ ] RECOMMENDATION message in logs - **Phase:** 5 - **Evidence:** log output

---

**Checklist Progress:** 0/5 items complete (0%)

---

## Definition of Done

### Implementation
- [ ] NEAR_MISSES array detection logic added
- [ ] Command prefix logging (first 20 chars)
- [ ] Recommendation message generation
- [ ] Conditional logging (only when near-misses found)

### Quality
- [ ] All 4 acceptance criteria have passing tests
- [ ] Edge cases covered (no near-misses, multiple near-misses)
- [ ] Performance overhead acceptable (< 20ms)

### Testing
- [ ] Unit tests for near-miss detection
- [ ] Integration tests verifying log output

### Documentation
- [ ] Inline comments explaining near-miss logic

---

## Change Log

**Current Status:** Backlog

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-01 12:00 | claude/devforgeai-story-creation | Created | Story created from RCA-015 REC-3 | STORY-197-pattern-match-failure-logging.story.md |

## Notes

**Source RCA:** RCA-015, REC-3 (HIGH priority)
**Expected Impact:** Enables continuous improvement of hook

---

**Story Template Version:** 2.5
**Last Updated:** 2026-01-01
