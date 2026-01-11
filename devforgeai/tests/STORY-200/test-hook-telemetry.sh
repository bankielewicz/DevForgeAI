#!/bin/bash

################################################################################
# TEST SUITE: STORY-200 - Hook Telemetry Metrics
# Description: Verify hook-telemetry.sh correctly calculates metrics from logs
#
# Acceptance Criteria:
# - AC#1: Total Invocation Count (SVC-001)
# - AC#2: Auto-Approval Count (SVC-002)
# - AC#3: Blocked Count (SVC-003)
# - AC#4: Approval Rate Calculation (SVC-004, SVC-005)
# - AC#5: Top Unknown Patterns Report (SVC-006)
#
# Technical Spec Requirements:
# - BR-001: Warning if approval rate < 90%
# - BR-002: Handle missing log files gracefully
#
# Test Status: FAILING (Red Phase) - hook-telemetry.sh does not exist yet
################################################################################

# Note: Not using set -e to allow all tests to run even if some fail

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SCRIPT_PATH="$PROJECT_ROOT/devforgeai/scripts/hook-telemetry.sh"
TEST_DIR="$PROJECT_ROOT/devforgeai/tests/STORY-200"
FIXTURES_DIR="$TEST_DIR/fixtures"
TEST_NAME="STORY-200: Hook Telemetry Metrics"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Helper function to run telemetry script and capture output
run_telemetry() {
    local log_file="$1"
    local unknown_file="$2"

    if [ -f "$SCRIPT_PATH" ]; then
        bash "$SCRIPT_PATH" --log "$log_file" --unknown "$unknown_file" 2>&1
    else
        echo "ERROR: Script not found: $SCRIPT_PATH"
        return 1
    fi
}

# Helper function to assert script exists
assert_script_exists() {
    local description="$1"
    ((TESTS_RUN++))

    if [ -f "$SCRIPT_PATH" ]; then
        echo -e "${GREEN}PASS${NC}: $description"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}FAIL${NC}: $description"
        echo "  Expected: $SCRIPT_PATH to exist"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Helper function to assert output contains string
assert_output_contains() {
    local output="$1"
    local expected="$2"
    local description="$3"
    ((TESTS_RUN++))

    if echo "$output" | grep -q "$expected"; then
        echo -e "${GREEN}PASS${NC}: $description"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}FAIL${NC}: $description"
        echo "  Expected output to contain: $expected"
        echo "  Actual output: $output"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Helper function to assert output matches pattern
assert_output_matches() {
    local output="$1"
    local pattern="$2"
    local description="$3"
    ((TESTS_RUN++))

    if echo "$output" | grep -qE "$pattern"; then
        echo -e "${GREEN}PASS${NC}: $description"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}FAIL${NC}: $description"
        echo "  Expected output to match pattern: $pattern"
        echo "  Actual output: $output"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Helper function to assert exit code
assert_exit_code() {
    local expected="$1"
    local actual="$2"
    local description="$3"
    ((TESTS_RUN++))

    if [ "$actual" -eq "$expected" ]; then
        echo -e "${GREEN}PASS${NC}: $description"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}FAIL${NC}: $description"
        echo "  Expected exit code: $expected"
        echo "  Actual exit code: $actual"
        ((TESTS_FAILED++))
        return 1
    fi
}

echo ""
echo -e "${BLUE}===============================================================================${NC}"
echo -e "${BLUE}TEST SUITE: $TEST_NAME${NC}"
echo -e "${BLUE}===============================================================================${NC}"
echo ""

cd "$PROJECT_ROOT" || exit 1

################################################################################
# TEST GROUP 0: Pre-Requisites
################################################################################

echo -e "${BLUE}Test Group 0: Pre-Requisites${NC}"
echo ""

# Test 0.1: Script file exists
assert_script_exists "hook-telemetry.sh script exists"

# Test 0.2: Script is executable (if exists)
((TESTS_RUN++))
if [ -f "$SCRIPT_PATH" ] && [ -x "$SCRIPT_PATH" ]; then
    echo -e "${GREEN}PASS${NC}: Script is executable"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}: Script is executable"
    echo "  Expected: $SCRIPT_PATH to be executable"
    ((TESTS_FAILED++))
fi

# Test 0.3: Test fixtures exist
((TESTS_RUN++))
if [ -f "$FIXTURES_DIR/sample-pre-tool-use.log" ]; then
    echo -e "${GREEN}PASS${NC}: Sample pre-tool-use.log fixture exists"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}: Sample pre-tool-use.log fixture exists"
    ((TESTS_FAILED++))
fi

