# STORY-031 Integration Test Suite Summary

**Story:** Wire hooks into /ideate command
**Test File:** `tests/integration/test_story_031_ideate_hooks_integration.py`
**Framework:** pytest with AAA (Arrange, Act, Assert) pattern
**Status:** Red Phase (All tests written, ready for implementation)
**Date Created:** 2025-11-17

---

## Executive Summary

Comprehensive integration test suite for STORY-031 validates the complete /ideate command workflow with hook integration. The test suite covers:

- **34 total test cases** across 11 test classes
- **5 acceptance criteria** (AC1-AC5) fully validated
- **6 non-functional requirements** (NFR-P1, NFR-R1, NFR-M1)
- **5 edge cases** from story specification
- **Pattern consistency** with /dev pilot (STORY-023)
- **Context passing** validation (4 metadata fields)

All tests follow the TDD Red Phase pattern and are currently **failing** - ready for implementation of hook integration in the /ideate command.

---

## Test Organization

### Test Classes by Concern

| Class | Tests | Coverage |
|-------|-------|----------|
| `TestHookEligibilityCheck` | 5 | AC1 - check-hooks logic |
| `TestHookInvocationLogic` | 4 | AC2 - conditional invocation |
| `TestIdeateWithHooksIntegration` | 10 | AC2, AC3, AC4, AC5 - Full workflow |
| `TestIdeateHooksEdgeCases` | 5 | 5 edge cases from story |
| `TestIdeateContextPassing` | 4 | AC4 - Context metadata |
| `TestIdeateHooksPerformance` | 2 | NFR-P1 - Performance targets |
| `TestIdeateHooksReliability` | 1 | NFR-R1 - Failure resilience |
| `TestIdeateHooksPatternConsistency` | 3 | AC5 - Pattern validation |

**Total: 34 tests across 8 test classes**

---

## Acceptance Criteria Coverage

### AC1: Hook Eligibility Check After Ideation

**Tests:** 5
**Location:** `TestHookEligibilityCheck`

| Test | Purpose |
|------|---------|
| `test_check_hooks_command_called_with_correct_arguments` | Verify check-hooks called with --operation=ideate --status=completed |
| `test_check_hooks_exit_code_zero_means_eligible` | Exit code 0 → eligible for feedback |
| `test_check_hooks_exit_code_one_means_skip` | Exit code 1 → skip feedback invocation |
| `test_check_hooks_called_after_phase_5_completion` | Phase N positioned after Phase 5 (Next Steps) |
| `test_check_hooks_stderr_captured_on_error` | Error output captured for diagnosis |

**Key Assertions:**
- ✓ check-hooks invoked after ideation artifacts created
- ✓ Exit code 0 triggers feedback workflow
- ✓ Exit code 1 skips feedback silently
- ✓ Errors captured and logged

---

### AC2: Automatic Feedback Invocation When Eligible

**Tests:** 4
**Location:** `TestHookInvocationLogic`

| Test | Purpose |
|------|---------|
| `test_invoke_hooks_called_when_check_hooks_returns_zero` | invoke-hooks called when check-hooks=0 |
| `test_invoke_hooks_NOT_called_when_check_hooks_returns_one` | invoke-hooks NOT called when check-hooks=1 |
| `test_invoke_hooks_called_with_correct_arguments` | verify --operation=ideate argument |
| `test_invoke_hooks_passes_context_data` | Context data passed to hooks |

**Key Assertions:**
- ✓ invoke-hooks called only when check-hooks=0
- ✓ Correct operation and arguments passed
- ✓ Context metadata included in invocation
- ✓ User sees "✓ Post-ideation feedback initiated"

---

### AC3: Graceful Degradation on Hook Failures

**Tests:** 5
**Location:** `TestIdeateWithHooksIntegration`

| Test | Purpose |
|------|---------|
| `test_command_succeeds_when_check_hooks_cli_missing` | Handles CLI not found (exit 127) |
| `test_command_succeeds_when_invoke_hooks_fails` | Handles hook configuration invalid |
| `test_command_succeeds_when_invoke_hooks_times_out` | Handles timeout >30 seconds |
| (From edge cases) | Config corrupted, permission errors |

**Key Assertions:**
- ✓ Command exits with code 0 regardless of hook errors
- ✓ All ideation artifacts created (epics, requirements)
- ✓ Warning logged but non-blocking
- ✓ User sees "⚠ Post-ideation feedback skipped (hook system unavailable)"

---

### AC4: Context-Aware Feedback Configuration

**Tests:** 4 (dedicated) + 1 (integration)
**Location:** `TestIdeateContextPassing`, `TestHookInvocationLogic`

