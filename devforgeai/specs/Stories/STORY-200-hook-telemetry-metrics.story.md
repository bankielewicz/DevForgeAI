---
id: STORY-200
title: Add Telemetry for Hook Performance Metrics
type: feature
epic: EPIC-033-framework-enhancement-triage-q4-2025
sprint: Backlog
status: Backlog
points: 2
depends_on: ["STORY-195", "STORY-197"]
priority: Low
assigned_to: Unassigned
created: 2026-01-01
source_rca: RCA-015
source_recommendation: REC-6
format_version: "2.5"
---

# Story: Add Telemetry for Hook Performance Metrics

## Description

**As a** DevForgeAI framework maintainer,
**I want** a script that generates weekly hook effectiveness reports,
**so that** I can track approval rate trends and identify when the hook needs updating.

**Context from RCA-015:**
Currently there is no visibility into hook effectiveness over time. Adding telemetry will enable tracking of improvement (approval rate should increase as patterns added), identification of degradation, and celebration of wins (approval rate >90% = good).

## Acceptance Criteria

### AC#1: Total Invocation Count

**Given** the pre-tool-use.log file
**When** the telemetry script runs
**Then** total hook invocations are counted and displayed

---

### AC#2: Auto-Approval Count

**Given** the pre-tool-use.log file
**When** the telemetry script runs
**Then** auto-approved commands (containing "AUTO-APPROVE") are counted

---

### AC#3: Blocked Count

**Given** the pre-tool-use.log file
**When** the telemetry script runs
**Then** blocked commands (containing "BLOCK") are counted

---

### AC#4: Approval Rate Calculation

**Given** auto-approved and total counts
**When** the telemetry script runs
**Then** approval rate is calculated: auto-approved / total × 100%

---

### AC#5: Top Unknown Patterns Report

**Given** the hook-unknown-commands.log file
**When** the telemetry script runs
**Then** top 10 unknown patterns are displayed for pattern addition candidates

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "hook-telemetry.sh"
      file_path: "devforgeai/scripts/hook-telemetry.sh"
      interface: "Bash Script"
      lifecycle: "On-demand execution (weekly)"
      dependencies: []
      requirements:
        - id: "SVC-001"
          description: "Count total hook invocations (wc -l pre-tool-use.log)"
          testable: true
          test_requirement: "Test: Script outputs 'Total invocations: N'"
          priority: "High"
        - id: "SVC-002"
          description: "Count auto-approved (grep 'AUTO-APPROVE' | wc -l)"
          testable: true
          test_requirement: "Test: Script outputs 'Auto-approved: N'"
          priority: "High"
        - id: "SVC-003"
          description: "Count blocked (grep 'BLOCK' | wc -l)"
          testable: true
          test_requirement: "Test: Script outputs 'Blocked: N'"
          priority: "High"
        - id: "SVC-004"
          description: "Count manual approval (grep 'ASK USER' | wc -l)"
          testable: true
          test_requirement: "Test: Script outputs 'Manual approval: N'"
          priority: "Medium"
        - id: "SVC-005"
          description: "Calculate approval rate percentage"
          testable: true
          test_requirement: "Test: Script outputs 'Approval rate: N.N%'"
          priority: "Critical"
        - id: "SVC-006"
          description: "Display top 10 unknown patterns"
          testable: true
          test_requirement: "Test: Script outputs top 10 unknown command prefixes"
          priority: "Medium"

  business_rules:
    - id: "BR-001"
      rule: "Approval rate target is >90%"
      trigger: "Telemetry report generation"
      validation: "Display warning if approval rate < 90%"
      error_handling: "Display 'WARNING: Approval rate below target'"
      test_requirement: "Test: Warning displayed when rate < 90%"
      priority: "Medium"

    - id: "BR-002"
      rule: "Handle missing log files gracefully"
      trigger: "Log file not found"
      validation: "Script exits with informative message"
      error_handling: "Display 'Log file not found: {path}'"
      test_requirement: "Test: Script handles missing log without crash"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Generate report in < 10 seconds for 100,000 log entries"
      metric: "< 10 seconds for large log files"
      test_requirement: "Test: Time script execution on large log"
      priority: "Low"
