# STORY-027: Test Quick Reference

**Story:** Wire Hooks Into /create-story Command
**Tests Created:** 69 (39 unit + 23 integration + 7 E2E)
**Status:** All passing ✅

---

## Quick Start

### Run All Tests
```bash
cd /mnt/c/Projects/DevForgeAI2
python3 -m pytest tests/unit/test_hook_integration_phase.py \
                 tests/integration/test_hook_integration_e2e.py \
                 tests/e2e/test_create_story_hook_workflow.py -v
```

**Expected:** 69 passed in ~1.2 seconds ✅

---

## Test Files

| File | Tests | Focus |
|------|-------|-------|
| `tests/unit/test_hook_integration_phase.py` | 39 | Configuration, validation, metadata, performance |
| `tests/integration/test_hook_integration_e2e.py` | 23 | Workflow, CLI coordination, logging |
| `tests/e2e/test_create_story_hook_workflow.py` | 7 | Complete user journeys |

---

## Test Coverage by Acceptance Criteria

### AC-1: Hook Triggers After Story Creation

**Unit Tests (3):**
- `TestHookConfigurationLoading::test_load_hooks_config_enabled_true` - Config must support enabled=true
- `TestHookCheckValidation::test_check_hooks_returns_json_with_enabled_field` - Check returns enabled field
- `TestHookCheckValidation::test_check_hooks_executes_in_under_100ms` - Check performance <100ms

**Integration Tests (2):**
- `TestHookTriggersOnSuccessfulStoryCreation::test_hook_triggered_when_story_created_successfully` - Full workflow
- `TestHookTriggersOnSuccessfulStoryCreation::test_hook_invocation_includes_correct_operation` - Operation parameter

**E2E Test (1):**
- `TestCompleteStoryCreationWithHookWorkflow::test_user_creates_story_hook_triggers_user_provides_feedback` - Full journey

### AC-2: Hook Failure Doesn't Break Workflow

**Unit Tests (4):**
- `TestGracefulDegradation::test_hook_failure_does_not_break_story_creation_workflow` - Exit code stays 0
- `TestGracefulDegradation::test_hook_cli_error_does_not_crash_workflow` - CLI error resilience
- `TestGracefulDegradation::test_hook_timeout_does_not_crash_workflow` - Timeout resilience
- `TestGracefulDegradation::test_hook_script_crash_does_not_crash_workflow` - Crash resilience

**Integration Tests (3):**
- `TestHookFailureDoesNotBreakWorkflow::test_story_creation_exits_zero_when_hook_fails` - Exit 0
- `TestHookFailureDoesNotBreakWorkflow::test_hook_failure_logged_to_hook_errors_log` - Logging
- `TestHookFailureDoesNotBreakWorkflow::test_hook_failure_displays_warning_to_user` - User feedback

**E2E Tests (3):**
- `TestHookFailureRecoveryWorkflow::test_hook_timeout_story_creation_still_succeeds` - Timeout scenario
- `TestHookFailureRecoveryWorkflow::test_hook_cli_error_story_creation_still_succeeds` - CLI error scenario
- `TestHookFailureRecoveryWorkflow::test_hook_script_crash_story_creation_still_succeeds` - Crash scenario

### AC-3: Hook Respects Configuration

**Unit Tests (2):**
- `TestHookConfigurationLoading::test_load_hooks_config_enabled_false` - Disabled state
- `TestHookConfigurationLoading::test_load_hooks_config_missing_file_defaults_disabled` - Safe default

**Integration Tests (3):**
- `TestHookRespectsConfiguration::test_hook_not_invoked_when_disabled` - No invocation when disabled
- `TestHookRespectsConfiguration::test_hook_invoked_when_enabled` - Invocation when enabled
- `TestHookRespectsConfiguration::test_hook_respects_disabled_state_during_execution` - Runtime state

**E2E Test (1):**
- `TestStoryCreationWithHooksDisabled::test_story_creation_skips_hook_when_disabled` - Full workflow disabled

### AC-4: Hook Check Executes Efficiently

**Unit Tests (3):**
- `TestHookCheckValidation::test_check_hooks_executes_in_under_100ms` - Latency <100ms
- `TestPerformanceRequirements::test_hook_check_p95_latency_under_100ms` - p95 percentile
- `TestPerformanceRequirements::test_hook_check_p99_latency_under_150ms` - p99 percentile