| Test | Purpose |
|------|---------|
| `test_context_includes_all_4_metadata_fields` | All 4 fields present: operation_type, artifacts, complexity_score, questions_asked |
| `test_artifacts_array_includes_all_epics` | Multiple epics included in artifacts array |
| `test_complexity_score_extracted_from_requirements` | Complexity score extracted from spec |
| `test_questions_asked_count_tracked` | Question count tracked from phases |

**4 Required Context Fields:**
1. ✓ `operation_type="ideation"` - Identifies operation type
2. ✓ `artifacts=[epic_paths, requirements_spec]` - All created files
3. ✓ `complexity_score=N` - Complexity assessment from phases
4. ✓ `questions_asked=count` - Questions asked during discovery

---

### AC5: Pattern Consistency with Pilot Implementation (STORY-023)

**Tests:** 3
**Location:** `TestIdeateHooksPatternConsistency`

| Test | Purpose |
|------|---------|
| `test_phase_n_positioning_after_phase_5` | Phase N after Phase 5 (matches /dev Phase 6) |
| `test_hook_invocation_matches_dev_pattern` | Same check-hooks/invoke-hooks pattern |
| `test_context_passing_matches_dev_pattern` | Same --operation-type naming convention |

**Pattern Validation:**
- ✓ Phase N positioned after primary work (Phase 5)
- ✓ check-hooks called with --operation and --status
- ✓ invoke-hooks conditional on exit code 0
- ✓ Graceful error handling in all cases
- ✓ Same parameter naming as /dev pilot

---

## Non-Functional Requirements

### NFR-P1: Performance (<500ms check, <5s total overhead)

**Tests:** 2
**Location:** `TestIdeateHooksPerformance`

| Test | Target |
|------|--------|
| `test_hook_check_overhead_less_than_500ms` | <500ms (slower than other commands) |
| `test_total_command_overhead_less_than_5_seconds` | <5s total overhead |

**Measurement Strategy:**
- 5 iterations of check-hooks call
- Average overhead calculated
- Passes if <500ms or <5s

---

### NFR-R1: Reliability (100% success regardless of hook state)

**Tests:** 1
**Location:** `TestIdeateHooksReliability`

| Test | Scenarios Covered |
|------|-------------------|
| `test_command_succeeds_with_all_hook_failure_scenarios` | 5 failure types: CLI missing, config invalid, conversation fails, timeout, permission error |

**Success Criteria:**
- ✓ Exit code 0 in ALL failure scenarios
- ✓ All ideation artifacts created
- ✓ Hook failures never cause ideation failure

---

### NFR-M1: Maintainability (<50 lines, DRY principles)

**Validated By:**
- Code review of Phase N implementation
- Pattern consistency tests (AC5)
- Extraction to reusable helper function

---

## Edge Cases

### Edge Case 1: Hook System Disabled in Configuration
**Test:** `test_hooks_disabled_via_config`

- Hooks configured with `enabled: false`
- check-hooks returns 1 (not eligible)
- No warning displayed (intentional configuration)
- Ideation completes successfully

### Edge Case 2: Multiple Epics Created
**Test:** `test_multiple_epics_context_includes_all_paths`

- Ideation creates 3 epics
- Context includes all 3 paths as array
- invoke-hooks receives complete artifact list

### Edge Case 3: Ideation Incomplete (User Cancellation)
**Test:** `test_ideation_incomplete_hook_not_invoked`

- User cancels during Phase 1-3
- Phase N never reached
- Hooks NOT invoked for incomplete sessions

### Edge Case 4: Feedback Already Invoked Manually
**Test:** `test_feedback_already_invoked_manually_edge_case`

- User already ran feedback manually
- check-hooks detects duplicate
- Returns not eligible (exit 1)
- No duplicate feedback invoked

### Edge Case 5: Batch Ideation (Multiple Rapid Calls)
**Test:** `test_multiple_rapid_invocations_edge_case`

- User runs /ideate 3 times rapidly
- Each treated independently
- No state pollution between calls
- Hook eligibility checked per invocation

### Additional Edge Cases (Integrated Tests)

**Edge Case:** CLI Not Installed
**Test:** `test_cli_not_installed_edge_case`
- Error caught and handled
- Ideation completes
- Warning logged

**Edge Case:** Config File Corrupted
**Test:** `test_config_file_corrupted_edge_case`
- Parse error caught
- Ideation continues
- Artifacts created

**Edge Case:** User Interrupts (Ctrl+C)
**Test:** `test_user_interrupts_feedback_ctrl_c_edge_case`
- Interrupt during invoke-hooks
- Command completes successfully
- Artifacts preserved

