#!/bin/bash
#
# Run All Tests for STORY-168
# Migration Script Test Suite Runner
#

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "========================================================================"
echo "STORY-168 Test Suite: RCA-012 Story Migration Script"
echo "========================================================================"
echo ""

# Track overall results
TOTAL_TESTS=0
TOTAL_PASSED=0
TOTAL_FAILED=0
SUITES_PASSED=0
SUITES_FAILED=0

run_test_suite() {
    local suite_name="$1"
    local test_file="$2"

    echo "--------------------------------------------------------------------"
    echo "Running: $suite_name"
    echo "--------------------------------------------------------------------"

    if bash "$SCRIPT_DIR/$test_file"; then
        SUITES_PASSED=$((SUITES_PASSED + 1))
    else
        SUITES_FAILED=$((SUITES_FAILED + 1))
    fi

    echo ""
}

# Run all test suites
run_test_suite "AC#1: Script Exists" "test-ac1-script-exists.sh"
run_test_suite "AC#2: Find/Replace" "test-ac2-find-replace.sh"
run_test_suite "AC#3: Backup Creation" "test-ac3-backup-creation.sh"
run_test_suite "AC#4: Format Version" "test-ac4-format-version.sh"
run_test_suite "AC#5: Directory Handling" "test-ac5-directory-handling.sh"
run_test_suite "Edge Cases" "test-edge-cases.sh"

# Print overall summary
echo "========================================================================"
echo "OVERALL SUMMARY"
echo "========================================================================"
echo "Test suites passed: $SUITES_PASSED"
echo "Test suites failed: $SUITES_FAILED"
echo "Total suites:       $((SUITES_PASSED + SUITES_FAILED))"
echo ""

if [[ $SUITES_FAILED -eq 0 ]]; then
    echo "ALL TEST SUITES PASSED"
    exit 0
else
    echo "SOME TEST SUITES FAILED"
    exit 1
fi
