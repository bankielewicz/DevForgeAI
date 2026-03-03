# STORY-149: Phase Completion Validation Script - Test Generation Summary

**Status**: Test Generation Complete (TDD Red Phase)
**Created**: 2025-12-28
**Story ID**: STORY-149
**Epic**: EPIC-031

---

## Test Generation Overview

Generated comprehensive failing test suite for STORY-149 (Phase Completion Validation Script) following Test-Driven Development (TDD) Red phase principles.

**Key Principle**: ALL TESTS ARE EXPECTED TO FAIL INITIALLY - no implementation code exists yet. Tests validate they are properly written by expecting ModuleNotFoundError/ImportError/AttributeError from non-existent implementation module.

---

## Test File Location

**File**: `/mnt/c/Projects/DevForgeAI2/tests/unit/STORY-149/test_validate_phase_completion.py`
**Framework**: pytest
**Total Test Classes**: 10
**Total Test Functions**: 47
**Lines of Code**: 850+

---

## Test Coverage Summary

### Coverage by Acceptance Criteria

#### AC#1: CLI command validates phase completion
**Tests**: 5 functions
- `test_phase_check_validates_completion_exit_code_zero` - Valid phase returns exit code 0
- `test_phase_check_blocks_incomplete_phase` - Incomplete phase returns exit code 1
- `test_phase_check_errors_on_missing_state_file` - Missing state file returns exit code 2
- `test_phase_check_invalid_story_id_format` - Invalid STORY-XXX format rejected
- `test_phase_check_invalid_phase_ids` - Phase IDs outside 01-10 range rejected

**Test Class**: `TestPhaseCheckCommand`

#### AC#2: Validates all required subagents invoked
**Tests**: 5 functions
- `test_phase_check_validates_all_subagents_invoked` - All subagents present = pass
- `test_phase_check_rejects_missing_subagents` - Any missing subagent = fail
- `test_phase_check_rejects_all_missing_subagents` - Empty invoked list = fail
- `test_phase_check_exact_match_subagents` - Exact match passes
- `test_phase_check_extra_subagents_allowed` - Superset of required is acceptable

**Test Class**: `TestSubagentValidation`

#### AC#3: Validates checkpoint passed flag
**Tests**: 4 functions
- `test_phase_check_validates_checkpoint_passed` - checkpoint_passed=true = pass
- `test_phase_check_rejects_checkpoint_failed` - checkpoint_passed=false = fail
- `test_phase_check_rejects_missing_checkpoint_flag` - Missing flag defaults to failed
- `test_phase_check_checkpoint_overrides_subagents` - Checkpoint failure blocks despite all subagents

**Test Class**: `TestCheckpointValidation`

#### AC#4: Record subagent invocation command
**Tests**: 4 functions
- `test_record_subagent_appends_entry` - Subagent appended to invocation list
- `test_record_subagent_append_only_semantics` - Idempotent (no duplicates)
- `test_record_subagent_errors_on_missing_state_file` - Missing state file = error
- `test_record_subagent_invalid_phase_id` - Invalid phase ID = error

**Test Class**: `TestRecordSubagentCommand`

#### AC#5: Complete phase command marks completion
**Tests**: 5 functions
- `test_complete_phase_marks_completion` - Phase status becomes "completed"
- `test_complete_phase_requires_all_subagents` - Missing subagents block completion (BR-002)
- `test_complete_phase_requires_checkpoint_passed` - Failed checkpoint blocks completion (BR-003)
- `test_complete_phase_errors_on_missing_state_file` - Missing state file = error
- `test_complete_phase_advances_current_phase` - current_phase pointer advances to next phase

**Test Class**: `TestCompletePhaseCommand`

#### AC#6: Exit codes enable external enforcement
**Tests**: 4 functions
- `test_exit_code_zero_allows_progression` - Exit code 0 = proceed
- `test_exit_code_one_blocks_progression` - Exit code 1 = blocked
- `test_exit_code_two_signals_error` - Exit code 2 = error
- `test_exit_codes_only_0_1_2` - Only valid codes are 0, 1, 2

