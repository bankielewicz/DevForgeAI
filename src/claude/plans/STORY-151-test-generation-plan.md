# STORY-151: Post-Subagent Recording Hook - Test Generation Plan

**Story**: STORY-151 - Post-Subagent Recording Hook
**Phase**: TDD Red (Test-First Design)
**Created**: 2025-12-28
**Status**: Test Generation In Progress

## Overview

Generate failing tests for STORY-151 following Test-Driven Development (TDD) principles. Tests MUST fail initially as implementation does not exist yet. This plan guides systematic test generation from acceptance criteria and technical specifications.

## Story Summary

A Claude Code hook (`post_tool_call` event) that automatically records subagent invocations to the phase state file for audit trail purposes.

### Key Components
1. Hook script: `devforgeai/hooks/post-subagent-recording.sh`
2. Hook registration: `.claude/hooks.yaml`
3. Subagent filter config: `devforgeai/config/workflow-subagents.yaml`
4. Logging: `devforgeai/logs/subagent-recordings.log`

## Acceptance Criteria to Test

| AC# | Requirement | Test Type |
|-----|-----------|-----------|
| AC#1 | Hook registration in hooks config | Unit |
| AC#2 | Record subagent invocation on success | Unit/Integration |
| AC#3 | Extract story context (3 priority sources) | Unit |
| AC#4 | Skip non-workflow subagents | Unit |
| AC#5 | Handle missing state file gracefully | Unit |
| AC#6 | Log all recording attempts | Unit |

## Test Organization

### Directory Structure
```
tests/STORY-151/
├── unit/
│   ├── test_hook_registration.sh
│   ├── test_story_context_extraction.sh
│   ├── test_subagent_filtering.sh
│   ├── test_state_file_handling.sh
│   └── test_logging.sh
├── integration/
│   ├── test_full_recording_workflow.sh
│   └── test_hook_with_real_task_call.sh
└── run_all_tests.sh
```

### Test Files to Generate

#### 1. `tests/STORY-151/unit/test_hook_registration.sh`
Tests AC#1 - Hook registration in hooks.yaml

**Test Cases**:
- `test_hook_registered_in_hooks_yaml` - Hook exists with correct event
- `test_hook_script_path_correct` - Script path points to correct file
- `test_hook_blocking_flag_false` - Hook has blocking: false
- `test_hook_filter_matches_task_tool` - Filter matches Task tool calls
- `test_hook_filter_requires_subagent_type` - Filter checks for subagent_type param

#### 2. `tests/STORY-151/unit/test_story_context_extraction.sh`
Tests AC#3 - Extract story context from multiple sources (priority order)

**Test Cases**:
- `test_extract_from_env_var_highest_priority` - DEVFORGEAI_STORY_ID takes precedence
- `test_extract_from_latest_state_file` - Falls back to most recent state file
- `test_extract_from_grep_pattern` - Falls back to grep for STORY-XXX
- `test_priority_order_respected` - Sources checked in correct priority
- `test_no_story_context_detected` - Gracefully handles missing story

#### 3. `tests/STORY-151/unit/test_subagent_filtering.sh`
Tests AC#4 - Filter workflow vs non-workflow subagents

**Test Cases**:
- `test_workflow_subagent_recorded` - Workflow subagent (test-automator) recorded
- `test_non_workflow_subagent_skipped` - Non-workflow (internet-sleuth) skipped
- `test_filter_config_loaded_from_yaml` - workflow-subagents.yaml loaded correctly
- `test_all_workflow_subagents_recognized` - All 10 in list recognized
- `test_excluded_subagents_skipped_silently` - Excluded list processed

#### 4. `tests/STORY-151/unit/test_state_file_handling.sh`
Tests AC#5 - Handle missing state file gracefully

**Test Cases**:
- `test_skip_when_state_file_missing` - Skips with exit 0 when state missing
- `test_log_warning_for_missing_state` - Logs warning message
- `test_no_state_modification_on_missing_file` - State file not created/modified
- `test_workflow_continues_on_missing_state` - Non-blocking behavior

#### 5. `tests/STORY-151/unit/test_logging.sh`
Tests AC#6 - Log all recording attempts

**Test Cases**:
- `test_log_file_created` - Log file created at correct path
- `test_log_entry_json_lines_format` - Each line is valid JSON
- `test_log_contains_required_fields` - timestamp, story_id, subagent_name, phase_id, result, reason
- `test_log_timestamp_iso8601` - Timestamp in ISO-8601 format
- `test_log_result_values` - Result field contains recorded/skipped/error
- `test_log_includes_reason_text` - Reason field explains why action taken

#### 6. `tests/STORY-151/integration/test_full_recording_workflow.sh`
Tests full end-to-end workflow

**Test Cases**:
- `test_workflow_subagent_recorded_end_to_end` - Complete recording flow
- `test_non_workflow_subagent_skipped_end_to_end` - Complete skip flow
- `test_missing_state_file_graceful_exit` - Graceful handling
- `test_log_and_state_consistency` - Log matches state file

#### 7. `tests/STORY-151/integration/test_hook_with_real_task_call.sh`
Tests hook invocation from Task tool

