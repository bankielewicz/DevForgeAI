#!/bin/bash

###############################################################################
# TEST FILE: test-ac4-invalid-arguments.sh
# AC#4: Handle Invalid Arguments
#
# Story: STORY-159 - Create /create-stories-from-rca Command Shell
# Purpose: Verify error handling for invalid arguments
#
# Test Framework: Bash shell scripts (DevForgeAI standard)
# Location: /mnt/c/Projects/DevForgeAI2/tests/STORY-159/
#
# TDD Status: RED PHASE (Tests fail before implementation)
# Expected Failures: 5 tests fail (no error handling)
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
COMMAND_FILE=".claude/commands/create-stories-from-rca.md"
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
RCA_DIR="devforgeai/RCA"

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
    echo -e "${GREEN}✓ PASS${NC}"
}

test_fail() {
    local reason="$1"
    ((TESTS_FAILED++))
    echo -e "${RED}✗ FAIL${NC}: ${reason}"
}

assert_file_exists() {
    local file_path="$1"
    if [[ ! -f "${PROJECT_ROOT}/${file_path}" ]]; then
        return 1
    fi
    return 0
}

assert_file_contains() {
    local file_path="$1"
    local search_string="$2"

    if grep -q "${search_string}" "${PROJECT_ROOT}/${file_path}" 2>/dev/null; then
        return 0
    fi
    return 1
}

# Get list of available RCA files
get_available_rca_ids() {
    local rca_files=$(find "${PROJECT_ROOT}/${RCA_DIR}" -name "RCA-*.md" 2>/dev/null | xargs -I {} basename {} | sed 's/-.*//' | sort -u)
    echo "${rca_files}"
}

###############################################################################
# Test Case 4.1: Missing argument shows error message
###############################################################################

test_ac4_missing_argument_shows_error() {
    test_start "AC#4.1: Command with no argument shows error message"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Check if command file contains error handling for missing arguments
    if grep -qE "(missing|required|argument|RCA.ID|expected)" "${PROJECT_ROOT}/${COMMAND_FILE}" 2>/dev/null; then
        test_pass
    else
        test_fail "No error handling for missing arguments found"
    fi
}

###############################################################################
# Test Case 4.2: Error message includes format guidance
###############################################################################

test_ac4_error_includes_format_guidance() {
    test_start "AC#4.2: Error message includes format guidance (Expected: RCA-NNN)"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Check for format guidance in error messages
    if grep -qE "(RCA-[0-9]{3}|format|pattern|example)" "${PROJECT_ROOT}/${COMMAND_FILE}" 2>/dev/null; then
        test_pass
    else
        test_fail "No format guidance found in error messages"
    fi
}

###############################################################################
# Test Case 4.3: Error message lists available RCAs
###############################################################################

test_ac4_error_lists_available_rcas() {
    test_start "AC#4.3: Error message includes list of available RCAs"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Check if RCA directory exists and has files
    if [[ ! -d "${PROJECT_ROOT}/${RCA_DIR}" ]]; then
        test_fail "RCA directory not found: ${PROJECT_ROOT}/${RCA_DIR}"
        return
    fi

    local rca_count=$(find "${PROJECT_ROOT}/${RCA_DIR}" -name "RCA-*.md" 2>/dev/null | wc -l)

    if [[ ${rca_count} -gt 0 ]]; then
        # Check if command file mentions listing or showing available RCAs
        if grep -qE "(available|list|show)" "${PROJECT_ROOT}/${COMMAND_FILE}" 2>/dev/null; then
            test_pass
        else
            test_fail "No mention of listing available RCAs in error handling"
        fi
    else
        test_fail "No RCA files found to test listing functionality"
    fi
}

###############################################################################
# Test Case 4.4: Non-existent RCA ID shows clear error
###############################################################################

test_ac4_nonexistent_rca_shows_error() {
    test_start "AC#4.4: Non-existent RCA ID shows clear error with available RCAs"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Check if command has logic to handle non-existent RCA IDs
    if grep -qE "(not found|does not exist|invalid|not available)" "${PROJECT_ROOT}/${COMMAND_FILE}" 2>/dev/null; then
        test_pass
    else
        test_fail "No error handling for non-existent RCA IDs found"
    fi
}

###############################################################################
# Test Case 4.5: Invalid format shows actionable guidance
###############################################################################

test_ac4_invalid_format_actionable() {
    test_start "AC#4.5: Invalid format errors provide actionable guidance"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Check for clear error messages and guidance (case-insensitive)
    if grep -qiE "(error|guidance|usage|example|format)" "${PROJECT_ROOT}/${COMMAND_FILE}" 2>/dev/null; then
        test_pass
    else
        test_fail "Error messages lack actionable guidance"
    fi
}

###############################################################################
# Test Suite Execution
###############################################################################

main() {
    echo "=============================================================="
    echo "STORY-159 Test Suite: AC#4 - Invalid Arguments & Error Handling"
    echo "Test Framework: Bash shell scripts"
    echo "Expected Status: ALL TESTS FAIL (TDD Red Phase - no error impl)"
    echo "=============================================================="

    # Run all tests
    test_ac4_missing_argument_shows_error
    test_ac4_error_includes_format_guidance
    test_ac4_error_lists_available_rcas
    test_ac4_nonexistent_rca_shows_error
    test_ac4_invalid_format_actionable

    # Print summary
    echo ""
    echo "=============================================================="
    echo "Test Summary:"
    echo "  Total Tests:  ${TESTS_RUN}"
    echo "  Passed:       ${TESTS_PASSED}"
    echo "  Failed:       ${TESTS_FAILED}"
    echo "=============================================================="

    if [[ ${TESTS_FAILED} -eq 0 ]]; then
        echo -e "${GREEN}✓ All tests passed!${NC}"
        return 0
    else
        echo -e "${RED}✗ ${TESTS_FAILED} test(s) failed${NC}"
        return 1
    fi
}

# Run test suite
main "$@"
