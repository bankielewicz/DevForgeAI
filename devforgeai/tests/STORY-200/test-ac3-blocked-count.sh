#!/bin/bash

################################################################################
# TEST SUITE: AC#3 - Blocked Count (SVC-003)
# Story: STORY-200
# Description: Verify hook-telemetry.sh counts blocked commands
#
# Technical Requirement:
# - SVC-003: Count blocked (grep 'BLOCK' | wc -l)
# - Output: "Blocked: N"
#
# Test Status: FAILING (Red Phase) - hook-telemetry.sh does not exist yet
################################################################################

# Note: Not using set -e to allow all tests to run

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SCRIPT_PATH="$PROJECT_ROOT/devforgeai/scripts/hook-telemetry.sh"
FIXTURES_DIR="$PROJECT_ROOT/devforgeai/tests/STORY-200/fixtures"
TEST_NAME="AC#3: Blocked Count"

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

# Test 1: Output contains "Blocked:"
((TESTS_RUN++))
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" 2>&1 || true)
    if echo "$output" | grep -q "Blocked:"; then
        echo -e "${GREEN}PASS${NC}: Output contains 'Blocked:'"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: Output contains 'Blocked:'"
        ((TESTS_FAILED++))
    fi
else
    echo -e "${RED}FAIL${NC}: Output contains 'Blocked:'"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 2: Blocked count is accurate (10 BLOCK markers in sample)
((TESTS_RUN++))
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" 2>&1 || true)
    if echo "$output" | grep -qE "Blocked:.*10"; then
        echo -e "${GREEN}PASS${NC}: Blocked count equals 10"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: Blocked count equals 10"
        echo "  Output: $output"
        ((TESTS_FAILED++))
    fi
else
    echo -e "${RED}FAIL${NC}: Blocked count equals 10"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 3: Counts only lines containing BLOCK (not BLOCKED or blocking)
((TESTS_RUN++))
if [ -f "$SCRIPT_PATH" ]; then
    # Verify against grep count with word boundary
    expected_count=$(grep -c "Decision: BLOCK" "$FIXTURES_DIR/sample-pre-tool-use.log" 2>/dev/null || echo "0")
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" 2>&1 || true)
    if echo "$output" | grep -qE "Blocked:.*$expected_count"; then
        echo -e "${GREEN}PASS${NC}: Count matches grep BLOCK"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: Count matches grep BLOCK"
        echo "  Expected: $expected_count"
        ((TESTS_FAILED++))
    fi
else
    echo -e "${RED}FAIL${NC}: Count matches grep BLOCK"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 4: Zero blocked count when no BLOCK markers
((TESTS_RUN++))
if [ -f "$SCRIPT_PATH" ]; then
    temp_file=$(mktemp)
    echo "2026-01-10 10:00:01 Decision: AUTO-APPROVE" > "$temp_file"
    echo "2026-01-10 10:00:02 Decision: ASK USER" >> "$temp_file"
    output=$(run_telemetry "$temp_file" 2>&1 || true)
    rm -f "$temp_file"
    if echo "$output" | grep -qE "Blocked:.*0"; then
        echo -e "${GREEN}PASS${NC}: Zero blocked when no BLOCK markers"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: Zero blocked when no BLOCK markers"
        ((TESTS_FAILED++))
    fi
else
    echo -e "${RED}FAIL${NC}: Zero blocked when no BLOCK markers"
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
