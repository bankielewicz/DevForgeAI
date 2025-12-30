#!/bin/bash

################################################################################
# Test Runner: STORY-146 Test Suite
#
# Runs all failing tests for STORY-146: Enforce TodoWrite in All 6 Phases
#
# Expected: All tests FAIL (TDD Red phase)
# Reason: TodoWrite not yet added to workflow files
#
# Usage: bash run-tests.sh
# Output: Summary of all test results
################################################################################

echo "================================================================================"
echo "STORY-146 Test Suite Runner"
echo "Title: Enforce TodoWrite in All 6 Ideation Phases"
echo "================================================================================"
echo ""
echo "Running TDD Red Phase Tests (Expected: ALL FAIL)"
echo "Time: $(date)"
echo ""

TEST_DIR="/mnt/c/Projects/DevForgeAI2/tests/results/STORY-146"
PASS_COUNT=0
FAIL_COUNT=0
TOTAL_COUNT=0

# Array to store test results
declare -a RESULTS

# Run each test
for test_file in "$TEST_DIR"/test_*.sh; do
    if [ -f "$test_file" ]; then
        TEST_NAME=$(basename "$test_file" .sh)
        TOTAL_COUNT=$((TOTAL_COUNT + 1))

        echo "────────────────────────────────────────────────────────────────────────────────"
        echo "Running: $TEST_NAME"
        echo "────────────────────────────────────────────────────────────────────────────────"

        # Run test and capture output
        OUTPUT=$("$test_file" 2>&1)
        EXIT_CODE=$?

        # Display output
        echo "$OUTPUT"
        echo ""

        # Track result
        if [ $EXIT_CODE -eq 0 ]; then
            RESULTS+=("✓ $TEST_NAME")
            PASS_COUNT=$((PASS_COUNT + 1))
        else
            RESULTS+=("✗ $TEST_NAME")
            FAIL_COUNT=$((FAIL_COUNT + 1))
        fi
    fi
done

# Display summary
echo "================================================================================"
echo "Test Summary"
echo "================================================================================"
echo "Total Tests: $TOTAL_COUNT"
echo "Passed: $PASS_COUNT (GREEN - Tests that should pass)"
echo "Failed: $FAIL_COUNT (RED - TDD Red phase expected)"
echo ""

echo "Results:"
for result in "${RESULTS[@]}"; do
    echo "  $result"
done

echo ""
echo "================================================================================"

# Exit with appropriate code
if [ $FAIL_COUNT -eq $TOTAL_COUNT ]; then
    echo "SUCCESS: All tests failed as expected (TDD Red phase)"
    echo "Next step: Add TodoWrite to workflow files (TDD Green phase)"
    exit 0
elif [ $PASS_COUNT -eq $TOTAL_COUNT ]; then
    echo "SUCCESS: All tests passed (TDD Green phase complete)"
    exit 0
else
    echo "PARTIAL: Some tests passed, some failed (investigate)"
    exit 1
fi