((TESTS_RUN++))
if [ -f "$FIXTURES_DIR/sample-unknown-commands.log" ]; then
    echo -e "${GREEN}PASS${NC}: Sample unknown-commands.log fixture exists"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}: Sample unknown-commands.log fixture exists"
    ((TESTS_FAILED++))
fi

echo ""

################################################################################
# TEST GROUP 1: AC#1 - Total Invocation Count (SVC-001)
################################################################################

echo -e "${BLUE}Test Group 1: AC#1 - Total Invocation Count (SVC-001)${NC}"
echo ""

# Test 1.1: Total invocations displayed
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" "$FIXTURES_DIR/sample-unknown-commands.log" 2>&1 || true)
    assert_output_contains "$output" "Total invocations:" "Output contains 'Total invocations:'"
else
    ((TESTS_RUN++))
    echo -e "${RED}FAIL${NC}: Output contains 'Total invocations:'"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 1.2: Total count is accurate (100 entries in sample)
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" "$FIXTURES_DIR/sample-unknown-commands.log" 2>&1 || true)
    assert_output_matches "$output" "Total invocations:.*100" "Total count equals 100"
else
    ((TESTS_RUN++))
    echo -e "${RED}FAIL${NC}: Total count equals 100"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

echo ""

################################################################################
# TEST GROUP 2: AC#2 - Auto-Approval Count (SVC-002)
################################################################################

echo -e "${BLUE}Test Group 2: AC#2 - Auto-Approval Count (SVC-002)${NC}"
echo ""

# Test 2.1: Auto-approved count displayed
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" "$FIXTURES_DIR/sample-unknown-commands.log" 2>&1 || true)
    assert_output_contains "$output" "Auto-approved:" "Output contains 'Auto-approved:'"
else
    ((TESTS_RUN++))
    echo -e "${RED}FAIL${NC}: Output contains 'Auto-approved:'"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 2.2: Auto-approved count is accurate (50 AUTO-APPROVE markers)
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" "$FIXTURES_DIR/sample-unknown-commands.log" 2>&1 || true)
    assert_output_matches "$output" "Auto-approved:.*50" "Auto-approved count equals 50"
else
    ((TESTS_RUN++))
    echo -e "${RED}FAIL${NC}: Auto-approved count equals 50"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

echo ""

################################################################################
# TEST GROUP 3: AC#3 - Blocked Count (SVC-003)
################################################################################

echo -e "${BLUE}Test Group 3: AC#3 - Blocked Count (SVC-003)${NC}"
echo ""

# Test 3.1: Blocked count displayed
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" "$FIXTURES_DIR/sample-unknown-commands.log" 2>&1 || true)
    assert_output_contains "$output" "Blocked:" "Output contains 'Blocked:'"
else
    ((TESTS_RUN++))
    echo -e "${RED}FAIL${NC}: Output contains 'Blocked:'"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 3.2: Blocked count is accurate (10 BLOCK markers)
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" "$FIXTURES_DIR/sample-unknown-commands.log" 2>&1 || true)
    assert_output_matches "$output" "Blocked:.*10" "Blocked count equals 10"
else
    ((TESTS_RUN++))
    echo -e "${RED}FAIL${NC}: Blocked count equals 10"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

echo ""

################################################################################
# TEST GROUP 4: Manual Approval Count (SVC-004)
################################################################################

echo -e "${BLUE}Test Group 4: Manual Approval Count (SVC-004)${NC}"
echo ""

# Test 4.1: Manual approval count displayed
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" "$FIXTURES_DIR/sample-unknown-commands.log" 2>&1 || true)
    assert_output_contains "$output" "Manual approval:" "Output contains 'Manual approval:'"
else
    ((TESTS_RUN++))
    echo -e "${RED}FAIL${NC}: Output contains 'Manual approval:'"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 4.2: Manual approval count is accurate (40 ASK USER markers)
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" "$FIXTURES_DIR/sample-unknown-commands.log" 2>&1 || true)
    assert_output_matches "$output" "Manual approval:.*40" "Manual approval count equals 40"
else
    ((TESTS_RUN++))
    echo -e "${RED}FAIL${NC}: Manual approval count equals 40"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

echo ""

################################################################################
# TEST GROUP 5: AC#4 - Approval Rate Calculation (SVC-005)
################################################################################

echo -e "${BLUE}Test Group 5: AC#4 - Approval Rate Calculation (SVC-005)${NC}"
echo ""

# Test 5.1: Approval rate displayed
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" "$FIXTURES_DIR/sample-unknown-commands.log" 2>&1 || true)
    assert_output_contains "$output" "Approval rate:" "Output contains 'Approval rate:'"
else
    ((TESTS_RUN++))
    echo -e "${RED}FAIL${NC}: Output contains 'Approval rate:'"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 5.2: Approval rate is percentage format
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" "$FIXTURES_DIR/sample-unknown-commands.log" 2>&1 || true)
    assert_output_matches "$output" "Approval rate:.*%" "Approval rate includes percentage sign"
