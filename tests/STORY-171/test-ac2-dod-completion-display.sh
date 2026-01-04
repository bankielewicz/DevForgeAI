#!/bin/bash

###############################################################################
# TEST FILE: test-ac2-dod-completion-display.sh
# AC#2: Command Displays DoD Completion
#
# Story: STORY-171 - RCA-013 /dev-status Command
# Purpose: Verify command displays DoD completion percentage correctly
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
# Test Case 2.1: Command file exists (prerequisite)
###############################################################################

test_ac2_command_file_exists() {
    test_start "AC#2.1: Command file exists at .claude/commands/dev-status.md"

    if assert_file_exists "${COMMAND_FILE}"; then
        test_pass
    else
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
    fi
}

###############################################################################
# Test Case 2.2: Command documents "DoD Completion:" output format
###############################################################################

test_ac2_dod_completion_output_format() {
    test_start "AC#2.2: Command documents 'DoD Completion:' output format"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Command documentation must specify "DoD Completion:" output format
    if assert_content_contains "${COMMAND_FILE}" "DoD Completion:"; then
        test_pass
    else
        test_fail "Command does not document 'DoD Completion:' output format"
    fi
}

###############################################################################
# Test Case 2.3: Command documents completion format with fraction and percentage
###############################################################################

test_ac2_dod_format_fraction_and_percentage() {
    test_start "AC#2.3: Command documents DoD format with fraction and percentage (e.g., '26/30 (87%)')"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Command documentation must show example format like "26/30 (87%)"
    # Looking for pattern: number/number (number%)
    if grep -qE "[0-9]+/[0-9]+\s*\([0-9]+%\)" "${PROJECT_ROOT}/${COMMAND_FILE}" 2>/dev/null; then
        test_pass
    else
        test_fail "Command does not document DoD format with fraction and percentage (N/M (X%))"
    fi
}

###############################################################################
# Test Case 2.4: Command documents DoD checkbox counting logic
###############################################################################

test_ac2_dod_checkbox_counting_logic() {
    test_start "AC#2.4: Command documents DoD checkbox counting logic"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Command documentation must explain how to count DoD checkboxes
    # Looking for references to checkbox syntax like "- [x]" or "- [ ]" or "DoD items"
    if grep -qiE "\[x\]|\[ \]|DoD.*item|checkbox|count" "${PROJECT_ROOT}/${COMMAND_FILE}" 2>/dev/null; then
        test_pass
    else
        test_fail "Command does not document DoD checkbox counting logic"
    fi
}

###############################################################################
# Test Case 2.5: Command documents reading story file for DoD section
###############################################################################

test_ac2_reads_story_file() {
    test_start "AC#2.5: Command documents reading story file for DoD section"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Command must reference reading story file or Definition of Done
    if grep -qiE "story.*file|Definition of Done|\.story\.md|Read.*story" "${PROJECT_ROOT}/${COMMAND_FILE}" 2>/dev/null; then
        test_pass
    else
        test_fail "Command does not document reading story file for DoD section"
    fi
}

###############################################################################
# Test Suite Execution
###############################################################################

main() {
    echo "=============================================================="
    echo "STORY-171 Test Suite: AC#2 - DoD Completion Display"
    echo "Test Framework: Bash shell scripts"
    echo "Expected Status: ALL TESTS FAIL (TDD Red Phase)"
    echo "=============================================================="

    # Run all tests
    test_ac2_command_file_exists
    test_ac2_dod_completion_output_format
    test_ac2_dod_format_fraction_and_percentage
    test_ac2_dod_checkbox_counting_logic
    test_ac2_reads_story_file

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
