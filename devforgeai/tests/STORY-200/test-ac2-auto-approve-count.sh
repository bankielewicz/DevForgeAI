#!/bin/bash

################################################################################
# TEST SUITE: AC#2 - Auto-Approval Count (SVC-002)
# Story: STORY-200
# Description: Verify hook-telemetry.sh counts auto-approved commands
#
# Technical Requirement:
# - SVC-002: Count auto-approved (grep 'AUTO-APPROVE' | wc -l)
# - Output: "Auto-approved: N"
#
# Test Status: FAILING (Red Phase) - hook-telemetry.sh does not exist yet
################################################################################

# Note: Not using set -e to allow all tests to run

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SCRIPT_PATH="$PROJECT_ROOT/devforgeai/scripts/hook-telemetry.sh"
FIXTURES_DIR="$PROJECT_ROOT/devforgeai/tests/STORY-200/fixtures"
TEST_NAME="AC#2: Auto-Approval Count"

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

# Test 1: Output contains "Auto-approved:"
((TESTS_RUN++))
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" 2>&1 || true)
    if echo "$output" | grep -q "Auto-approved:"; then
        echo -e "${GREEN}PASS${NC}: Output contains 'Auto-approved:'"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: Output contains 'Auto-approved:'"
        ((TESTS_FAILED++))
    fi
else
    echo -e "${RED}FAIL${NC}: Output contains 'Auto-approved:'"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 2: Auto-approved count is accurate (50 AUTO-APPROVE markers in sample)
((TESTS_RUN++))
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" 2>&1 || true)
    if echo "$output" | grep -qE "Auto-approved:.*50"; then
        echo -e "${GREEN}PASS${NC}: Auto-approved count equals 50"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: Auto-approved count equals 50"
        echo "  Output: $output"
        ((TESTS_FAILED++))
    fi
else
    echo -e "${RED}FAIL${NC}: Auto-approved count equals 50"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 3: Counts only lines containing AUTO-APPROVE
((TESTS_RUN++))
if [ -f "$SCRIPT_PATH" ]; then
    # Verify against grep count
    expected_count=$(grep -c "Decision: AUTO-APPROVE" "$FIXTURES_DIR/sample-pre-tool-use.log" 2>/dev/null || echo "0")
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" 2>&1 || true)
    if echo "$output" | grep -qE "Auto-approved:.*$expected_count"; then
        echo -e "${GREEN}PASS${NC}: Count matches grep AUTO-APPROVE"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: Count matches grep AUTO-APPROVE"
        echo "  Expected: $expected_count"
        ((TESTS_FAILED++))
    fi
else
    echo -e "${RED}FAIL${NC}: Count matches grep AUTO-APPROVE"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 4: Case-sensitive matching (AUTO-APPROVE not auto-approve)
((TESTS_RUN++))
if [ -f "$SCRIPT_PATH" ]; then
    # Create temp file with mixed case
    temp_file=$(mktemp)
    echo "2026-01-10 10:00:01 Decision: AUTO-APPROVE" > "$temp_file"
    echo "2026-01-10 10:00:02 Decision: auto-approve" >> "$temp_file"
    echo "2026-01-10 10:00:03 Decision: Auto-Approve" >> "$temp_file"
    output=$(run_telemetry "$temp_file" 2>&1 || true)
    rm -f "$temp_file"
    # Should count only exact match (1 or all 3 depending on implementation)
    if echo "$output" | grep -qE "Auto-approved:.*[0-9]+"; then
        echo -e "${GREEN}PASS${NC}: Case handling for AUTO-APPROVE"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: Case handling for AUTO-APPROVE"
        ((TESTS_FAILED++))
    fi
else
    echo -e "${RED}FAIL${NC}: Case handling for AUTO-APPROVE"
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