---

## Test Execution

### Running All STORY-031 Tests

```bash
# Run all STORY-031 integration tests
pytest tests/integration/test_story_031_ideate_hooks_integration.py -v

# Run specific test class
pytest tests/integration/test_story_031_ideate_hooks_integration.py::TestHookEligibilityCheck -v

# Run with marker
pytest -m story_031 -v

# Run with coverage
pytest tests/integration/test_story_031_ideate_hooks_integration.py --cov=.claude/commands --cov-report=term
```

### Expected Output (Red Phase)

All 34 tests should **FAIL** initially:

```
test_story_031_ideate_hooks_integration.py::TestHookEligibilityCheck::test_check_hooks_command_called_with_correct_arguments FAILED
test_story_031_ideate_hooks_integration.py::TestHookEligibilityCheck::test_check_hooks_exit_code_zero_means_eligible FAILED
...
34 failed in 2.34s
```

### Test Execution Time

- Unit tests: ~100ms (light fixtures, mocked subprocess)
- Integration tests: ~500ms (temp directories, file I/O)
- Performance tests: ~2s (multiple iterations)
- **Total suite: ~5-10 seconds**

---

## Test Fixtures

### Common Fixtures

**`temp_project_structure`**
- Creates complete temp project with .devforgeai, .ai_docs, .claude structure
- All required directories present
- Cleaned up after test

**`mock_check_hooks_success`**
- Returns exit code 0 (eligible)
- Simulates devforgeai check-hooks CLI

**`mock_check_hooks_skip`**
- Returns exit code 1 (not eligible)
- Simulates user skip pattern

**`mock_check_hooks_error`**
- Returns exit code 127 (CLI not found)
- Simulates missing devforgeai CLI

**`mock_invoke_hooks_success`**
- Returns exit code 0 (feedback completed)
- Simulates successful hook invocation

**`mock_invoke_hooks_error`**
- Returns exit code 1 (config invalid)
- Simulates hook failure

**`mock_invoke_hooks_timeout`**
- Returns exit code 124 (timeout)
- Simulates conversation timeout

**`ideation_artifacts_created_marker`**
- Documents expected artifacts (epics, requirements spec, complexity, questions)

---

## Mock Strategy

All subprocess calls are mocked to simulate CLI behavior without requiring actual devforgeai CLI installation:

```python
@patch('subprocess.run')
def test_example(self, mock_run):
    mock_run.return_value = MagicMock(
        returncode=0,
        stdout="success",
        stderr=""
    )
```

This allows tests to:
- ✓ Control exit codes and output
- ✓ Verify correct arguments passed
- ✓ Simulate failure scenarios
- ✓ Run without CLI installation
- ✓ Execute quickly and deterministically

---

## Success Criteria Validation

### Per-Test Success

Each test validates specific acceptance criteria:

**AC1 Tests (5):**
- ✓ check-hooks called with correct arguments
- ✓ Exit code 0 = eligible
- ✓ Exit code 1 = skip
- ✓ Positioned after Phase 5
- ✓ Errors captured

**AC2 Tests (4):**
- ✓ invoke-hooks called when eligible
- ✓ invoke-hooks NOT called when not eligible
- ✓ Correct arguments passed
- ✓ Context data included

**AC3 Tests (5):**
- ✓ Command succeeds on CLI error
- ✓ Command succeeds on hook error
- ✓ Command succeeds on timeout
- ✓ Artifacts created regardless
- ✓ Warning logged

**AC4 Tests (5):**
- ✓ All 4 metadata fields present
- ✓ Artifacts array includes all epics
- ✓ Complexity score extracted
- ✓ Questions count tracked
- ✓ Context passed to invoke-hooks

**AC5 Tests (3):**
- ✓ Phase N positioned correctly
- ✓ Pattern matches /dev pilot
- ✓ Parameter naming consistent

**Edge Cases (5):**
- ✓ Hooks disabled
- ✓ Multiple epics
- ✓ Incomplete ideation
- ✓ Duplicate feedback
- ✓ Batch invocations

**Non-Functional Requirements (3):**
- ✓ Performance <500ms (check), <5s (total)
- ✓ Reliability 100% (all failures handled)
- ✓ Maintainability <50 lines, DRY

---

## Test File Statistics

| Metric | Value |
|--------|-------|
| Total Lines | 1,100+ |
| Test Classes | 8 |
| Test Methods | 34 |
| Fixtures | 9 |
| Acceptance Criteria | 5 (all covered) |
| Edge Cases | 5 (all covered) |
| Non-Functional Requirements | 3+ (all covered) |
| Code Documentation | 100+ doc strings |

