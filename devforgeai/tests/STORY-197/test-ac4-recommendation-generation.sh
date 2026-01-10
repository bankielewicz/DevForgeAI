#!/bin/bash
###############################################################################
# STORY-197 Test Suite: AC#4 - Recommendation Generation
#
# Acceptance Criteria:
# Given a near-miss pattern is detected
# When the hook logs the near-miss
# Then a recommendation message is included:
#   "RECOMMENDATION: Command contains safe pattern but doesn't start with it -
#    consider adding pattern"
#
# Technical Spec: CFG-003 - Generate recommendation message for near-misses
#
# Test Status: FAILING (Red Phase) - recommendation generation not yet implemented
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

# Expected recommendation message (per AC#4)
EXPECTED_RECOMMENDATION="RECOMMENDATION: Command contains safe pattern but doesn't start with it"

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
# Test AC#4.1: Hook contains exact recommendation message template
###############################################################################

test_recommendation_template_exists() {
    local test_name="AC#4.1: Hook contains recommendation message template"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    # Check for the recommendation text in the hook file
    if grep -q "RECOMMENDATION:" "$HOOK_FILE" 2>/dev/null && \
       grep -q "contains safe pattern\|safe pattern" "$HOOK_FILE" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Expected: 'RECOMMENDATION: ... contains safe pattern ...' in $HOOK_FILE"
        echo "  Reason: Recommendation message (CFG-003) not yet implemented"
        ((TESTS_FAILED++))
    fi
}

###############################################################################
# Test AC#4.2: Recommendation logged for near-miss command
###############################################################################

test_recommendation_logged_for_near_miss() {
    local test_name="AC#4.2: Recommendation logged when near-miss detected"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    setup

    # Command that triggers near-miss (contains 'pytest' but starts with 'foo')
    # Note: 'cd ' is now a safe pattern (STORY-195), so we use 'foo' which is not
    local test_input='{"tool_name":"Bash","tool_input":{"command":"foo && pytest tests/"}}'

    echo "$test_input" | bash "$HOOK_FILE" > /dev/null 2>&1 || true

    # Check for recommendation in log
    if grep -q "RECOMMENDATION" "$LOG_FILE" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Expected: 'RECOMMENDATION' in log when near-miss detected"
        echo "  Reason: Recommendation generation not yet implemented"
        ((TESTS_FAILED++))
    fi

    teardown
}

###############################################################################
# Test AC#4.3: Recommendation includes "consider adding pattern"
###############################################################################

test_recommendation_includes_action() {
    local test_name="AC#4.3: Recommendation includes 'consider adding pattern'"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    setup

    # Command that triggers near-miss
    local test_input='{"tool_name":"Bash","tool_input":{"command":"source venv/bin/activate && pytest"}}'

    echo "$test_input" | bash "$HOOK_FILE" > /dev/null 2>&1 || true

    # Check for actionable recommendation
    if grep -q "consider adding pattern\|adding pattern\|add pattern" "$LOG_FILE" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Expected: 'consider adding pattern' in recommendation"
        echo "  Reason: Actionable recommendation not yet implemented"
        ((TESTS_FAILED++))
    fi

    teardown
}

###############################################################################
# Test AC#4.4: No recommendation for commands without near-miss
###############################################################################

test_no_recommendation_without_near_miss() {
    local test_name="AC#4.4: No recommendation for commands without near-miss patterns"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    setup

    # Command that doesn't contain ANY safe pattern (no near-miss possible)
    local test_input='{"tool_name":"Bash","tool_input":{"command":"totally_unknown_command --flag"}}'

    echo "$test_input" | bash "$HOOK_FILE" > /dev/null 2>&1 || true

    # Recommendation should NOT appear (no near-miss to recommend on)
    if grep -q "RECOMMENDATION" "$LOG_FILE" 2>/dev/null; then
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Recommendation should NOT appear for commands without safe patterns"
        ((TESTS_FAILED++))
    else
        echo -e "${GREEN}PASS${NC}: $test_name"
        echo "  Correctly no recommendation for unknown command"
        ((TESTS_PASSED++))
    fi

    teardown
}

###############################################################################
# Test AC#4.5: No recommendation for safe (matching) commands
###############################################################################

test_no_recommendation_for_safe_commands() {
    local test_name="AC#4.5: No recommendation for safe (matching) commands"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    setup

    # Safe command that MATCHES (starts with safe pattern)
    local test_input='{"tool_name":"Bash","tool_input":{"command":"pytest tests/unit/"}}'

    echo "$test_input" | bash "$HOOK_FILE" > /dev/null 2>&1 || true

    # Recommendation should NOT appear (command matched - no near-miss)
    if grep -q "RECOMMENDATION" "$LOG_FILE" 2>/dev/null; then
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Recommendation should NOT appear for safe matching commands"
        ((TESTS_FAILED++))
    else
        echo -e "${GREEN}PASS${NC}: $test_name"
        echo "  Correctly no recommendation for safe command"
        ((TESTS_PASSED++))
    fi

    teardown
}

###############################################################################
# Test AC#4.6: Recommendation message matches exact expected format
###############################################################################

test_exact_recommendation_format() {
    local test_name="AC#4.6: Recommendation matches expected format exactly"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    setup

    # Command that triggers near-miss
    local test_input='{"tool_name":"Bash","tool_input":{"command":"export FOO=bar && npm run test"}}'

    echo "$test_input" | bash "$HOOK_FILE" > /dev/null 2>&1 || true

    # Check for exact format per AC#4
    if grep -q "RECOMMENDATION: Command contains safe pattern but doesn't start with it" "$LOG_FILE" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Expected exact message: '$EXPECTED_RECOMMENDATION'"
        echo "  Reason: Exact recommendation format not yet implemented"
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
    echo -e "${BLUE}STORY-197 Test Suite: AC#4 - Recommendation Generation${NC}"
    echo -e "${BLUE}===============================================================================${NC}"
    echo ""
    echo "Target File: $HOOK_FILE"
    echo "Log File: $LOG_FILE"
    echo ""
    echo "Expected Recommendation Format:"
    echo "  '$EXPECTED_RECOMMENDATION'"
    echo ""

    # Run all tests
    test_recommendation_template_exists
    test_recommendation_logged_for_near_miss
    test_recommendation_includes_action
    test_no_recommendation_without_near_miss
    test_no_recommendation_for_safe_commands
    test_exact_recommendation_format

    # Print summary
    echo ""
    echo -e "${BLUE}===============================================================================${NC}"
    echo -e "${BLUE}Test Summary: AC#4 - Recommendation Generation${NC}"
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
        echo "Reason: Recommendation generation (CFG-003) not yet implemented"
        echo ""
        echo "Next Step (Green Phase): Add RECOMMENDATION log message for near-misses"
        exit 1
    fi
}

main "$@"
