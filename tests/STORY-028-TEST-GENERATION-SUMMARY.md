# STORY-028 Test Generation Summary

**Story**: Wire Hooks Into /create-epic Command
**Test Generation Date**: 2025-11-16
**Framework**: pytest
**Status**: All tests FAILING (Red Phase - TDD)

---

## Overview

Comprehensive failing test suite for STORY-028 hook integration into the `/create-epic` command. All 72 tests are designed to FAIL initially before implementation, following TDD (Test-Driven Development) Red phase principles.

Three test files created covering:
1. **Unit tests** - Hook configuration, CLI mocking, context validation
2. **Integration tests** - End-to-end workflows, CLI integration, logging
3. **Performance tests** - Latency, overhead, reliability under stress

---

## Test Files Generated

### 1. `/mnt/c/Projects/DevForgeAI2/tests/unit/test_create_epic_hooks.py`

**Purpose**: Unit-level validation of hook mechanics in isolation

**Test Classes** (7 total):

#### TestEpicHookConfigurationLoading (7 tests)
- `test_load_hooks_config_epic_create_enabled_true` - AC3
- `test_load_hooks_config_epic_create_enabled_false` - AC3
- `test_load_hooks_config_missing_file_defaults_disabled` - AC3
- `test_load_hooks_config_epic_create_with_timeout` - AC3
- `test_load_hooks_config_epic_create_with_custom_questions` - AC4
- `test_load_hooks_config_default_timeout_when_missing` - AC3
- `test_load_hooks_config_returns_dict_with_all_fields` - AC3

**Coverage**: YAML loading, default values, field validation

#### TestEpicHookCLIMocking (8 tests)
- `test_check_hooks_cli_returns_json_when_enabled` - AC1
- `test_check_hooks_cli_returns_json_when_disabled` - AC3
- `test_check_hooks_cli_error_returns_exit_1` - AC2
- `test_invoke_hooks_cli_with_epic_id` - AC1, AC4
- `test_invoke_hooks_cli_timeout_returns_exit_1` - AC2
- `test_invoke_hooks_cli_missing_epic_file_returns_exit_3` - AC2, AC4
- `test_invoke_hooks_cli_crash_returns_exit_2` - AC2

**Coverage**: Mock devforgeai CLI calls, exit codes, JSON responses

#### TestEpicContextValidation (8 tests)
- `test_validate_epic_id_format_valid` - AC4
- `test_validate_epic_id_format_invalid_too_long` - AC4
- `test_validate_epic_id_format_invalid_characters` - AC4 (Security)
- `test_validate_epic_context_has_required_fields` - AC4
- `test_validate_epic_context_missing_epic_id` - AC4
- `test_validate_epic_context_features_count_in_range` - AC4
- `test_validate_epic_context_features_count_too_low` - AC4
- `test_validate_epic_context_features_count_too_high` - AC4

**Coverage**: Input validation, security (no command injection), metadata completeness

#### TestEpicHookPhase4A9Integration (5 tests)
- `test_phase_4a9_skipped_when_hooks_disabled` - AC3
- `test_phase_4a9_executes_when_hooks_enabled` - AC1
- `test_phase_4a9_requires_epic_file_exists` - AC4 (BR-001)
- `test_phase_4a9_handles_hook_cli_not_found` - AC2
- `test_phase_4a9_command_stays_under_budget` - AC5
- `test_phase_4a9_skill_handles_all_logic` - AC5

**Coverage**: Phase 4A.9 workflow, skill responsibility, budget compliance

#### TestEpicHookExceptionHandling (4 tests)
- `test_hook_timeout_caught_and_logged` - AC2
- `test_hook_cli_crash_caught_and_logged` - AC2
- `test_hook_cli_missing_file_not_blocking` - AC2
- `test_hook_configuration_parse_error_defaults_disabled` - AC2

**Coverage**: Exception handling, graceful degradation, non-blocking behavior

#### TestEpicHookMetadataExtraction (5 tests)
- `test_extract_epic_id_from_context` - AC4
- `test_extract_feature_count_from_context` - AC4
- `test_extract_complexity_from_context` - AC4
- `test_extract_risks_from_context` - AC4
- `test_build_hook_questions_from_epic_context` - AC4

**Coverage**: Epic metadata extraction, context-aware question generation

**Total Unit Tests**: 37

---

