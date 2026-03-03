#!/bin/bash

###############################################################################
# TEST FILE: test-ac1-current-phase-display.sh
# AC#1: Command Displays Current Phase
#
# Story: STORY-171 - RCA-013 /dev-status Command
# Purpose: Verify command file exists and displays current phase correctly
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
# Test Case 1.1: Command file exists at correct location
###############################################################################

test_ac1_command_file_exists() {
    test_start "AC#1.1: Command file exists at .claude/commands/dev-status.md"

    if assert_file_exists "${COMMAND_FILE}"; then
        test_pass
    else
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
    fi
}

###############################################################################
# Test Case 1.2: Command file has YAML frontmatter with required fields
###############################################################################

test_ac1_yaml_frontmatter_valid() {
    test_start "AC#1.2: YAML frontmatter contains required fields (name, description, argument-hint)"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    local required_fields=("name" "description" "argument-hint")
    local missing_fields=()

    for field in "${required_fields[@]}"; do
        if ! grep -q "^${field}:" "${PROJECT_ROOT}/${COMMAND_FILE}" 2>/dev/null; then
            missing_fields+=("${field}")
        fi
    done

    if [[ ${#missing_fields[@]} -eq 0 ]]; then
        test_pass
    else
        test_fail "Missing YAML fields: ${missing_fields[*]}"
    fi
}

###############################################################################
# Test Case 1.3: Command documents "Current Phase:" output format
###############################################################################

test_ac1_current_phase_output_format() {
    test_start "AC#1.3: Command documents 'Current Phase:' output format"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Command documentation must specify "Current Phase:" output format
    if assert_content_contains "${COMMAND_FILE}" "Current Phase:"; then
        test_pass
    else
        test_fail "Command does not document 'Current Phase:' output format"
    fi
}

###############################################################################
# Test Case 1.4: Command documents phase format with phase number and name
###############################################################################

test_ac1_phase_format_with_number_and_name() {
    test_start "AC#1.4: Command documents phase format with number and name (e.g., '4.5 (Deferral Challenge)')"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Command documentation must show example format with phase number and name
    # Looking for pattern like "4.5" followed by "(Deferral" or similar phase name in parentheses
    if grep -qE "[0-9]+(\.[0-9]+)?\s*\([A-Z]" "${PROJECT_ROOT}/${COMMAND_FILE}" 2>/dev/null; then
        test_pass
    else
        test_fail "Command does not document phase format with number and name in parentheses"
    fi
}

###############################################################################
# Test Case 1.5: Command references phase-state.json for phase data
###############################################################################

test_ac1_references_phase_state_json() {
    test_start "AC#1.5: Command references phase-state.json as data source"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Command must reference phase-state.json file for reading current phase
    if assert_content_contains "${COMMAND_FILE}" "phase-state"; then
        test_pass
    else
        test_fail "Command does not reference phase-state.json for phase data"
    fi
}

###############################################################################
# Test Suite Execution
###############################################################################

main() {
    echo "=============================================================="
    echo "STORY-171 Test Suite: AC#1 - Current Phase Display"
    echo "Test Framework: Bash shell scripts"
    echo "Expected Status: ALL TESTS FAIL (TDD Red Phase)"
    echo "=============================================================="

    # Run all tests
    test_ac1_command_file_exists
    test_ac1_yaml_frontmatter_valid
    test_ac1_current_phase_output_format
    test_ac1_phase_format_with_number_and_name
    test_ac1_references_phase_state_json

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
