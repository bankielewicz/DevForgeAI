#!/bin/bash
##############################################################################
# Test Suite: STORY-374 AC#7 - Session-level "don't ask again" persistence
# Purpose: Verify the reference file documents that when user selects
#          "don't ask again this session":
#          - Daemon start prompt is suppressed for remainder of session
#          - CLI mode is used automatically
#          - No AskUserQuestion invoked for daemon start in same session
#          - Suppression flag is in-memory only (resets on new session)
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

# AC#7 Test 1: Session suppression flag documented
test_suppression_flag_documented() {
    [ -f "$REF_FILE" ] && grep -qi 'daemon_prompt_suppressed\|suppression.*flag\|suppress.*flag\|session.*flag' "$REF_FILE"
}

# AC#7 Test 2: Flag defaults to false documented
test_flag_default_false() {
    [ -f "$REF_FILE" ] && grep -qi 'default.*false\|false.*default\|initially.*false' "$REF_FILE"
}

# AC#7 Test 3: Flag set to true when user selects suppress option
test_flag_set_on_suppress() {
    [ -f "$REF_FILE" ] && grep -qi 'set.*true\|flag.*true\|suppress.*true\|true.*suppress' "$REF_FILE"
}

# AC#7 Test 4: Prompt suppressed for remainder of session
test_prompt_suppressed_remainder() {
    [ -f "$REF_FILE" ] && grep -qi 'remainder.*session\|rest.*session\|suppress.*session\|session.*suppress' "$REF_FILE"
}

# AC#7 Test 5: CLI mode used automatically when suppressed
test_cli_auto_when_suppressed() {
    [ -f "$REF_FILE" ] && grep -qi 'CLI.*automatic\|automatic.*CLI\|suppressed.*CLI\|CLI.*suppressed' "$REF_FILE"
}

# AC#7 Test 6: No AskUserQuestion when flag is true
test_no_ask_when_suppressed() {
    [ -f "$REF_FILE" ] && grep -qi 'skip.*AskUser\|no.*AskUser\|bypass.*prompt\|suppress.*prompt\|skip.*prompt' "$REF_FILE"
}

# AC#7 Test 7: In-memory only (no persistent file) documented
test_in_memory_only() {
    [ -f "$REF_FILE" ] && grep -qi 'in-memory\|in memory\|not.*persist\|no.*persistent\|memory.*only' "$REF_FILE"
}

# AC#7 Test 8: Resets on new session documented
test_resets_on_new_session() {
    [ -f "$REF_FILE" ] && grep -qi 'reset.*session\|new.*session.*reset\|session.*reset\|resets.*new' "$REF_FILE"
}

# AC#7 Test 9: Subsequent status checks skip prompt when suppressed
test_subsequent_checks_skip_prompt() {
    [ -f "$REF_FILE" ] && grep -qi 'subsequent.*skip\|skip.*subsequent\|next.*check.*skip\|suppressed.*check' "$REF_FILE"
}

# Run all tests
echo "============================================================"
echo "STORY-374 AC#7: Session-level don't ask again persistence"
echo "============================================================"

run_test "Suppression flag documented" test_suppression_flag_documented
run_test "Flag defaults to false" test_flag_default_false
run_test "Flag set to true on suppress option" test_flag_set_on_suppress
run_test "Prompt suppressed for remainder of session" test_prompt_suppressed_remainder
run_test "CLI mode auto when suppressed" test_cli_auto_when_suppressed
run_test "No AskUserQuestion when flag true" test_no_ask_when_suppressed
run_test "In-memory only (no persistent file)" test_in_memory_only
run_test "Resets on new session" test_resets_on_new_session
run_test "Subsequent status checks skip prompt" test_subsequent_checks_skip_prompt

echo ""
echo "============================================================"
echo "Results: $TESTS_PASSED/$TESTS_RUN passed, $TESTS_FAILED failed"
echo "============================================================"

exit $TESTS_FAILED