**Test Cases**:
- `test_hook_called_after_task_success` - Hook triggered post-call
- `test_hook_not_blocking_on_error` - Hook failure doesn't block workflow
- `test_multiple_subagents_logged_sequentially` - Multiple calls recorded

## Test Framework Details

### Test Framework: Bash with bats
- **File**: Tests use `.sh` extension with bash/bats syntax
- **Naming**: `test_[function]_[scenario]_[expected]`
- **Pattern**: AAA (Arrange, Act, Assert)
- **Exit Codes**: 0 = pass, 1 = fail

### Test Dependencies
- Bash 4.0+
- bats (Bash Automated Testing System)
- jq (JSON parsing for log validation)
- devforgeai CLI tools

### Helper Functions to Use
```bash
# Create mock state file
create_mock_state_file() { ... }

# Create mock workflow-subagents.yaml
create_mock_config() { ... }

# Read and parse JSON log entries
parse_log_json() { ... }

# Verify STORY-XXX pattern
extract_story_id() { ... }

# Clean up test artifacts
cleanup_test_files() { ... }
```

## Testing Strategy

### Unit Tests (Per AC)
Each AC has dedicated unit tests validating behavior in isolation:
- Mock environment variables
- Mock config files
- Mock state files
- Validate script output and exit codes

### Integration Tests
Test complete workflows:
- Subagent recording flow
- Non-workflow subagent skip flow
- Error handling with actual files

## Expected Test Failures

All tests MUST fail initially because:
1. Hook script `devforgeai/hooks/post-subagent-recording.sh` does not exist
2. Hook not registered in `.claude/hooks.yaml`
3. Config file `devforgeai/config/workflow-subagents.yaml` does not exist
4. Log path `devforgeai/logs/subagent-recordings.log` not created by hook

**Test Failure Pattern**:
```bash
test_hook_registered_in_hooks_yaml
  Error: .claude/hooks.yaml missing post-subagent-recording entry
  Expected: post-subagent-recording hook exists
  Actual: Hook not found

test_hook_script_path_correct
  Error: devforgeai/hooks/post-subagent-recording.sh not found
  Expected: Script exists
  Actual: File does not exist
```

## TDD Workflow (Red -> Green -> Refactor)

### Red Phase (This Plan)
1. Generate failing tests from AC
2. Run tests - all fail
3. Document expected behavior

### Green Phase (Implementation)
1. Create hook script
2. Register hook in hooks.yaml
3. Create subagent filter config
4. Implement story context extraction
5. Implement logging
6. Run tests - all pass

### Refactor Phase
1. Extract duplicate code
2. Optimize performance
3. Improve error messages
4. Ensure Bash best practices

## Testing Coverage Map

| AC# | Test File | Tests | Coverage |
|-----|-----------|-------|----------|
| AC#1 | test_hook_registration.sh | 5 | 100% |
| AC#2 | test_full_recording_workflow.sh | 3 | 100% |
| AC#3 | test_story_context_extraction.sh | 5 | 100% |
| AC#4 | test_subagent_filtering.sh | 5 | 100% |
| AC#5 | test_state_file_handling.sh | 4 | 100% |
| AC#6 | test_logging.sh | 6 | 100% |
| Integration | test_hook_with_real_task_call.sh | 3 | 100% |

**Total Test Cases**: 31 tests

## Edge Cases Covered

1. **No state file exists** - AC#5
   - Expected: Skip with exit 0, log warning
   - Test: `test_skip_when_state_file_missing`

2. **Story ID extraction fails** - AC#3
   - Expected: Skip with exit 0, log reason
   - Test: `test_no_story_context_detected`

3. **Invalid subagent_type** - AC#4
   - Expected: Skip or log as unknown
   - Test: `test_non_workflow_subagent_skipped`

4. **Concurrent recordings** - Tech Spec mention
   - Expected: File locking handled (STORY-148)
   - Test: Integration tests validate ordering

5. **CLI missing/error** - Tech Spec edge case
   - Expected: Log error, exit 0 (non-blocking)
   - Test: Integration test with mock failure

## Performance Requirements

**Non-functional requirement**: Hook execution < 50ms (p95 latency)

Test to add:
- `test_hook_performance_under_50ms` - Measure execution time

## Validation Checklist

Before running tests:
- [ ] Test files created in `tests/STORY-151/`
- [ ] All 31 test cases defined
- [ ] Each test has clear AAA structure
- [ ] Test names describe scenario and expectation
- [ ] Dependencies documented
- [ ] Mock data generation functions ready
- [ ] Test runner script (`run_all_tests.sh`) created
- [ ] Tests fail when run (Red phase verification)

## Notes

- All tests should be shell scripts (.sh) following bash conventions
- Use `#!/usr/bin/env bash` shebang
- Include `set -euo pipefail` for safety
- Tests should clean up temp files after execution
- Log assertions should validate JSON format

## Next Steps

1. Generate test files from this plan
2. Run all tests to verify they FAIL (TDD Red)
3. Document each test failure reason
4. Pass to development phase for implementation
5. Phase 03 will make tests pass with implementation
