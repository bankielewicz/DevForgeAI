# STORY-153: Skill Validation Integration - Test Generation Plan

**Story ID**: STORY-153
**Created**: 2025-12-29
**Status**: Planning Phase
**Test Framework**: Bash (for Markdown content validation via Grep)

---

## Executive Summary

This plan generates comprehensive failing tests for STORY-153 (Skill Validation Integration) that validate the devforgeai-development SKILL.md file contains required validation calls at each phase transition point.

**Key Objective**: Create 7 test functions that verify:
1. init-state validation call in Phase 00
2. phase-check blocking at each phase transition
3. record-subagent calls after Task invocations
4. complete-phase calls at phase endpoints
5. All 10 phases have appropriate validation
6. Error handling includes HALT on failure
7. Backward compatibility warning for missing CLI

---

## Test Framework Selection

**Framework**: Bash/Grep-based testing (per AC specs)

**Rationale**:
- STORY-153 validates Markdown content patterns in SKILL.md
- Grep patterns most efficient for markdown header/content validation
- Bash test framework allows direct pattern matching of file content
- No external test dependencies required

**Test Location**: `/mnt/c/Projects/DevForgeAI2/tests/STORY-153/`

---

## Test File Structure

```
tests/STORY-153/
├── test-validation-calls.sh          # Main test suite
├── fixtures/
│   ├── expected-init-state-call.txt  # Expected pattern
│   ├── expected-phase-check.txt      # Expected pattern
│   └── expected-complete-phase.txt   # Expected pattern
└── results/
    └── test-results.txt              # Test execution results
```

---

## Test Cases (7 tests per AC)

### Test 1: test_init_state_called_at_start
**AC**: AC#4 - Initialize state file at workflow start
**Purpose**: Verify SKILL.md has `devforgeai-validate init-state` call in Phase 00
**Assertion**: Grep for pattern `devforgeai-validate init-state` in phase-01 section OR phase initialization section
**Expected Result**: PASS - Pattern found
**Current Result**: FAIL - No init-state call yet (TDD Red)

### Test 2: test_phase_check_blocks_incomplete
**AC**: AC#1 - Add validation call before each phase transition
**Purpose**: Verify all phases 01-10 have `devforgeai-validate phase-check` calls
**Assertion**: Count occurrences of `phase-check` in SKILL.md, verify >= 9 occurrences (phases 01-10 minus phase 00)
**Expected Result**: PASS - >= 9 phase-check calls found
**Current Result**: FAIL - No phase-check calls exist (TDD Red)

### Test 3: test_subagent_recorded_after_task
**AC**: AC#2 - Add subagent recording after each subagent invocation
**Purpose**: Verify `devforgeai-validate record-subagent` calls exist after Task invocations
**Assertion**: Search for pattern of Task followed by record-subagent call
**Expected Result**: PASS - record-subagent patterns found
**Current Result**: FAIL - No record-subagent calls (TDD Red)

### Test 4: test_complete_phase_called
**AC**: AC#3 - Add checkpoint completion call at phase end
**Purpose**: Verify `devforgeai-validate complete-phase` calls exist at phase ends
**Assertion**: Count occurrences of `complete-phase` in SKILL.md, verify >= 10 occurrences (one per phase)
**Expected Result**: PASS - >= 10 complete-phase calls found
**Current Result**: FAIL - No complete-phase calls (TDD Red)

### Test 5: test_all_phases_have_validation
**AC**: AC#1, AC#3 - All phases have validation calls
**Purpose**: Meta-test verifying that every phase (except 00) has complete validation structure
**Assertion**: For each phase section, verify presence of phase-check and complete-phase
**Expected Result**: PASS - All 10 phases have appropriate validation
**Current Result**: FAIL - Validation structure incomplete (TDD Red)

