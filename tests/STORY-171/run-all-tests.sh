#!/bin/bash

###############################################################################
# TEST SUITE RUNNER: run-all-tests.sh
# Story: STORY-171 - RCA-013 /dev-status Command
#
# Purpose: Execute all acceptance criteria test files and report summary
#
# Test Framework: Bash shell scripts (DevForgeAI standard)
# Location: /mnt/c/Projects/DevForgeAI2/tests/STORY-171/
#
# TDD Status: RED PHASE (All tests expected to fail before implementation)
###############################################################################

set -u

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Script location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Aggregate counters
TOTAL_SUITES=0
SUITES_PASSED=0
SUITES_FAILED=0
TOTAL_TESTS=0
TESTS_PASSED=0
TESTS_FAILED=0

###############################################################################
# Test Suite Execution
###############################################################################

run_test_file() {
    local test_file="$1"
    local test_name=$(basename "${test_file}" .sh)

    echo -e "\n${CYAN}========================================${NC}"
    echo -e "${CYAN}Running: ${test_name}${NC}"
    echo -e "${CYAN}========================================${NC}"

    ((TOTAL_SUITES++))

    # Run test and capture output
    if bash "${test_file}"; then
        ((SUITES_PASSED++))
    else
        ((SUITES_FAILED++))
    fi
}

###############################################################################
# Main Execution
###############################################################################

main() {
    echo "=============================================================="
    echo "STORY-171: RCA-013 /dev-status Command"
    echo "Test Suite Runner"
    echo "=============================================================="
    echo ""
    echo "Story: Implement /dev-status command to show development progress"
    echo "Expected Status: ALL TESTS FAIL (TDD Red Phase)"
    echo "Test Files: 5 (one per acceptance criterion)"
    echo ""

    # Run all test files in order
    run_test_file "${SCRIPT_DIR}/test-ac1-current-phase-display.sh"
    run_test_file "${SCRIPT_DIR}/test-ac2-dod-completion-display.sh"
    run_test_file "${SCRIPT_DIR}/test-ac3-remaining-items-list.sh"
    run_test_file "${SCRIPT_DIR}/test-ac4-iteration-count-display.sh"
    run_test_file "${SCRIPT_DIR}/test-ac5-next-action-suggestion.sh"

    # Print aggregate summary
    echo ""
    echo "=============================================================="
    echo "AGGREGATE TEST SUMMARY - STORY-171"
    echo "=============================================================="
    echo ""
    echo "Test Suites:"
    echo "  Total Suites: ${TOTAL_SUITES}"
    echo "  Suites Passed: ${SUITES_PASSED}"
    echo "  Suites Failed: ${SUITES_FAILED}"
    echo ""
    echo "=============================================================="

    if [[ ${SUITES_FAILED} -eq 0 ]]; then
        echo -e "${GREEN}ALL TEST SUITES PASSED!${NC}"
        return 0
    else
        echo -e "${RED}${SUITES_FAILED} TEST SUITE(S) FAILED${NC}"
        echo ""
        echo "TDD RED PHASE: This is expected before implementation."
        echo "Next step: Create .claude/commands/dev-status.md to make tests pass."
        return 1
    fi
}

# Run main function
main "$@"
