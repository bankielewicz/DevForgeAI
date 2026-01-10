#!/bin/bash
################################################################################
# STORY-199: Run All Tests
#
# Purpose: Execute all acceptance criteria tests for STORY-199
#          Hook Design Philosophy Documentation
#
# Usage: ./run-all-tests.sh
################################################################################

set -uo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOTAL_PASSED=0
TOTAL_FAILED=0
TOTAL_TESTS=0

echo ""
echo "=============================================================="
echo "${BLUE}STORY-199: Hook Design Philosophy Documentation${NC}"
echo "=============================================================="
echo "Running all acceptance criteria tests..."
echo ""

# Function to run a test and track results
run_test() {
    local test_file="$1"
    local test_name="$2"

    echo "--------------------------------------------------------------"
    echo "${BLUE}Running: ${test_name}${NC}"
    echo "--------------------------------------------------------------"

    if bash "${SCRIPT_DIR}/${test_file}"; then
        ((TOTAL_PASSED++))
    else
        ((TOTAL_FAILED++))
    fi
    ((TOTAL_TESTS++))
    echo ""
}

# Run all AC tests
run_test "test-ac1-readme-creation.sh" "AC#1: README Creation"
run_test "test-ac2-safe-pattern-criteria.sh" "AC#2: Safe Pattern Criteria"
run_test "test-ac3-blocked-pattern-criteria.sh" "AC#3: Blocked Pattern Criteria"
run_test "test-ac4-update-process.sh" "AC#4: Update Process Documentation"
run_test "test-ac5-debugging-information.sh" "AC#5: Debugging Information"

# Final Summary
echo ""
echo "=============================================================="
echo "${BLUE}STORY-199: FINAL SUMMARY${NC}"
echo "=============================================================="
echo ""
echo -e "Total Test Suites:  ${TOTAL_TESTS}"
echo -e "Passed:             ${GREEN}${TOTAL_PASSED}${NC}"
echo -e "Failed:             ${RED}${TOTAL_FAILED}${NC}"
echo ""

if [ ${TOTAL_FAILED} -eq 0 ]; then
    echo -e "${GREEN}=============================================================="
    echo "ALL STORY-199 TESTS PASSED"
    echo "==============================================================${NC}"
    exit 0
else
    echo -e "${RED}=============================================================="
    echo "SOME STORY-199 TESTS FAILED"
    echo "==============================================================${NC}"
    exit 1
fi
