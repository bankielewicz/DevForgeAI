#!/bin/bash

################################################################################
# TEST SUITE: AC#4 - Approval Rate Calculation (SVC-004, SVC-005)
# Story: STORY-200
# Description: Verify hook-telemetry.sh calculates approval rate correctly
#
# Technical Requirements:
# - SVC-004: Count manual approval (grep 'ASK USER' | wc -l)
# - SVC-005: Calculate approval rate percentage
# - BR-001: Warning if approval rate < 90%
# - Formula: auto-approved / total * 100%
#
# Test Status: FAILING (Red Phase) - hook-telemetry.sh does not exist yet
################################################################################

# Note: Not using set -e to allow all tests to run

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SCRIPT_PATH="$PROJECT_ROOT/devforgeai/scripts/hook-telemetry.sh"
FIXTURES_DIR="$PROJECT_ROOT/devforgeai/tests/STORY-200/fixtures"
TEST_NAME="AC#4: Approval Rate Calculation"

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

# Test 1: Output contains "Approval rate:"
((TESTS_RUN++))
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" 2>&1 || true)
    if echo "$output" | grep -q "Approval rate:"; then
        echo -e "${GREEN}PASS${NC}: Output contains 'Approval rate:'"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: Output contains 'Approval rate:'"
        ((TESTS_FAILED++))
    fi
else
    echo -e "${RED}FAIL${NC}: Output contains 'Approval rate:'"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 2: Approval rate includes percentage sign
((TESTS_RUN++))
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" 2>&1 || true)
    if echo "$output" | grep -qE "Approval rate:.*%"; then
        echo -e "${GREEN}PASS${NC}: Approval rate includes % sign"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: Approval rate includes % sign"
        ((TESTS_FAILED++))
    fi
else
    echo -e "${RED}FAIL${NC}: Approval rate includes % sign"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 3: Approval rate calculation is accurate (50/100 = 50%)
((TESTS_RUN++))
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" 2>&1 || true)
    # Sample has 50 AUTO-APPROVE out of 100 total = 50%
    if echo "$output" | grep -qE "Approval rate:.*50(.0)?%"; then
        echo -e "${GREEN}PASS${NC}: Approval rate equals 50%"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: Approval rate equals 50%"
        echo "  Output: $output"
        ((TESTS_FAILED++))
    fi
else
    echo -e "${RED}FAIL${NC}: Approval rate equals 50%"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 4: Manual approval count displayed
((TESTS_RUN++))
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" 2>&1 || true)
    if echo "$output" | grep -q "Manual approval:"; then
        echo -e "${GREEN}PASS${NC}: Output contains 'Manual approval:'"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: Output contains 'Manual approval:'"
        ((TESTS_FAILED++))
    fi
else
    echo -e "${RED}FAIL${NC}: Output contains 'Manual approval:'"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 5: Manual approval count accurate (40 ASK USER markers)
((TESTS_RUN++))
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" 2>&1 || true)
    if echo "$output" | grep -qE "Manual approval:.*40"; then
        echo -e "${GREEN}PASS${NC}: Manual approval count equals 40"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: Manual approval count equals 40"
        ((TESTS_FAILED++))
    fi
else
    echo -e "${RED}FAIL${NC}: Manual approval count equals 40"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 6: Warning displayed when rate < 90%
((TESTS_RUN++))
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" 2>&1 || true)
    # 50% is below 90% threshold
    if echo "$output" | grep -qiE "WARNING|warning"; then
        echo -e "${GREEN}PASS${NC}: Warning displayed when rate < 90%"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: Warning displayed when rate < 90%"
        ((TESTS_FAILED++))
    fi
else
    echo -e "${RED}FAIL${NC}: Warning displayed when rate < 90%"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 7: Warning mentions 90% target
((TESTS_RUN++))
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" 2>&1 || true)
    if echo "$output" | grep -qE "(WARNING|warning).*90%|90%.*(target|threshold)"; then
        echo -e "${GREEN}PASS${NC}: Warning mentions 90% target"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: Warning mentions 90% target"
        ((TESTS_FAILED++))
    fi
else
    echo -e "${RED}FAIL${NC}: Warning mentions 90% target"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 8: No warning when rate >= 90%
((TESTS_RUN++))
if [ -f "$SCRIPT_PATH" ]; then
    temp_file=$(mktemp)
    # Create file with 95% approval rate (95 AUTO-APPROVE, 5 ASK USER)
    for i in {1..95}; do
        echo "2026-01-10 10:00:$i Decision: AUTO-APPROVE" >> "$temp_file"
    done
    for i in {1..5}; do
        echo "2026-01-10 10:01:$i Decision: ASK USER" >> "$temp_file"
    done
    output=$(run_telemetry "$temp_file" 2>&1 || true)
    rm -f "$temp_file"
    if ! echo "$output" | grep -qiE "WARNING|warning"; then
        echo -e "${GREEN}PASS${NC}: No warning when rate >= 90%"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: No warning when rate >= 90%"
        ((TESTS_FAILED++))
    fi
else
    echo -e "${RED}FAIL${NC}: No warning when rate >= 90%"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 9: Handle division by zero (empty log)
((TESTS_RUN++))
if [ -f "$SCRIPT_PATH" ]; then
    temp_file=$(mktemp)
    touch "$temp_file"  # Empty file
    output=$(run_telemetry "$temp_file" 2>&1 || true)
    rm -f "$temp_file"
    # Should not crash or show NaN/Inf
    if ! echo "$output" | grep -qiE "nan|inf|divide|error"; then
        echo -e "${GREEN}PASS${NC}: Handles empty log (no division by zero)"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: Handles empty log (no division by zero)"
        ((TESTS_FAILED++))
    fi
else
    echo -e "${RED}FAIL${NC}: Handles empty log (no division by zero)"
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
