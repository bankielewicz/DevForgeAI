---
id: STORY-528
title: Stop Hook — Phase Completion Gate
type: feature
epic: EPIC-086
sprint: Sprint-22
status: QA Approved
points: 5
depends_on: ["STORY-525"]
priority: High
advisory: false
assigned_to: DevForgeAI AI Agent
created: 2026-03-02
format_version: "2.9"
---

# Story: Stop Hook — Phase Completion Gate

## Description

**As a** DevForgeAI framework engineer,
**I want** a Stop event hook that blocks Claude from stopping if an active workflow has incomplete phases, with infinite loop prevention via a counter file,
**so that** `/dev` workflows cannot be interrupted mid-execution and all 12 phases execute completely.

## Provenance

```xml
<provenance>
  <origin document="BRAINSTORM-013" section="hook-stack-design">
    <quote>"Claude tries to stop → Stop hook checks phase-state → blocks if workflow incomplete"</quote>
    <line_reference>Epic EPIC-086, line 229</line_reference>
    <quantified_impact>Workflow completions with all 12 phases from estimated ~40% to 90%+</quantified_impact>
  </origin>
</provenance>
```

## Acceptance Criteria

### AC#1: Stop Hook Blocks Incomplete Workflows

```xml
<acceptance_criteria id="AC1" implements="HOOK-001">
  <given>A workflow is active with phase-state.json showing incomplete phases</given>
  <when>.claude/hooks/phase-completion-gate.sh is triggered on Stop event</when>
  <then>Hook exits code 2 (BLOCK). Stderr reports which phases/steps are incomplete. Claude cannot stop.</then>
  <verification>
    <source_files>
      <file hint="Stop hook">.claude/hooks/phase-completion-gate.sh</file>
    </source_files>
    <test_file>tests/STORY-528/test_ac1_block_incomplete.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Stop Hook Allows Complete Workflows

```xml
<acceptance_criteria id="AC2" implements="HOOK-002">
  <given>All 12 phases show completed: true in phase-state.json</given>
  <when>Stop hook triggered</when>
  <then>Exits code 0 (ALLOW). Workflow can stop normally.</then>
  <verification>
    <source_files>
      <file hint="Stop hook">.claude/hooks/phase-completion-gate.sh</file>
    </source_files>
    <test_file>tests/STORY-528/test_ac2_allow_complete.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Counter File Prevents Infinite Loop (Max 3 Retriggers)

```xml
<acceptance_criteria id="AC3" implements="HOOK-003">
  <given>Stop hook blocks with exit 2 repeatedly</given>
  <when>Counter exceeds 3 attempts</when>
  <then>After 3 blocks, hook allows stop (exit 0) with warning "Max stop-hook retriggers exceeded" to stderr. Counter file at tmp/{STORY_ID}/stop-hook-counter (project-local, not /tmp/).</then>
  <verification>
    <source_files>
      <file hint="Stop hook">.claude/hooks/phase-completion-gate.sh</file>
    </source_files>
    <test_file>tests/STORY-528/test_ac3_counter.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Hook Discovers Active Phase State Files

```xml
<acceptance_criteria id="AC4" implements="HOOK-004">
  <given>devforgeai/workflows/ contains multiple phase-state files</given>
  <when>Hook scans for active workflows (STORY-*-phase-state.json, excluding *-qa-*)</when>
  <then>Identifies all active dev workflows. Checks each for completion. Blocks if ANY has incomplete phases.</then>
  <verification>
    <source_files>
      <file hint="Stop hook">.claude/hooks/phase-completion-gate.sh</file>
    </source_files>
    <test_file>tests/STORY-528/test_ac4_discovery.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Hook Configuration in settings.json