else
    ((TESTS_RUN++))
    echo -e "${RED}FAIL${NC}: Approval rate includes percentage sign"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 5.3: Approval rate calculation is accurate (50/100 = 50%)
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" "$FIXTURES_DIR/sample-unknown-commands.log" 2>&1 || true)
    assert_output_matches "$output" "Approval rate:.*50(.0)?%" "Approval rate equals 50%"
else
    ((TESTS_RUN++))
    echo -e "${RED}FAIL${NC}: Approval rate equals 50%"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

echo ""

################################################################################
# TEST GROUP 6: BR-001 - Warning When Rate < 90%
################################################################################

echo -e "${BLUE}Test Group 6: BR-001 - Warning When Rate < 90%${NC}"
echo ""

# Test 6.1: Warning displayed when rate < 90%
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" "$FIXTURES_DIR/sample-unknown-commands.log" 2>&1 || true)
    assert_output_contains "$output" "WARNING" "Output contains 'WARNING' when rate < 90%"
else
    ((TESTS_RUN++))
    echo -e "${RED}FAIL${NC}: Output contains 'WARNING' when rate < 90%"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 6.2: Warning mentions approval rate target
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" "$FIXTURES_DIR/sample-unknown-commands.log" 2>&1 || true)
    assert_output_matches "$output" "WARNING.*90%" "Warning mentions 90% target"
else
    ((TESTS_RUN++))
    echo -e "${RED}FAIL${NC}: Warning mentions 90% target"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

echo ""

################################################################################
# TEST GROUP 7: BR-002 - Missing Log File Handling
################################################################################

echo -e "${BLUE}Test Group 7: BR-002 - Missing Log File Handling${NC}"
echo ""

# Test 7.1: Script handles missing pre-tool-use.log gracefully
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "/nonexistent/path/pre-tool-use.log" "$FIXTURES_DIR/sample-unknown-commands.log" 2>&1 || true)
    exit_code=$?
    assert_output_contains "$output" "not found\|No such file\|does not exist" "Script reports missing log file"
else
    ((TESTS_RUN++))
    echo -e "${RED}FAIL${NC}: Script reports missing log file"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 7.2: Script handles missing unknown-commands.log gracefully
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" "/nonexistent/path/unknown.log" 2>&1 || true)
    assert_output_contains "$output" "not found\|No such file\|does not exist\|skipping" "Script reports or skips missing unknown-commands.log"
else
    ((TESTS_RUN++))
    echo -e "${RED}FAIL${NC}: Script reports or skips missing unknown-commands.log"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 7.3: Script does not crash on missing files
if [ -f "$SCRIPT_PATH" ]; then
    run_telemetry "/nonexistent/path/pre-tool-use.log" "/nonexistent/path/unknown.log" >/dev/null 2>&1
    exit_code=$?
    # Should exit with non-zero but not crash (exit code != 127 for command not found)
    ((TESTS_RUN++))
    if [ "$exit_code" -ne 127 ]; then
        echo -e "${GREEN}PASS${NC}: Script does not crash on missing files"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: Script does not crash on missing files"
        echo "  Exit code indicates script not found or crash"
        ((TESTS_FAILED++))
    fi
else
    ((TESTS_RUN++))
    echo -e "${RED}FAIL${NC}: Script does not crash on missing files"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

echo ""

################################################################################
# TEST GROUP 8: AC#5 - Top Unknown Patterns Report (SVC-006)
################################################################################

echo -e "${BLUE}Test Group 8: AC#5 - Top Unknown Patterns Report (SVC-006)${NC}"
echo ""

# Test 8.1: Top unknown patterns section displayed
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" "$FIXTURES_DIR/sample-unknown-commands.log" 2>&1 || true)
    assert_output_contains "$output" "unknown patterns\|Unknown patterns\|Top.*patterns" "Output contains unknown patterns section"
else
    ((TESTS_RUN++))
    echo -e "${RED}FAIL${NC}: Output contains unknown patterns section"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 8.2: Top pattern displayed (cd /mnt with 25 occurrences)
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" "$FIXTURES_DIR/sample-unknown-commands.log" 2>&1 || true)
    assert_output_contains "$output" "cd /mnt" "Top pattern 'cd /mnt' is displayed"
else
    ((TESTS_RUN++))
    echo -e "${RED}FAIL${NC}: Top pattern 'cd /mnt' is displayed"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 8.3: Pattern counts are displayed
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" "$FIXTURES_DIR/sample-unknown-commands.log" 2>&1 || true)
    assert_output_matches "$output" "[0-9]+ occurrence\|[0-9]+x\|([0-9]+)" "Pattern occurrence counts are shown"
