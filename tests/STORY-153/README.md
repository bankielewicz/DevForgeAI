# STORY-153: Skill Validation Integration - Test Suite

**Story**: Skill Validation Integration
**Status**: TDD Red Phase (All tests failing - expected)
**Framework**: Bash/Grep
**Date**: 2025-12-29

---

## Overview

This test suite validates that the devforgeai-development SKILL.md file includes all required validation calls for phase enforcement in the TDD workflow.

**Test Results**: 0/8 PASS (0%)

---

## Test Execution

### Run All Tests
```bash
bash tests/STORY-153/test-validation-calls.sh
```

### Expected Output (TDD Red Phase)
```
==========================================
STORY-153: Skill Validation Integration
Test Suite - TDD Red Phase
==========================================

Running tests...

FAIL: test_init_state_called_at_start
  Expected pattern: devforgeai-validate init-state
  File: ...

FAIL: test_phase_check_blocks_incomplete
  ...

[... 8 test results ...]

==========================================
Test Summary
==========================================
Tests Run: 8
Tests Passed: 0
Tests Failed: 8
Pass Rate: 0%
==========================================
```

---

## Test Cases

### 1. test_init_state_called_at_start
**Acceptance Criteria**: AC#4
**Purpose**: Verify SKILL.md initializes phase state tracking

Searches for pattern: `devforgeai-validate init-state`

**Status**: FAIL (not yet implemented)

### 2. test_phase_check_blocks_incomplete
**Acceptance Criteria**: AC#1
**Purpose**: Verify phase transitions check previous phase completion

Searches for pattern: `devforgeai-validate phase-check`
Expects: >= 9 occurrences (phases 01-10)

**Status**: FAIL (found 3, need 9+)

### 3. test_subagent_recorded_after_task
**Acceptance Criteria**: AC#2
**Purpose**: Verify subagent invocations are recorded

Searches for pattern: `devforgeai-validate record-subagent`

**Status**: FAIL (not yet implemented)

### 4. test_complete_phase_called
**Acceptance Criteria**: AC#3
**Purpose**: Verify phase completion is recorded

Searches for pattern: `devforgeai-validate complete-phase`
Expects: >= 10 occurrences (one per phase)

**Status**: FAIL (found 0, need 10+)

### 5. test_all_phases_have_validation
**Acceptance Criteria**: AC#1, AC#3
**Purpose**: Verify all 10 phases exist

Searches for: Phase section headers (`## Phase`)
Expects: >= 10 sections

**Status**: FAIL (found 4 phases)

### 6. test_halt_on_validation_failure
**Acceptance Criteria**: AC#5
**Purpose**: Verify error handling with HALT instruction

Searches for: Both `HALT` and `exit code` patterns

**Status**: FAIL (not yet implemented)

### 7. test_backward_compatibility
**Acceptance Criteria**: AC#6
**Purpose**: Verify warning for missing CLI

Searches for: `warning`, `CLI not installed`, `pip install`, or `backward`

**Status**: FAIL (not yet implemented)

### 8. test_validation_call_locations_config
**Technical Spec**: Validation locations YAML
**Purpose**: Verify configuration file exists

File: `devforgeai/config/validation-call-locations.yaml`

**Status**: FAIL (file not yet created)

---

## Test Framework Details

**Language**: Bash (native to Claude Code Terminal)

**Dependencies**: None (uses grep, standard utilities)

**Test Helpers**:
- `assert_pattern_exists()` - Grep pattern existence check
- `assert_pattern_count()` - Grep pattern count assertion
- `assert_file_exists()` - File existence check

**Line Count**: 294 lines total

---

## Roadmap to All Tests Passing

### Phase 03: Implementation (TDD Green)
The following changes to SKILL.md will make tests PASS:

1. **Add init-state call** in Phase 00 (Preflight section)
   - Status: Makes test #1 PASS

2. **Add 9+ phase-check calls** at phase transition points
   - Status: Makes test #2 PASS
   - Additional phase definitions: Makes test #5 PASS

3. **Add record-subagent calls** after each Task invocation
   - Status: Makes test #3 PASS

4. **Add 10+ complete-phase calls** at end of each phase
   - Status: Makes test #4 PASS

5. **Add error handling** with HALT instruction
   - Status: Makes test #6 PASS

6. **Add backward compatibility** warning message
   - Status: Makes test #7 PASS

7. **Create validation-call-locations.yaml** config
   - Status: Makes test #8 PASS

### Phase 04: Refactoring
- Improve test code quality
- Add edge case coverage
- Optimize patterns

### Phase 05: Integration
- End-to-end validation test
- Verify enforcement system works in real /dev workflow

---

## Files

```
tests/STORY-153/
├── README.md                          # This file
├── test-validation-calls.sh           # Main test suite
└── results/
    └── test-results.txt               # Test execution results
```

---

## Key Metrics

| Metric | Value |
|--------|-------|
| Total Tests | 8 |
| Currently Passing | 0 (TDD Red) |
| Test File Size | 9.7 KB (294 lines) |
| Execution Time | <1 second |
| External Dependencies | None |

---

## TDD Workflow Status

**Current Phase**: Red (Tests Failing)
- All 8 tests FAIL ✓ (expected and correct)
- SKILL.md modifications not yet implemented
- Test framework confirmed working

**Next Phase**: Green (Implementation)
- Modify SKILL.md per AC requirements
- Re-run tests until all PASS
- Target: 8/8 PASS (100%)

**Final Phase**: Refactor (Improvement)
- Improve test code quality
- Add documentation
- Optimize patterns

---

## References

- **Story File**: `devforgeai/specs/Stories/STORY-153-skill-validation-integration.story.md`
- **SKILL.md**: `.claude/skills/devforgeai-development/SKILL.md`
- **Test Plan**: `.claude/plans/STORY-153-test-generation-plan.md`
- **Summary**: `.claude/plans/STORY-153-test-generation-summary.md`

---

## Troubleshooting

### Tests don't run
```bash
# Ensure file is executable
chmod +x tests/STORY-153/test-validation-calls.sh

# Run with explicit bash
bash tests/STORY-153/test-validation-calls.sh
```

### All tests already passing
If all tests pass before implementation, the test file may be checking patterns that already exist in SKILL.md. Verify:
1. Current SKILL.md has validation calls already
2. Tests are checking for the NEW patterns to be added
3. Adjust pattern matching if needed

### Grep patterns not matching
- Check for whitespace/line ending issues
- Verify pattern format in SKILL.md
- Run individual grep tests:
  ```bash
  grep "devforgeai-validate init-state" .claude/skills/devforgeai-development/SKILL.md
  ```

---

**Last Updated**: 2025-12-29
**Status**: Ready for Implementation Phase
