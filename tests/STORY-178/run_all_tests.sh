#!/bin/bash
###############################################################################
# STORY-178: Run All Tests
#
# Purpose: Execute all acceptance criteria tests for STORY-178
# Story: Document Specification File Testing Pattern in Test-Automator
#
# Usage: ./run_all_tests.sh
###############################################################################

set -euo pipefail

TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}=================================================================${NC}"
echo -e "${CYAN}  STORY-178: Document Specification File Testing Pattern${NC}"
echo -e "${CYAN}  Test Suite Execution${NC}"
echo -e "${CYAN}=================================================================${NC}"
echo ""

# Track overall results
TOTAL_SUITES=0
PASSED_SUITES=0
FAILED_SUITES=0

run_test_suite() {
    local test_file=$1
    local test_name=$2

    TOTAL_SUITES=$((TOTAL_SUITES + 1))

    echo -e "${YELLOW}---------------------------------------------------------------${NC}"
    echo -e "${YELLOW}Running: $test_name${NC}"
    echo -e "${YELLOW}---------------------------------------------------------------${NC}"

    if bash "$TEST_DIR/$test_file"; then
        PASSED_SUITES=$((PASSED_SUITES + 1))
        echo -e "${GREEN}Suite PASSED: $test_name${NC}"
    else
        FAILED_SUITES=$((FAILED_SUITES + 1))
        echo -e "${RED}Suite FAILED: $test_name${NC}"
    fi
    echo ""
}

# Run all AC test suites
run_test_suite "test_ac1_spec_file_testing_section.sh" "AC-1: Specification File Testing Section Added"
run_test_suite "test_ac2_structural_testing_guidance.sh" "AC-2: Structural Testing Guidance"
run_test_suite "test_ac3_tool_invocation_guidance.sh" "AC-3: Tool Invocation Testing Guidance"
run_test_suite "test_ac4_anti_pattern_documented.sh" "AC-4: Anti-Pattern Documented"
run_test_suite "test_ac5_example_patterns.sh" "AC-5: Example Patterns Provided"

# Final Summary
echo -e "${CYAN}=================================================================${NC}"
echo -e "${CYAN}  FINAL SUMMARY${NC}"
echo -e "${CYAN}=================================================================${NC}"
echo ""
echo -e "Test Suites Run:    ${BLUE}$TOTAL_SUITES${NC}"
echo -e "Test Suites Passed: ${GREEN}$PASSED_SUITES${NC}"
echo -e "Test Suites Failed: ${RED}$FAILED_SUITES${NC}"
echo ""

if [ "$FAILED_SUITES" -eq 0 ]; then
    echo -e "${GREEN}ALL TESTS PASSED${NC}"
    echo ""
    echo "Story STORY-178 acceptance criteria validated."
    exit 0
else
    echo -e "${RED}TESTS FAILED${NC}"
    echo ""
    echo "TDD Red Phase: Tests are expected to FAIL before implementation."
    echo "Implement the 'Specification File Testing' section in test-automator.md"
    echo "to make these tests pass."
    exit 1
fi
