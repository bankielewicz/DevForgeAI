#!/bin/bash

################################################################################
# TEST SUITE: AC#1 - Total Invocation Count (SVC-001)
# Story: STORY-200
# Description: Verify hook-telemetry.sh counts total hook invocations
#
# Technical Requirement:
# - SVC-001: Count total hook invocations (wc -l pre-tool-use.log)
# - Output: "Total invocations: N"
#
# Test Status: FAILING (Red Phase) - hook-telemetry.sh does not exist yet
################################################################################

# Note: Not using set -e to allow all tests to run

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SCRIPT_PATH="$PROJECT_ROOT/devforgeai/scripts/hook-telemetry.sh"
FIXTURES_DIR="$PROJECT_ROOT/devforgeai/tests/STORY-200/fixtures"
TEST_NAME="AC#1: Total Invocation Count"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

run_telemetry() {
    local log_file="$1"
    if [ -f "$SCRIPT_PATH" ]; then
        bash "$SCRIPT_PATH" --log "$log_file" 2>&1
    else
        echo "ERROR: Script not found"
        return 1
    fi
}

echo ""
echo -e "${BLUE}===============================================================================${NC}"
echo -e "${BLUE}TEST SUITE: $TEST_NAME${NC}"
echo -e "${BLUE}===============================================================================${NC}"
echo ""

cd "$PROJECT_ROOT" || exit 1

# Test 1: Script exists
((TESTS_RUN++))
if [ -f "$SCRIPT_PATH" ]; then
    echo -e "${GREEN}PASS${NC}: hook-telemetry.sh exists"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}: hook-telemetry.sh exists"
    echo "  Expected: $SCRIPT_PATH"
    ((TESTS_FAILED++))
fi

# Test 2: Output contains "Total invocations:"
((TESTS_RUN++))
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" 2>&1 || true)
    if echo "$output" | grep -q "Total invocations:"; then
        echo -e "${GREEN}PASS${NC}: Output contains 'Total invocations:'"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: Output contains 'Total invocations:'"
        ((TESTS_FAILED++))
    fi
else
    echo -e "${RED}FAIL${NC}: Output contains 'Total invocations:'"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 3: Total count is accurate (100 entries in sample fixture)
((TESTS_RUN++))
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" 2>&1 || true)
    if echo "$output" | grep -qE "Total invocations:.*100"; then
        echo -e "${GREEN}PASS${NC}: Total count equals 100"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: Total count equals 100"
        echo "  Output: $output"
        ((TESTS_FAILED++))
    fi
else
    echo -e "${RED}FAIL${NC}: Total count equals 100"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 4: Counts all lines excluding comments
((TESTS_RUN++))
if [ -f "$SCRIPT_PATH" ]; then
    # Verify it doesn't count comment lines (lines starting with #)
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" 2>&1 || true)
    # Sample has ~15 comment lines + 100 data lines
    if echo "$output" | grep -qE "Total invocations:.*100"; then
        echo -e "${GREEN}PASS${NC}: Comments excluded from count"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: Comments excluded from count"
        ((TESTS_FAILED++))
    fi
else
    echo -e "${RED}FAIL${NC}: Comments excluded from count"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

echo ""
echo -e "${BLUE}===============================================================================${NC}"
echo "Tests Run: $TESTS_RUN | Passed: $TESTS_PASSED | Failed: $TESTS_FAILED"
echo -e "${BLUE}===============================================================================${NC}"

if [ $TESTS_FAILED -gt 0 ]; then
    echo -e "${RED}STATUS: FAILING (Red Phase)${NC}"
    exit 1
else
    echo -e "${GREEN}STATUS: PASSING${NC}"
    exit 0
fi
