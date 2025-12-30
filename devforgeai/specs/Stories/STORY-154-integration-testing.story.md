---
id: STORY-154
title: Integration Testing - Phase Execution Enforcement
type: feature
status: QA Approved
priority: Medium
story-points: 3
epic: EPIC-031
sprint: null
created: 2025-12-24
updated: 2025-12-24
assignee: null
depends-on: [STORY-153]
blocks: []
---

## User Story

**As a** quality assurance engineer,
**I want** comprehensive end-to-end integration tests for the Phase Execution Enforcement System,
**So that** I can verify the RCA-022 scenario (mandatory phases skipped) is impossible after implementation of all three enforcement layers.

---

## Acceptance Criteria

### AC#1: Verify RCA-022 scenario is blocked

**Given** a test /dev workflow is initiated for a test story
**When** Claude attempts to skip Phase 01 (tech-stack-detector) and proceed directly to Phase 03 (implementation)
**Then** the pre-phase-transition hook blocks the transition with error message "Phase 01 incomplete. Required subagents: tech-stack-detector. Invoked subagents: none."

### AC#2: Verify complete workflow succeeds

**Given** a test /dev workflow is initiated for a test story
**When** all phases are executed in order with all required subagents invoked
**Then** the workflow completes successfully with state file showing all 10 phases as "completed" and checkpoint_passed=true.

### AC#3: Verify subagent recording accuracy

**Given** a test workflow invokes 5 subagents across different phases
**When** the workflow completes
**Then** the state file contains exactly 5 subagent invocation records with correct phase_id, subagent_name, and timestamps for each.

### AC#4: Verify state file archival on completion

**Given** a test workflow completes all phases successfully
**When** the story status is updated to "QA Approved"
**Then** the state file is moved from `devforgeai/workflows/STORY-XXX-phase-state.json` to `devforgeai/workflows/completed/STORY-XXX-phase-state.json`.

### AC#5: Verify enforcement logs capture all decisions

**Given** a test workflow includes 3 blocked transitions and 10 allowed transitions
**When** the workflow completes
**Then** the `devforgeai/logs/phase-enforcement.log` contains 13 entries (3 blocked + 10 allowed) with complete decision context for each.

### AC#6: Verify backward compatibility with CLI not installed

**Given** the devforgeai-validate CLI is not installed in the test environment
**When** a /dev workflow is initiated
**Then** warning messages are displayed but the workflow continues without blocking, demonstrating backward compatibility for legacy environments.

---

## Technical Specification

```yaml
technical_specification:
  version: "2.0"

  components:
    - type: TestSuite
      name: PhaseEnforcementIntegrationTests
      file_path: devforgeai/tests/STORY-154/
      description: "End-to-end integration tests for Phase Execution Enforcement System"
      test_files:
        - name: test-rca022-scenario-blocked.sh
          description: "Verify RCA-022 phase skipping is blocked"
          test_requirement: "AC#1"
        - name: test-complete-workflow.sh
          description: "Verify full workflow succeeds"
          test_requirement: "AC#2"
        - name: test-subagent-recording.sh
          description: "Verify subagent invocations recorded"
          test_requirement: "AC#3"
        - name: test-state-archival.sh
          description: "Verify state file archival"
          test_requirement: "AC#4"
        - name: test-enforcement-logging.sh
          description: "Verify enforcement log completeness"
          test_requirement: "AC#5"
        - name: test-backward-compatibility.sh
          description: "Verify CLI-absent behavior"
          test_requirement: "AC#6"

    - type: TestFixtures
      name: TestStoryFixtures
      file_path: devforgeai/tests/STORY-154/fixtures/
      description: "Test stories and mock data for integration tests"
      fixtures:
        - name: STORY-TEST-001.story.md
          description: "Minimal test story for enforcement testing"
        - name: mock-subagent-responses/
          description: "Canned responses for subagent mocking"
        - name: expected-state-files/
          description: "Expected state file contents for assertion"

    - type: TestHarness
      name: EnforcementTestHarness
      file_path: devforgeai/tests/STORY-154/harness/
      description: "Test harness for simulating workflow execution"
      components:
        - name: mock-claude-executor.py
          description: "Simulates Claude executing SKILL.md phases"
        - name: hook-test-runner.sh
          description: "Executes hooks in isolation for testing"
        - name: state-file-validator.py
          description: "Validates state file structure and content"

    - type: Configuration
      name: IntegrationTestConfig
      file_path: devforgeai/tests/STORY-154/config.yaml
      description: "Configuration for integration test environment"
      content:
        test_environment:
          workflows_dir: "devforgeai/tests/STORY-154/test-workflows"
          logs_dir: "devforgeai/tests/STORY-154/test-logs"
          archive_dir: "devforgeai/tests/STORY-154/test-workflows/completed"
        timeout:
          per_test: 30  # seconds
          total_suite: 300  # seconds
        cleanup:
          enabled: true
          preserve_on_failure: true
      test_requirement: "test_config_loads_correctly"

  business_rules:
    - id: BR-001
      description: "All 6 ACs must pass for STORY-154 to be complete"
      validation: "100% AC pass rate required"
      test_requirement: "test_all_acs_covered"

    - id: BR-002
      description: "Tests must be deterministic (no flakiness)"
      validation: "3 consecutive runs produce same results"
      test_requirement: "test_determinism"

    - id: BR-003
      description: "Test cleanup must be reliable"
      validation: "No leftover state files after test completion"
      test_requirement: "test_cleanup_complete"

    - id: BR-004
      description: "RCA-022 scenario must be 100% blocked"
      validation: "Phase skip attempt always results in blocking"
      test_requirement: "test_rca022_blocked_100_percent"

  non_functional_requirements:
    - category: Performance
      requirement: "Full test suite completes in < 5 minutes"
      metric: "Total execution time"
      test_requirement: "test_suite_performance"

    - category: Reliability
      requirement: "Tests must be deterministic (no flaky tests)"
      metric: "0% flakiness rate over 10 runs"
      test_requirement: "test_no_flakiness"

    - category: Coverage
      requirement: "All enforcement layers covered by tests"
      metric: "Layer 1, 2, 3 each have dedicated tests"
      test_requirement: "test_layer_coverage"
```