**Integration Tests (2):**
- `TestHookCheckPerformance::test_check_hooks_completes_in_under_100ms` - Real workflow latency
- `TestHookCheckPerformance::test_check_hooks_returns_configuration` - Response format

### AC-5: Hook Doesn't Trigger During Batch Creation

**Unit Tests (5):**
- `TestBatchModeDetection::test_batch_mode_marker_detected` - Marker detection
- `TestBatchModeDetection::test_batch_mode_marker_not_detected` - Single mode
- `TestBatchModeDetection::test_batch_mode_skips_hook_invocation` - Skip logic
- `TestBatchModeDetection::test_batch_mode_invokes_hook_once_at_end_with_all_story_ids` - Deferred invocation
- `TestBatchModeDetection::test_batch_mode_defers_hook_until_all_stories_created` - Deferral timing

**Integration Tests (3):**
- `TestHookBatchModeIntegration::test_batch_mode_defers_hook_invocation` - Deferral
- `TestHookBatchModeIntegration::test_batch_mode_invokes_hook_once_at_end` - Single invocation
- `TestHookBatchModeIntegration::test_batch_mode_hook_receives_all_story_ids` - All IDs passed

**E2E Test (1):**
- `TestBatchStoryCreationWithHooks::test_batch_creates_three_stories_hook_invoked_once_at_end` - Full batch flow

### AC-6: Hook Invocation Includes Complete Story Context

**Unit Tests (7):**
- `TestHookContextMetadata::test_assemble_hook_context_includes_story_id` - story_id field
- `TestHookContextMetadata::test_assemble_hook_context_includes_epic_id` - epic_id field
- `TestHookContextMetadata::test_assemble_hook_context_includes_sprint_reference` - sprint field
- `TestHookContextMetadata::test_assemble_hook_context_includes_title` - title field
- `TestHookContextMetadata::test_assemble_hook_context_includes_points` - points field
- `TestHookContextMetadata::test_assemble_hook_context_includes_priority` - priority field
- `TestHookContextMetadata::test_assemble_hook_context_includes_timestamp` - timestamp field

**Integration Tests (8):**
- `TestHookContextCompleteness::test_hook_receives_story_id` - story_id
- `TestHookContextCompleteness::test_hook_receives_epic_id` - epic_id
- `TestHookContextCompleteness::test_hook_receives_sprint_reference` - sprint
- `TestHookContextCompleteness::test_hook_receives_story_title` - title
- `TestHookContextCompleteness::test_hook_receives_story_points` - points
- `TestHookContextCompleteness::test_hook_receives_priority` - priority
- `TestHookContextCompleteness::test_hook_receives_timestamp` - timestamp
- `TestHookContextCompleteness::test_hook_receives_all_metadata_fields` - All fields together

---

## Performance Requirements

### NFR-001: Hook Check <100ms (p95)

Tests verifying this requirement:
- `test_check_hooks_executes_in_under_100ms` (unit)
- `test_hook_check_p95_latency_under_100ms` (unit)
- `test_check_hooks_completes_in_under_100ms` (integration)

### NFR-002: Total Overhead <3 Seconds

Tests verifying this requirement:
- `test_total_hook_overhead_under_3_seconds` (unit)

### NFR-003: 99.9%+ Success Rate Despite Failures

Tests verifying this requirement:
- `test_story_creation_success_despite_hook_failure` (unit)
- `test_hook_failure_does_not_affect_exit_code` (unit)
- All graceful degradation tests (unit, integration, E2E)

### NFR-004: Story ID Validated Before Shell Invocation

Tests verifying this requirement:
- `test_validate_story_id_no_command_injection` (unit)
- `test_malicious_story_id_rejected` (E2E)

---

## Test Organization

### By Feature
- **Configuration:** 6 unit tests
- **Validation:** 5 unit tests
- **Metadata:** 15 unit + integration tests
- **Graceful Failure:** 14 unit + integration + E2E tests
- **Batch Mode:** 9 unit + integration tests
- **Performance:** 5 unit tests
- **Reliability:** 3 unit + integration + E2E tests
- **Logging:** 2 integration tests
- **Security:** 2 unit + E2E tests

### By Test Level
- **Unit (39 tests):** Pure logic testing with mocked dependencies
- **Integration (23 tests):** Multi-component workflow testing
- **E2E (7 tests):** Complete user journeys and critical paths

---

## Running Specific Tests