**Test Class**: `TestExitCodeEnforcement`

---

## Edge Cases Tested

**Test Class**: `TestEdgeCases` (8 functions)

1. **Story ID Validation**
   - Rejects STORY-01 (too short)
   - Rejects STORY-0001 (too long)
   - Rejects story-001 (lowercase)
   - Rejects STORY_001 (underscore)
   - Rejects empty string

2. **Phase ID Validation**
   - Rejects phase "00" (below range)
   - Rejects phase "11" (above range)
   - Rejects "001" (three digits)
   - Rejects "1" (single digit)

3. **Corrupt State Files**
   - Invalid JSON in state file → exit code 2
   - Empty state file → exit code 2

4. **Phase Ordering**
   - Cannot skip phases (transition 01→03 blocked)
   - Must complete sequentially

5. **Empty Requirements**
   - Phases with no required subagents (07, 08, 09) = valid with empty lists

6. **Idempotency**
   - Multiple record-subagent calls with same subagent = no duplicates

---

## Non-Functional Requirements Tested

**Test Class**: `TestNonFunctionalRequirements` (2 functions)

1. **Performance** (NFR-001)
   - phase-check command < 30ms (reads state file + validates)
   - Test: `test_phase_check_performance_under_30ms`

2. **Error Messages** (NFR-002)
   - Specific, actionable error messages
   - Indicate which subagent missing, what checkpoint issue, etc.
   - Test: `test_error_messages_are_specific_and_actionable`

---

## Integration with PhaseState Module (STORY-148)

**Test Class**: `TestIntegrationWithPhaseState` (3 functions)

1. **phase-check Integration**
   - Uses PhaseState module to read state
   - Delegates to `validate_phase_check()` function
   - Returns tuple of (exit_code, message)

2. **record-subagent Integration**
   - Delegates to `PhaseState.record_subagent()`
   - Passes correct parameters to PhaseState

3. **complete-phase Integration**
   - Delegates to `PhaseState.complete_phase()`
   - Passes correct parameters to PhaseState

---

## Fixture Definitions

### `temp_project_dir`
Creates temporary project directory with `devforgeai/workflows/` subdirectory for state files.

### `phase_state_fixture`
Complete, valid phase state structure:
- Phase 01: completed with all subagents and checkpoint passed
- Phase 02-03: pending
- Suitable for positive test cases

### `incomplete_phase_state`
Phase state with missing subagents (tech-stack-detector):
- Phase 01: missing one required subagent
- Suitable for validation failure tests

### `checkpoint_failed_state`
Phase state where checkpoint validation failed:
- All subagents invoked but checkpoint_passed=false
- Suitable for checkpoint failure tests

---

## Expected Behavior (TDD Red Phase)

**All tests WILL FAIL initially because:**

1. Module `installer.validate_phase_completion` does not exist
2. Functions `phase_check_command()`, `record_subagent_command()`, etc. are not implemented
3. Constants `EXIT_CODE_PROCEED`, `EXIT_CODE_BLOCKED`, `EXIT_CODE_ERROR` are undefined

**Test structure explicitly expects these failures:**
```python
try:
    from installer.validate_phase_completion import ...
except ImportError:
    # Expected to fail in TDD Red phase
    pass
```

---

## Running the Tests

### Run all tests:
```bash
cd /mnt/c/Projects/DevForgeAI2
export PYTHONPATH=".:$PYTHONPATH"
pytest tests/unit/STORY-149/test_validate_phase_completion.py -v
```

### Run specific test class:
```bash
pytest tests/unit/STORY-149/test_validate_phase_completion.py::TestPhaseCheckCommand -v
```

### Run specific test function:
```bash
pytest tests/unit/STORY-149/test_validate_phase_completion.py::TestPhaseCheckCommand::test_phase_check_validates_completion_exit_code_zero -v
```

### With coverage report:
```bash
pytest tests/unit/STORY-149/test_validate_phase_completion.py --cov=installer --cov-report=term-missing
```