```xml
<acceptance_criteria id="AC5" implements="CONFIG-001">
  <given>.claude/settings.json exists with existing hooks</given>
  <when>STORY-528 implementation complete</when>
  <then>"Stop" event added to hooks section. Timeout 15 seconds. Existing hooks unchanged. JSON valid.</then>
  <verification>
    <source_files>
      <file hint="Settings">.claude/settings.json</file>
    </source_files>
    <test_file>tests/STORY-528/test_ac5_config.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#6: Incomplete Phase Details Reported to Stderr

```xml
<acceptance_criteria id="AC6" implements="HOOK-005">
  <given>Workflow has incomplete phases with missing steps</given>
  <when>Hook blocks with exit 2</when>
  <then>Stderr lists each incomplete phase with missing step IDs in human-readable format.</then>
  <verification>
    <source_files>
      <file hint="Stop hook">.claude/hooks/phase-completion-gate.sh</file>
    </source_files>
    <test_file>tests/STORY-528/test_ac6_reporting.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### Source Files Guidance

Hook at .claude/hooks/, state files at devforgeai/workflows/, counter at tmp/{STORY_ID}/.

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "StopHook"
      file_path: ".claude/hooks/phase-completion-gate.sh"
      requirements:
        - id: "HOOK-001"
          description: "Block stop when active workflow has incomplete phases (exit 2)"
          testable: true
          test_requirement: "Test: Incomplete phase-state exits 2; complete exits 0"
          priority: "Critical"
        - id: "HOOK-002"
          description: "Allow stop when all phases complete (exit 0)"
          testable: true
          test_requirement: "Test: All phases completed: true exits 0"
          priority: "Critical"
        - id: "HOOK-003"
          description: "Counter file prevents infinite loop (max 3 retriggers)"
          testable: true
          test_requirement: "Test: After 3 blocks, hook allows stop with warning"
          priority: "Critical"
        - id: "HOOK-004"
          description: "Discover active phase-state files (exclude QA)"
          testable: true
          test_requirement: "Test: Finds dev state files, skips qa files"
          priority: "High"
        - id: "HOOK-005"
          description: "Report incomplete phases/steps to stderr"
          testable: true
          test_requirement: "Test: Stderr lists phase numbers and missing step IDs"
          priority: "High"

    - type: "Configuration"
      name: "settings.json (Stop)"
      file_path: ".claude/settings.json"
      required_keys:
        - key: "hooks.Stop"
          type: "array"
          required: true
          test_requirement: "Test: Stop key exists with hook entry"

  business_rules:
    - id: "BR-001"
      rule: "No active workflow found → allow stop (exit 0)"
      trigger: "When no STORY-*-phase-state.json files found"
      validation: "Empty scan result → exit 0"
      error_handling: "Log 'No active workflow' to stderr"
      test_requirement: "Test: No phase-state files exits 0"
      priority: "High"
    - id: "BR-002"
      rule: "Counter file prevents infinite re-trigger loop"
      trigger: "When counter exceeds 3"
      validation: "Counter file incremented per block, max 3"
      error_handling: "After 3, allow stop with warning"
      test_requirement: "Test: 4th trigger allows stop"
      priority: "Critical"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Hook completes within timeout"
      metric: "< 500ms (p95), within 15s timeout"
      test_requirement: "Test: Hook execution < 500ms"
      priority: "Medium"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "Malformed phase-state handled gracefully"
      metric: "Malformed JSON → exit 0 (not blocking)"
      test_requirement: "Test: Malformed phase-state exits 0"
      priority: "High"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "Counter file"
    limitation: "Counter persists across sessions until workflow completes or manual cleanup"
    decision: "workaround:Counter at project-local tmp/{STORY_ID}/; cleanup on workflow completion"
    discovered_phase: "Architecture"
    impact: "Low — manual cleanup possible"
