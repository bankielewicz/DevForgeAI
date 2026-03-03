#!/bin/bash
# STORY-189: Run all acceptance criteria tests
# Usage: bash tests/STORY-189/run-all-tests.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_ROOT"

echo "========================================"
echo " STORY-189: QA Lifecycle Hook Documentation"
echo " Running All Acceptance Criteria Tests"
echo "========================================"
echo ""

TOTAL=0
PASSED=0
FAILED=0

run_test() {
    local test_file=$1
    local test_name=$2
    TOTAL=$((TOTAL + 1))

    echo "--- Running: $test_name ---"
    if bash "$test_file"; then
        PASSED=$((PASSED + 1))
        echo ""
    else
        FAILED=$((FAILED + 1))
        echo ""
    fi
}

# Run each AC test
run_test "$SCRIPT_DIR/test-ac1-qa-lifecycle-section.sh" "AC-1: QA Lifecycle Section"
run_test "$SCRIPT_DIR/test-ac2-hook-names-defined.sh" "AC-2: Hook Names Defined"
run_test "$SCRIPT_DIR/test-ac3-invocation-pattern.sh" "AC-3: Invocation Pattern"
run_test "$SCRIPT_DIR/test-ac4-example-implementations.sh" "AC-4: Example Implementations"
run_test "$SCRIPT_DIR/test-ac5-parameters-documented.sh" "AC-5: Parameters Documented"

echo "========================================"
echo " STORY-189 Test Results"
echo "========================================"
echo " Total:  $TOTAL"
echo " Passed: $PASSED"
echo " Failed: $FAILED"
echo "========================================"

if [[ $FAILED -gt 0 ]]; then
    echo ""
    echo "STATUS: RED (Tests failing as expected for TDD)"
    exit 1
else
    echo ""
    echo "STATUS: GREEN (All tests passing)"
    exit 0
fi