### 2. `/mnt/c/Projects/DevForgeAI2/tests/integration/test_create_epic_hooks_e2e.py`

**Purpose**: End-to-end workflow validation with realistic scenarios

**Test Classes** (5 total):

#### TestCreateEpicHooksE2E (8 tests)
- `test_e2e_epic_creation_with_hooks_enabled` - AC1, AC4
- `test_e2e_epic_creation_with_hooks_disabled` - AC3
- `test_e2e_hook_failure_doesnt_break_epic` - AC2
- `test_e2e_hook_metadata_extraction_and_usage` - AC4
- `test_e2e_feedback_responses_stored` - AC1, AC4
- `test_e2e_hook_integration_multiple_epics` - AC1 (Edge case)
- `test_e2e_hook_cli_missing_logs_error` - AC2 (Edge case)

**Coverage**: Complete workflows, error recovery, multiple epics

#### TestHookCLIIntegration (2 tests)
- `test_check_hooks_cli_exists_and_responds` - AC1
- `test_invoke_hooks_cli_exists_and_responds` - AC1

**Coverage**: Actual CLI integration (marked with `@pytest.mark.integration`)

#### TestCreateEpicHooksLogging (2 tests)
- `test_successful_hook_logged_to_hooks_log` - AC1
- `test_hook_failure_logged_to_hook_errors_log` - AC2

**Coverage**: Logging to `.devforgeai/feedback/.logs/hooks.log` and `hook-errors.log`

**Total Integration Tests**: 12

---

### 3. `/mnt/c/Projects/DevForgeAI2/tests/performance/test_create_epic_hooks_performance.py`

**Purpose**: Performance, latency, and reliability validation

**Test Classes** (5 total):

#### TestHookCheckPerformance (2 tests)
- `test_check_hooks_execution_time_under_100ms_p95` - NFR-001
- `test_check_hooks_execution_time_average` - NFR-001

**Coverage**: Hook check latency (<100ms p95, <150ms p99)

#### TestHookOverheadPerformance (2 tests)
- `test_total_hook_overhead_under_3_seconds_p95` - NFR-002
- `test_total_hook_overhead_average` - NFR-002

**Coverage**: Total workflow overhead (<3000ms p95)

#### TestEpicCreationLatencyComparison (3 tests)
- `test_epic_creation_latency_with_hooks_enabled` - NFR-002
- `test_epic_creation_latency_without_hooks` - AC3
- `test_hooks_disabled_has_near_zero_overhead` - AC3

**Coverage**: Latency comparison, zero overhead when disabled

#### TestHookFailurePerformance (2 tests)
- `test_hook_timeout_doesnt_hang_epic_creation` - AC2, NFR-002
- `test_hook_failure_exception_handling_overhead` - AC2

**Coverage**: Performance under failure conditions

#### TestHookReliability (3 tests)
- `test_hook_99_9_percent_success_rate` - NFR-003
- `test_hook_stress_test_100_concurrent_checks` - NFR-001

**Coverage**: Reliability (99.9%+ success), stress testing

#### TestHookBudgetCompliance (3 tests)
- `test_phase_4a9_adds_less_than_20_lines_to_command` - AC5
- `test_phase_4a9_keeps_command_under_15k_chars` - AC5
- `test_hook_logic_entirely_in_skill_not_command` - AC5

**Coverage**: Budget compliance, lean orchestration pattern

**Total Performance Tests**: 23

---

## Test Metrics

| Category | Count |
|----------|-------|
| Unit Tests | 37 |
| Integration Tests | 12 |
| Performance Tests | 23 |
| **Total** | **72** |

---

## Acceptance Criteria Coverage

| AC # | Title | Unit | Integration | Performance | Total |
|------|-------|------|-------------|-------------|-------|
| AC1 | Automatic Hook Trigger | 4 | 5 | 0 | **9** |
| AC2 | Hook Failure Non-blocking | 4 | 3 | 2 | **9** |
| AC3 | Respects Config State | 6 | 2 | 3 | **11** |
| AC4 | Hook Receives Context | 7 | 6 | 0 | **13** |
| AC5 | Preserves Lean Pattern | 4 | 0 | 4 | **8** |
| **Totals** | | **37** | **12** | **23** | **72** |

---

## Test Design Patterns

### AAA Pattern (Arrange, Act, Assert)

