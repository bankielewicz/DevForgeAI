#!/bin/bash
###############################################################################
# STORY-197 Test Suite: AC#3 - Near-Miss Log Format
#
# Acceptance Criteria:
# Given a near-miss detection
# When the near-miss is logged
# Then log includes: command prefix, near-miss patterns, and recommendation message
#
# Technical Spec: CFG-001, CFG-002, CFG-003 - Complete log format
#
# Test Status: FAILING (Red Phase) - near-miss log format not yet implemented
###############################################################################

set -uo pipefail

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

# Get project root
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
HOOK_FILE="$PROJECT_ROOT/.claude/hooks/pre-tool-use.sh"
LOG_FILE="$PROJECT_ROOT/devforgeai/logs/pre-tool-use.log"
TEST_LOG_BACKUP=""

###############################################################################
# Setup and Teardown
###############################################################################

setup() {
    # Backup existing log file if it exists
    if [[ -f "$LOG_FILE" ]]; then
        TEST_LOG_BACKUP=$(mktemp)
        cp "$LOG_FILE" "$TEST_LOG_BACKUP"
    fi
    # Clear log file for clean test
    mkdir -p "$(dirname "$LOG_FILE")"
    : > "$LOG_FILE"
}

teardown() {
    # Restore original log file if backed up
    if [[ -n "$TEST_LOG_BACKUP" && -f "$TEST_LOG_BACKUP" ]]; then
        mv "$TEST_LOG_BACKUP" "$LOG_FILE"
    fi
}

###############################################################################
# Test AC#3.1: Log format includes "NEAR-MISS DETECTED" header
###############################################################################

test_near_miss_header() {
    local test_name="AC#3.1: Log format includes 'NEAR-MISS DETECTED' header"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    if grep -q "NEAR-MISS DETECTED\|NEAR_MISS DETECTED" "$HOOK_FILE" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Expected: 'NEAR-MISS DETECTED' header in log output"
        echo "  Reason: Near-miss log format not yet implemented"
        ((TESTS_FAILED++))
    fi
}

###############################################################################
# Test AC#3.2: Log includes command prefix field
###############################################################################

test_log_includes_command_prefix() {
    local test_name="AC#3.2: Near-miss log includes command prefix field"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    setup

    # Command that should trigger near-miss: contains 'pytest' but starts with 'foo'
    # Note: 'cd ' is now a safe pattern (STORY-195), so we use 'foo' which is not
    local test_input='{"tool_name":"Bash","tool_input":{"command":"foo && pytest tests/unit/"}}'

    echo "$test_input" | bash "$HOOK_FILE" > /dev/null 2>&1 || true

    # Check for command prefix in log
    if grep -qi "near.miss" "$LOG_FILE" 2>/dev/null && \
       grep -q "Command starts with:\|command.prefix\|Command:" "$LOG_FILE" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Expected: Near-miss log to include command prefix field"
        echo "  Reason: Near-miss log format not yet implemented"
        ((TESTS_FAILED++))
    fi

    teardown
}

###############################################################################
# Test AC#3.3: Log includes near-miss patterns field
###############################################################################

test_log_includes_patterns() {
    local test_name="AC#3.3: Near-miss log includes detected patterns"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    setup

    # Command that should trigger near-miss with 'pytest' pattern
    # Note: 'cd ' is now a safe pattern (STORY-195), so we use 'myapp' which is not
    local test_input='{"tool_name":"Bash","tool_input":{"command":"myapp init && pytest tests/"}}'

    echo "$test_input" | bash "$HOOK_FILE" > /dev/null 2>&1 || true

    # Check for patterns field in log
    if grep -qi "near.miss" "$LOG_FILE" 2>/dev/null && \
       grep -q "Near-miss patterns:\|patterns:\|pytest" "$LOG_FILE" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Expected: Near-miss log to include 'Near-miss patterns:' with 'pytest'"
        echo "  Reason: Near-miss log format not yet implemented"
        ((TESTS_FAILED++))
    fi

    teardown
}

###############################################################################
# Test AC#3.4: Log includes recommendation message
###############################################################################

