#!/bin/bash
# STORY-156 Test Suite - AC#2: Multi-Select Recommendations via AskUserQuestion
# Purpose: Verify AskUserQuestion presents options with multiSelect: true
# Framework: Bash shell script tests
# Status: FAILING (Red phase - functionality not implemented)

set -euo pipefail

TEST_NAME="AC#2: Multi-Select Recommendations via AskUserQuestion"
TEST_FILE="$(basename "$0")"
SCRIPT_UNDER_TEST=".claude/commands/create-stories-from-rca.md"

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

run_test() {
    local test_name="$1"
    local test_func="$2"
    TESTS_RUN=$((TESTS_RUN + 1))
    echo -e "\n${YELLOW}Running:${NC} $test_name"
    if $test_func; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo -e "${GREEN}PASS${NC}: $test_name"
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC}: $test_name"
    fi
}

test_selection_prompt_function_exists() {
    grep -q "prompt_user_for_selection\|ask.*selection\|AskUserQuestion" "$SCRIPT_UNDER_TEST"
}

test_askuserquestion_invoked() {
    grep -q "AskUserQuestion" "$SCRIPT_UNDER_TEST"
}

test_multiselect_true() {
    grep -q "multiSelect.*true\|multiSelect: true" "$SCRIPT_UNDER_TEST"
}

test_question_text_set() {
    grep -q "question.*Which recommendations\|header.*Select" "$SCRIPT_UNDER_TEST"
}

test_options_from_recommendations() {
    grep -q "options.*recommendation\|option.*REC-\|options.*\$" "$SCRIPT_UNDER_TEST"
}

test_accepts_recommendations_array() {
    grep -q "function.*prompt_user_for_selection" "$SCRIPT_UNDER_TEST" || \
    grep -q "prompt_user_for_selection.*\$1" "$SCRIPT_UNDER_TEST"
}

test_captures_user_selection() {
    grep -q "response\|selection\|answer\|result" "$SCRIPT_UNDER_TEST"
}

test_each_recommendation_selectable() {
    grep -q "for.*recommendation\|while.*read\|mapfile\|array" "$SCRIPT_UNDER_TEST"
}

test_selected_options_returned() {
    grep -q "echo.*selected\|return.*selection\|selected_recs" "$SCRIPT_UNDER_TEST"
}

test_integrates_with_rca_parser() {
    grep -q "STORY-155\|rca.*parser\|parse.*output" "$SCRIPT_UNDER_TEST"
}

echo "========================================="
echo "STORY-156 Test Suite"
echo "AC#2: Multi-Select via AskUserQuestion"
echo "========================================="

run_test "prompt_user_for_selection function exists" test_selection_prompt_function_exists
run_test "AskUserQuestion tool is invoked" test_askuserquestion_invoked
run_test "multiSelect parameter set to true" test_multiselect_true
run_test "Question text is configured" test_question_text_set
run_test "Options built from recommendations" test_options_from_recommendations
run_test "Function accepts recommendations array" test_accepts_recommendations_array
run_test "User selection is captured" test_captures_user_selection
run_test "Each recommendation is selectable" test_each_recommendation_selectable
run_test "Selected options are returned" test_selected_options_returned
run_test "Integrates with STORY-155 RCA parser" test_integrates_with_rca_parser

echo ""
echo "========================================="
echo "Test Summary"
echo "========================================="
echo "Total tests run: $TESTS_RUN"
echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
echo -e "${RED}Failed: $TESTS_FAILED${NC}"
echo "========================================="

[ $TESTS_FAILED -eq 0 ] && exit 1 || exit 0
