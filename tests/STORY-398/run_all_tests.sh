#!/bin/bash
# Test Runner: STORY-398 - Quality Validation & Regression Check
# Story: STORY-398
# Generated: 2026-02-13

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

TOTAL_PASSED=0
TOTAL_FAILED=0
TESTS_RUN=0

echo "=============================================="
echo "  STORY-398: Quality Validation Test Suite"
echo "=============================================="
echo ""

run_suite() {
    local test_file="$1"
    local test_name="$2"
    TESTS_RUN=$((TESTS_RUN + 1))

    echo "--- [$TESTS_RUN] $test_name ---"
    if bash "$test_file"; then
        echo "  >> SUITE PASSED"
    else
        echo "  >> SUITE FAILED"
        TOTAL_FAILED=$((TOTAL_FAILED + 1))
    fi
    echo ""
}

run_suite "$SCRIPT_DIR/test_ac1_evaluation_pipeline.sh" "AC#1: Evaluation Pipeline"
run_suite "$SCRIPT_DIR/test_ac2_regression_suite.sh" "AC#2: Regression Suite"
run_suite "$SCRIPT_DIR/test_ac3_rollback_capability.sh" "AC#3: Rollback Capability"
run_suite "$SCRIPT_DIR/test_ac4_signoff_document.sh" "AC#4: Sign-Off Document"
run_suite "$SCRIPT_DIR/test_ac5_quality_comparison.sh" "AC#5: Quality Comparison"

echo "=============================================="
echo "  Final Results: $TESTS_RUN suites run"
echo "  Failed suites: $TOTAL_FAILED"
echo "=============================================="

[ "$TOTAL_FAILED" -eq 0 ] && exit 0 || exit 1
