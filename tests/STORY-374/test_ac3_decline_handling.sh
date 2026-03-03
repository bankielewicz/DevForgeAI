#!/bin/bash
##############################################################################
# Test Suite: STORY-374 AC#3 - Graceful handling when user declines daemon start
# Purpose: Verify the reference file documents that when user says No:
#          - Workflow continues using CLI mode immediately
#          - No error is raised
#          - No repeated warning for "don't ask again" responses
#          - Performance degrades gracefully to CLI-mode latency (~200ms)
# Phase: TDD Red - All tests expected to FAIL before implementation
##############################################################################

set -o pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
REF_FILE="${PROJECT_ROOT}/src/claude/skills/devforgeai-development/references/treelint-daemon-lifecycle.md"

run_test() {
    local test_name=$1
    local test_func=$2
    TESTS_RUN=$((TESTS_RUN + 1))
    echo -e "\n[Test $TESTS_RUN] $test_name"
    if $test_func; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo -e "${GREEN}PASSED${NC}"
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAILED${NC}"
    fi
}

# AC#3 Test 1: CLI mode fallback documented when user declines
test_cli_fallback_on_decline() {
    [ -f "$REF_FILE" ] && grep -qi 'decline.*CLI\|no.*CLI mode\|user.*decline.*CLI\|falls* back.*CLI' "$REF_FILE"
}

# AC#3 Test 2: CLI mode uses treelint command --format json (without daemon)
test_cli_mode_command_format() {
    [ -f "$REF_FILE" ] && grep -qi 'CLI.*treelint\|treelint.*--format json.*CLI\|without daemon' "$REF_FILE"
}

# AC#3 Test 3: No error raised on decline documented
test_no_error_on_decline() {
    [ -f "$REF_FILE" ] && grep -qi 'no error\|no.*error.*raised\|graceful\|without error' "$REF_FILE"
}

# AC#3 Test 4: No repeated prompt for suppress option documented
test_no_repeated_prompt_for_suppress() {
    [ -f "$REF_FILE" ] && grep -qi "no.*repeat\|suppress.*prompt\|don't ask again.*session\|suppress" "$REF_FILE"
}

# AC#3 Test 5: Graceful performance degradation documented (~200ms per query)
test_graceful_degradation_documented() {
    [ -f "$REF_FILE" ] && grep -qi 'graceful.*degrad\|CLI.*latency\|200ms.*query\|CLI.*200ms\|~200ms' "$REF_FILE"
}

# AC#3 Test 6: Workflow continues immediately (no blocking)
test_workflow_continues_immediately() {
    [ -f "$REF_FILE" ] && grep -qi 'continue.*immediately\|proceed.*CLI\|workflow.*continue\|immediately.*CLI' "$REF_FILE"
}

# AC#3 Test 7: Both decline paths documented (continue with CLI vs don't ask again)
test_both_decline_paths_documented() {
    [ -f "$REF_FILE" ] && grep -qi 'continue.*CLI' "$REF_FILE" && grep -qi "don't ask again\|suppress" "$REF_FILE"
}

# Run all tests
echo "============================================================"
echo "STORY-374 AC#3: Graceful handling when user declines daemon start"
echo "============================================================"

run_test "CLI fallback on user decline" test_cli_fallback_on_decline
run_test "CLI mode command format documented" test_cli_mode_command_format
run_test "No error raised on decline" test_no_error_on_decline
run_test "No repeated prompt for suppress option" test_no_repeated_prompt_for_suppress
run_test "Graceful performance degradation (~200ms)" test_graceful_degradation_documented
run_test "Workflow continues immediately" test_workflow_continues_immediately
run_test "Both decline paths documented" test_both_decline_paths_documented

echo ""
echo "============================================================"
echo "Results: $TESTS_PASSED/$TESTS_RUN passed, $TESTS_FAILED failed"
echo "============================================================"

exit $TESTS_FAILED
