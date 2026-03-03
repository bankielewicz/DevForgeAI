#!/bin/bash
# Test Runner: STORY-499 - Expand Halt Trigger to Cover "Not Applicable" Reframing
# Generated: 2026-02-24
# Phase: RED (all tests should FAIL before implementation)
#
# Runs all 4 acceptance criteria test files and provides aggregate summary.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOTAL_PASSED=0
TOTAL_FAILED=0
TOTAL_SUITES=0
FAILED_SUITES=0

echo "======================================================"
echo "  STORY-499: Expand Halt Trigger to Cover N/A Reframing"
echo "  Test Suite Runner"
echo "  Date: $(date '+%Y-%m-%d %H:%M:%S')"
echo "======================================================"
echo ""

run_suite() {
    local test_file="$1"
    local suite_name="$2"
    ((TOTAL_SUITES++))

    echo "------------------------------------------------------"
    echo "  Running: $suite_name"
    echo "  File: $test_file"
    echo "------------------------------------------------------"

    bash "$test_file"
    local exit_code=$?

    if [ $exit_code -eq 0 ]; then
        echo "  >>> SUITE PASSED <<<"
        ((TOTAL_PASSED++))
    else
        echo "  >>> SUITE FAILED <<<"
        ((TOTAL_FAILED++))
        ((FAILED_SUITES++))
    fi
    echo ""
}

# Run all test suites
run_suite "${SCRIPT_DIR}/test_ac1_halt_trigger_operational.sh" "AC#1: Halt Trigger Updated in Operational File"
run_suite "${SCRIPT_DIR}/test_ac2_halt_trigger_source.sh"      "AC#2: Halt Trigger Updated in Source File"
run_suite "${SCRIPT_DIR}/test_ac3_skip_coverage.sh"            "AC#3: Original Skip Coverage Preserved"
run_suite "${SCRIPT_DIR}/test_ac4_prescriptive_action.sh"      "AC#4: Prescriptive Action Includes Reference File Loading"

# Aggregate Summary
echo "======================================================"
echo "  AGGREGATE RESULTS"
echo "======================================================"
echo "  Suites Passed: $TOTAL_PASSED / $TOTAL_SUITES"
echo "  Suites Failed: $TOTAL_FAILED / $TOTAL_SUITES"
echo ""

if [ $FAILED_SUITES -eq 0 ]; then
    echo "  STATUS: ALL SUITES PASSED"
    exit 0
else
    echo "  STATUS: $FAILED_SUITES SUITE(S) FAILED"
    echo ""
    echo "  Expected in RED phase: All suites should FAIL"
    echo "  If any suite PASSED, investigate test specificity."
    exit 1
fi
