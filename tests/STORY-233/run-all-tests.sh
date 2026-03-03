#!/bin/bash
# STORY-233: Run all Decision Context Search tests
# This is a simple runner that executes each test script
#
# Usage: bash tests/STORY-233/run-all-tests.sh
#
# Expected output: All tests should FAIL (TDD Red Phase)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=============================================="
echo "STORY-233: Running All Tests"
echo "Search and Retrieve Decision Context"
echo "=============================================="
echo ""

total_exit_code=0
test_count=0
failed_tests=0

for test_file in "$SCRIPT_DIR"/test-ac*.sh; do
    echo "Running: $(basename "$test_file")"
    echo "----------------------------------------------"
    bash "$test_file"
    exit_code=$?
    test_count=$((test_count + 1))
    if [[ $exit_code -ne 0 ]]; then
        total_exit_code=1
        failed_tests=$((failed_tests + 1))
    fi
    echo ""
done

echo "=============================================="
echo "STORY-233 Test Suite Summary"
echo "=============================================="
echo "Test files run: $test_count"
echo "Test files failed: $failed_tests"
echo ""

if [[ $total_exit_code -eq 0 ]]; then
    echo "STATUS: GREEN - All tests passed"
else
    echo "STATUS: RED (TDD Red Phase - Expected)"
    echo ""
    echo "Expected Functions to Implement in plan_file_kb.sh:"
    echo "  - search_by_story_id(index_dir, story_id)"
    echo "  - search_by_date_range(index_dir, start_date, end_date)"
    echo "  - search_by_keywords(index_dir, keywords)"
    echo "  - retrieve_decision_context(index_dir, plan_file)"
fi
echo "=============================================="

exit $total_exit_code
