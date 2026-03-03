#!/bin/bash
# Test Runner: STORY-395 - Batch Rollout Wave 1
# Runs all 7 AC test files and reports aggregate results.
# Generated: 2026-02-13

set -uo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$(dirname "$0")/../.." && pwd)}"
export PROJECT_ROOT
TEST_DIR="$(cd "$(dirname "$0")" && pwd)"

TOTAL_SUITES=0
PASSED_SUITES=0
FAILED_SUITES=0
FAILED_LIST=()

echo "=============================================="
echo "  STORY-395: Batch Rollout Wave 1 - Test Suite"
echo "  Running all 7 Acceptance Criteria tests"
echo "=============================================="
echo ""

run_suite() {
    local test_file="$1"
    local test_name="$2"
    ((TOTAL_SUITES++))

    echo "----------------------------------------------"
    echo "  Running: $test_name"
    echo "----------------------------------------------"

    if bash "$test_file"; then
        echo ""
        echo "  >> Suite PASSED: $test_name"
        ((PASSED_SUITES++))
    else
        echo ""
        echo "  >> Suite FAILED: $test_name"
        ((FAILED_SUITES++))
        FAILED_LIST+=("$test_name")
    fi
    echo ""
}

run_suite "$TEST_DIR/test_ac1_template_conformance.sh" "AC#1: Template Conformance"
run_suite "$TEST_DIR/test_ac2_anthropic_patterns.sh" "AC#2: Anthropic Patterns"
run_suite "$TEST_DIR/test_ac3_before_after_evaluation.sh" "AC#3: Before/After Evaluation"
run_suite "$TEST_DIR/test_ac4_zero_regression.sh" "AC#4: Zero Regression"
run_suite "$TEST_DIR/test_ac5_line_limits.sh" "AC#5: Line Limits"
run_suite "$TEST_DIR/test_ac6_prompt_versioning.sh" "AC#6: Prompt Versioning"
run_suite "$TEST_DIR/test_ac7_operational_sync.sh" "AC#7: Operational Sync"

echo "=============================================="
echo "  STORY-395 Aggregate Results"
echo "=============================================="
echo "  Total Suites:  $TOTAL_SUITES"
echo "  Passed Suites: $PASSED_SUITES"
echo "  Failed Suites: $FAILED_SUITES"

if [ ${#FAILED_LIST[@]} -gt 0 ]; then
    echo ""
    echo "  Failed Suites:"
    for suite in "${FAILED_LIST[@]}"; do
        echo "    - $suite"
    done
fi

echo "=============================================="

if [ "$FAILED_SUITES" -eq 0 ]; then
    echo "  OVERALL: ALL SUITES PASSED"
    exit 0
else
    echo "  OVERALL: $FAILED_SUITES SUITE(S) FAILED"
    exit 1
fi
