#!/bin/bash

# STORY-132: Master Test Runner
# Executes all acceptance criteria tests and reports overall status

set -e

TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESULTS_FILE="$TEST_DIR/test-results.txt"

echo "=========================================="
echo "STORY-132: Delegate Next Action to Skill"
echo "Running All Acceptance Criteria Tests"
echo "=========================================="
echo ""

# Initialize results file
> "$RESULTS_FILE"

# Track overall pass/fail
TOTAL_TESTS=4
PASSED_TESTS=0
FAILED_TESTS=0

# Run each test
echo "Executing AC#1: Command Phase 5 Removal..."
if bash "$TEST_DIR/test-ac1-phase5-removed.sh"; then
    echo "" >> "$RESULTS_FILE"
    echo "[PASS] AC#1: Command Phase 5 Removed" >> "$RESULTS_FILE"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo "" >> "$RESULTS_FILE"
    echo "[FAIL] AC#1: Command Phase 5 Removed" >> "$RESULTS_FILE"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi
echo ""

echo "Executing AC#2: Skill Phase 6.6 Owns Next Action..."
if bash "$TEST_DIR/test-ac2-skill-owns-nextaction.sh"; then
    echo "[PASS] AC#2: Skill Phase 6.6 Owns Next Action" >> "$RESULTS_FILE"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo "[FAIL] AC#2: Skill Phase 6.6 Owns Next Action" >> "$RESULTS_FILE"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi
echo ""

echo "Executing AC#3: Command Shows Brief Confirmation Only..."
if bash "$TEST_DIR/test-ac3-command-confirmation-only.sh"; then
    echo "[PASS] AC#3: Command Shows Brief Confirmation Only" >> "$RESULTS_FILE"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo "[FAIL] AC#3: Command Shows Brief Confirmation Only" >> "$RESULTS_FILE"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi
echo ""

echo "Executing AC#4: No Duplicate Next-Action Questions..."
if bash "$TEST_DIR/test-ac4-no-duplicate-questions.sh"; then
    echo "[PASS] AC#4: No Duplicate Next-Action Questions" >> "$RESULTS_FILE"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo "[FAIL] AC#4: No Duplicate Next-Action Questions" >> "$RESULTS_FILE"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi
echo ""

# Print summary
echo "=========================================="
echo "TEST SUMMARY"
echo "=========================================="
echo "Total Tests: $TOTAL_TESTS"
echo "Passed: $PASSED_TESTS"
echo "Failed: $FAILED_TESTS"
echo ""

if [ "$FAILED_TESTS" -eq 0 ]; then
    echo "✓ ALL TESTS PASSED"
    echo ""
    echo "STORY-132 Implementation Status: VERIFIED"
    echo "  - Command Phase 5 successfully removed"
    echo "  - Skill Phase 6.6 owns next-action determination"
    echo "  - Command shows brief confirmation only"
    echo "  - No duplication of questions across boundary"
    exit 0
else
    echo "✗ SOME TESTS FAILED"
    echo ""
    echo "Review failures above and fix issues:"
    cat "$RESULTS_FILE"
    exit 1
fi