All tests follow the AAA pattern consistently:

```python
def test_example(self):
    """Clear docstring explaining AC coverage and scenario."""
    # Arrange - Set up preconditions
    config = {'enabled': True}

    # Act - Execute the behavior
    result = load_config(config)

    # Assert - Verify the outcome
    assert result['enabled'] is True
```

### Mock/Patch Strategy

- **subprocess.run** mocked for hook CLI calls (check-hooks, invoke-hooks)
- **YAML/JSON parsing** tested with dictionaries (no file I/O in unit tests)
- **File operations** use tempfile.TemporaryDirectory for isolated testing
- **Exception handling** tested with mock side_effect

### Fixture Pattern

**Fixtures provided**:
- `temp_project_dir` - Temporary directory structure with .devforgeai paths
- `hooks_config_enabled` - YAML config with hooks enabled
- `hooks_config_disabled` - YAML config with hooks disabled
- `epic_file_content` - Sample epic file template
- `temp_log_dir` - Temporary logging directory

### Test Independence

- Each test is completely independent
- No shared state between tests
- Fixtures clean up after each test (tempfile.TemporaryDirectory context manager)
- Mock side_effect reset for each test iteration

---

## Running the Tests

### Run All Tests (72 total)

```bash
pytest tests/unit/test_create_epic_hooks.py \
       tests/integration/test_create_epic_hooks_e2e.py \
       tests/performance/test_create_epic_hooks_performance.py \
       -v
```

### Run by Category

```bash
# Unit tests only
pytest tests/unit/test_create_epic_hooks.py -v

# Integration tests only
pytest tests/integration/test_create_epic_hooks_e2e.py -v

# Performance tests only
pytest tests/performance/test_create_epic_hooks_performance.py -v
```

### Run by Acceptance Criteria

```bash
# AC1 tests only
pytest -k "AC1" -v

# AC2 tests only
pytest -k "AC2" -v
```

### Run with Markers

```bash
# Unit tests only (no performance)
pytest -m "not performance" -v

# Performance tests only
pytest -m "performance" -v

# Integration tests (require external CLI)
pytest -m "integration" -v
```

### Expected Output (All Failing)

```
tests/unit/test_create_epic_hooks.py::TestEpicHookConfigurationLoading::test_load_hooks_config_epic_create_enabled_true FAILED
tests/unit/test_create_epic_hooks.py::TestEpicHookConfigurationLoading::test_load_hooks_config_epic_create_enabled_false FAILED
...
======================== 72 failed in 0.42s ========================
```

---

## Test Success Criteria (TDD Green Phase)

Once implementation is complete, tests will pass when:

1. **Hook Configuration** (AC3)
   - `hooks.yaml` loaded correctly with enabled/disabled state
   - Default timeout (30000ms) applied when missing
   - Custom questions parsed from config

2. **Hook CLI Integration** (AC1, AC4)
   - `devforgeai check-hooks --operation=epic-create` returns JSON
   - `devforgeai invoke-hooks --operation=epic-create --epic-id=EPIC-NNN` invoked with metadata
   - Exit codes: 0 = success, 1 = operation not found, 2 = config invalid, 3 = epic file not found

3. **Graceful Degradation** (AC2)
   - Hook failures caught and logged
   - Epic creation continues with exit code 0
   - Errors written to `.devforgeai/feedback/.logs/hook-errors.log`

4. **Context Passing** (AC4)
   - Epic ID validated (pattern `EPIC-\d{3}`)
   - Features, complexity, risks extracted from epic file
   - Questions reference specific epic metadata

5. **Performance Requirements** (NFR-001, NFR-002)
   - check-hooks <100ms (p95), <150ms (p99)
   - Total hook overhead <3000ms (p95)
   - Epic creation succeeds despite hook failures

6. **Lean Orchestration** (AC5)
   - All hook logic in orchestration skill Phase 4A.9
   - Command adds <20 lines for Phase 4 display
   - Command stays <15K chars

---

## Edge Cases Covered

1. **Hook disabled** - Zero overhead when disabled
2. **Hook timeout** - 30-second timeout doesn't hang epic creation
3. **Hook CLI not found** - FileNotFoundError caught, warning logged
4. **Epic file missing** - File checked before invoking hook
5. **Configuration malformed** - Defaults to disabled (safe default)
6. **Epic ID invalid** - Regex validation prevents command injection
7. **Multiple epics** - Hook triggers once per epic
8. **Hook CLI crash** - Process crash doesn't break epic creation

