#!/bin/bash
##############################################################################
# Test Suite: STORY-374 AC#2 - User-prompted daemon start (no silent auto-start)
# Purpose: Verify the reference file documents that when daemon is stopped,
#          Claude prompts via AskUserQuestion with three options:
#          start daemon, continue with CLI, don't ask again this session.
#          Claude MUST NOT start the daemon without explicit user consent.
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

# AC#2 Test 1: AskUserQuestion invocation documented when daemon is stopped
test_ask_user_question_documented() {
    [ -f "$REF_FILE" ] && grep -q 'AskUserQuestion' "$REF_FILE"
}

# AC#2 Test 2: Prompt triggered specifically when status is stopped
test_prompt_on_stopped_state() {
    [ -f "$REF_FILE" ] && grep -qi 'stopped.*prompt\|stopped.*ask\|status.*stopped.*AskUser' "$REF_FILE"
}

# AC#2 Test 3: Option 1 - Start the daemon
test_start_daemon_option_documented() {
    [ -f "$REF_FILE" ] && grep -qi 'start.*daemon\|yes.*start\|start the daemon' "$REF_FILE"
}

# AC#2 Test 4: Option 2 - Continue with CLI mode
test_cli_mode_option_documented() {
    [ -f "$REF_FILE" ] && grep -qi 'continue.*CLI\|CLI mode\|no.*continue' "$REF_FILE"
}

# AC#2 Test 5: Option 3 - Don't ask again this session
test_suppress_option_documented() {
    [ -f "$REF_FILE" ] && grep -qi "don.*ask again\|suppress\|don't ask again" "$REF_FILE"
}

# AC#2 Test 6: Performance improvement explanation in prompt (~200ms to ~5ms)
test_performance_explanation_documented() {
    [ -f "$REF_FILE" ] && grep -q '200ms' "$REF_FILE" && grep -q '5ms' "$REF_FILE"
}

# AC#2 Test 7: No silent auto-start constraint documented (EPIC-058)
test_no_silent_auto_start() {
    [ -f "$REF_FILE" ] && grep -qi 'no.*silent\|MUST NOT.*start.*without\|explicit.*consent\|user consent' "$REF_FILE"
}

# AC#2 Test 8: EPIC-058 constraint referenced (daemon lifecycle managed by user)
test_epic_058_constraint_referenced() {
    [ -f "$REF_FILE" ] && grep -q 'EPIC-058\|user.*managed.*lifecycle\|daemon lifecycle.*managed.*user' "$REF_FILE"
}

# AC#2 Test 9: Three options documented in AskUserQuestion format
test_three_options_in_prompt() {
    [ -f "$REF_FILE" ] && grep -qi 'options\|option' "$REF_FILE" && grep -qi 'start' "$REF_FILE" && grep -qi 'CLI\|decline' "$REF_FILE" && grep -qi "don't ask\|suppress" "$REF_FILE"
}

# AC#2 Test 10: treelint daemon start command documented (executed only after consent)
test_daemon_start_command_documented() {
    [ -f "$REF_FILE" ] && grep -q 'treelint daemon start' "$REF_FILE"
}

# Run all tests
echo "============================================================"
echo "STORY-374 AC#2: User-prompted daemon start (no silent auto-start)"
echo "============================================================"

run_test "AskUserQuestion invocation documented" test_ask_user_question_documented
run_test "Prompt on stopped state" test_prompt_on_stopped_state
run_test "Option: Start the daemon" test_start_daemon_option_documented
run_test "Option: Continue with CLI mode" test_cli_mode_option_documented
run_test "Option: Don't ask again this session" test_suppress_option_documented
run_test "Performance improvement explained (200ms to 5ms)" test_performance_explanation_documented
run_test "No silent auto-start constraint" test_no_silent_auto_start
run_test "EPIC-058 constraint referenced" test_epic_058_constraint_referenced
run_test "Three options in prompt" test_three_options_in_prompt
run_test "treelint daemon start command documented" test_daemon_start_command_documented

echo ""
echo "============================================================"
echo "Results: $TESTS_PASSED/$TESTS_RUN passed, $TESTS_FAILED failed"
echo "============================================================"

exit $TESTS_FAILED
