#!/bin/bash

################################################################################
# STORY-230: Track Error Recovery Patterns - Test Runner
#
# Runs all acceptance criteria tests for STORY-230.
# Expected: All tests FAIL initially (TDD Red phase)
#
# Usage: bash run_tests.sh
################################################################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_TOTAL=0

echo "============================================================"
echo "STORY-230: Track Error Recovery Patterns - Test Suite"
echo "============================================================"
echo ""
echo "TDD Phase: RED (tests should fail - implementation not started)"
echo "Date: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""
echo "------------------------------------------------------------"

# Function to run a single test
run_test() {
    local test_file=$1
    local test_name=$(basename "$test_file" .sh)
    TESTS_TOTAL=$((TESTS_TOTAL + 1))

    echo ""
    echo "Running: $test_name"
    echo "------------------------------------------------------------"

    bash "$test_file"
    local exit_code=$?

    if [ $exit_code -eq 0 ]; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo "[PASSED] $test_name"
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo "[FAILED] $test_name (exit code: $exit_code)"
    fi

    echo "------------------------------------------------------------"
}

# Run all test_*.sh files
for test_file in "$SCRIPT_DIR"/test_*.sh; do
    if [ -f "$test_file" ]; then
        run_test "$test_file"
    fi
done

# Summary
echo ""
echo "============================================================"
echo "TEST SUMMARY"
echo "============================================================"
echo ""
echo "Total:  $TESTS_TOTAL"
echo "Passed: $TESTS_PASSED"
echo "Failed: $TESTS_FAILED"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo "STATUS: ALL TESTS PASSED"
    echo ""
    echo "TDD Phase Complete: GREEN (all tests passing)"
    exit 0
else
    echo "STATUS: TESTS FAILING ($TESTS_FAILED/$TESTS_TOTAL)"
    echo ""
    echo "TDD Phase: RED (expected - implementation needed)"
    echo ""
    echo "Next Steps:"
    echo "  1. Implement Error Recovery Patterns section in session-miner.md"
    echo "  2. Add RecoveryEntry data model"
    echo "  3. Define recovery action classification algorithm"
    echo "  4. Add success rate calculation workflow"
    echo "  5. Define error-recovery correlation analysis"
    echo "  6. Re-run tests to verify GREEN phase"
    exit 1
fi
