#!/bin/bash
# STORY-192: Run all acceptance criteria tests
# Distinguishes Test Specifications from Executable Tests
#
# Usage: ./run-all-tests.sh
#
# Expected: All tests FAIL until implementation complete (TDD Red phase)

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=============================================="
echo "STORY-192: Distinguish Test Specifications"
echo "         from Executable Tests"
echo "=============================================="
echo ""
echo "Running all acceptance criteria tests..."
echo ""

# Track overall results
TOTAL_PASSED=0
TOTAL_FAILED=0

# Run each test and capture results
run_test() {
    local test_file="$1"
    local test_name="$(basename "$test_file" .sh)"

    echo "----------------------------------------------"
    echo "Running: $test_name"
    echo "----------------------------------------------"

    if bash "$test_file"; then
        ((TOTAL_PASSED++))
    else
        ((TOTAL_FAILED++))
    fi
    echo ""
}

# Run all AC tests
run_test "$SCRIPT_DIR/test-ac1-implementation-type-detection.sh"
run_test "$SCRIPT_DIR/test-ac2-slash-commands-get-specifications.sh"
run_test "$SCRIPT_DIR/test-ac3-code-gets-executable-tests.sh"
run_test "$SCRIPT_DIR/test-ac4-terminology-updated.sh"
run_test "$SCRIPT_DIR/test-ac5-output-naming-distinguished.sh"

echo "=============================================="
echo "STORY-192 Test Summary"
echo "=============================================="
echo ""
echo "Test suites passed: $TOTAL_PASSED"
echo "Test suites failed: $TOTAL_FAILED"
echo ""

if [[ $TOTAL_FAILED -gt 0 ]]; then
    echo "STATUS: RED (TDD Phase - Tests failing as expected)"
    echo ""
    echo "Next steps:"
    echo "1. Implement AC-1: Add implementation type detection to test-automator.md"
    echo "2. Implement AC-2: Add Test Specification Document terminology"
    echo "3. Implement AC-3: Add Executable unit tests terminology"
    echo "4. Implement AC-4: Update phase-02-test-first.md terminology"
    echo "5. Implement AC-5: Add output naming conventions"
    exit 1
else
    echo "STATUS: GREEN (All tests passing)"
    exit 0
fi
