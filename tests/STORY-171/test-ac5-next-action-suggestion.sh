#!/bin/bash

###############################################################################
# TEST FILE: test-ac5-next-action-suggestion.sh
# AC#5: Suggests Next Action
#
# Story: STORY-171 - RCA-013 /dev-status Command
# Purpose: Verify command suggests next action based on story state
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
# Test Case 5.1: Command file exists (prerequisite)
###############################################################################

test_ac5_command_file_exists() {
    test_start "AC#5.1: Command file exists at .claude/commands/dev-status.md"

    if assert_file_exists "${COMMAND_FILE}"; then
        test_pass
    else
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
    fi
}

###############################################################################
# Test Case 5.2: Command documents "Suggested Next Action:" section
###############################################################################

test_ac5_next_action_section() {
    test_start "AC#5.2: Command documents 'Suggested Next Action:' section"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Command documentation must specify "Suggested Next Action:" section
    if grep -qiE "Suggested.*Next.*Action|Next.*Action" "${PROJECT_ROOT}/${COMMAND_FILE}" 2>/dev/null; then
        test_pass
    else
        test_fail "Command does not document 'Suggested Next Action' section"
    fi
}

###############################################################################
# Test Case 5.3: Command documents /dev continuation suggestion
###############################################################################

test_ac5_dev_continuation_suggestion() {
    test_start "AC#5.3: Command documents '/dev STORY-XXX' continuation suggestion"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Command documentation must suggest /dev command for continuing development
    if grep -qE "/dev\s+STORY-" "${PROJECT_ROOT}/${COMMAND_FILE}" 2>/dev/null; then
        test_pass
    else
        test_fail "Command does not document '/dev STORY-XXX' continuation suggestion"
    fi
}

###############################################################################
# Test Case 5.4: Command documents /resume-dev suggestion
###############################################################################

test_ac5_resume_dev_suggestion() {
    test_start "AC#5.4: Command documents '/resume-dev STORY-XXX N' suggestion for phase resumption"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Command documentation must suggest /resume-dev command
    if grep -qiE "/resume-dev|resume.*phase" "${PROJECT_ROOT}/${COMMAND_FILE}" 2>/dev/null; then
        test_pass
    else
        test_fail "Command does not document '/resume-dev' suggestion"
    fi
}

###############################################################################
# Test Case 5.5: Command documents /qa suggestion for complete stories
###############################################################################

test_ac5_qa_suggestion_for_complete() {
    test_start "AC#5.5: Command documents '/qa STORY-XXX' suggestion when development complete"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Command documentation must suggest /qa command for complete stories
    if grep -qE "/qa\s+STORY-" "${PROJECT_ROOT}/${COMMAND_FILE}" 2>/dev/null; then
        test_pass
    else
        test_fail "Command does not document '/qa STORY-XXX' suggestion"
    fi
}

###############################################################################
# Test Case 5.6: Command documents state-based suggestion logic
###############################################################################

test_ac5_state_based_logic() {
    test_start "AC#5.6: Command documents state-based suggestion logic (different actions for different states)"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Command must explain different suggestions for different states
    # Looking for conditional logic like "if complete" or "if in development"
    if grep -qiE "(if|when).*complet|based on.*state|development.*complete" "${PROJECT_ROOT}/${COMMAND_FILE}" 2>/dev/null; then
        test_pass
    else
        test_fail "Command does not document state-based suggestion logic"
    fi
}

###############################################################################
# Test Suite Execution
###############################################################################

main() {
    echo "=============================================================="
    echo "STORY-171 Test Suite: AC#5 - Next Action Suggestion"
    echo "Test Framework: Bash shell scripts"
    echo "Expected Status: ALL TESTS FAIL (TDD Red Phase)"
    echo "=============================================================="

    # Run all tests
    test_ac5_command_file_exists
    test_ac5_next_action_section
    test_ac5_dev_continuation_suggestion
    test_ac5_resume_dev_suggestion
    test_ac5_qa_suggestion_for_complete
    test_ac5_state_based_logic

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