---

## Edge Cases

1. **Test environment contamination:** Clean state before each test
2. **Concurrent test execution:** Isolated workflows per test
3. **Hook permission issues:** Verify script execution permissions
4. **State file corruption simulation:** Test recovery behavior
5. **Timeout during workflow:** Verify timeout is logged correctly
6. **Partial failure recovery:** Test HALT and resume behavior
7. **Log rotation during test:** Ensure logs capture complete

---

## Definition of Done

### Implementation
- [x] Test suite directory structure created at `devforgeai/tests/STORY-154/`
- [x] 6 test scripts created (one per AC)
- [x] Test fixtures created (mock story, responses, expected states)
- [x] Test harness implemented for workflow simulation
- [x] config.yaml created with test environment settings
- [x] Cleanup script for post-test state cleanup

### Quality
- [x] All 6 acceptance criteria have passing tests
- [x] Tests are deterministic (no flakiness)
- [x] Test execution time < 5 minutes total
- [x] Clean test isolation (no cross-test dependencies)

### Testing
- [x] `test-rca022-scenario-blocked.sh` passes
- [x] `test-complete-workflow.sh` passes
- [x] `test-subagent-recording.sh` passes
- [x] `test-state-archival.sh` passes
- [x] `test-enforcement-logging.sh` passes
- [x] `test-backward-compatibility.sh` passes
- [x] 10-run determinism check passes

### Documentation
- [x] Test execution instructions in README
- [x] Test coverage matrix documented
- [x] Failure debugging guide

---

## Dependencies

### Upstream (this story depends on)
- STORY-153: Skill Validation Integration (provides the integrated enforcement system to test)

### Downstream (blocked by this story)
- None (final story in epic)

---

## Related Documents

| Document | Path |
|----------|------|
| Epic | `devforgeai/specs/Epics/EPIC-031-phase-execution-enforcement.epic.md` |
| RCA-022 | `devforgeai/RCA/RCA-022-mandatory-tdd-phases-skipped.md` |
| STORY-148 | `devforgeai/specs/Stories/STORY-148-phase-state-file-module.story.md` |
| STORY-149 | `devforgeai/specs/Stories/STORY-149-phase-validation-script.story.md` |
| STORY-150 | `devforgeai/specs/Stories/STORY-150-pre-phase-transition-hook.story.md` |
| STORY-151 | `devforgeai/specs/Stories/STORY-151-post-subagent-recording-hook.story.md` |
| STORY-153 | `devforgeai/specs/Stories/STORY-153-skill-validation-integration.story.md` |

---

## Implementation Notes

- [x] Test suite directory structure created at `devforgeai/tests/STORY-154/`
- [x] 6 test scripts created (one per AC)
- [x] Test fixtures created (mock story, responses, expected states)
- [x] Test harness implemented for workflow simulation
- [x] config.yaml created with test environment settings
- [x] Cleanup script for post-test state cleanup (in run-tests.sh)
- [x] All 6 acceptance criteria have passing tests (100% pass rate)
- [x] Tests are deterministic (no flakiness detected in multiple runs)
- [x] Test execution time < 5 minutes total (~2 seconds actual)
- [x] Clean test isolation (unique STORY-TEST-XXX IDs per test)
- [x] All individual test scripts pass
- [x] 10-run determinism check passes
- [x] Test execution instructions in README.md
- [x] Test coverage matrix documented in README.md
- [x] Failure debugging guide in README.md

**Developer:** DevForgeAI AI Agent (claude/opus)
**Implemented:** 2025-12-30

### TDD Workflow Summary

- **Red Phase:** Generated 6 failing test scripts from acceptance criteria
- **Green Phase:** Fixed test assertions for proper JSON parsing and PATH manipulation
- **Refactor Phase:** Code reviewed - EXCELLENT quality, no critical issues
- **Integration:** All cross-component interactions validated

## Workflow Status

**Current Status:** QA Approved
**Created:** 2025-12-24
**Last Updated:** 2025-12-30

### Status History
| Date | From | To | By | Notes |
|------|------|-----|-----|-------|
| 2025-12-24 | - | Backlog | DevForgeAI | Story created via /create-missing-stories EPIC-031 |
| 2025-12-30 | Dev Complete | QA Approved | claude/qa-result-interpreter | QA Deep: Passed - Coverage 100%, 0 blocking violations |
