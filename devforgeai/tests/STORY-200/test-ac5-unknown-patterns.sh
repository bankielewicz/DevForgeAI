#!/bin/bash

################################################################################
# TEST SUITE: AC#5 - Top Unknown Patterns Report (SVC-006)
# Story: STORY-200
# Description: Verify hook-telemetry.sh displays top 10 unknown patterns
#
# Technical Requirement:
# - SVC-006: Display top 10 unknown patterns
# - Source: hook-unknown-commands.log
# - Output: Pattern with occurrence count
#
# Test Status: FAILING (Red Phase) - hook-telemetry.sh does not exist yet
################################################################################

# Note: Not using set -e to allow all tests to run

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SCRIPT_PATH="$PROJECT_ROOT/devforgeai/scripts/hook-telemetry.sh"
FIXTURES_DIR="$PROJECT_ROOT/devforgeai/tests/STORY-200/fixtures"
TEST_NAME="AC#5: Top Unknown Patterns Report"

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
    local unknown_file="$2"
    if [ -f "$SCRIPT_PATH" ]; then
        bash "$SCRIPT_PATH" --log "$log_file" --unknown "$unknown_file" 2>&1
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

# Test 1: Output contains unknown patterns section
((TESTS_RUN++))
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" "$FIXTURES_DIR/sample-unknown-commands.log" 2>&1 || true)
    if echo "$output" | grep -qiE "unknown patterns|top.*patterns"; then
        echo -e "${GREEN}PASS${NC}: Output contains unknown patterns section"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: Output contains unknown patterns section"
        ((TESTS_FAILED++))
    fi
else
    echo -e "${RED}FAIL${NC}: Output contains unknown patterns section"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 2: Top pattern displayed (cd /mnt with 25 occurrences)
((TESTS_RUN++))
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" "$FIXTURES_DIR/sample-unknown-commands.log" 2>&1 || true)
    if echo "$output" | grep -q "cd /mnt"; then
        echo -e "${GREEN}PASS${NC}: Top pattern 'cd /mnt' is displayed"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: Top pattern 'cd /mnt' is displayed"
        ((TESTS_FAILED++))
    fi
else
    echo -e "${RED}FAIL${NC}: Top pattern 'cd /mnt' is displayed"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 3: Second pattern displayed (python3 -c with 18 occurrences)
((TESTS_RUN++))
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" "$FIXTURES_DIR/sample-unknown-commands.log" 2>&1 || true)
    if echo "$output" | grep -q "python3 -c"; then
        echo -e "${GREEN}PASS${NC}: Second pattern 'python3 -c' is displayed"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: Second pattern 'python3 -c' is displayed"
        ((TESTS_FAILED++))
    fi
else
    echo -e "${RED}FAIL${NC}: Second pattern 'python3 -c' is displayed"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 4: Pattern occurrence counts are shown
((TESTS_RUN++))
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" "$FIXTURES_DIR/sample-unknown-commands.log" 2>&1 || true)
    # Should show counts like "25 occurrences" or "(25)" or "25x"
    if echo "$output" | grep -qE "[0-9]+ occurrence|[0-9]+x|\([0-9]+\)"; then
        echo -e "${GREEN}PASS${NC}: Pattern occurrence counts are shown"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: Pattern occurrence counts are shown"
        ((TESTS_FAILED++))
    fi
else
    echo -e "${RED}FAIL${NC}: Pattern occurrence counts are shown"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 5: Limited to top 10 patterns
((TESTS_RUN++))
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" "$FIXTURES_DIR/sample-unknown-commands.log" 2>&1 || true)
    # Count numbered pattern entries (1. pattern, 2. pattern, etc.)
    pattern_count=$(echo "$output" | grep -cE "^\s*[0-9]+\." 2>/dev/null || echo "0")
    if [ "$pattern_count" -le 10 ] && [ "$pattern_count" -gt 0 ]; then
        echo -e "${GREEN}PASS${NC}: Output limited to top 10 patterns (found $pattern_count)"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: Output limited to top 10 patterns"
        echo "  Found: $pattern_count patterns"
        ((TESTS_FAILED++))
    fi
else
    echo -e "${RED}FAIL${NC}: Output limited to top 10 patterns"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 6: Patterns sorted by occurrence count (descending)
((TESTS_RUN++))
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" "$FIXTURES_DIR/sample-unknown-commands.log" 2>&1 || true)
    # cd /mnt (25) should appear before python3 -c (18)
    cd_line=$(echo "$output" | grep -n "cd /mnt" | head -1 | cut -d: -f1)
    python_line=$(echo "$output" | grep -n "python3 -c" | head -1 | cut -d: -f1)
    if [ -n "$cd_line" ] && [ -n "$python_line" ] && [ "$cd_line" -lt "$python_line" ]; then
        echo -e "${GREEN}PASS${NC}: Patterns sorted by occurrence (descending)"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: Patterns sorted by occurrence (descending)"
        ((TESTS_FAILED++))
    fi
else
    echo -e "${RED}FAIL${NC}: Patterns sorted by occurrence (descending)"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 7: Handle missing unknown-commands.log gracefully
((TESTS_RUN++))
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" "/nonexistent/unknown.log" 2>&1 || true)
    # Should not crash, may show message about missing file or skip section
    if ! echo "$output" | grep -qiE "error|crash|traceback"; then
        echo -e "${GREEN}PASS${NC}: Handles missing unknown-commands.log gracefully"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: Handles missing unknown-commands.log gracefully"
        ((TESTS_FAILED++))
    fi
else
    echo -e "${RED}FAIL${NC}: Handles missing unknown-commands.log gracefully"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 8: Handle empty unknown-commands.log
((TESTS_RUN++))
if [ -f "$SCRIPT_PATH" ]; then
    temp_file=$(mktemp)
    touch "$temp_file"
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" "$temp_file" 2>&1 || true)
    rm -f "$temp_file"
    # Should show "No unknown patterns" or similar, not crash
    if echo "$output" | grep -qiE "no unknown|0 unknown|none|empty"; then
        echo -e "${GREEN}PASS${NC}: Handles empty unknown-commands.log"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: Handles empty unknown-commands.log"
        echo "  Output should indicate no unknown patterns"
        ((TESTS_FAILED++))
    fi
else
    echo -e "${RED}FAIL${NC}: Handles empty unknown-commands.log"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 9: Pattern grouping by prefix (cd /mnt/c/Projects/* grouped as cd /mnt)
((TESTS_RUN++))
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" "$FIXTURES_DIR/sample-unknown-commands.log" 2>&1 || true)
    # The 25 "cd /mnt/c/Projects/..." entries should be grouped
    if echo "$output" | grep -qE "(cd /mnt|cd).*(25|2[0-9])"; then
        echo -e "${GREEN}PASS${NC}: Similar patterns grouped correctly"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: Similar patterns grouped correctly"
        ((TESTS_FAILED++))
    fi
else
    echo -e "${RED}FAIL${NC}: Similar patterns grouped correctly"
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
