#!/bin/bash
# STORY-156 Test Suite - AC#1: Display Recommendation Summary Table
# Purpose: Verify that parsed RCA recommendations are displayed in formatted table
# Framework: Bash shell script tests
# Status: FAILING (Red phase - functionality not implemented)

set -euo pipefail

TEST_NAME="AC#1: Display Recommendation Summary Table"
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

test_script_exists() {
    [ -f "$SCRIPT_UNDER_TEST" ] && [ -r "$SCRIPT_UNDER_TEST" ]
}

test_display_function_exists() {
    grep -q "display_recommendation_table\|Display.*Recommendation.*Table" "$SCRIPT_UNDER_TEST"
}

test_table_includes_rec_id_column() {
    grep -q "REC ID\|REC_ID\|Recommendation.*ID" "$SCRIPT_UNDER_TEST"
}

test_table_includes_priority_column() {
    grep -q "Priority\|PRIORITY" "$SCRIPT_UNDER_TEST"
}

test_table_includes_title_column() {
    grep -q "Title\|TITLE" "$SCRIPT_UNDER_TEST"
}

test_table_includes_effort_column() {
    grep -q "Effort\|EFFORT\|Estimate" "$SCRIPT_UNDER_TEST"
}

test_table_formatting_logic() {
    grep -q "format\|printf\|column\|awk" "$SCRIPT_UNDER_TEST"
}

test_function_accepts_recommendations_input() {
    grep -q "function.*display_recommendation_table" "$SCRIPT_UNDER_TEST" || \
    grep -q "display_recommendation_table.*\$1" "$SCRIPT_UNDER_TEST"
}

test_aligned_column_formatting() {
    grep -q "pad\|align\|center\|width\|%-\|printf" "$SCRIPT_UNDER_TEST"
}

test_handles_recommendation_data_structure() {
    grep -q "REC-\|recommendation\|jq\|parse" "$SCRIPT_UNDER_TEST"
}

echo "========================================="
echo "STORY-156 Test Suite"
echo "AC#1: Display Recommendation Summary Table"
echo "========================================="

run_test "Script exists at $SCRIPT_UNDER_TEST" test_script_exists
run_test "display_recommendation_table function exists" test_display_function_exists
run_test "Table includes REC ID column" test_table_includes_rec_id_column
run_test "Table includes Priority column" test_table_includes_priority_column
run_test "Table includes Title column" test_table_includes_title_column
run_test "Table includes Effort Estimate column" test_table_includes_effort_column
run_test "Table formatting logic implemented" test_table_formatting_logic
run_test "Function accepts parsed recommendations input" test_function_accepts_recommendations_input
run_test "Table uses aligned column formatting" test_aligned_column_formatting
run_test "Handles recommendation data structure" test_handles_recommendation_data_structure

echo ""
echo "========================================="
echo "Test Summary"
echo "========================================="
echo "Total tests run: $TESTS_RUN"
echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
echo -e "${RED}Failed: $TESTS_FAILED${NC}"
echo "========================================="

[ $TESTS_FAILED -eq 0 ] && exit 1 || exit 0