test_log_includes_recommendation() {
    local test_name="AC#3.4: Near-miss log includes recommendation message"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    setup

    # Command that should trigger near-miss
    # Note: 'cd ' is now a safe pattern (STORY-195), so we use 'myapp' which is not
    local test_input='{"tool_name":"Bash","tool_input":{"command":"myapp build && npm run test"}}'

    echo "$test_input" | bash "$HOOK_FILE" > /dev/null 2>&1 || true

    # Check for recommendation in log
    if grep -qi "near.miss" "$LOG_FILE" 2>/dev/null && \
       grep -q "RECOMMENDATION" "$LOG_FILE" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Expected: Near-miss log to include 'RECOMMENDATION:' message"
        echo "  Reason: Near-miss log format not yet implemented"
        ((TESTS_FAILED++))
    fi

    teardown
}

###############################################################################
# Test AC#3.5: Multiple near-miss patterns logged correctly
###############################################################################

test_multiple_patterns_logged() {
    local test_name="AC#3.5: Multiple near-miss patterns logged correctly"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    setup

    # Command that contains multiple safe patterns: 'git status' and 'git diff'
    # Note: 'echo ' is a safe pattern (STORY-195), so we use 'myapp' which is not
    local test_input='{"tool_name":"Bash","tool_input":{"command":"myapp check && git status && git diff"}}'

    echo "$test_input" | bash "$HOOK_FILE" > /dev/null 2>&1 || true

    # Check for multiple patterns in log
    local git_status_found=$(grep -c "git status" "$LOG_FILE" 2>/dev/null || echo "0")
    local git_diff_found=$(grep -c "git diff" "$LOG_FILE" 2>/dev/null || echo "0")

    if grep -qi "near.miss" "$LOG_FILE" 2>/dev/null && \
       [[ "$git_status_found" -ge 1 ]] && [[ "$git_diff_found" -ge 1 ]]; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Expected: Both 'git status' and 'git diff' in near-miss patterns"
        echo "  Reason: Multiple pattern detection not yet implemented"
        ((TESTS_FAILED++))
    fi

    teardown
}

###############################################################################
# Test AC#3.6: Structured log format (timestamp + fields)
###############################################################################

test_structured_log_format() {
    local test_name="AC#3.6: Near-miss log uses structured format with timestamp"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    setup

    # Command that should trigger near-miss
    local test_input='{"tool_name":"Bash","tool_input":{"command":"foo && pytest tests/"}}'

    echo "$test_input" | bash "$HOOK_FILE" > /dev/null 2>&1 || true

    # Check for timestamp format [YYYY-MM-DD HH:MM:SS] and structured fields
    if grep -qE '\[[0-9]{4}-[0-9]{2}-[0-9]{2}' "$LOG_FILE" 2>/dev/null && \
       grep -qi "near.miss" "$LOG_FILE" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Expected: Timestamped near-miss log entry"
        echo "  Reason: Structured log format not yet implemented"
        ((TESTS_FAILED++))
    fi

    teardown
}

###############################################################################
# Main Test Execution
###############################################################################

main() {
    echo ""
    echo -e "${BLUE}===============================================================================${NC}"
    echo -e "${BLUE}STORY-197 Test Suite: AC#3 - Near-Miss Log Format${NC}"
    echo -e "${BLUE}===============================================================================${NC}"
    echo ""
    echo "Target File: $HOOK_FILE"
    echo "Log File: $LOG_FILE"
    echo ""

    # Run all tests
    test_near_miss_header
    test_log_includes_command_prefix
    test_log_includes_patterns
    test_log_includes_recommendation
    test_multiple_patterns_logged
    test_structured_log_format

    # Print summary
    echo ""
    echo -e "${BLUE}===============================================================================${NC}"
    echo -e "${BLUE}Test Summary: AC#3 - Near-Miss Log Format${NC}"
    echo -e "${BLUE}===============================================================================${NC}"
    echo "Tests Run:    $TESTS_RUN"
    echo -e "Passed:       ${GREEN}$TESTS_PASSED${NC}"
    echo -e "Failed:       ${RED}$TESTS_FAILED${NC}"
    echo ""

    if [ $TESTS_FAILED -eq 0 ]; then
        echo -e "${GREEN}All tests passed!${NC}"
        exit 0
    else
        echo -e "${RED}STATUS: FAILING (Red Phase)${NC}"
        echo ""
        echo "Expected: Tests should FAIL initially (TDD Red phase)"
        echo "Reason: Near-miss log format (CFG-001, CFG-002, CFG-003) not yet implemented"
        echo ""
        echo "Next Step (Green Phase): Implement structured near-miss log output"
        exit 1
    fi
}

main "$@"
