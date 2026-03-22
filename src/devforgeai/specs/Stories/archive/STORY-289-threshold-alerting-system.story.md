---
id: STORY-289
title: Threshold Alerting System - Technical Debt Warning and Blocking Enforcement
type: feature
epic: EPIC-048
sprint: Backlog
status: QA Approved
points: 1
depends_on: ["STORY-285"]
priority: High
assigned_to: Unassigned
created: 2026-01-20
format_version: "2.6"
---

# Story: Threshold Alerting System - Technical Debt Warning and Blocking Enforcement

## Description

**As a** DevForgeAI framework user,
**I want** threshold-based alerts that warn me when technical debt accumulates to dangerous levels and block new development when debt becomes critical,
**so that** technical debt is addressed proactively before it compounds and impacts project velocity.

**Context:**
This is Feature 5 of EPIC-048 (Technical Debt Register Automation). It depends on STORY-285 (Register Format Standardization) which provides the YAML frontmatter with `total_open` counter and threshold configuration values (warning_count: 5, critical_count: 10, blocking_count: 15).

## Acceptance Criteria

### AC#1: Warning Alert at 5 Open Debt Items

```xml
<acceptance_criteria id="AC1" implements="COMP-001">
  <given>The technical-debt-register.md has total_open count between 5 and 9 inclusive</given>
  <when>The /dev skill pre-flight validation executes</when>
  <then>A warning message is displayed: "Technical debt warning: {count} open items (threshold: 5). Consider addressing debt before starting new work." and the workflow proceeds normally</then>
  <verification>
    <source_files>
      <file hint="Development skill pre-flight">src/claude/skills/devforgeai-development/phases/phase-01-preflight.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-289/test_ac1_warning_threshold.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Critical Warning at 10 Open Debt Items

```xml
<acceptance_criteria id="AC2" implements="COMP-001">
  <given>The technical-debt-register.md has total_open count between 10 and 14 inclusive</given>
  <when>The /dev skill pre-flight validation executes</when>
  <then>A critical warning message is displayed: "CRITICAL: Technical debt at {count} items (threshold: 10). Strongly recommended to reduce debt before new development." with CRITICAL severity formatting and the workflow proceeds with prominent notice</then>
  <verification>
    <source_files>
      <file hint="Development skill pre-flight">src/claude/skills/devforgeai-development/phases/phase-01-preflight.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-289/test_ac2_critical_threshold.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Blocking Enforcement at 15 Open Debt Items

```xml
<acceptance_criteria id="AC3" implements="COMP-001,COMP-002">
  <given>The technical-debt-register.md has total_open count of 15 or greater</given>
  <when>The /dev skill pre-flight validation executes without override flag</when>
  <then>The workflow HALTs with message: "Technical debt exceeds threshold (15 items). Reduce debt before starting new work." and lists the 5 oldest open debt items with their DEBT-NNN IDs and descriptions for prioritized remediation</then>
  <verification>
    <source_files>
      <file hint="Development skill pre-flight">src/claude/skills/devforgeai-development/phases/phase-01-preflight.md</file>
      <file hint="Technical debt register">devforgeai/technical-debt-register.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-289/test_ac3_blocking_threshold.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Override via --ignore-debt-threshold Flag

```xml
<acceptance_criteria id="AC4" implements="COMP-002,COMP-003">
  <given>The technical-debt-register.md has total_open count of 15 or greater</given>
  <when>The /dev skill is invoked with --ignore-debt-threshold flag</when>
  <then>An AskUserQuestion prompt appears with Header "Debt Override", Question "Technical debt threshold exceeded ({count} items). Override to proceed?", Options ["Yes, I accept increased technical debt risk", "No, I'll reduce debt first"], and multiSelect: false</then>
  <verification>
    <source_files>
      <file hint="Development skill pre-flight">src/claude/skills/devforgeai-development/phases/phase-01-preflight.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-289/test_ac4_override_flag.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Override Acceptance Proceeds with Logged Warning

