#!/bin/bash
# STORY-313: Run all acceptance criteria tests
# Master test runner for triple mirror consolidation

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=============================================="
echo "STORY-313: Consolidate Triple Mirror Pattern"
echo "Running All Acceptance Criteria Tests"
echo "=============================================="
echo ""

TOTAL_SUITES=0
PASSED_SUITES=0
FAILED_SUITES=0

run_suite() {
    local suite_name="$1"
    local suite_script="$2"

    echo "----------------------------------------------"
    echo "Running: $suite_name"
    echo "----------------------------------------------"

    TOTAL_SUITES=$((TOTAL_SUITES + 1))

    if bash "$SCRIPT_DIR/$suite_script"; then
        echo "Suite PASSED: $suite_name"
        PASSED_SUITES=$((PASSED_SUITES + 1))
    else
        echo "Suite FAILED: $suite_name"
        FAILED_SUITES=$((FAILED_SUITES + 1))
    fi
    echo ""
}

# Run all test suites
run_suite "AC#1: Sync Script Tests" "test-ac1-sync-script.sh"
run_suite "AC#2: CI Workflow Tests" "test-ac2-ci-workflow.sh"
run_suite "AC#3: ADR Tests" "test-ac3-adr.sh"

echo "=============================================="
echo "STORY-313 Test Summary"
echo "=============================================="
echo "Total Suites: $TOTAL_SUITES"
echo "Passed: $PASSED_SUITES"
echo "Failed: $FAILED_SUITES"
echo "=============================================="

if [ $FAILED_SUITES -gt 0 ]; then
    echo "RESULT: FAILED (TDD Red Phase - Expected)"
    exit 1
fi

echo "RESULT: PASSED"
exit 0
