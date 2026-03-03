#!/bin/bash

##############################################################################
# Test Runner: STORY-173 - Add Plan File Creation Constraints to Subagents
#
# This script runs all acceptance criteria tests for STORY-173.
#
# Acceptance Criteria:
#   AC#1: Backend Architect Plan File Constraint
#   AC#2: API Designer Plan File Constraint
#   AC#3: Inline Plan Content Instruction
#   AC#4: Existing Functionality Preserved
#
# Usage:
#   ./run_all_tests.sh           # Run all tests
#   ./run_all_tests.sh --quick   # Run only critical tests
##############################################################################

set -e

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test suite counters
SUITES_RUN=0
SUITES_PASSED=0
SUITES_FAILED=0
FAILED_SUITES=()

##############################################################################
# Helper Functions
##############################################################################

run_test_suite() {
    local test_file="$1"
    local suite_name="$2"

    SUITES_RUN=$((SUITES_RUN + 1))

    echo ""
    echo -e "${BLUE}========================================================================"
    echo " Running Test Suite: $suite_name"
    echo "========================================================================${NC}"

    if [[ ! -f "$test_file" ]]; then
        echo -e "${RED}ERROR: Test file not found: $test_file${NC}"
        SUITES_FAILED=$((SUITES_FAILED + 1))
        FAILED_SUITES+=("$suite_name (file not found)")
        return 1
    fi

    if bash "$test_file"; then
        echo -e "${GREEN}Suite PASSED: $suite_name${NC}"
        SUITES_PASSED=$((SUITES_PASSED + 1))
    else
        echo -e "${RED}Suite FAILED: $suite_name${NC}"
        SUITES_FAILED=$((SUITES_FAILED + 1))
        FAILED_SUITES+=("$suite_name")
    fi
}

##############################################################################
# Main Execution
##############################################################################

echo ""
echo "========================================================================"
echo " STORY-173: Add Plan File Creation Constraints to Subagents"
echo " Test Suite Runner"
echo "========================================================================"
echo ""
echo "Test Directory: $SCRIPT_DIR"
echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Run all test suites
run_test_suite "$SCRIPT_DIR/test_ac1_backend_architect_constraint.sh" "AC#1 - Backend Architect Constraint"
run_test_suite "$SCRIPT_DIR/test_ac2_api_designer_constraint.sh" "AC#2 - API Designer Constraint"
run_test_suite "$SCRIPT_DIR/test_ac3_inline_plan_content_instruction.sh" "AC#3 - Inline Plan Content Instruction"
run_test_suite "$SCRIPT_DIR/test_ac4_existing_functionality_preserved.sh" "AC#4 - Existing Functionality Preserved"

##############################################################################
# Final Summary
##############################################################################

echo ""
echo "========================================================================"
echo " STORY-173 Test Execution Summary"
echo "========================================================================"
echo ""
echo "Test Suites Run:     $SUITES_RUN"
echo -e "Test Suites Passed:  ${GREEN}$SUITES_PASSED${NC}"
echo -e "Test Suites Failed:  ${RED}$SUITES_FAILED${NC}"
echo ""

if [[ ${#FAILED_SUITES[@]} -gt 0 ]]; then
    echo -e "${RED}Failed Test Suites:${NC}"
    for suite in "${FAILED_SUITES[@]}"; do
        echo "  - $suite"
    done
    echo ""
fi

echo "========================================================================"

if [[ $SUITES_FAILED -eq 0 ]]; then
    echo -e "${GREEN}"
    echo "  SUCCESS: All STORY-173 acceptance criteria tests passed!"
    echo -e "${NC}"
    exit 0
else
    echo -e "${RED}"
    echo "  FAILURE: $SUITES_FAILED of $SUITES_RUN test suites failed"
    echo ""
    echo "  TDD Red Phase: Tests are designed to FAIL initially."
    echo "  Implementation required to make tests pass."
    echo -e "${NC}"
    exit 1
fi