### Test 6: test_halt_on_validation_failure
**AC**: AC#5 - Clear error handling with HALT
**Purpose**: Verify SKILL.md contains error handling instructions for validation failures
**Assertion**: Search for pattern `HALT` in context of validation failure handling
**Assertion**: Search for pattern `non-zero` or `exit code` in error handling section
**Expected Result**: PASS - Error handling with HALT found
**Current Result**: FAIL - Error handling not yet implemented (TDD Red)

### Test 7: test_backward_compatibility
**AC**: AC#6 - Backward compatibility with missing CLI
**Purpose**: Verify SKILL.md includes warning/continue logic if CLI not installed
**Assertion**: Search for pattern about warning, CLI not available, or continue option
**Expected Result**: PASS - Backward compatibility warning found
**Current Result**: FAIL - Backward compatibility not yet implemented (TDD Red)

### Test 8 (Optional): test_validation_locations_complete
**Tech Spec**: validation-call-locations.yaml required
**Purpose**: Verify validation-call-locations.yaml file created with all 10 phases
**Assertion**: File exists and contains all phase IDs 00-10
**Expected Result**: PASS - File exists with complete phase coverage
**Current Result**: FAIL - File doesn't exist (TDD Red)

### Test 9 (Optional): test_pattern_consistency
**Tech Spec**: BR-001 - Validation calls use consistent pattern
**Purpose**: Verify all validation calls follow same pattern/format
**Assertion**: All phase-check calls have same format, all complete-phase calls same format
**Expected Result**: PASS - 100% pattern consistency
**Current Result**: FAIL - Patterns inconsistent (TDD Red)

---

## Test Execution Plan

### Phase: Red (Failing Tests)

1. **Create test file**: `/mnt/c/Projects/DevForgeAI2/tests/STORY-153/test-validation-calls.sh`
   - Write all 7 test functions
   - Each test should FAIL initially (no implementation yet)

2. **Create fixtures directory**: `/mnt/c/Projects/DevForgeAI2/tests/STORY-153/fixtures/`
   - Expected pattern files for reference

3. **Run tests**:
   ```bash
   cd /mnt/c/Projects/DevForgeAI2
   bash tests/STORY-153/test-validation-calls.sh
   ```
   - Expected: All tests FAIL (0/7 passing)

### Phase: Green (Implementation)
- Developer (via devforgeai-development skill) implements changes to SKILL.md
- Add validation calls per acceptance criteria
- Create validation-call-locations.yaml

### Phase: Refactoring
- Improve test patterns/readability
- Extract common test logic
- Add performance benchmarks if applicable

---

## Test Implementation Details

### Test File: test-validation-calls.sh

