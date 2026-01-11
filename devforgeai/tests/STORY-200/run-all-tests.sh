#!/bin/bash

################################################################################
# RUN ALL TESTS: STORY-200 - Hook Telemetry Metrics
# Description: Execute all acceptance criteria tests for STORY-200
#
# Usage: bash devforgeai/tests/STORY-200/run-all-tests.sh
#
# Test Files:
# - test-hook-telemetry.sh (comprehensive suite)
# - test-ac1-total-count.sh (AC#1: Total Invocation Count)
# - test-ac2-auto-approve-count.sh (AC#2: Auto-Approval Count)
# - test-ac3-blocked-count.sh (AC#3: Blocked Count)
# - test-ac4-approval-rate.sh (AC#4: Approval Rate Calculation)
# - test-ac5-unknown-patterns.sh (AC#5: Top Unknown Patterns)
#
# Expected Status: ALL FAILING (Red Phase)
################################################################################

set -e

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TEST_DIR="$PROJECT_ROOT/devforgeai/tests/STORY-200"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo -e "${BLUE}===============================================================================${NC}"
echo -e "${BLUE}STORY-200: Hook Telemetry Metrics - Test Suite Runner${NC}"
echo -e "${BLUE}===============================================================================${NC}"
echo ""

cd "$PROJECT_ROOT" || exit 1

# Track results
SUITES_RUN=0
SUITES_PASSED=0
SUITES_FAILED=0

# Function to run a test suite
run_suite() {
    local test_file="$1"
    local test_name="$2"

    if [ ! -f "$test_file" ]; then
        echo -e "${YELLOW}SKIP${NC}: $test_name (file not found)"
        return 0
    fi

    echo ""
    echo -e "${BLUE}Running: $test_name${NC}"
    echo "File: $test_file"
    echo ""

    ((SUITES_RUN++))

    if bash "$test_file"; then
        echo -e "${GREEN}PASSED${NC}: $test_name"
        ((SUITES_PASSED++))
    else
        echo -e "${RED}FAILED${NC}: $test_name"
        ((SUITES_FAILED++))
    fi
}

# Run individual AC tests
run_suite "$TEST_DIR/test-ac1-total-count.sh" "AC#1: Total Invocation Count"
run_suite "$TEST_DIR/test-ac2-auto-approve-count.sh" "AC#2: Auto-Approval Count"
run_suite "$TEST_DIR/test-ac3-blocked-count.sh" "AC#3: Blocked Count"
run_suite "$TEST_DIR/test-ac4-approval-rate.sh" "AC#4: Approval Rate Calculation"
run_suite "$TEST_DIR/test-ac5-unknown-patterns.sh" "AC#5: Top Unknown Patterns"

# Final summary
echo ""
echo -e "${BLUE}===============================================================================${NC}"
echo -e "${BLUE}STORY-200 TEST SUMMARY${NC}"
echo -e "${BLUE}===============================================================================${NC}"
echo ""
echo "Test Suites Run:    $SUITES_RUN"
echo "Test Suites Passed: $SUITES_PASSED"
echo "Test Suites Failed: $SUITES_FAILED"
echo ""

if [ $SUITES_FAILED -gt 0 ]; then
    echo -e "${RED}OVERALL STATUS: FAILING (Red Phase)${NC}"
    echo ""
    echo "This is expected for TDD Red phase."
    echo "All tests should fail because hook-telemetry.sh does not exist yet."
    echo ""
    echo "Next Step: Implement devforgeai/scripts/hook-telemetry.sh"
    echo ""
    exit 1
else
    echo -e "${GREEN}OVERALL STATUS: PASSING${NC}"
    echo ""
    echo "All acceptance criteria tests passed."
    echo "STORY-200 implementation complete."
    echo ""
    exit 0
fi
