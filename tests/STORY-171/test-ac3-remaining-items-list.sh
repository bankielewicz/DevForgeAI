#!/bin/bash

###############################################################################
# TEST FILE: test-ac3-remaining-items-list.sh
# AC#3: Command Lists Remaining Items
#
# Story: STORY-171 - RCA-013 /dev-status Command
# Purpose: Verify command lists remaining DoD items by category
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

    if grep -q "${pattern}" "${PROJECT_ROOT}/${COMMAND_FILE}" 2>/dev/null; then
        return 0
    fi
    return 1
}

###############################################################################
# Test Case 3.1: Command file exists (prerequisite)
###############################################################################

test_ac3_command_file_exists() {
    test_start "AC#3.1: Command file exists at .claude/commands/dev-status.md"

    if assert_file_exists "${COMMAND_FILE}"; then
        test_pass
    else
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
    fi
}

###############################################################################
# Test Case 3.2: Command documents "Remaining DoD Items:" section
###############################################################################

test_ac3_remaining_items_section() {
    test_start "AC#3.2: Command documents 'Remaining DoD Items:' section"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Command documentation must specify "Remaining DoD Items:" or similar section
    if grep -qiE "Remaining.*DoD|Remaining.*Item|incomplete.*item" "${PROJECT_ROOT}/${COMMAND_FILE}" 2>/dev/null; then
        test_pass
    else
        test_fail "Command does not document 'Remaining DoD Items' section"
    fi
}

###############################################################################
# Test Case 3.3: Command documents categorization by Implementation
###############################################################################

test_ac3_implementation_category() {
    test_start "AC#3.3: Command documents 'Implementation' category for remaining items"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Command documentation must show Implementation category
    if grep -qi "Implementation" "${PROJECT_ROOT}/${COMMAND_FILE}" 2>/dev/null; then
        test_pass
    else
        test_fail "Command does not document 'Implementation' category"
    fi
}

###############################################################################
# Test Case 3.4: Command documents categorization by Quality
###############################################################################

test_ac3_quality_category() {
    test_start "AC#3.4: Command documents 'Quality' category for remaining items"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Command documentation must show Quality category
    if grep -qi "Quality" "${PROJECT_ROOT}/${COMMAND_FILE}" 2>/dev/null; then
        test_pass
    else
        test_fail "Command does not document 'Quality' category"
    fi
}

###############################################################################
# Test Case 3.5: Command documents categorization by Testing
###############################################################################

test_ac3_testing_category() {
    test_start "AC#3.5: Command documents 'Testing' category for remaining items"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Command documentation must show Testing category
    if grep -qi "Testing" "${PROJECT_ROOT}/${COMMAND_FILE}" 2>/dev/null; then
        test_pass
    else
        test_fail "Command does not document 'Testing' category"
    fi
}

###############################################################################
# Test Case 3.6: Command documents remaining item count per category
###############################################################################

test_ac3_item_count_per_category() {
    test_start "AC#3.6: Command documents item count per category (e.g., 'X remaining' or 'X items')"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Command documentation must show count format like "2 remaining" or "N items"
    if grep -qiE "[0-9]+\s*(remaining|items?)" "${PROJECT_ROOT}/${COMMAND_FILE}" 2>/dev/null; then
        test_pass
    else
        test_fail "Command does not document item count per category format"
    fi
}

###############################################################################
# Test Suite Execution
###############################################################################

main() {
    echo "=============================================================="
    echo "STORY-171 Test Suite: AC#3 - Remaining Items List"
    echo "Test Framework: Bash shell scripts"
    echo "Expected Status: ALL TESTS FAIL (TDD Red Phase)"
    echo "=============================================================="

    # Run all tests
    test_ac3_command_file_exists
    test_ac3_remaining_items_section
    test_ac3_implementation_category
    test_ac3_quality_category
    test_ac3_testing_category
    test_ac3_item_count_per_category

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
