#!/bin/bash
###############################################################################
# STORY-197 Test Suite: AC#1 - Near-Miss Detection
#
# Acceptance Criteria:
# Given a command that doesn't match any safe pattern
# When the command contains a safe pattern (but doesn't start with it)
# Then the hook logs the command and the near-miss patterns found
#
# Technical Spec: CFG-001 - Add near-miss detection after pattern matching loop
# Business Rule: BR-001 - Near-miss uses contains matching (*pattern*) not prefix
#
# Test Status: FAILING (Red Phase) - near-miss detection not yet implemented
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

# Helper function for assertions
assert_contains() {
    local file="$1"
    local pattern="$2"
    local description="$3"
    ((TESTS_RUN++))

    if grep -q "$pattern" "$file" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}: $description"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}FAIL${NC}: $description"
        echo "  Expected pattern: $pattern"
        echo "  In file: $file"
        ((TESTS_FAILED++))
        return 1
    fi
}

assert_not_contains() {
    local file="$1"
    local pattern="$2"
    local description="$3"
    ((TESTS_RUN++))

    if ! grep -q "$pattern" "$file" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}: $description"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}FAIL${NC}: $description"
        echo "  Pattern should NOT be present: $pattern"
        echo "  But was found in file: $file"
        ((TESTS_FAILED++))
        return 1
    fi
}

###############################################################################
# Test AC#1.1: Hook contains NEAR_MISSES array logic
###############################################################################

test_near_misses_array_exists() {
    local test_name="AC#1.1: Hook contains NEAR_MISSES array logic"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    if grep -q "NEAR_MISSES" "$HOOK_FILE" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Expected: NEAR_MISSES variable in $HOOK_FILE"
        echo "  Reason: Near-miss detection logic not yet implemented"
        ((TESTS_FAILED++))
    fi
}

###############################################################################
# Test AC#1.2: Contains matching uses *pattern* syntax (BR-001)
###############################################################################

test_contains_matching_syntax() {
    local test_name="AC#1.2: Contains matching uses *pattern* syntax (BR-001)"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    # Check for contains matching syntax: *$pattern* or *${pattern}*
    if grep -E '\*\$\{?pattern\}?\*|\*"\$pattern"\*' "$HOOK_FILE" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Expected: Contains matching syntax (*pattern*) for near-miss detection"
        echo "  Reason: Near-miss should use contains matching, not prefix matching"
        ((TESTS_FAILED++))
    fi
}

###############################################################################
# Test AC#1.3: Near-miss detected for 'foo && pytest'
###############################################################################

test_near_miss_cd_pytest() {
    local test_name="AC#1.3: Near-miss detected for 'foo && pytest'"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    setup

    # Simulate command that contains 'pytest' but starts with 'foo' (not a safe pattern)
    # This should trigger near-miss detection per BR-001
    # Note: 'cd ' is now a safe pattern (STORY-195), so we use 'foo' which is not
    local test_input='{"tool_name":"Bash","tool_input":{"command":"foo && pytest tests/"}}'

    echo "$test_input" | bash "$HOOK_FILE" > /dev/null 2>&1 || true

    # Check if near-miss was logged
    if grep -q "NEAR.MISS\|near.miss\|near_miss" "$LOG_FILE" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Expected: Near-miss logged for 'foo && pytest tests/'"
        echo "  Command contains 'pytest' (safe pattern) but starts with 'foo'"
        echo "  Reason: Near-miss detection not yet implemented"
        ((TESTS_FAILED++))
    fi

    teardown
}

###############################################################################
# Test AC#1.4: Near-miss includes detected pattern name
###############################################################################

test_near_miss_includes_pattern_name() {
    local test_name="AC#1.4: Near-miss log includes detected pattern name"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    setup

    # Test command that contains safe pattern 'git status' but doesn't start with it
    # Note: 'echo ' is a safe pattern (STORY-195), so we use 'myapp' which is not
    local test_input='{"tool_name":"Bash","tool_input":{"command":"myapp check && git status"}}'

    echo "$test_input" | bash "$HOOK_FILE" > /dev/null 2>&1 || true

    # Check if the near-miss log includes the pattern that was detected
    if grep -q "git status\|git.status" "$LOG_FILE" 2>/dev/null && \
       grep -qi "near.miss\|near_miss" "$LOG_FILE" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Expected: Near-miss log to include pattern name 'git status'"
        echo "  Reason: Near-miss detection not yet implemented"
        ((TESTS_FAILED++))
    fi

    teardown
}

###############################################################################
# Test AC#1.5: No near-miss for commands that don't contain safe patterns
###############################################################################

test_no_near_miss_for_unknown_command() {
    local test_name="AC#1.5: No near-miss logged for commands without safe patterns"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    setup

    # Test command that doesn't contain ANY safe pattern
    local test_input='{"tool_name":"Bash","tool_input":{"command":"unknown_command --flag"}}'

    echo "$test_input" | bash "$HOOK_FILE" > /dev/null 2>&1 || true

    # Check that NO near-miss was logged (since command has no safe patterns)
    if grep -qi "near.miss\|near_miss" "$LOG_FILE" 2>/dev/null; then
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Near-miss should NOT be logged for commands without any safe patterns"
        ((TESTS_FAILED++))
    else
        echo -e "${GREEN}PASS${NC}: $test_name"
        echo "  Correctly no near-miss logged for unknown command"
        ((TESTS_PASSED++))
    fi

    teardown
}

###############################################################################
# Main Test Execution
###############################################################################

main() {
    echo ""
    echo -e "${BLUE}===============================================================================${NC}"
    echo -e "${BLUE}STORY-197 Test Suite: AC#1 - Near-Miss Detection${NC}"
    echo -e "${BLUE}===============================================================================${NC}"
    echo ""
    echo "Target File: $HOOK_FILE"
    echo "Log File: $LOG_FILE"
    echo ""

    # Run all tests
    test_near_misses_array_exists
    test_contains_matching_syntax
    test_near_miss_cd_pytest
    test_near_miss_includes_pattern_name
    test_no_near_miss_for_unknown_command

    # Print summary
    echo ""
    echo -e "${BLUE}===============================================================================${NC}"
    echo -e "${BLUE}Test Summary: AC#1 - Near-Miss Detection${NC}"
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
        echo "Reason: Near-miss detection (CFG-001, BR-001) not yet implemented"
        echo ""
        echo "Next Step (Green Phase): Implement NEAR_MISSES array logic in pre-tool-use.sh"
        exit 1
    fi
}

main "$@"
