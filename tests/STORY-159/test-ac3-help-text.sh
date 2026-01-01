#!/bin/bash

###############################################################################
# TEST FILE: test-ac3-help-text.sh
# AC#3: Implement Help Text
#
# Story: STORY-159 - Create /create-stories-from-rca Command Shell
# Purpose: Verify help text is implemented and displays correctly
#
# Test Framework: Bash shell scripts (DevForgeAI standard)
# Location: /mnt/c/Projects/DevForgeAI2/tests/STORY-159/
#
# TDD Status: RED PHASE (Tests fail before implementation)
# Expected Failures: 5 tests fail (no help implementation)
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

# Check if help text is documented in the command file
contains_help_documentation() {
    local file_path="$1"

    # Look for help-related sections in markdown
    if grep -qE "(##.*Help|--help|help.*command)" "${PROJECT_ROOT}/${file_path}" 2>/dev/null; then
        return 0
    fi
    return 1
}

# Check if command file contains usage examples
contains_usage_examples() {
    local file_path="$1"

    # Look for example commands (typically in code blocks)
    if grep -qE "(\`\`\`.*create-stories-from-rca|/create-stories-from-rca.*RCA)" "${PROJECT_ROOT}/${file_path}" 2>/dev/null; then
        return 0
    fi
    return 1
}

###############################################################################
# Test Case 3.1: --help flag documentation
###############################################################################

test_ac3_help_flag_displays_help() {
    test_start "AC#3.1: Command documents --help flag for displaying help"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Check if help flag is documented
    if assert_file_contains "${COMMAND_FILE}" "\-\-help"; then
        test_pass
    else
        test_fail "No --help flag documentation found in command file"
    fi
}

###############################################################################
# Test Case 3.2: help argument documentation
###############################################################################

test_ac3_help_argument_displays_help() {
    test_start "AC#3.2: Command documents 'help' argument for displaying help"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Check if help argument is documented (appears in usage or description)
    # Look for "help" as argument, not just as --help flag
    if grep -E '(help.*argument|"help"|help.*Display|ARG.*==.*"help")' "${PROJECT_ROOT}/${COMMAND_FILE}" 2>/dev/null | grep -q .; then
        test_pass
    else
        test_fail "No 'help' argument documentation found in command file"
    fi
}

###############################################################################
# Test Case 3.3: Help text includes usage information
###############################################################################

test_ac3_help_includes_usage() {
    test_start "AC#3.3: Help text includes usage information and command syntax"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Check for usage section and command syntax
    if grep -qE "(Usage|usage|USAGE|\s/create-stories-from-rca)" "${PROJECT_ROOT}/${COMMAND_FILE}" 2>/dev/null; then
        test_pass
    else
        test_fail "No usage information found in command file"
    fi
}

###############################################################################
# Test Case 3.4: Help text includes examples
###############################################################################

test_ac3_help_includes_examples() {
    test_start "AC#3.4: Help text includes at least one example command"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Check for example commands in documentation
    if contains_usage_examples "${COMMAND_FILE}"; then
        test_pass
    else
        test_fail "No example commands found in help text"
    fi
}

###############################################################################
# Test Case 3.5: Help text mentions related commands
###############################################################################

test_ac3_help_mentions_related_commands() {
    test_start "AC#3.5: Help text references related commands (/rca, /brainstorm, /create-story, etc.)"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Check for references to related commands
    local related_commands_found=0
    local related_commands=("rca" "create-story" "brainstorm")

    for related_cmd in "${related_commands[@]}"; do
        if assert_file_contains "${COMMAND_FILE}" "${related_cmd}"; then
            ((related_commands_found++))
        fi
    done

    # At least one related command should be mentioned
    if [[ ${related_commands_found} -gt 0 ]]; then
        test_pass
    else
        test_fail "No related commands mentioned in help text"
    fi
}

###############################################################################
# Test Suite Execution
###############################################################################

main() {
    echo "=============================================================="
    echo "STORY-159 Test Suite: AC#3 - Help Text Implementation"
    echo "Test Framework: Bash shell scripts"
    echo "Expected Status: ALL TESTS FAIL (TDD Red Phase - no help impl)"
    echo "=============================================================="

    # Run all tests
    test_ac3_help_flag_displays_help
    test_ac3_help_argument_displays_help
    test_ac3_help_includes_usage
    test_ac3_help_includes_examples
    test_ac3_help_mentions_related_commands

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
