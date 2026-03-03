#!/bin/bash

###############################################################################
# TEST FILE: test-ac4-iteration-count-display.sh
# AC#4: Command Shows Iteration Count
#
# Story: STORY-171 - RCA-013 /dev-status Command
# Purpose: Verify command displays TDD iteration count correctly
#
# Test Framework: Bash shell scripts (DevForgeAI standard)
# Location: /mnt/c/Projects/DevForgeAI2/tests/STORY-171/
#
# TDD Status: RED PHASE (Tests fail before implementation)
# Expected Failures: All tests fail (command file does not exist yet)
###############################################################################

set -u

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Constants
COMMAND_FILE=".claude/commands/dev-status.md"
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"

###############################################################################
# Test Utility Functions
###############################################################################

test_start() {
    local test_name="$1"
    ((TESTS_RUN++))
    echo -e "\n${YELLOW}[TEST ${TESTS_RUN}]${NC} ${test_name}"
}

test_pass() {
    ((TESTS_PASSED++))
    echo -e "${GREEN}PASS${NC}"
}

test_fail() {
    local reason="$1"
    ((TESTS_FAILED++))
    echo -e "${RED}FAIL${NC}: ${reason}"
}

assert_file_exists() {
    local file_path="$1"
    if [[ ! -f "${PROJECT_ROOT}/${file_path}" ]]; then
        return 1
    fi
    return 0
}

assert_content_contains() {
    local file_path="$1"
    local pattern="$2"

    if grep -q "${pattern}" "${PROJECT_ROOT}/${file_path}" 2>/dev/null; then
        return 0
    fi
    return 1
}

###############################################################################
# Test Case 4.1: Command file exists (prerequisite)
###############################################################################

test_ac4_command_file_exists() {
    test_start "AC#4.1: Command file exists at .claude/commands/dev-status.md"

    if assert_file_exists "${COMMAND_FILE}"; then
        test_pass
    else
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
    fi
}

###############################################################################
# Test Case 4.2: Command documents "TDD Iteration:" output format
###############################################################################

test_ac4_tdd_iteration_output_format() {
    test_start "AC#4.2: Command documents 'TDD Iteration:' output format"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Command documentation must specify "TDD Iteration:" output format
    if assert_content_contains "${COMMAND_FILE}" "TDD Iteration:"; then
        test_pass
    else
        test_fail "Command does not document 'TDD Iteration:' output format"
    fi
}

###############################################################################
# Test Case 4.3: Command documents iteration number format
###############################################################################

test_ac4_iteration_number_format() {
    test_start "AC#4.3: Command documents iteration number format (e.g., 'TDD Iteration: 2')"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Command documentation must show example format like "TDD Iteration: 2"
    # Looking for pattern: TDD Iteration followed by a number
    if grep -qE "TDD Iteration:\s*[0-9]+" "${PROJECT_ROOT}/${COMMAND_FILE}" 2>/dev/null; then
        test_pass
    else
        test_fail "Command does not document iteration number format"
    fi
}

###############################################################################
# Test Case 4.4: Command references phase-state.json for iteration count
###############################################################################

test_ac4_references_iteration_count_source() {
    test_start "AC#4.4: Command references phase-state.json for iteration_count"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Command must reference iteration_count from phase-state.json or story file
    if grep -qiE "iteration.?count|phase.?state" "${PROJECT_ROOT}/${COMMAND_FILE}" 2>/dev/null; then
        test_pass
    else
        test_fail "Command does not reference iteration count data source"
    fi
}

###############################################################################
# Test Case 4.5: Command documents default iteration value (1 if not present)
###############################################################################

test_ac4_default_iteration_value() {
    test_start "AC#4.5: Command documents default iteration value for first iteration"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Command should document default iteration count (typically 1)
    # Looking for mention of default or first iteration
    if grep -qiE "default|first.*iteration|iteration.*1|TDD Iteration: 1" "${PROJECT_ROOT}/${COMMAND_FILE}" 2>/dev/null; then
        test_pass
    else
        test_fail "Command does not document default iteration value"
    fi
}

###############################################################################
# Test Suite Execution
###############################################################################

main() {
    echo "=============================================================="
    echo "STORY-171 Test Suite: AC#4 - Iteration Count Display"
    echo "Test Framework: Bash shell scripts"
    echo "Expected Status: ALL TESTS FAIL (TDD Red Phase)"
    echo "=============================================================="

    # Run all tests
    test_ac4_command_file_exists
    test_ac4_tdd_iteration_output_format
    test_ac4_iteration_number_format
    test_ac4_references_iteration_count_source
    test_ac4_default_iteration_value

    # Print summary
    echo ""
    echo "=============================================================="
    echo "Test Summary:"
    echo "  Total Tests:  ${TESTS_RUN}"
    echo "  Passed:       ${TESTS_PASSED}"
    echo "  Failed:       ${TESTS_FAILED}"
    echo "=============================================================="

    if [[ ${TESTS_FAILED} -eq 0 ]]; then
        echo -e "${GREEN}All tests passed!${NC}"
        return 0
    else
        echo -e "${RED}${TESTS_FAILED} test(s) failed${NC}"
        return 1
    fi
}

# Run test suite
main "$@"