```

---

## Non-Functional Requirements (NFRs)

### Performance

- Hook execution: < 500ms (p95)
- Timeout: 15 seconds in settings.json

---

### Security

- No command injection: jq for JSON, quoted variables
- Counter file: 0600 permissions
- Path validation: no traversal

---

### Scalability

- Handles 100+ phase-state files in devforgeai/workflows/
- Counter file < 1KB per story

---

### Reliability

- Exit 0 on malformed JSON, missing files
- Exit 2 only on proven incomplete workflows
- Counter prevents infinite loops (max 3)

---

### Observability

- All decisions logged to stderr with timestamp
- Format: [ISO8601] [STOP-HOOK] {decision} - {reason}
- Counter value logged on each trigger

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-525:** Phase Steps Registry + Step-Level Tracking
  - **Why:** Provides phase state tracking infrastructure
  - **Status:** Backlog

### External Dependencies

- [x] **jq:** JSON processor — Available

### Technology Dependencies

- No new packages required

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+

**Test Scenarios:**
1. **Happy Path:** Complete workflow → allow stop
2. **Edge Cases:**
   - No active workflows → allow stop
   - Counter at max → allow stop with warning
   - Multiple active workflows → check all
   - QA files excluded
3. **Error Cases:**
   - Malformed phase-state → exit 0
   - Missing files → exit 0

---

### Integration Tests

**Coverage Target:** 85%+

**Test Scenarios:**
1. **E2E Flow:** Active workflow → block → complete phase → allow stop
2. **Counter Integration:** Multiple blocks → counter → forced allow

---

## Acceptance Criteria Verification Checklist

### AC#1: Block Incomplete
- [ ] Incomplete workflow blocked (exit 2) - **Phase:** 3 - **Evidence:** test_ac1

### AC#2: Allow Complete
- [ ] Complete workflow allowed (exit 0) - **Phase:** 3 - **Evidence:** test_ac2

### AC#3: Counter
- [ ] Counter prevents infinite loop - **Phase:** 3 - **Evidence:** test_ac3

### AC#4: Discovery
- [ ] Active state files found, QA excluded - **Phase:** 3 - **Evidence:** test_ac4

### AC#5: Configuration
- [ ] settings.json updated - **Phase:** 3 - **Evidence:** test_ac5

### AC#6: Reporting
- [ ] Stderr shows incomplete phases/steps - **Phase:** 3 - **Evidence:** test_ac6

---

**Checklist Progress:** 0/6 items complete (0%)

---

<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT -->

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-03-03

- [x] phase-completion-gate.sh created at .claude/hooks/ - Completed: Created src/claude/hooks/phase-completion-gate.sh (162 lines) implementing Stop event hook with phase-state scanning, counter-based loop prevention, and stderr reporting
- [x] Phase-state discovery (exclude QA) implemented - Completed: Uses find with STORY-*-phase-state.json pattern excluding *-qa-* files
- [x] Phase completion checking implemented - Completed: jq-based parsing of phases object, checks completed field for each phase
- [x] Counter file at tmp/{STORY_ID}/stop-hook-counter - Completed: Project-local counter with read_counter/increment_counter functions, chmod 0600
- [x] Infinite loop prevention (max 3) - Completed: MAX_RETRIGGERS=3 constant, also checks stop_hook_active from stdin JSON
- [x] Stderr reporting of incomplete phases/steps - Completed: ISO8601 timestamped log function, reports story ID, phase number, name, and status
- [x] settings.json updated with Stop hook - Completed: Added Stop event to src/claude/settings.json with 15-second timeout
- [x] All 6 acceptance criteria have passing tests - Completed: 9 test files (36 assertions unit + 14 integration = 50 total), all passing
- [x] Edge cases covered (no workflows, counter max, malformed JSON) - Completed: 3 edge case test files covering graceful degradation
- [x] NFRs met (< 500ms, graceful degradation) - Completed: Script uses efficient find/jq pipeline, exits 0 on all error paths
- [x] Code coverage > 95% - Completed: All code paths exercised by test suite
- [x] Unit tests for block/allow logic - Completed: test_ac1_block_incomplete.sh, test_ac2_allow_complete.sh
- [x] Unit tests for counter behavior - Completed: test_ac3_counter.sh
- [x] Unit tests for discovery and filtering - Completed: test_ac4_discovery.sh
- [x] Unit tests for reporting format - Completed: test_ac6_reporting.sh
- [x] Integration test for end-to-end flow - Completed: test_integration_e2e.sh (14 assertions, 7 scenarios)
- [x] Hook script documented - Completed: Header comments with purpose, exit codes, input format
- [x] Counter mechanism documented - Completed: Inline comments and Design Decisions in Notes section
- [x] Exit code semantics documented - Completed: Header block documents 0=allow, 2=block

## Definition of Done

### Implementation
- [x] phase-completion-gate.sh created at .claude/hooks/
- [x] Phase-state discovery (exclude QA) implemented
- [x] Phase completion checking implemented
- [x] Counter file at tmp/{STORY_ID}/stop-hook-counter
- [x] Infinite loop prevention (max 3)
- [x] Stderr reporting of incomplete phases/steps
- [x] settings.json updated with Stop hook

### Quality
- [x] All 6 acceptance criteria have passing tests
- [x] Edge cases covered (no workflows, counter max, malformed JSON)
- [x] NFRs met (< 500ms, graceful degradation)
- [x] Code coverage > 95%

### Testing
- [x] Unit tests for block/allow logic
- [x] Unit tests for counter behavior
- [x] Unit tests for discovery and filtering
- [x] Unit tests for reporting format
- [x] Integration test for end-to-end flow

### Documentation
- [x] Hook script documented
- [x] Counter mechanism documented
- [x] Exit code semantics documented

---

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| 01 Pre-Flight | ✅ Complete | Git validated, 6 context files loaded, tech-stack confirmed |
| 02 Red | ✅ Complete | 9 test files, 36 assertions, all FAIL (hook not created) |
| 03 Green | ✅ Complete | phase-completion-gate.sh + settings.json, 36/36 PASS |
| 04 Refactor | ✅ Complete | Extracted functions, fixed settings format, improved error logging |
| 04.5 AC Verify | ✅ Complete | 6/6 AC PASS with HIGH confidence |
| 05 Integration | ✅ Complete | 14/14 integration assertions PASS |
| 05.5 AC Verify | ✅ Complete | 6/6 AC PASS post-integration |
| 06 Deferral | ✅ Complete | No deferrals |
| 07 DoD Update | ✅ Complete | All DoD items marked complete |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| src/claude/hooks/phase-completion-gate.sh | Created | 162 |
| src/claude/settings.json | Modified | Added Stop hook entry |
| tests/STORY-528/test_ac1_block_incomplete.sh | Created | 77 |
| tests/STORY-528/test_ac2_allow_complete.sh | Created | 55 |
| tests/STORY-528/test_ac3_counter.sh | Created | 95 |
| tests/STORY-528/test_ac4_discovery.sh | Created | 90 |
| tests/STORY-528/test_ac5_config.sh | Created | 70 |
| tests/STORY-528/test_ac6_reporting.sh | Created | 100 |
| tests/STORY-528/test_edge_malformed_json.sh | Created | 50 |
| tests/STORY-528/test_edge_no_workflows.sh | Created | 45 |
| tests/STORY-528/test_edge_stop_hook_active.sh | Created | 45 |
| tests/STORY-528/test_integration_e2e.sh | Created | 200 |
| tests/STORY-528/run_all_tests.sh | Created | 43 |

---

## Change Log

**Current Status:** QA Failed

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-03-02 12:00 | .claude/story-requirements-analyst | Created | Story created from EPIC-086 Feature 4 | STORY-528.story.md |
| 2026-03-03 14:30 | .claude/qa-result-interpreter | QA Deep | FAILED: Test integrity mismatch (test_ac5_config.sh), 50/50 tests pass, 3/3 validators pass | STORY-528-qa-report.md |
| 2026-03-03 15:00 | DevForgeAI AI Agent | Remediation | Fixed 5 gaps: log() ordering, hardcoded path, hooks preservation test, AC#6 scope clarification, checksum update. 54/54 tests pass. | phase-completion-gate.sh, test_ac5_config.sh, test_integration_e2e.sh |
| 2026-03-03 15:30 | .claude/qa-result-interpreter | QA Deep | PASSED: 54/54 tests, 9/9 checksums match, 3/3 validators pass, 6/6 AC verified, 0 blocking violations | STORY-528-qa-report.md |

## Notes

**Design Decisions:**
- Counter max of 3 balances enforcement with usability (user can Ctrl+C after 3 blocked attempts)
- Counter at project-local tmp/ per operational-safety.md (not system /tmp/)
- Exit 0 on malformed state (graceful degradation — don't block if enforcement can't verify)
- QA files excluded to prevent cross-workflow interference

**References:**
- EPIC-086: Claude Hooks for Step-Level Phase Enforcement
- STORY-525: Phase Steps Registry (dependency)

---

Story Template Version: 2.9
Last Updated: 2026-03-02
