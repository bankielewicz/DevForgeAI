#!/bin/bash
# Test Runner: STORY-490 - RCA Status Dashboard in /audit-deferrals
# Generated: 2026-02-23
# TDD Phase: RED (all tests expected to FAIL before implementation)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

TOTAL_PASSED=0
TOTAL_FAILED=0
SUITES_PASSED=0
SUITES_FAILED=0

run_suite() {
    local script="$1"
    echo ""
    bash "$script"
    local exit_code=$?
    if [ $exit_code -eq 0 ]; then
        ((SUITES_PASSED++))
    else
        ((SUITES_FAILED++))
    fi
    return $exit_code
}

echo "======================================================"
echo "  STORY-490 Test Suite"
echo "  RCA Status Dashboard in /audit-deferrals"
echo "======================================================"

run_suite "$SCRIPT_DIR/test_ac1_open_rcas_section.sh" || true
run_suite "$SCRIPT_DIR/test_ac2_rca_scanning.sh" || true
run_suite "$SCRIPT_DIR/test_ac3_zero_rcas.sh" || true

echo ""
echo "======================================================"
echo "  Suite Summary: $SUITES_PASSED passed, $SUITES_FAILED failed"
echo "======================================================"

[ $SUITES_FAILED -eq 0 ] && exit 0 || exit 1