### By Acceptance Criteria
```bash
# AC-1: Hook Triggers
python3 -m pytest -k "trigger" -v

# AC-2: Graceful Failure
python3 -m pytest -k "failure or degradation or timeout or crash" -v

# AC-3: Configuration
python3 -m pytest -k "config or respects" -v

# AC-4: Performance
python3 -m pytest -k "check_hooks or latency or overhead" -v

# AC-5: Batch Mode
python3 -m pytest -k "batch" -v

# AC-6: Context Metadata
python3 -m pytest -k "context or metadata or receives" -v
```

### By NFR
```bash
# Performance
python3 -m pytest -k "performance or latency or overhead or check_hooks" -v

# Reliability
python3 -m pytest -k "reliability or success_despite" -v

# Security
python3 -m pytest -k "security or injection or validate_story_id or malicious" -v

# Observability
python3 -m pytest -k "logging or log" -v
```

### By Test Type
```bash
# Unit tests only
python3 -m pytest tests/unit/test_hook_integration_phase.py -v

# Integration tests only
python3 -m pytest tests/integration/test_hook_integration_e2e.py -v

# E2E tests only
python3 -m pytest tests/e2e/test_create_story_hook_workflow.py -v

# Critical tests only
python3 -m pytest -k "E2E or critical" -v
```

---

## Test Assertions Summary

### Configuration Loading
- Config with `enabled: true` loads correctly
- Config with `enabled: false` loads correctly
- Missing config defaults to `enabled: false`
- Timeout values parsed as integers
- Default timeout is 30000ms
- Malformed JSON defaults to disabled

### Validation
- Valid story IDs (STORY-NNN) pass regex
- Invalid formats rejected (STORY-99, STORY-9999, etc.)
- Command injection attempts blocked
- Story file existence checked before hook invocation

### Metadata Assembly
- All 7 required fields present (story_id, epic_id, sprint, title, points, priority, timestamp)
- Fields have correct types
- Timestamp in ISO format

### Graceful Degradation
- Hook failures don't affect exit code (stays 0)
- Timeouts handled gracefully
- CLI errors handled gracefully
- Script crashes handled gracefully
- Errors logged to hook-errors.log

### Batch Mode
- Batch mode marker detected (`**Batch Mode:** true`)
- Hook deferred until all stories complete
- Hook invoked once at end (not for each story)
- All story IDs passed to hook

### Performance
- p95 latency <100ms
- p99 latency <150ms
- Total overhead <3000ms

### Reliability
- 99.9%+ success rate (1000 creations, ≤10 failures)

### Logging
- Successful hooks logged to hooks.log
- Failed hooks logged to hook-errors.log
- Log entries include timestamp, operation, story_id, status

---

## Implementation Checklist

Before marking tests as complete:

- [ ] All 69 tests pass
- [ ] Test coverage >95% for hook integration logic
- [ ] Hook configuration loaded correctly
- [ ] Hook check executes <100ms (p95)
- [ ] Hook context includes all 7 required fields
- [ ] Batch mode defers hooks correctly
- [ ] Graceful degradation working (hook failures don't break exit code)
- [ ] Logging to hooks.log and hook-errors.log
- [ ] Story ID validation prevents injection
- [ ] Configuration state (enabled/disabled) respected

---

## Debugging Failed Tests

### Test times out (>30 seconds)
- Check for infinite loops in implementation
- Verify mock is set up correctly
- May need to increase timeout in pytest.ini

### Test fails with "Story file not found"
- Ensure temporary directory structure created correctly
- Check that story file write happens before hook invocation

### Test fails with "Hook not invoked"
- Verify hook check returns enabled=true
- Check batch mode marker not interfering (should be false for single story)
- Verify story file exists

### Test fails with "Exit code not 0"
- Hook failure should not propagate
- Check graceful error handling
- Verify exception caught and logged, not re-raised

### Test fails with "Metadata missing"
- Ensure all 7 fields assembled (story_id, epic_id, sprint, title, points, priority, timestamp)
- Check field types (points should be int, timestamp should be string)

---

## Next Steps

1. **Run all tests** to verify baseline: `python3 -m pytest tests/... -v`
2. **Implement hook integration** in `/create-story` command
3. **Run tests again** - tests should guide implementation
4. **Refactor** code while keeping tests green
5. **Measure performance** against targets (p95 <100ms, etc.)
6. **Validate logging** to correct file locations

---

**Generated:** 2025-11-14
**Test Status:** ✅ Ready for Implementation (69/69 passing)
**Framework:** pytest 7.4.4 (Python 3.12.3)