```bash
#!/bin/bash
# STORY-153: Skill Validation Integration - Test Suite

set -euo pipefail

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SKILL_FILE="${PROJECT_ROOT}/.claude/skills/devforgeai-development/SKILL.md"
RESULTS_FILE="${PROJECT_ROOT}/tests/STORY-153/results/test-results.txt"

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Helper function: assert_pattern_exists
assert_pattern_exists() {
    local pattern="$1"
    local file="$2"
    local test_name="$3"

    if grep -q "$pattern" "$file"; then
        echo "PASS: $test_name"
        ((TESTS_PASSED++))
        return 0
    else
        echo "FAIL: $test_name"
        echo "  Expected pattern: $pattern"
        echo "  File: $file"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Helper function: assert_pattern_count
assert_pattern_count() {
    local pattern="$1"
    local file="$2"
    local expected_count=$3
    local test_name="$4"

    local actual_count=$(grep -c "$pattern" "$file" || echo 0)

    if [ "$actual_count" -ge "$expected_count" ]; then
        echo "PASS: $test_name (found $actual_count >= $expected_count)"
        ((TESTS_PASSED++))
        return 0
    else
        echo "FAIL: $test_name (found $actual_count, expected >= $expected_count)"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Test 1: init_state_called_at_start
test_init_state_called_at_start() {
    ((TESTS_RUN++))
    assert_pattern_exists \
        "devforgeai-validate init-state" \
        "$SKILL_FILE" \
        "test_init_state_called_at_start"
}

# Test 2: phase_check_blocks_incomplete
test_phase_check_blocks_incomplete() {
    ((TESTS_RUN++))
    assert_pattern_count \
        "devforgeai-validate phase-check" \
        "$SKILL_FILE" \
        9 \
        "test_phase_check_blocks_incomplete"
}

# Test 3: subagent_recorded_after_task
test_subagent_recorded_after_task() {
    ((TESTS_RUN++))
    assert_pattern_exists \
        "devforgeai-validate record-subagent" \
        "$SKILL_FILE" \
        "test_subagent_recorded_after_task"
}

# Test 4: complete_phase_called
test_complete_phase_called() {
    ((TESTS_RUN++))
    assert_pattern_count \
        "devforgeai-validate complete-phase" \
        "$SKILL_FILE" \
        10 \
        "test_complete_phase_called"
}

# Test 5: all_phases_have_validation
test_all_phases_have_validation() {
    ((TESTS_RUN++))
    # Check that phase sections exist and contain validation calls
    local phase_count=$(grep -c "^## Phase" "$SKILL_FILE" || echo 0)

    if [ "$phase_count" -ge 10 ]; then
        echo "PASS: test_all_phases_have_validation (found $phase_count phases)"
        ((TESTS_PASSED++))
    else
        echo "FAIL: test_all_phases_have_validation (found $phase_count phases, expected >= 10)"
        ((TESTS_FAILED++))
    fi
}

# Test 6: halt_on_validation_failure
test_halt_on_validation_failure() {
    ((TESTS_RUN++))
    # Look for HALT in context of validation error handling
    if grep -A 3 "non-zero exit code\|validation failure" "$SKILL_FILE" | grep -q "HALT"; then
        echo "PASS: test_halt_on_validation_failure"
        ((TESTS_PASSED++))
    else
        echo "FAIL: test_halt_on_validation_failure - HALT not found in error handling"
        ((TESTS_FAILED++))
    fi
}

# Test 7: backward_compatibility
test_backward_compatibility() {
    ((TESTS_RUN++))
    # Look for warning or continue logic if CLI not installed
    if grep -q "Phase enforcement not available\|CLI not installed\|pip install devforgeai" "$SKILL_FILE"; then
        echo "PASS: test_backward_compatibility"
        ((TESTS_PASSED++))
    else
        echo "FAIL: test_backward_compatibility - warning message not found"
        ((TESTS_FAILED++))
    fi
}

# Main execution
main() {
    echo "=========================================="
    echo "STORY-153: Skill Validation Integration"
    echo "Test Suite Execution"
    echo "=========================================="
    echo ""

    # Create results directory
    mkdir -p "${PROJECT_ROOT}/tests/STORY-153/results"

    # Run all tests
    test_init_state_called_at_start
    test_phase_check_blocks_incomplete
    test_subagent_recorded_after_task
    test_complete_phase_called
    test_all_phases_have_validation
    test_halt_on_validation_failure
    test_backward_compatibility

    # Report summary
    echo ""
    echo "=========================================="
    echo "Test Summary"
    echo "=========================================="
    echo "Tests Run: $TESTS_RUN"
    echo "Tests Passed: $TESTS_PASSED"
    echo "Tests Failed: $TESTS_FAILED"
    echo "Pass Rate: $(( TESTS_PASSED * 100 / TESTS_RUN ))%"
    echo "=========================================="

    # Write results to file
    {
        echo "STORY-153 Test Results - $(date)"
        echo "Tests Run: $TESTS_RUN"
        echo "Tests Passed: $TESTS_PASSED"
        echo "Tests Failed: $TESTS_FAILED"
        echo "Pass Rate: $(( TESTS_PASSED * 100 / TESTS_RUN ))%"
    } > "$RESULTS_FILE"

    # Exit with failure if any tests failed (TDD Red phase)
    [ "$TESTS_FAILED" -eq 0 ] && exit 0 || exit 1
}

main "$@"
```

---

## Progress Checkpoints

