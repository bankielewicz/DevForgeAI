#!/bin/bash
# STORY-215: Run all acceptance criteria tests
# This script runs all AC tests and reports overall status

# Note: Not using set -e to allow all tests to run

TEST_DIR="/mnt/c/Projects/DevForgeAI2/tests/STORY-215"
TOTAL_PASS=0
TOTAL_FAIL=0

echo "============================================================"
echo "STORY-215: Pre-Skill Execution Checklist Tests"
echo "============================================================"
echo ""
echo "Running all acceptance criteria tests..."
echo ""

# Run AC-1 tests
echo "------------------------------------------------------------"
if bash "$TEST_DIR/test-ac1-section-placement.sh"; then
    ((TOTAL_PASS++))
else
    ((TOTAL_FAIL++))
fi
echo ""

# Run AC-2 tests
echo "------------------------------------------------------------"
if bash "$TEST_DIR/test-ac2-verification-points.sh"; then
    ((TOTAL_PASS++))
else
    ((TOTAL_FAIL++))
fi
echo ""

# Run AC-3 tests
echo "------------------------------------------------------------"
if bash "$TEST_DIR/test-ac3-enforcement-pattern.sh"; then
    ((TOTAL_PASS++))
else
    ((TOTAL_FAIL++))
fi
echo ""

# Run AC-4 tests
echo "------------------------------------------------------------"
if bash "$TEST_DIR/test-ac4-exact-text.sh"; then
    ((TOTAL_PASS++))
else
    ((TOTAL_FAIL++))
fi
echo ""

# Summary
echo "============================================================"
echo "STORY-215 Test Summary"
echo "============================================================"
echo "AC Tests Passed: $TOTAL_PASS/4"
echo "AC Tests Failed: $TOTAL_FAIL/4"
echo ""

if [ $TOTAL_FAIL -gt 0 ]; then
    echo "OVERALL: FAILED"
    echo ""
    echo "TDD Red Phase: Tests are correctly failing."
    echo "Proceed to implementation phase to make tests pass."
    exit 1
else
    echo "OVERALL: PASSED"
    echo ""
    echo "All acceptance criteria verified successfully."
    exit 0
fi