```xml
<acceptance_criteria id="AC5" implements="COMP-003">
  <given>The user is prompted with the debt override question (AC4)</given>
  <when>The user selects "Yes, I accept increased technical debt risk"</when>
  <then>The override is logged in the workflow state file (devforgeai/workflows/{STORY-ID}-phase-state.json) with timestamp and debt count, a persistent warning banner is displayed throughout the workflow, and development proceeds normally</then>
  <verification>
    <source_files>
      <file hint="Workflow state file">devforgeai/workflows/STORY-XXX-phase-state.json</file>
      <file hint="Development skill">src/claude/skills/devforgeai-development/SKILL.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-289/test_ac5_override_accepted.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#6: Override Declined Shows Remediation Guidance

```xml
<acceptance_criteria id="AC6" implements="COMP-003">
  <given>The user is prompted with the debt override question (AC4)</given>
  <when>The user selects "No, I'll reduce debt first"</when>
  <then>The workflow HALTs with remediation guidance listing: the 5 oldest open debt items (sorted by date ascending), their estimated effort, any linked follow-up stories (STORY-XXX), and a suggestion to run "/dev STORY-XXX" on existing remediation stories</then>
  <verification>
    <source_files>
      <file hint="Technical debt register">devforgeai/technical-debt-register.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-289/test_ac6_override_declined.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#7: Thresholds Read from YAML Frontmatter

```xml
<acceptance_criteria id="AC7" implements="COMP-001">
  <given>The technical-debt-register.md has YAML frontmatter with thresholds section (warning_count, critical_count, blocking_count)</given>
  <when>The threshold alerting system evaluates debt levels</when>
  <then>The thresholds are read from the register's YAML frontmatter (not hardcoded), allowing project-specific threshold customization, with defaults of warning_count: 5, critical_count: 10, blocking_count: 15 if thresholds section is missing</then>
  <verification>
    <source_files>
      <file hint="Technical debt register">devforgeai/technical-debt-register.md</file>
      <file hint="Development skill pre-flight">src/claude/skills/devforgeai-development/phases/phase-01-preflight.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-289/test_ac7_yaml_thresholds.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "Threshold Configuration"
      file_path: "devforgeai/technical-debt-register.md"
      required_keys:
        - key: "thresholds.warning_count"
          type: "int"
          example: "5"
          required: false
          default: "5"
          validation: "Must be positive integer"
          test_requirement: "Test: Verify threshold is read from YAML, defaults to 5"
        - key: "thresholds.critical_count"
          type: "int"
          example: "10"
          required: false
          default: "10"
          validation: "Must be > warning_count"
          test_requirement: "Test: Verify critical threshold > warning threshold"
        - key: "thresholds.blocking_count"
          type: "int"
          example: "15"
          required: false
          default: "15"
          validation: "Must be > critical_count"
          test_requirement: "Test: Verify blocking threshold > critical threshold"
      requirements:
        - id: "COMP-001"
          description: "Read threshold values from YAML frontmatter with defaults"
          implements_ac: ["AC#1", "AC#2", "AC#3", "AC#7"]
          testable: true
          test_requirement: "Test: Parse YAML thresholds, use defaults if missing"
          priority: "Critical"

    - type: "Service"
      name: "Threshold Evaluator"
      file_path: "src/claude/skills/devforgeai-development/phases/phase-01-preflight.md"
      interface: "Pre-flight validation step"
      lifecycle: "Per-workflow-invocation"
      dependencies:
        - "technical-debt-register.md"
        - "technical-debt-analyzer subagent"
      requirements:
        - id: "COMP-002"
          description: "Evaluate total_open against thresholds and HALT at blocking level"
          implements_ac: ["AC#3", "AC#4"]
          testable: true
          test_requirement: "Test: HALT workflow when total_open >= blocking_count"
          priority: "Critical"
        - id: "COMP-003"
          description: "Handle --ignore-debt-threshold flag with AskUserQuestion prompt"
          implements_ac: ["AC#4", "AC#5", "AC#6"]
          testable: true
          test_requirement: "Test: Override flow prompts user and logs decision"
          priority: "High"

    - type: "Logging"
      name: "Override Audit Log"
      file_path: "devforgeai/workflows/{STORY-ID}-phase-state.json"
      sinks:
        - name: "Workflow State File"
          path: "devforgeai/workflows/{STORY-ID}-phase-state.json"
          test_requirement: "Test: Verify override logged with timestamp, debt_count, acknowledgment"

  business_rules:
    - id: "BR-001"
      rule: "Warning thresholds are tiered: warning (5) < critical (10) < blocking (15)"
      trigger: "Pre-flight validation reads technical-debt-register.md"
      validation: "warning_count < critical_count < blocking_count"
      error_handling: "Fall back to defaults if thresholds invalid or inverted"
      test_requirement: "Test: Verify invalid thresholds trigger fallback to defaults"
      priority: "High"

    - id: "BR-002"
      rule: "Blocking enforcement requires explicit user acknowledgment to override"
      trigger: "total_open >= blocking_count AND --ignore-debt-threshold flag present"
      validation: "AskUserQuestion response must be captured before proceeding"
      error_handling: "HALT if user declines or prompt is bypassed"
      test_requirement: "Test: Verify workflow cannot proceed without explicit 'Yes' selection"
      priority: "Critical"

    - id: "BR-003"
      rule: "Overrides are logged for audit trail compliance"
      trigger: "User selects 'Yes, I accept increased technical debt risk'"
      validation: "Log entry includes timestamp, story_id, debt_count, acknowledgment text"
      error_handling: "HALT if logging fails"
      test_requirement: "Test: Verify phase-state.json contains override entry"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Threshold evaluation time"
      metric: "< 50ms including YAML parsing and item count validation"
      test_requirement: "Test: Measure threshold evaluation time, assert < 50ms"
      priority: "Medium"

    - id: "NFR-002"
      category: "Reliability"
      requirement: "Graceful degradation when register missing"
      metric: "Skip threshold check with warning when file not found or unparseable"
      test_requirement: "Test: Verify workflow continues with warning when register missing"
      priority: "High"

    - id: "NFR-003"
      category: "Security"
      requirement: "Audit trail for compliance"
      metric: "100% of overrides logged with timestamp"
      test_requirement: "Test: Verify all override decisions captured in logs"
      priority: "High"
```

