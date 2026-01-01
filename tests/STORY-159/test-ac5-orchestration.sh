#!/bin/bash

###############################################################################
# TEST FILE: test-ac5-orchestration.sh
# AC#5: Orchestrate to Story Creation Components
#
# Story: STORY-159 - Create /create-stories-from-rca Command Shell
# Purpose: Verify command orchestrates all 4 story creation phases
#
# Test Framework: Bash shell scripts (DevForgeAI standard)
# Location: /mnt/c/Projects/DevForgeAI2/tests/STORY-159/
#
# TDD Status: RED PHASE (Tests fail before implementation)
# Expected Failures: 6 tests fail (no skill invocations)
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

# Get file size in characters
get_file_char_count() {
    local file_path="$1"
    if [[ ! -f "${PROJECT_ROOT}/${file_path}" ]]; then
        echo "0"
        return
    fi
    wc -c < "${PROJECT_ROOT}/${file_path}" | tr -d ' '
}

###############################################################################
# Test Case 5.1: Command invokes story creation skill
###############################################################################

test_ac5_invokes_story_creation_skill() {
    test_start "AC#5.1: Command invokes story creation orchestration (Skill or Task)"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Check for Skill() invocation for story creation
    if grep -qE "(Skill.*create|Skill.*story|Task.*create)" "${PROJECT_ROOT}/${COMMAND_FILE}" 2>/dev/null; then
        test_pass
    else
        test_fail "No Skill() or Task() invocation for story creation found"
    fi
}

###############################################################################
# Test Case 5.2: Orchestration includes STORY-155 (RCA Parser)
###############################################################################

test_ac5_orchestration_includes_story_155() {
    test_start "AC#5.2: Orchestration references STORY-155 (RCA Parser)"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Check for STORY-155 reference
    if assert_file_contains "${COMMAND_FILE}" "STORY-155"; then
        test_pass
    else
        test_fail "STORY-155 not referenced in command orchestration"
    fi
}

###############################################################################
# Test Case 5.3: Orchestration includes STORY-156 (Recommendation Selector)
###############################################################################

test_ac5_orchestration_includes_story_156() {
    test_start "AC#5.3: Orchestration references STORY-156 (Recommendation Selector)"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Check for STORY-156 reference
    if assert_file_contains "${COMMAND_FILE}" "STORY-156"; then
        test_pass
    else
        test_fail "STORY-156 not referenced in command orchestration"
    fi
}

###############################################################################
# Test Case 5.4: Orchestration includes STORY-157 (Batch Story Creator)
###############################################################################

test_ac5_orchestration_includes_story_157() {
    test_start "AC#5.4: Orchestration references STORY-157 (Batch Story Creator)"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Check for STORY-157 reference
    if assert_file_contains "${COMMAND_FILE}" "STORY-157"; then
        test_pass
    else
        test_fail "STORY-157 not referenced in command orchestration"
    fi
}

###############################################################################
# Test Case 5.5: Orchestration includes STORY-158 (RCA Story Linker)
###############################################################################

test_ac5_orchestration_includes_story_158() {
    test_start "AC#5.5: Orchestration references STORY-158 (RCA Story Linker)"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Check for STORY-158 reference
    if assert_file_contains "${COMMAND_FILE}" "STORY-158"; then
        test_pass
    else
        test_fail "STORY-158 not referenced in command orchestration"
    fi
}

###############################################################################
# Test Case 5.6: Command respects size limit (BR-001: < 15,000 characters)
###############################################################################

test_ac5_command_respects_size_limit() {
    test_start "AC#5.6: Command file respects lean orchestration limit (< 15,000 characters per BR-001)"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    local char_count=$(get_file_char_count "${COMMAND_FILE}")
    local size_limit=15000

    if [[ ${char_count} -lt ${size_limit} ]]; then
        test_pass
    else
        test_fail "Command file exceeds size limit: ${char_count} characters (limit: ${size_limit})"
    fi
}

###############################################################################
# Test Suite Execution
###############################################################################

main() {
    echo "=============================================================="
    echo "STORY-159 Test Suite: AC#5 - Orchestration & Story References"
    echo "Test Framework: Bash shell scripts"
    echo "Expected Status: ALL TESTS FAIL (TDD Red Phase - no skills impl)"
    echo "=============================================================="

    # Run all tests
    test_ac5_invokes_story_creation_skill
    test_ac5_orchestration_includes_story_155
    test_ac5_orchestration_includes_story_156
    test_ac5_orchestration_includes_story_157
    test_ac5_orchestration_includes_story_158
    test_ac5_command_respects_size_limit

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