else
    ((TESTS_RUN++))
    echo -e "${RED}FAIL${NC}: Pattern occurrence counts are shown"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 8.4: Limited to top 10 patterns
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" "$FIXTURES_DIR/sample-unknown-commands.log" 2>&1 || true)
    # Count lines that look like pattern entries (numbered or with counts)
    pattern_count=$(echo "$output" | grep -cE "^\s*[0-9]+\." || echo "0")
    ((TESTS_RUN++))
    if [ "$pattern_count" -le 10 ] && [ "$pattern_count" -gt 0 ]; then
        echo -e "${GREEN}PASS${NC}: Output limited to top 10 patterns"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: Output limited to top 10 patterns"
        echo "  Found: $pattern_count patterns (expected: 1-10)"
        ((TESTS_FAILED++))
    fi
else
    ((TESTS_RUN++))
    echo -e "${RED}FAIL${NC}: Output limited to top 10 patterns"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

echo ""

################################################################################
# TEST GROUP 9: Output Format Validation
################################################################################

echo -e "${BLUE}Test Group 9: Output Format Validation${NC}"
echo ""

# Test 9.1: Report header displayed
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" "$FIXTURES_DIR/sample-unknown-commands.log" 2>&1 || true)
    assert_output_contains "$output" "Hook Telemetry Report\|Telemetry Report\|=== Hook" "Report has header"
else
    ((TESTS_RUN++))
    echo -e "${RED}FAIL${NC}: Report has header"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 9.2: Date displayed in report
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$FIXTURES_DIR/sample-pre-tool-use.log" "$FIXTURES_DIR/sample-unknown-commands.log" 2>&1 || true)
    assert_output_matches "$output" "Date:.*[0-9]{4}-[0-9]{2}-[0-9]{2}\|[0-9]{4}-[0-9]{2}-[0-9]{2}" "Report contains date"
else
    ((TESTS_RUN++))
    echo -e "${RED}FAIL${NC}: Report contains date"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

echo ""

################################################################################
# TEST GROUP 10: Empty Log Handling
################################################################################

echo -e "${BLUE}Test Group 10: Empty Log Handling${NC}"
echo ""

# Create empty log fixture for testing
EMPTY_LOG="$FIXTURES_DIR/empty.log"
touch "$EMPTY_LOG" 2>/dev/null || true

# Test 10.1: Script handles empty log file
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$EMPTY_LOG" "$FIXTURES_DIR/sample-unknown-commands.log" 2>&1 || true)
    assert_output_matches "$output" "Total invocations:.*0\|No invocations\|empty" "Script handles empty log file"
else
    ((TESTS_RUN++))
    echo -e "${RED}FAIL${NC}: Script handles empty log file"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

# Test 10.2: Division by zero avoided when total is 0
if [ -f "$SCRIPT_PATH" ]; then
    output=$(run_telemetry "$EMPTY_LOG" "$FIXTURES_DIR/sample-unknown-commands.log" 2>&1 || true)
    # Should not contain "nan", "inf", or crash
    ((TESTS_RUN++))
    if ! echo "$output" | grep -qiE "nan|inf|divide by zero|floating point"; then
        echo -e "${GREEN}PASS${NC}: No division by zero error"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: No division by zero error"
        echo "  Output contains division error indicators"
        ((TESTS_FAILED++))
    fi
else
    ((TESTS_RUN++))
    echo -e "${RED}FAIL${NC}: No division by zero error"
    echo "  Reason: Script does not exist"
    ((TESTS_FAILED++))
fi

echo ""

################################################################################
# TEST SUMMARY
################################################################################

echo -e "${BLUE}===============================================================================${NC}"
echo -e "${BLUE}TEST SUMMARY: $TEST_NAME${NC}"
echo -e "${BLUE}===============================================================================${NC}"
echo ""
echo "Tests Run:    $TESTS_RUN"
echo "Tests Passed: $TESTS_PASSED"
echo "Tests Failed: $TESTS_FAILED"
echo ""

if [ $TESTS_FAILED -gt 0 ]; then
    echo -e "${RED}STATUS: FAILING (Red Phase)${NC}"
    echo ""
    echo "Expected: All tests should be FAILING initially (TDD Red phase)"
    echo "Reason:   hook-telemetry.sh does not yet exist at devforgeai/scripts/"
    echo ""
    echo "Next Step (Green Phase): Create hook-telemetry.sh implementation"
    echo ""
    exit 1
else
    echo -e "${GREEN}STATUS: PASSING${NC}"
    echo ""
    echo "All assertions passed. STORY-200 requirements satisfied."
    echo ""
    exit 0
fi