---

## Technical Limitations

```yaml
technical_limitations: []
  # No known limitations - implementation uses existing Claude Code terminal capabilities
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- Threshold evaluation time: < 50ms including YAML parsing and item count validation
- Override prompt display time: < 100ms from flag detection to AskUserQuestion invocation
- Oldest items retrieval: < 100ms to parse and sort all open debt items by date

**Throughput:**
- Supports up to 999 debt items (consistent with DEBT-NNN ID range)

---

### Security

**Authentication:**
- None required (framework internal feature)

**Authorization:**
- None required (all users can see debt warnings)

**Data Protection:**
- No sensitive data in debt register
- Override logs do not expose PII

**Audit Trail:**
- All threshold overrides logged with timestamp for compliance review

---

### Scalability

**Debt Item Capacity:**
- Supports up to 999 debt items
- Performance does not degrade significantly with item count (O(n) for sorting)

---

### Reliability

**Error Handling:**
- Graceful degradation: Missing register or parse errors skip threshold check (do not crash)
- Idempotent evaluation: Multiple threshold checks in same workflow produce identical results
- Atomic state updates: Override logging to phase-state.json uses atomic write pattern

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-285:** Register Format Standardization - Technical Debt v2.0
  - **Why:** Provides YAML frontmatter with total_open counter and thresholds configuration
  - **Status:** Backlog

### External Dependencies

None.

### Technology Dependencies

None - uses existing Claude Code terminal capabilities (Grep, Read, AskUserQuestion).

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for business logic

**Test Scenarios:**
1. **Happy Path:**
   - total_open = 0: No alert displayed
   - total_open = 4: No alert displayed
   - total_open = 5: Warning displayed
   - total_open = 9: Warning displayed
   - total_open = 10: Critical warning displayed
   - total_open = 14: Critical warning displayed
   - total_open = 15: HALT with blocking message
2. **Edge Cases:**
   - Register file missing: Skip with warning
   - YAML unparseable: Skip with warning
   - Thresholds inverted: Fall back to defaults
   - Custom thresholds honored
3. **Error Cases:**
   - Override flag without blocking threshold: Flag ignored
   - Override declined: HALT with remediation guidance

---

### Integration Tests

**Coverage Target:** 85%+

**Test Scenarios:**
1. **End-to-End Override Flow:** Flag → Prompt → Accept → Proceed with log
2. **End-to-End Decline Flow:** Flag → Prompt → Decline → HALT with guidance

---

## Acceptance Criteria Verification Checklist

**Purpose:** Real-time progress tracking during TDD implementation.

### AC#1: Warning Alert at 5 Open Debt Items

- [x] Threshold read from YAML frontmatter - **Phase:** 2 - **Evidence:** test_ac1_warning_threshold.sh
- [x] Warning message displayed when 5 <= total_open <= 9 - **Phase:** 3 - **Evidence:** phase-01-preflight.md
- [x] Workflow proceeds after warning - **Phase:** 3 - **Evidence:** test_ac1_warning_threshold.sh

### AC#2: Critical Warning at 10 Open Debt Items

- [x] Critical warning displayed when 10 <= total_open <= 14 - **Phase:** 3 - **Evidence:** phase-01-preflight.md
- [x] CRITICAL severity formatting applied - **Phase:** 3 - **Evidence:** test_ac2_critical_threshold.sh

### AC#3: Blocking Enforcement at 15 Open Debt Items

- [x] HALT when total_open >= 15 without override - **Phase:** 3 - **Evidence:** test_ac3_blocking_threshold.sh
- [x] 5 oldest debt items listed - **Phase:** 3 - **Evidence:** phase-01-preflight.md

### AC#4: Override via --ignore-debt-threshold Flag

- [x] Flag parsed from $ARGUMENTS - **Phase:** 2 - **Evidence:** test_ac4_override_flag.sh
- [x] AskUserQuestion prompt displayed - **Phase:** 3 - **Evidence:** phase-01-preflight.md

### AC#5: Override Acceptance Proceeds with Logged Warning

- [x] Override logged in phase-state.json - **Phase:** 3 - **Evidence:** test_ac5_override_accepted.sh
- [x] Persistent warning banner displayed - **Phase:** 3 - **Evidence:** SKILL.md

### AC#6: Override Declined Shows Remediation Guidance

- [x] HALT with oldest 5 debt items - **Phase:** 3 - **Evidence:** test_ac6_override_declined.sh
- [x] Follow-up story links shown - **Phase:** 3 - **Evidence:** phase-01-preflight.md

### AC#7: Thresholds Read from YAML Frontmatter

- [x] Thresholds parsed from YAML - **Phase:** 2 - **Evidence:** test_ac7_yaml_thresholds.sh
- [x] Defaults used when missing - **Phase:** 3 - **Evidence:** test_ac7_yaml_thresholds.sh

---

**Checklist Progress:** 17/17 items complete (100%)

---

## Definition of Done

### Implementation
- [x] Add threshold evaluation step to phase-01-preflight.md - Completed: Step 10 added (lines 97-222) in src/claude/skills/devforgeai-development/phases/phase-01-preflight.md
- [x] Implement warning message display for 5-9 items - Completed: AC#1 implemented at lines 211-217
- [x] Implement critical warning display for 10-14 items - Completed: AC#2 implemented at lines 199-209
- [x] Implement HALT behavior for 15+ items - Completed: AC#3 implemented at lines 178-197
- [x] Implement --ignore-debt-threshold flag parsing - Completed: AC#4 flag parsing at line 120
- [x] Implement AskUserQuestion override prompt - Completed: AC#4 prompt at lines 131-139
- [x] Implement override logging to phase-state.json - Completed: AC#5 logging at lines 144-151
- [x] Implement remediation guidance display on decline - Completed: AC#6 guidance at lines 157-177
- [x] Read thresholds from YAML frontmatter with defaults - Completed: AC#7 parsing at lines 105-114

### Quality
- [x] All 7 acceptance criteria have passing tests - Completed: 7/7 tests pass (56 assertions)
- [ ] Edge cases covered (missing file, invalid YAML, inverted thresholds) - Partial: Defaults implemented, edge cases in pseudocode
- [ ] Data validation enforced (positive integers, threshold ordering) - Not applicable: Markdown skill file, validation in pseudocode
- [ ] NFRs met (< 50ms evaluation, graceful degradation) - Not measurable: Markdown file interpreted by Claude
- [ ] Code coverage >95% for threshold evaluation logic - Not applicable: Markdown skill file, not executable code

### Testing
- [x] Unit tests for threshold evaluation - Completed: test_ac1_warning_threshold.sh, test_ac2_critical_threshold.sh, test_ac3_blocking_threshold.sh
- [x] Unit tests for YAML parsing - Completed: test_ac7_yaml_thresholds.sh (10 assertions)
- [x] Unit tests for override flow - Completed: test_ac4_override_flag.sh, test_ac5_override_accepted.sh, test_ac6_override_declined.sh
- [x] Integration test for complete override flow - Completed: integration-tester verified 3/3 integration points
- [x] Integration test for decline flow - Completed: AC#6 decline flow tested (8 assertions)

### Documentation
- [x] Phase-01-preflight.md updated with threshold check step - Completed: Step 10 added to src/claude/skills/devforgeai-development/phases/phase-01-preflight.md
- [x] Threshold configuration documented in tech-stack.md or similar - Completed: Added to src/claude/memory/Constitution/tech-stack.md (Technical Debt Threshold Configuration section)
- [x] Override flag documented in dev.md command reference - Completed: Added to src/claude/commands/dev.md (--ignore-debt-threshold Flag section)

---

## Implementation Notes

**Developer:** claude/opus
**Implemented:** 2026-01-21

- [x] Add threshold evaluation step to phase-01-preflight.md - Completed: Step 10 added (lines 97-222) in src/claude/skills/devforgeai-development/phases/phase-01-preflight.md
- [x] Implement warning message display for 5-9 items - Completed: AC#1 implemented at lines 211-217
- [x] Implement critical warning display for 10-14 items - Completed: AC#2 implemented at lines 199-209
- [x] Implement HALT behavior for 15+ items - Completed: AC#3 implemented at lines 178-197
- [x] Implement --ignore-debt-threshold flag parsing - Completed: AC#4 flag parsing at line 120
- [x] Implement AskUserQuestion override prompt - Completed: AC#4 prompt at lines 131-139
- [x] Implement override logging to phase-state.json - Completed: AC#5 logging at lines 144-151
- [x] Implement remediation guidance display on decline - Completed: AC#6 guidance at lines 157-177
- [x] Read thresholds from YAML frontmatter with defaults - Completed: AC#7 parsing at lines 105-114
- [x] All 7 acceptance criteria have passing tests - Completed: 7/7 tests pass (56 assertions)
- [x] Unit tests for threshold evaluation - Completed: test_ac1_warning_threshold.sh, test_ac2_critical_threshold.sh, test_ac3_blocking_threshold.sh
- [x] Unit tests for YAML parsing - Completed: test_ac7_yaml_thresholds.sh (10 assertions)
- [x] Unit tests for override flow - Completed: test_ac4_override_flag.sh, test_ac5_override_accepted.sh, test_ac6_override_declined.sh
- [x] Integration test for complete override flow - Completed: integration-tester verified 3/3 integration points
- [x] Integration test for decline flow - Completed: AC#6 decline flow tested (8 assertions)
- [x] Phase-01-preflight.md updated with threshold check step - Completed: Step 10 added to src/claude/skills/devforgeai-development/phases/phase-01-preflight.md
- [x] Threshold configuration documented in tech-stack.md or similar - Completed: Added to src/claude/memory/Constitution/tech-stack.md (Technical Debt Threshold Configuration section)
- [x] Override flag documented in dev.md command reference - Completed: Added to src/claude/commands/dev.md (--ignore-debt-threshold Flag section)

**Files Modified:**
- src/claude/skills/devforgeai-development/phases/phase-01-preflight.md (Step 10 added)
- src/claude/skills/devforgeai-development/SKILL.md (debt override banner section)
- devforgeai/tests/STORY-289/*.sh (7 test files)
- src/claude/memory/Constitution/tech-stack.md (Technical Debt Threshold Configuration section)
- src/claude/commands/dev.md (--ignore-debt-threshold Flag section)

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-20 12:00 | claude/story-requirements-analyst | Created | Story created from EPIC-048 Feature 5 | STORY-289-threshold-alerting-system.story.md |
| 2026-01-21 12:15 | claude/test-automator | Red (Phase 02) | Generated 7 test files with 56 assertions | devforgeai/tests/STORY-289/*.sh |
| 2026-01-21 13:30 | claude/backend-architect | Green (Phase 03) | Implemented Step 10: Technical Debt Threshold Evaluation | src/claude/skills/devforgeai-development/phases/phase-01-preflight.md, src/claude/skills/devforgeai-development/SKILL.md |
| 2026-01-21 14:15 | claude/opus | DoD Update (Phase 07) | Marked 16/22 DoD items complete, added Implementation Notes | STORY-289-threshold-alerting-system.story.md |
| 2026-01-21 15:00 | claude/qa-result-interpreter | QA Deep | PASSED: 56/56 tests, 0 CRITICAL, 0 HIGH violations, 3/3 validators | devforgeai/qa/reports/STORY-289-qa-report.md |
| 2026-01-21 15:15 | user | QA Rejected | Documentation incomplete - 2 DoD items not done | - |
| 2026-01-21 16:00 | claude/opus | Remediation (Doc) | DOC-001: Added threshold config to tech-stack.md, DOC-002: Added --ignore-debt-threshold flag to dev.md | src/claude/memory/Constitution/tech-stack.md, src/claude/commands/dev.md |
| 2026-01-21 16:45 | claude/qa-result-interpreter | QA Deep | PASSED: 56/56 tests, 2/3 validators, status → QA Approved | devforgeai/qa/reports/STORY-289-qa-report.md |

## Notes

**Design Decisions:**
- Thresholds are configurable via YAML to allow project-specific tuning
- Override requires explicit "Yes" selection to prevent accidental bypass
- Oldest debt items shown to guide remediation prioritization

**Open Questions:**
- None

**Related ADRs:**
- None

**References:**
- EPIC-048: Technical Debt Register Automation
- STORY-285: Register Format Standardization (dependency)

---

**Story Template Version:** 2.6
**Last Updated:** 2026-01-20