---

## Success Criteria (After Implementation)

**Phase 02 (Green) Success when:**
- [ ] All 47 tests pass (100% pass rate)
- [ ] Exit codes return only 0, 1, or 2
- [ ] phase-check validates completion correctly
- [ ] record-subagent appends without duplicates (idempotent)
- [ ] complete-phase marks completion and advances phase
- [ ] All required subagents validated before completion
- [ ] Checkpoint flag required before completion
- [ ] Story IDs and phase IDs validated correctly
- [ ] Error conditions return appropriate exit codes
- [ ] Error messages are specific and actionable

**Phase 04 (Refactoring) Success when:**
- [ ] Code follows PEP 8 and coding standards
- [ ] No anti-patterns detected
- [ ] Coverage >= 95% for business logic
- [ ] Code is DRY (no duplication)
- [ ] Functions have single responsibility
- [ ] Type hints present

---

## Test Metrics

| Metric | Value |
|--------|-------|
| Total Test Classes | 10 |
| Total Test Functions | 47 |
| Test File Size | ~850 lines |
| Lines per Test | ~18 lines average |
| AC Coverage | 100% (all 6 ACs tested) |
| Edge Cases | 8 scenarios |
| NFRs Tested | 2 (performance, error messages) |
| Integration Tests | 3 (with PhaseState) |

---

## Implementation Roadmap

**Phase 02 (Green): Implement these functions in `installer/validate_phase_completion.py`**

1. `validate_phase_check(story_id, from_phase, to_phase, project_root)` → (exit_code, message)
2. `validate_subagents_invoked(required, invoked)` → bool
3. `validate_checkpoint_passed(checkpoint_passed)` → bool
4. `phase_check_command(story_id, from_phase, to_phase, project_root)` → int (exit code)
5. `record_subagent_command(story_id, phase_id, subagent_name, project_root)` → int (exit code)
6. `complete_phase_command(story_id, phase_id, checkpoint_passed, project_root)` → int (exit code)
7. `ValidatePhaseCompletion` class (if needed for CLI entry points)

**Implementation Requirements:**
- Use existing `installer.phase_state.PhaseState` class to manage state files
- Return only exit codes 0, 1, or 2
- Validate story ID matches STORY-XXX pattern
- Validate phase IDs are 01-10
- Provide specific error messages (missing subagent X, checkpoint failed, etc.)
- Support idempotent record-subagent (no duplicates)
- Enforce phase completion order (cannot skip phases)

---

## Dependencies

- **Upstream (STORY-148)**: PhaseState class must be implemented and working
  - All tests can run without STORY-148 completion (using manual phase state fixtures)
  - Production code will depend on STORY-148 PhaseState class

- **Downstream (STORY-150, STORY-152)**: These stories depend on phase-check CLI working
  - Cannot proceed with testing those stories until STORY-149 implementation complete

---

## Notes for Developer

1. **TDD Discipline**: Don't look at tests and implement; implement to MAKE tests pass
2. **Start with simplest test**: `test_phase_check_validates_completion_exit_code_zero`
3. **Validate assumptions**: Each test verifies specific behavior; follow them exactly
4. **Error messages**: Look at test scenarios to understand what errors should say
5. **Exit codes**: Strictly 0, 1, or 2 - no other codes allowed
6. **Idempotency**: record-subagent must be safe to call multiple times
7. **Phase ordering**: Tests verify sequential completion - enforce this rigorously

---

## Related Files

| File | Purpose |
|------|---------|
| `/mnt/c/Projects/DevForgeAI2/installer/phase_state.py` | PhaseState class (STORY-148) |
| `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-149-phase-validation-script.story.md` | Story file with full AC/Tech Spec |
| `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/context/coding-standards.md` | Python/pytest standards |
| `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/context/tech-stack.md` | pytest framework requirement |

---

**Status**: Ready for Phase 02 (TDD Green) Implementation
**Next**: Implement `installer/validate_phase_completion.py` to make all 47 tests pass
