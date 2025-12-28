# STORY-149: Phase Completion Validation Script - Test Suite

## Overview

Comprehensive test suite for the Phase Completion Validation Script (STORY-149) that implements CLI commands for validating phase transitions in the TDD workflow.

**Test Framework**: pytest
**Language**: Python 3.9+
**Status**: TDD Red Phase (all tests expected to fail - implementation doesn't exist yet)

---

## Test File

**Location**: `/mnt/c/Projects/DevForgeAI2/tests/unit/STORY-149/test_validate_phase_completion.py`

**Statistics**:
- 9 test classes
- 40 test functions
- ~850 lines of code
- 100% coverage of acceptance criteria

---

## Test Organization

### Test Classes

1. **TestPhaseCheckCommand** (5 tests)
   - AC#1: phase-check command validates phase completion
   - Tests successful validation, blocking, error conditions
   - Tests invalid story/phase IDs

2. **TestSubagentValidation** (5 tests)
   - AC#2: Validates all required subagents invoked
   - Tests complete match, partial match, empty list
   - Tests superset of required subagents (acceptable)

3. **TestCheckpointValidation** (4 tests)
   - AC#3: Validates checkpoint passed flag
   - Tests true/false/missing scenarios
   - Tests checkpoint overrides other validations

4. **TestRecordSubagentCommand** (4 tests)
   - AC#4: record-subagent appends invocation
   - Tests idempotent behavior (no duplicates)
   - Tests error conditions

5. **TestCompletePhaseCommand** (5 tests)
   - AC#5: complete-phase marks completion
   - Tests status update, timestamp, phase advancement
   - Tests blocking on missing subagents or failed checkpoint

6. **TestExitCodeEnforcement** (4 tests)
   - AC#6: Exit codes enable external enforcement
   - Tests exit code 0 (proceed), 1 (blocked), 2 (error)
   - Tests strict enforcement of these codes only

7. **TestEdgeCases** (8 tests)
   - Story ID format validation (STORY-XXX required)
   - Phase ID range validation (01-10 required)
   - Corrupt JSON handling
   - Phase ordering enforcement
   - Empty requirements handling

8. **TestNonFunctionalRequirements** (2 tests)
   - Performance: phase-check < 30ms
   - Error messages: specific and actionable

9. **TestIntegrationWithPhaseState** (3 tests)
   - Integration with STORY-148 PhaseState class
   - Proper delegation to PhaseState methods
   - Correct parameter passing

---

## Expected Test Results

### Current Status (Before Implementation)

**All 40 tests WILL FAIL** because:
1. Module `installer.validate_phase_completion` does not exist
2. Functions are not implemented
3. Constants are undefined

**Expected failure pattern**:
```
ModuleNotFoundError: No module named 'installer.validate_phase_completion'
```

This is **correct behavior** for TDD Red phase. The tests are written correctly and will catch ModuleNotFoundError as expected.

---

## Running the Tests

### Setup Environment

```bash
cd /mnt/c/Projects/DevForgeAI2
export PYTHONPATH=".:$PYTHONPATH"
```

### Run All Tests

```bash
pytest tests/unit/STORY-149/test_validate_phase_completion.py -v
```

### Run Specific Test Class

```bash
# Phase-check command tests
pytest tests/unit/STORY-149/test_validate_phase_completion.py::TestPhaseCheckCommand -v

# Subagent validation tests
pytest tests/unit/STORY-149/test_validate_phase_completion.py::TestSubagentValidation -v

# Exit code enforcement tests
pytest tests/unit/STORY-149/test_validate_phase_completion.py::TestExitCodeEnforcement -v
```

### Run Specific Test Function

```bash
pytest tests/unit/STORY-149/test_validate_phase_completion.py::TestPhaseCheckCommand::test_phase_check_validates_completion_exit_code_zero -v
```

### Run with Coverage Report

```bash
pytest tests/unit/STORY-149/test_validate_phase_completion.py \
    --cov=installer \
    --cov-report=term-missing \
    --cov-report=html
```

### Run with Detailed Output

```bash
pytest tests/unit/STORY-149/test_validate_phase_completion.py \
    -v \
    --tb=short \
    --capture=no
```

---

## Test Fixtures

All tests use fixtures to create temporary project directories and phase state structures.

### `temp_project_dir`
- Creates temporary directory with `devforgeai/workflows/` subdirectory
- Automatically cleaned up after test
- Used by all integration tests

### `phase_state_fixture`
- Complete, valid phase state structure
- Phase 01: completed with all subagents and checkpoint passed
- Phases 02-03: pending
- Used by positive/success test cases

### `incomplete_phase_state`
- Phase state with missing required subagents
- Phase 01: has git-validator but missing tech-stack-detector
- Used for validation failure tests

### `checkpoint_failed_state`
- Phase state where checkpoint validation failed
- All subagents invoked but checkpoint_passed=false
- Used for checkpoint failure tests

---

## Implementation Checklist

After implementing `installer/validate_phase_completion.py`, use this checklist to verify all tests pass:

### Phase-Check Command (AC#1)
- [ ] `test_phase_check_validates_completion_exit_code_zero` - Returns 0 for valid phase
- [ ] `test_phase_check_blocks_incomplete_phase` - Returns 1 for incomplete phase
- [ ] `test_phase_check_errors_on_missing_state_file` - Returns 2 for missing state
- [ ] `test_phase_check_invalid_story_id_format` - Rejects invalid STORY-XXX format
- [ ] `test_phase_check_invalid_phase_ids` - Rejects phase IDs outside 01-10

### Subagent Validation (AC#2)
- [ ] `test_phase_check_validates_all_subagents_invoked` - All required present = pass
- [ ] `test_phase_check_rejects_missing_subagents` - Any missing = fail
- [ ] `test_phase_check_rejects_all_missing_subagents` - Empty list = fail
- [ ] `test_phase_check_exact_match_subagents` - Exact match = pass
- [ ] `test_phase_check_extra_subagents_allowed` - Superset = pass

### Checkpoint Validation (AC#3)
- [ ] `test_phase_check_validates_checkpoint_passed` - true = pass
- [ ] `test_phase_check_rejects_checkpoint_failed` - false = fail
- [ ] `test_phase_check_rejects_missing_checkpoint_flag` - Missing = fail
- [ ] `test_phase_check_checkpoint_overrides_subagents` - Checkpoint blocks progression

### Record Subagent (AC#4)
- [ ] `test_record_subagent_appends_entry` - Appends to invocation list
- [ ] `test_record_subagent_append_only_semantics` - Idempotent (no duplicates)
- [ ] `test_record_subagent_errors_on_missing_state_file` - Returns 2 for missing state
- [ ] `test_record_subagent_invalid_phase_id` - Returns 2 for invalid phase

### Complete Phase (AC#5)
- [ ] `test_complete_phase_marks_completion` - Status becomes "completed"
- [ ] `test_complete_phase_requires_all_subagents` - Blocks if subagents missing (BR-002)
- [ ] `test_complete_phase_requires_checkpoint_passed` - Blocks if checkpoint failed (BR-003)
- [ ] `test_complete_phase_errors_on_missing_state_file` - Returns 2 for missing state
- [ ] `test_complete_phase_advances_current_phase` - current_phase advances to next

### Exit Codes (AC#6)
- [ ] `test_exit_code_zero_allows_progression` - Exit code = 0 for success
- [ ] `test_exit_code_one_blocks_progression` - Exit code = 1 for blocked
- [ ] `test_exit_code_two_signals_error` - Exit code = 2 for error
- [ ] `test_exit_codes_only_0_1_2` - Only valid codes are 0, 1, 2

### Edge Cases
- [ ] All 8 edge case tests pass
- [ ] Story ID validation (format STORY-XXX)
- [ ] Phase ID validation (range 01-10)
- [ ] Corrupt JSON handling
- [ ] Phase ordering enforcement
- [ ] Idempotent operations

### Non-Functional Requirements
- [ ] Performance: phase-check < 30ms
- [ ] Error messages: specific and actionable

---

## Key Implementation Requirements

From the tests, the implementation must:

1. **Exit Codes Only**: Return ONLY 0, 1, or 2
   - 0 = proceed (validation passed)
   - 1 = blocked (validation failed)
   - 2 = error (state file missing/invalid)

2. **Story ID Validation**: Match pattern STORY-XXX
   - Accept: STORY-001, STORY-149, STORY-999
   - Reject: STORY-01, STORY-0001, story-001, STORY_001

3. **Phase ID Validation**: Match range 01-10
   - Accept: 01, 02, ..., 10
   - Reject: 00, 11, 001, 1

4. **Subagent Validation**: All required subagents must be invoked
   - Superset of required is acceptable (extra subagents OK)
   - Missing any required subagent = fail

5. **Checkpoint Validation**: checkpoint_passed must be true
   - Missing or false = fail
   - Overrides other conditions

6. **Phase Ordering**: Must complete phases sequentially
   - Cannot skip phases (01→03 is blocked)
   - Current phase determined from state file

7. **Idempotent Operations**: record-subagent safe to call multiple times
   - Duplicate subagent names not added to list
   - Same exit code on repeat calls

8. **Error Messages**: Specific and actionable
   - Indicate missing subagent name
   - Explain checkpoint failure reason
   - Suggest remediation steps

---

## Integration with PhaseState (STORY-148)

The implementation will use the `PhaseState` class from STORY-148:

```python
from installer.phase_state import PhaseState

ps = PhaseState(project_root=Path(...))
state = ps.read("STORY-001")
ps.record_subagent("STORY-001", "01", "git-validator")
ps.complete_phase("STORY-001", "01", checkpoint_passed=True)
```

All tests use manual phase state fixtures, so they can run before STORY-148 is complete.

---

## Expected Metrics After Implementation

| Metric | Target |
|--------|--------|
| Test Pass Rate | 100% (40/40) |
| Code Coverage | >= 95% |
| Lines of Code | < 300 |
| Cyclomatic Complexity | < 10 per function |
| PEP 8 Compliance | 100% |
| Anti-pattern Violations | 0 |

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'installer'"

**Cause**: PYTHONPATH not set correctly

**Fix**:
```bash
cd /mnt/c/Projects/DevForgeAI2
export PYTHONPATH=".:$PYTHONPATH"
pytest tests/unit/STORY-149/
```

### "SyntaxError in test file"

**Cause**: Python version < 3.9

**Fix**: Ensure Python 3.9+ is installed:
```bash
python3 --version  # Should show 3.9+
```

### Tests still pass when they shouldn't

**Cause**: Implementation exists but tests don't properly validate behavior

**Fix**: Review test assertions and PhaseState integration points

---

## Next Steps

1. **Implement** `installer/validate_phase_completion.py` with:
   - `validate_phase_check()` function
   - `validate_subagents_invoked()` function
   - `validate_checkpoint_passed()` function
   - `phase_check_command()` CLI command
   - `record_subagent_command()` CLI command
   - `complete_phase_command()` CLI command

2. **Run tests**: Execute `pytest tests/unit/STORY-149/ -v`

3. **Verify all 40 tests pass**

4. **Check coverage**: Ensure >= 95% code coverage

5. **Code review**: Ensure no anti-patterns, PEP 8 compliance

6. **Integration test**: Verify phase transitions work end-to-end

---

## References

- **Story File**: `devforgeai/specs/Stories/STORY-149-phase-validation-script.story.md`
- **PhaseState Module**: `installer/phase_state.py` (STORY-148)
- **Tech Stack**: `devforgeai/specs/context/tech-stack.md` (pytest required)
- **Coding Standards**: `devforgeai/specs/context/coding-standards.md` (Python/pytest patterns)
- **Plan File**: `.claude/plans/STORY-149-test-generation-summary.md`

---

**Test Suite Generated**: 2025-12-28
**Test Framework**: pytest 7.0+
**Status**: Ready for Phase 02 (TDD Green - Implementation)