```

---

## Technical Limitations

```yaml
technical_limitations: []
```

---

## Non-Functional Requirements (NFRs)

### Performance
- Report generation: < 10 seconds for 100,000 log entries
- Memory efficient (streaming grep, not loading entire file)

### Reliability
- Handle missing log files gracefully
- Handle empty log files gracefully

---

## Dependencies

### Prerequisite Stories
- [ ] **STORY-195:** Add Common Command Composition Patterns
  - **Why:** Hook must be generating logs for telemetry to analyze
  - **Status:** Backlog

- [ ] **STORY-197:** Log Pattern Match Failures
  - **Why:** Near-miss logging enhances telemetry data
  - **Status:** Backlog

---

## Test Strategy

### Unit Tests
1. Test total count: Sample log with known line count
2. Test auto-approve count: Sample log with known markers
3. Test blocked count: Sample log with BLOCK markers
4. Test rate calculation: 50 auto-approve / 100 total = 50%

### Integration Tests
1. Run against actual pre-tool-use.log
2. Verify output format matches specification

---

## Acceptance Criteria Verification Checklist

### AC#1: Total Invocation Count
- [x] wc -l count implemented - **Phase:** 3 - **Evidence:** hook-telemetry.sh line 55
- [ ] Output format correct - **Phase:** 5 - **Evidence:** script output

### AC#2: Auto-Approval Count
- [x] grep AUTO-APPROVE implemented - **Phase:** 3 - **Evidence:** hook-telemetry.sh line 61
- [ ] Output format correct - **Phase:** 5 - **Evidence:** script output

### AC#3: Blocked Count
- [x] grep BLOCK implemented - **Phase:** 3 - **Evidence:** hook-telemetry.sh line 66

### AC#4: Approval Rate Calculation
- [x] Rate calculation formula - **Phase:** 3 - **Evidence:** hook-telemetry.sh line 78
- [ ] Percentage displayed - **Phase:** 5 - **Evidence:** script output

### AC#5: Top Unknown Patterns Report
- [x] Unknown patterns extraction - **Phase:** 3 - **Evidence:** hook-telemetry.sh lines 122-144
- [ ] Top 10 display - **Phase:** 5 - **Evidence:** script output

---

**Checklist Progress:** 5/9 items complete (55%)

---

## Definition of Done

### Implementation
- [ ] hook-telemetry.sh created at devforgeai/scripts/
- [ ] Total invocation count
- [ ] Auto-approved count
- [ ] Blocked count
- [ ] Manual approval count
- [ ] Approval rate calculation with percentage
- [ ] Top 10 unknown patterns
- [ ] Warning when rate < 90%

### Quality
- [ ] All 5 acceptance criteria have passing tests
- [ ] Edge cases covered (empty logs, missing files)
- [ ] Rate calculation accurate

### Testing
- [ ] Unit tests for each metric
- [ ] Integration test with sample logs

### Documentation
- [ ] Script header with usage instructions
- [ ] Output format documented

---

## Change Log

**Current Status:** Backlog

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-01 12:00 | claude/devforgeai-story-creation | Created | Story created from RCA-015 REC-6 | STORY-200-hook-telemetry-metrics.story.md |

## Notes

**Source RCA:** RCA-015, REC-6 (LOW priority)
**Expected Impact:** Metrics visibility, continuous improvement tracking

**Usage:**
```bash
bash devforgeai/scripts/hook-telemetry.sh
# Generates weekly effectiveness report
```

**Sample Output:**
```
=== Hook Telemetry Report ===
Date: 2026-01-01

Total invocations: 35,042
Auto-approved: 31,525
Blocked: 0
Manual approval: 3,517

Approval rate: 89.9%
⚠️ WARNING: Approval rate below 90% target

Top 10 unknown patterns:
  1. cd /mnt (55 occurrences)
  2. python3 -c (14 occurrences)
  ...
```

---

**Story Template Version:** 2.5
**Last Updated:** 2026-01-01
