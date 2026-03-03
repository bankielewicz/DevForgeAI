#!/bin/bash
# =============================================================================
# STORY-268: Run All Tests
# =============================================================================

cd /mnt/c/Projects/DevForgeAI2

TESTS_DIR="tests/results/STORY-268"
PASSED=0
FAILED=0

echo "============================================================"
echo "STORY-268: AC Verification Checklist Real-Time Updates"
echo "Test Suite Runner"
echo "============================================================"
echo ""

run_test() {
    local test_file="$1"
    local test_name=$(basename "$test_file" .sh)

    echo "------------------------------------------------------------"
    echo "Running: $test_name"
    echo "------------------------------------------------------------"

    if bash "$test_file"; then
        PASSED=$((PASSED + 1))
        echo "[PASSED] $test_name"
    else
        FAILED=$((FAILED + 1))
        echo "[FAILED] $test_name"
    fi
    echo ""
}

# Run all AC tests
run_test "$TESTS_DIR/test-ac1-tdd-red-phase-step5.sh"
run_test "$TESTS_DIR/test-ac2-tdd-green-phase-step4.sh"
run_test "$TESTS_DIR/test-ac3-tdd-refactor-phase-step6.sh"
run_test "$TESTS_DIR/test-ac4-integration-testing-step4.sh"
run_test "$TESTS_DIR/test-ac5-phase06-deferral-step7.sh"
run_test "$TESTS_DIR/test-ac6-git-workflow-step8.sh"
run_test "$TESTS_DIR/test-ac7-backward-compatibility.sh"
run_test "$TESTS_DIR/test-ac8-progress-display.sh"
run_test "$TESTS_DIR/test-all-phases-reference-workflow.sh"

TOTAL=$((PASSED + FAILED))

echo "============================================================"
echo "STORY-268 Test Suite Summary"
echo "============================================================"
echo ""
echo "Total Tests: $TOTAL"
echo "Passed:      $PASSED"
echo "Failed:      $FAILED"
echo ""

if [ $FAILED -gt 0 ]; then
    echo "OVERALL RESULT: FAIL (TDD Red Phase - Expected)"
    echo ""
    echo "Implementation Gaps Identified:"
    echo "  1. tdd-refactor-phase.md - Needs Step 6 dedicated section"
    echo "  2. phase-06-deferral-challenge.md - Needs AC Checklist section"
    exit 1
else
    echo "OVERALL RESULT: PASS"
    exit 0
fi