### Checkpoint 1: Test File Created
- [ ] `/mnt/c/Projects/DevForgeAI2/tests/STORY-153/test-validation-calls.sh` created
- [ ] All 7 test functions defined
- [ ] Test file is executable
- [ ] Test execution runs all tests

### Checkpoint 2: Tests Fail (TDD Red)
- [ ] Run test suite: `bash tests/STORY-153/test-validation-calls.sh`
- [ ] All tests FAIL (expected - implementation not yet done)
- [ ] Test results saved to `tests/STORY-153/results/test-results.txt`
- [ ] Pass rate: 0/7 (0%)

### Checkpoint 3: Implementation Phase
*(Handled by devforgeai-development skill in Phase 03)*
- [ ] SKILL.md updated with init-state call
- [ ] SKILL.md updated with phase-check calls
- [ ] SKILL.md updated with record-subagent calls
- [ ] SKILL.md updated with complete-phase calls
- [ ] Error handling with HALT implemented
- [ ] Backward compatibility warning added

### Checkpoint 4: Tests Pass (TDD Green)
- [ ] Run test suite again
- [ ] Tests should progressively pass as implementation adds validation calls
- [ ] Target: All tests PASS (7/7 = 100%)

---

## Implementation Verification

### Validation Call Patterns

**Pattern 1: init-state call** (in Phase 00/Preflight section)
```
Bash(command="devforgeai-validate init-state {story_id}")
```

**Pattern 2: phase-check call** (at start of phases 01-10)
```
Bash(command="devforgeai-validate phase-check {story_id} {phase_id}")
IF exit_code != 0: HALT
```

**Pattern 3: record-subagent call** (after each Task invocation)
```
Task(subagent_type="test-automator", ...)
Bash(command="devforgeai-validate record-subagent {story_id} {phase_id} {subagent_name}")
```

**Pattern 4: complete-phase call** (at end of each phase)
```
Bash(command="devforgeai-validate complete-phase {story_id} {phase_id} --checkpoint-passed")
```

---

## Additional Artifacts

### validation-call-locations.yaml
**Location**: `/mnt/c/Projects/DevForgeAI2/devforgeai/config/validation-call-locations.yaml`

**Purpose**: Mapping of where validation calls are inserted in SKILL.md

**Content**: (per AC spec) - 10 phases with validation locations and subagent references

---

## Test Execution Commands

### Run all tests:
```bash
bash /mnt/c/Projects/DevForgeAI2/tests/STORY-153/test-validation-calls.sh
```

### Expected output (TDD Red - All FAIL):
```
==========================================
STORY-153: Skill Validation Integration
Test Suite Execution
==========================================

FAIL: test_init_state_called_at_start
FAIL: test_phase_check_blocks_incomplete
FAIL: test_subagent_recorded_after_task
FAIL: test_complete_phase_called
FAIL: test_all_phases_have_validation
FAIL: test_halt_on_validation_failure
FAIL: test_backward_compatibility

==========================================
Test Summary
==========================================
Tests Run: 7
Tests Passed: 0
Tests Failed: 7
Pass Rate: 0%
==========================================
```

---

## References

- **Story File**: `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-153-skill-validation-integration.story.md`
- **Current SKILL.md**: `/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-development/SKILL.md`
- **Test Framework Decision**: Bash/Grep (per AC and tech-stack.md)
- **TDD Workflow**: Red → Green → Refactor

---

## Next Steps (After Plan Approval)

1. **Phase 02 (Test-First)**:
   - Create test file with all 7 test functions
   - Run tests to confirm all FAIL
   - Commit test file

2. **Phase 03 (Implementation)**:
   - Update SKILL.md with validation calls per AC
   - Create validation-call-locations.yaml
   - Run tests iteratively until all PASS

3. **Phase 04 (Refactoring)**:
   - Improve test code quality
   - Add documentation
   - Optimize patterns

4. **Phase 05 (Integration)**:
   - Integration test of full workflow
   - Verify validation enforcement during real /dev execution

---

**Status**: Ready for execution
**Last Updated**: 2025-12-29
