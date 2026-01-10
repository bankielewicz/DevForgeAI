#!/bin/bash
###############################################################################
# STORY-197 Test Suite: AC#2 - Command Prefix Logging
#
# Acceptance Criteria:
# Given a command that doesn't match any safe pattern
# When the hook prepares to ask user for approval
# Then the first 20 characters of the command are logged for analysis
#
# Technical Spec: CFG-002 - Log command prefix (first 20 chars) for analysis
#
# Test Status: FAILING (Red Phase) - command prefix logging not yet implemented
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
# Test AC#2.1: Hook contains "Command starts with:" log statement
###############################################################################

test_command_prefix_log_statement() {
    local test_name="AC#2.1: Hook contains 'Command starts with:' log statement"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    if grep -q "Command starts with:" "$HOOK_FILE" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Expected: 'Command starts with:' text in $HOOK_FILE"
        echo "  Reason: Command prefix logging (CFG-002) not yet implemented"
        ((TESTS_FAILED++))
    fi
}

###############################################################################
# Test AC#2.2: Hook extracts first 20 characters
###############################################################################

test_first_20_chars_extraction() {
    local test_name="AC#2.2: Hook extracts first 20 characters of command"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    # Check for substring extraction syntax like ${COMMAND:0:20}
    if grep -E '\$\{COMMAND:0:20\}|\$\{cmd:0:20\}' "$HOOK_FILE" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Expected: Substring extraction syntax like \${COMMAND:0:20}"
        echo "  Reason: First 20 character extraction not yet implemented"
        ((TESTS_FAILED++))
    fi
}

###############################################################################
# Test AC#2.3: Log file contains command prefix for near-miss command
###############################################################################

test_log_contains_command_prefix() {
    local test_name="AC#2.3: Log contains first 20 chars for near-miss command"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    setup

    # Use a long command (>20 chars) that contains but doesn't start with safe patterns
    # 'unknown_long_cmd' doesn't match any safe pattern, but 'pytest' does
    # This triggers near-miss detection which logs the command prefix
    local long_command="unknown_long_cmd && pytest tests/"
    local expected_prefix="unknown_long_cmd &&"  # First 20 chars
    local test_input='{"tool_name":"Bash","tool_input":{"command":"'"$long_command"'"}}'

    echo "$test_input" | bash "$HOOK_FILE" > /dev/null 2>&1 || true

    # Check if log contains the command prefix
    if grep -q "Command starts with:" "$LOG_FILE" 2>/dev/null && \
       grep -q "unknown_long_cmd" "$LOG_FILE" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Expected: Log to contain 'Command starts with: $expected_prefix'"
        echo "  Reason: Command prefix logging not yet implemented"
        ((TESTS_FAILED++))
    fi

    teardown
}

###############################################################################
# Test AC#2.4: Short commands (<20 chars) logged in full
###############################################################################

test_short_command_logged_full() {
    local test_name="AC#2.4: Short commands (<20 chars) logged in full"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    setup

    # Use a short command (<20 chars) that contains a safe pattern
    # 'foo pytest' is 10 chars, contains 'pytest' safe pattern
    local short_command="foo pytest"  # 10 chars, contains 'pytest'
    local test_input='{"tool_name":"Bash","tool_input":{"command":"'"$short_command"'"}}'

    echo "$test_input" | bash "$HOOK_FILE" > /dev/null 2>&1 || true

    # Check if log contains the full short command
    if grep -q "Command starts with:" "$LOG_FILE" 2>/dev/null && \
       grep -q "foo pytest" "$LOG_FILE" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Expected: Log to contain 'Command starts with: foo pytest'"
        echo "  Reason: Command prefix logging not yet implemented"
        ((TESTS_FAILED++))
    fi

    teardown
}

###############################################################################
# Test AC#2.5: Command prefix logged only for non-matching commands
###############################################################################

test_prefix_not_logged_for_safe_commands() {
    local test_name="AC#2.5: Command prefix NOT logged for safe commands"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    setup

    # Use a safe command that WILL match
    local safe_command="git status"
    local test_input='{"tool_name":"Bash","tool_input":{"command":"'"$safe_command"'"}}'

    echo "$test_input" | bash "$HOOK_FILE" > /dev/null 2>&1 || true

    # Check that "Command starts with:" is NOT in log for safe commands
    if grep -q "Command starts with:" "$LOG_FILE" 2>/dev/null; then
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Command prefix should NOT be logged for safe (matching) commands"
        ((TESTS_FAILED++))
    else
        echo -e "${GREEN}PASS${NC}: $test_name"
        echo "  Correctly no prefix logging for safe command"
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
    echo -e "${BLUE}STORY-197 Test Suite: AC#2 - Command Prefix Logging${NC}"
    echo -e "${BLUE}===============================================================================${NC}"
    echo ""
    echo "Target File: $HOOK_FILE"
    echo "Log File: $LOG_FILE"
    echo ""

    # Run all tests
    test_command_prefix_log_statement
    test_first_20_chars_extraction
    test_log_contains_command_prefix
    test_short_command_logged_full
    test_prefix_not_logged_for_safe_commands

    # Print summary
    echo ""
    echo -e "${BLUE}===============================================================================${NC}"
    echo -e "${BLUE}Test Summary: AC#2 - Command Prefix Logging${NC}"
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
        echo "Reason: Command prefix logging (CFG-002) not yet implemented"
        echo ""
        echo "Next Step (Green Phase): Add 'Command starts with:' logging for first 20 chars"
        exit 1
    fi
}

main "$@"
