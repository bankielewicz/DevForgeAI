#!/bin/bash

##############################################################################
# Test Runner: STORY-089 - Coverage Validation Test Suite
# Purpose: Run all tests for epic coverage validation integration
##############################################################################

set -o pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║         STORY-089: Coverage Validation Test Suite            ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

TOTAL_TESTS=0
TOTAL_PASSED=0
TOTAL_FAILED=0

run_test_suite() {
    local test_file=$1
    local test_name=$2

    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}Running: ${test_name}${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

    if [[ ! -f "$test_file" ]]; then
        echo -e "${RED}Test file not found: $test_file${NC}"
        return 1
    fi

    chmod +x "$test_file"
    bash "$test_file"
    local exit_code=$?

    if [[ $exit_code -eq 0 ]]; then
        echo -e "${GREEN}✓ ${test_name} PASSED${NC}"
    else
        echo -e "${RED}✗ ${test_name} FAILED${NC}"
    fi

    return $exit_code
}

# Run all test suites
echo -e "${YELLOW}Starting test execution...${NC}"

# AC#1: Epic Validation Hook
run_test_suite "${SCRIPT_DIR}/test_epic_validation_hook.sh" "AC#1: Epic Validation Hook"
AC1_RESULT=$?

# AC#2: Coverage Quality Gate
run_test_suite "${SCRIPT_DIR}/test_orchestrate_gate.sh" "AC#2: Coverage Quality Gate"
AC2_RESULT=$?

# AC#3-4: Error Handling
run_test_suite "${SCRIPT_DIR}/test_error_handling.sh" "AC#3-4: Error Handling"
AC34_RESULT=$?

# AC#5: Confidence Scoring
run_test_suite "${SCRIPT_DIR}/test_confidence_scoring.sh" "AC#5: Confidence Scoring"
AC5_RESULT=$?

# Summary
echo ""
echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                    OVERALL SUMMARY                           ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

print_result() {
    local name=$1
    local result=$2

    if [[ $result -eq 0 ]]; then
        echo -e "  ${GREEN}✓${NC} $name"
    else
        echo -e "  ${RED}✗${NC} $name"
    fi
}

print_result "AC#1: Epic Validation Hook" $AC1_RESULT
print_result "AC#2: Coverage Quality Gate" $AC2_RESULT
print_result "AC#3-4: Error Handling" $AC34_RESULT
print_result "AC#5: Confidence Scoring" $AC5_RESULT

echo ""

# Calculate overall result
FAILED_SUITES=0
[[ $AC1_RESULT -ne 0 ]] && FAILED_SUITES=$((FAILED_SUITES + 1))
[[ $AC2_RESULT -ne 0 ]] && FAILED_SUITES=$((FAILED_SUITES + 1))
[[ $AC34_RESULT -ne 0 ]] && FAILED_SUITES=$((FAILED_SUITES + 1))
[[ $AC5_RESULT -ne 0 ]] && FAILED_SUITES=$((FAILED_SUITES + 1))

if [[ $FAILED_SUITES -eq 0 ]]; then
    echo -e "${GREEN}All test suites passed!${NC}"
    exit 0
else
    echo -e "${RED}${FAILED_SUITES} test suite(s) failed.${NC}"
    exit 1
fi