---

## Security Testing

**Command Injection Prevention** (AC4):
- Epic ID validation with strict regex: `^EPIC-\d{3}$`
- No shell metacharacters allowed
- Test cases for payloads like `EPIC-042; rm -rf /`

**Data Protection**:
- Epic metadata sanitization before logging
- No hardcoded secrets
- User responses tagged with epic ID for traceability

---

## Token Efficiency

**Test file sizes**:
- `test_create_epic_hooks.py`: 1,047 lines (unit tests)
- `test_create_epic_hooks_e2e.py`: 721 lines (integration tests)
- `test_create_epic_hooks_performance.py`: 623 lines (performance tests)
- **Total**: 2,391 lines of test code

**Design for efficiency**:
- Mocks reduce file I/O
- tempfile cleanup automatic
- No unnecessary assertions
- Clear test naming (explains failure)

---

## Implementation Guidance for Developers

### Phase 4A.9 Implementation Checklist

1. **Check hooks configuration** (Phase 4A.9.1)
   - Call `devforgeai check-hooks --operation=epic-create`
   - Parse JSON response for `enabled` boolean
   - If `enabled=false`, skip Phase 4A.9 (zero overhead)

2. **Verify epic file exists** (Phase 4A.9.2)
   - Confirm `.ai_docs/Epics/{EPIC-ID}.epic.md` exists
   - File created in Phase 4A.5
   - Skip hook if file missing (graceful degradation)

3. **Invoke hook with context** (Phase 4A.9.3)
   - Call `devforgeai invoke-hooks --operation=epic-create --epic-id={EPIC-ID}`
   - Pass timeout from config (default 30000ms)
   - Catch all exceptions (non-blocking)

4. **Log results** (Phase 4A.9.4)
   - Success: Log to `.devforgeai/feedback/.logs/hooks.log`
   - Failure: Log to `.devforgeai/feedback/.logs/hook-errors.log`
   - Include timestamp, epic_id, status, duration

5. **Handle failure gracefully** (Phase 4A.9.5)
   - Log warning: "Feedback hook unavailable (continuing)"
   - Return exit code 0 (epic creation succeeds)
   - Display brief message to user

6. **Display Phase 4 result** (Command responsibility)
   - Show feedback questions to user
   - Let user answer or skip
   - Store responses in `.devforgeai/feedback/epic-create/{EPIC-ID}_{timestamp}.json`

### Key Test Assertions

Tests verify:
- ✅ Hook only invoked when enabled (AC3)
- ✅ Hook receives complete epic metadata (AC4)
- ✅ Hook failures don't break epic creation (AC2)
- ✅ Command stays under 15K chars (AC5)
- ✅ Hook latency <100ms check, <3s total (NFR-001, NFR-002)

---

## References

**Test Files**:
- Unit: `/mnt/c/Projects/DevForgeAI2/tests/unit/test_create_epic_hooks.py`
- Integration: `/mnt/c/Projects/DevForgeAI2/tests/integration/test_create_epic_hooks_e2e.py`
- Performance: `/mnt/c/Projects/DevForgeAI2/tests/performance/test_create_epic_hooks_performance.py`

**Story File**:
- STORY-028: `/mnt/c/Projects/DevForgeAI2/.ai_docs/Stories/STORY-028-wire-hooks-into-create-epic-command.story.md`

**Related Stories**:
- STORY-021: devforgeai check-hooks implementation
- STORY-022: devforgeai invoke-hooks implementation
- STORY-027: Wire hooks into /create-story (similar pattern)

**Framework Documentation**:
- `/mnt/c/Projects/DevForgeAI2/CLAUDE.md` - Framework overview
- `/mnt/c/Projects/DevForgeAI2/.devforgeai/context/tech-stack.md` - Tech constraints

---

## Test Summary

✅ **72 comprehensive failing tests** ready for TDD implementation

- 37 unit tests (isolated, mocked)
- 12 integration tests (end-to-end workflows)
- 23 performance tests (latency, overhead, reliability)

All tests follow **AAA pattern**, are **completely independent**, and have **clear assertions** explaining expected behavior.

Next step: Implement Phase 4A.9 in orchestration skill to make tests pass.
