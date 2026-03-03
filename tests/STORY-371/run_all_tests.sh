#!/usr/bin/env bash
# =============================================================================
# STORY-371: Run All Acceptance Criteria Tests
# =============================================================================

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"

export PROJECT_ROOT

TOTAL_PASS=0
TOTAL_FAIL=0

echo "=============================================="
echo "  STORY-371: Code Quality Metrics via Treelint AST"
echo "  Running All Acceptance Criteria Tests"
echo "=============================================="
echo ""

for test_file in "${SCRIPT_DIR}"/test_ac*.sh; do
    test_name=$(basename "$test_file" .sh)
    echo ">>> Running: ${test_name}"
    echo "----------------------------------------------"

    if bash "$test_file"; then
        TOTAL_PASS=$((TOTAL_PASS + 1))
    else
        TOTAL_FAIL=$((TOTAL_FAIL + 1))
    fi

    echo ""
done

echo "=============================================="
echo "  STORY-371 OVERALL RESULTS"
echo "  Test Suites Passed: ${TOTAL_PASS}"
echo "  Test Suites Failed: ${TOTAL_FAIL}"
echo "=============================================="

if [[ "$TOTAL_FAIL" -gt 0 ]]; then
    echo "  OVERALL STATUS: FAILED (${TOTAL_FAIL} suite(s) failed)"
    exit 1
else
    echo "  OVERALL STATUS: ALL PASSED"
    exit 0
fi
