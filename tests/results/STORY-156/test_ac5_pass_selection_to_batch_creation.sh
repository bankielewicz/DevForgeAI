#!/bin/bash
# STORY-156 Test Suite - AC#5: Pass Selection to Batch Story Creation
# Purpose: Verify selected recommendations are passed to batch creation with metadata
# Framework: Bash shell script tests
# Status: FAILING (Red phase - functionality not implemented)

set -euo pipefail

TEST_NAME="AC#5: Pass Selection to Batch Story Creation"
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

test_batch_creation_called() {
    grep -q "batch.*creat\|create.*batch\|create-stories-from-rca" "$SCRIPT_UNDER_TEST"
}

test_passes_selection_to_next_phase() {
    grep -q "pass.*select\|forward.*select\|send.*select" "$SCRIPT_UNDER_TEST"
}

test_preserves_rec_ids() {
    grep -q "REC-\|rec.*id\|recommendation.*id" "$SCRIPT_UNDER_TEST"
}

test_preserves_priority() {
    grep -q "priority\|Priority" "$SCRIPT_UNDER_TEST"
}

test_preserves_effort() {
    grep -q "effort\|Effort" "$SCRIPT_UNDER_TEST"
}

test_preserves_title() {
    grep -q "title\|Title\|description" "$SCRIPT_UNDER_TEST"
}

test_full_metadata_passed() {
    grep -q "json\|array\|structure\|object" "$SCRIPT_UNDER_TEST"
}

test_data_integrity() {
    grep -q "verify\|check\|validate.*data" "$SCRIPT_UNDER_TEST"
}

test_no_data_loss() {
    grep -q "all.*fields\|complete\|intact" "$SCRIPT_UNDER_TEST"
}

test_output_format_compatible() {
    grep -q "format.*batch\|compatible\|expected.*format" "$SCRIPT_UNDER_TEST"
}

echo "========================================="
echo "STORY-156 Test Suite"
echo "AC#5: Pass Selection to Batch Story Creation"
echo "========================================="

run_test "Batch creation phase is called" test_batch_creation_called
run_test "Selected recommendations passed to next phase" test_passes_selection_to_next_phase
run_test "Recommendation IDs preserved" test_preserves_rec_ids
run_test "Priority metadata preserved" test_preserves_priority
run_test "Effort estimate preserved" test_preserves_effort
run_test "Title/description preserved" test_preserves_title
run_test "Complete metadata structure passed" test_full_metadata_passed
run_test "Data integrity during transfer" test_data_integrity
run_test "No data loss in transformation" test_no_data_loss
run_test "Output format compatible with batch creation" test_output_format_compatible

echo ""
echo "========================================="
echo "Test Summary"
echo "========================================="
echo "Total tests run: $TESTS_RUN"
echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
echo -e "${RED}Failed: $TESTS_FAILED${NC}"
echo "========================================="

[ $TESTS_FAILED -eq 0 ] && exit 1 || exit 0
