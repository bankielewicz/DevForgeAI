#!/bin/bash
# Test Runner: STORY-547 - When to Hire a Professional Framework
# Story: STORY-547
# Generated: 2026-03-06

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOTAL_PASSED=0
TOTAL_FAILED=0
SUITE_FAILURES=0

echo "=============================================="
echo "  STORY-547: When to Hire a Professional Tests"
echo "=============================================="
echo ""

run_suite() {
    local test_file="$1"
    local test_name="$2"

    echo "--- $test_name ---"
    output=$(bash "$SCRIPT_DIR/$test_file" 2>&1)
    exit_code=$?
    echo "$output"

    passed=$(echo "$output" | grep -oP '\d+(?= passed)' || echo "0")
    failed=$(echo "$output" | grep -oP '\d+(?= failed)' || echo "0")

    TOTAL_PASSED=$((TOTAL_PASSED + passed))
    TOTAL_FAILED=$((TOTAL_FAILED + failed))

    if [ "$exit_code" -ne 0 ]; then
        ((SUITE_FAILURES++))
    fi

    echo ""
}

run_suite "test_ac1_complexity_triggers.sh" "AC#1: Complexity Indicators"
run_suite "test_ac2_reference_accessible.sh" "AC#2: Reference Accessible"
run_suite "test_ac3_self_help_threshold.sh" "AC#3: Self-Help Threshold"
run_suite "test_ac4_disclaimer.sh" "AC#4: Disclaimer"
run_suite "test_ac5_line_count.sh" "AC#5: Line Count"

echo "=============================================="
echo "  OVERALL RESULTS"
echo "=============================================="
echo "  Total Passed: $TOTAL_PASSED"
echo "  Total Failed: $TOTAL_FAILED"
echo "  Suites Failed: $SUITE_FAILURES / 5"
echo "=============================================="

[ $TOTAL_FAILED -eq 0 ] && exit 0 || exit 1