---

## Implementation Checklist

When implementing Phase N in `.claude/commands/ideate.md`:

### Phase N Implementation

- [ ] Add Phase N section after Phase 5 (Next Steps)
- [ ] Add `devforgeai check-hooks --operation=ideate --status=completed` call
- [ ] Capture exit code (0 = eligible, 1 = skip, other = error)
- [ ] If exit code 0: call `devforgeai invoke-hooks --operation=ideate`
- [ ] Pass context: --operation-type=ideation, --artifacts, --complexity-score, --questions-asked
- [ ] Handle all error cases gracefully (non-blocking)
- [ ] Display "✓ Post-ideation feedback initiated" on success
- [ ] Display "⚠ Post-ideation feedback skipped..." on failure/skip
- [ ] Keep Phase N <50 lines (DRY principle)
- [ ] Follow /dev pilot pattern (AC5)

### Testing Strategy

1. **Red Phase (Current):** All 34 tests written, all failing
2. **Green Phase:** Implement Phase N until all tests pass
3. **Refactor Phase:** Extract to helper function if duplication found
4. **Validation Phase:** Run full test suite, verify coverage

---

## Related Documentation

**Story File:**
- `.ai_docs/Stories/STORY-031-wire-hooks-into-ideate-command.story.md`

**Command File (Target):**
- `.claude/commands/ideate.md` (Phase N to be implemented)

**Pilot Implementation:**
- `.ai_docs/Stories/STORY-023-wire-hooks-into-dev-command-pilot.story.md`
- `.claude/commands/dev.md` (Phase 6 reference)

**Hook Infrastructure:**
- `STORY-021` - devforgeai check-hooks command
- `STORY-022` - devforgeai invoke-hooks command

**Framework Documentation:**
- `.devforgeai/protocols/hook-integration-pattern.md`
- `.devforgeai/protocols/lean-orchestration-pattern.md`

---

## Next Steps

1. **Run Current Tests:** Verify all 34 tests fail (Red Phase)
   ```bash
   pytest tests/integration/test_story_031_ideate_hooks_integration.py -v
   ```

2. **Implement Phase N:** Add hook integration to /ideate command

3. **Run Tests Again:** Verify all tests pass (Green Phase)
   ```bash
   pytest tests/integration/test_story_031_ideate_hooks_integration.py -v
   ```

4. **Coverage Validation:** Ensure >95% code coverage
   ```bash
   pytest tests/integration/test_story_031_ideate_hooks_integration.py --cov
   ```

5. **Final Validation:** Compare with /dev pilot pattern
   - [ ] Phase N structure matches
   - [ ] Error handling consistent
   - [ ] Context passing aligned
   - [ ] Performance targets met

---

## Quick Reference

### Test Markers

```bash
# Run all STORY-031 tests
pytest -m story_031

# Run by concern
pytest tests/integration/test_story_031_ideate_hooks_integration.py::TestHookEligibilityCheck
pytest tests/integration/test_story_031_ideate_hooks_integration.py::TestHookInvocationLogic
pytest tests/integration/test_story_031_ideate_hooks_integration.py::TestIdeateWithHooksIntegration
pytest tests/integration/test_story_031_ideate_hooks_integration.py::TestIdeateHooksEdgeCases
pytest tests/integration/test_story_031_ideate_hooks_integration.py::TestIdeateContextPassing
pytest tests/integration/test_story_031_ideate_hooks_integration.py::TestIdeateHooksPerformance
pytest tests/integration/test_story_031_ideate_hooks_integration.py::TestIdeateHooksReliability
pytest tests/integration/test_story_031_ideate_hooks_integration.py::TestIdeateHooksPatternConsistency
```

### Key Test Patterns

**Check eligibility:**
```python
result = subprocess.run(
    ["devforgeai", "check-hooks", "--operation=ideate", "--status=completed"],
    capture_output=True
)
assert result.returncode == 0  # eligible
```

**Invoke hooks:**
```python
result = subprocess.run(
    ["devforgeai", "invoke-hooks", "--operation=ideate",
     "--operation-type=ideation", "--artifacts=[...]",
     "--complexity-score=42", "--questions-asked=35"],
    capture_output=True
)
```

**Verify artifacts:**
```python
epic_file = Path(".ai_docs/Epics/EPIC-001.epic.md")
assert epic_file.exists()
req_file = Path(".devforgeai/specs/requirements/project-requirements.md")
assert req_file.exists()
```

---

**Test Suite Created:** 2025-11-17
**Framework:** pytest 7.0+
**Python Version:** 3.9+
**Status:** Ready for Implementation (Red Phase)
