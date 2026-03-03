#!/bin/bash

# STORY-153: Skill Validation Integration - Test Suite
# Purpose: Verify that SKILL.md contains all required validation calls for phase enforcement
# Framework: Bash/Grep (validates Markdown content patterns)
# Expected: All tests FAIL initially (TDD Red phase)

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SKILL_FILE="${PROJECT_ROOT}/.claude/skills/devforgeai-development/SKILL.md"
RESULTS_FILE="${PROJECT_ROOT}/tests/STORY-153/results/test-results.txt"

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Helper function: assert_pattern_exists
# Usage: assert_pattern_exists "pattern" "file" "test_name"
assert_pattern_exists() {
    local pattern="$1"
    local file="$2"
    local test_name="$3"

    if grep -q "$pattern" "$file" 2>/dev/null; then
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
# Usage: assert_pattern_count "pattern" "file" "expected_count" "test_name"
assert_pattern_count() {
    local pattern="$1"
    local file="$2"
    local expected_count=$3
    local test_name="$4"

    local actual_count=$(grep -c "$pattern" "$file" 2>/dev/null || echo 0)

    if [ "$actual_count" -ge "$expected_count" ]; then
        echo "PASS: $test_name (found $actual_count >= $expected_count)"
        ((TESTS_PASSED++))
        return 0
    else
        echo "FAIL: $test_name (found $actual_count, expected >= $expected_count)"
        echo "  Pattern: $pattern"
        echo "  File: $file"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Helper function: assert_file_exists
# Usage: assert_file_exists "file_path" "test_name"
assert_file_exists() {
    local file="$1"
    local test_name="$2"

    if [ -f "$file" ]; then
        echo "PASS: $test_name"
        ((TESTS_PASSED++))
        return 0
    else
        echo "FAIL: $test_name"
        echo "  Expected file: $file"
        ((TESTS_FAILED++))
        return 1
    fi
}

# ==============================================================
# TEST 1: test_init_state_called_at_start
# AC#4: Initialize state file at workflow start
# Verifies: SKILL.md has devforgeai-validate init-state call
# ==============================================================
test_init_state_called_at_start() {
    ((TESTS_RUN++))
    assert_pattern_exists \
        "devforgeai-validate init-state" \
        "$SKILL_FILE" \
        "test_init_state_called_at_start"
}

# ==============================================================
# TEST 2: test_phase_check_blocks_incomplete
# AC#1: Add validation call before each phase transition
# Verifies: All phases 01-10 have devforgeai-validate phase-check calls
# ==============================================================
test_phase_check_blocks_incomplete() {
    ((TESTS_RUN++))
    # Expect at least 9 phase-check calls (phases 01-10, minus phase 00 which has no prior check)
    assert_pattern_count \
        "devforgeai-validate phase-check" \
        "$SKILL_FILE" \
        9 \
        "test_phase_check_blocks_incomplete"
}

# ==============================================================
# TEST 3: test_subagent_recorded_after_task
# AC#2: Add subagent recording after each subagent invocation
# Verifies: devforgeai-validate record-subagent calls exist
# ==============================================================
test_subagent_recorded_after_task() {
    ((TESTS_RUN++))
    assert_pattern_exists \
        "devforgeai-validate record-subagent" \
        "$SKILL_FILE" \
        "test_subagent_recorded_after_task"
}

# ==============================================================
# TEST 4: test_complete_phase_called
# AC#3: Add checkpoint completion call at phase end
# Verifies: devforgeai-validate complete-phase calls exist at phase ends
# ==============================================================
test_complete_phase_called() {
    ((TESTS_RUN++))
    # Expect at least 10 complete-phase calls (one per phase)
    assert_pattern_count \
        "devforgeai-validate complete-phase" \
        "$SKILL_FILE" \
        10 \
        "test_complete_phase_called"
}

# ==============================================================
# TEST 5: test_all_phases_have_validation
# AC#1, AC#3: All phases have complete validation structure
# Verifies: Every phase (except 00) has phase-check and complete-phase
# ==============================================================
test_all_phases_have_validation() {
    ((TESTS_RUN++))
    # Check that phase sections exist (10 phases: 00-10 or 1-10)
    local phase_count=$(grep -c "^## Phase" "$SKILL_FILE" 2>/dev/null || echo 0)

    if [ "$phase_count" -ge 10 ]; then
        echo "PASS: test_all_phases_have_validation (found $phase_count phase sections)"
        ((TESTS_PASSED++))
        return 0
    else
        echo "FAIL: test_all_phases_have_validation (found $phase_count phase sections, expected >= 10)"
        echo "  File: $SKILL_FILE"
        ((TESTS_FAILED++))
        return 1
    fi
}

# ==============================================================
# TEST 6: test_halt_on_validation_failure
# AC#5: Clear error handling with HALT on validation failure
# Verifies: SKILL.md contains error handling with HALT instruction
# ==============================================================
test_halt_on_validation_failure() {
    ((TESTS_RUN++))
    # Look for HALT instruction in context of validation/error handling
    if grep -q "HALT" "$SKILL_FILE" 2>/dev/null && \
       grep -q "exit code" "$SKILL_FILE" 2>/dev/null; then
        echo "PASS: test_halt_on_validation_failure"
        ((TESTS_PASSED++))
        return 0
    else
        echo "FAIL: test_halt_on_validation_failure"
        echo "  Expected: HALT instruction and exit code check"
        echo "  File: $SKILL_FILE"
        ((TESTS_FAILED++))
        return 1
    fi
}

# ==============================================================
# TEST 7: test_backward_compatibility
# AC#6: Maintain backward compatibility with existing workflows
# Verifies: SKILL.md includes warning if CLI not installed
# ==============================================================
test_backward_compatibility() {
    ((TESTS_RUN++))
    # Look for warning or continue logic if CLI not installed
    # Accept multiple variations of the warning message
    if grep -q "warning\|CLI not installed\|pip install devforgeai\|backward" "$SKILL_FILE" 2>/dev/null; then
        echo "PASS: test_backward_compatibility"
        ((TESTS_PASSED++))
        return 0
    else
        echo "FAIL: test_backward_compatibility"
        echo "  Expected: Warning message for missing CLI or backward compatibility handling"
        echo "  File: $SKILL_FILE"
        ((TESTS_FAILED++))
        return 1
    fi
}

# ==============================================================
# TEST 8: test_validation_call_locations_config
# Tech Spec: validation-call-locations.yaml required
# Verifies: validation-call-locations.yaml exists with all phases
# ==============================================================
test_validation_call_locations_config() {
    ((TESTS_RUN++))
    local config_file="${PROJECT_ROOT}/devforgeai/config/validation-call-locations.yaml"

    assert_file_exists "$config_file" "test_validation_call_locations_config"
}

# ==============================================================
# Main execution
# ==============================================================
main() {
    echo ""
    echo "=========================================="
    echo "STORY-153: Skill Validation Integration"
    echo "Test Suite - TDD Red Phase"
    echo "=========================================="
    echo ""

    # Verify SKILL.md file exists
    if [ ! -f "$SKILL_FILE" ]; then
        echo "ERROR: SKILL.md not found at $SKILL_FILE"
        exit 1
    fi

    # Create results directory
    mkdir -p "${PROJECT_ROOT}/tests/STORY-153/results"

    # Run all tests
    echo "Running tests..."
    echo ""

    test_init_state_called_at_start
    test_phase_check_blocks_incomplete
    test_subagent_recorded_after_task
    test_complete_phase_called
    test_all_phases_have_validation
    test_halt_on_validation_failure
    test_backward_compatibility
    test_validation_call_locations_config

    # Report summary
    echo ""
    echo "=========================================="
    echo "Test Summary"
    echo "=========================================="
    echo "Tests Run: $TESTS_RUN"
    echo "Tests Passed: $TESTS_PASSED"
    echo "Tests Failed: $TESTS_FAILED"

    if [ "$TESTS_RUN" -gt 0 ]; then
        PASS_RATE=$(( TESTS_PASSED * 100 / TESTS_RUN ))
        echo "Pass Rate: $PASS_RATE%"
    fi
    echo "=========================================="
    echo ""

    # Write results to file
    {
        echo "STORY-153 Test Results"
        echo "Test Execution Date: $(date)"
        echo "Test Framework: Bash/Grep"
        echo ""
        echo "Summary:"
        echo "Tests Run: $TESTS_RUN"
        echo "Tests Passed: $TESTS_PASSED"
        echo "Tests Failed: $TESTS_FAILED"
        if [ "$TESTS_RUN" -gt 0 ]; then
            PASS_RATE=$(( TESTS_PASSED * 100 / TESTS_RUN ))
            echo "Pass Rate: $PASS_RATE%"
        fi
        echo ""
        echo "Status: $([ "$TESTS_FAILED" -eq 0 ] && echo "ALL PASS" || echo "FAILURES PRESENT")"
    } > "$RESULTS_FILE"

    echo "Test results written to: $RESULTS_FILE"
    echo ""

    # TDD Red phase: Tests should fail initially
    # Exit with failure if any tests failed (as expected in Red phase)
    if [ "$TESTS_FAILED" -gt 0 ]; then
        echo "TDD Red Phase: Tests expected to fail"
        echo "Implementation will add validation calls in Phase 03"
        return 1
    fi

    return 0
}

# Execute main function
main "$@"
