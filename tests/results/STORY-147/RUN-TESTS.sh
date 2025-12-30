#!/bin/bash

# STORY-147 Test Suite Runner
# Runs all acceptance criteria tests for Smart Tech Recommendation Referencing
# Exit code: 0 if all tests pass, 1 if any test fails

set -e

PROJECT_ROOT="$(pwd)"
TEST_DIR="tests/results/STORY-147"

echo "======================================================================"
echo "STORY-147: Smart Tech Recommendation Referencing - Test Suite"
echo "======================================================================"
echo ""

TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Array to store results
declare -a RESULTS

# Run each test
for test_file in "$TEST_DIR"/test-*.sh; do
    if [ -f "$test_file" ]; then
        test_name=$(basename "$test_file")
        echo "Running: $test_name"
        echo "----------------------------------------------------------------------"
        
        if bash "$test_file"; then
            ((PASSED_TESTS++))
            RESULTS+=("✅ $test_name - PASSED")
        else
            ((FAILED_TESTS++))
            RESULTS+=("❌ $test_name - FAILED")
        fi
        echo ""
        ((TOTAL_TESTS++))
    fi
done

# Print summary
echo "======================================================================"
echo "TEST SUITE SUMMARY"
echo "======================================================================"
echo ""
echo "Total Test Files: $TOTAL_TESTS"
echo "Passed: $PASSED_TESTS"
echo "Failed: $FAILED_TESTS"
echo ""
echo "Results:"
for result in "${RESULTS[@]}"; do
    echo "  $result"
done
echo ""

if [ $FAILED_TESTS -eq 0 ]; then
    echo "✅ ALL TESTS PASSED - Ready for Phase 04 (Refactoring)"
    exit 0
else
    echo "⚠️  $FAILED_TESTS test(s) failing - This is expected in TDD RED phase"
    echo "    Implementation needed before tests will pass"
    exit 1
fi
