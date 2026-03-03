#!/usr/bin/env bash
# =============================================================================
# STORY-363: Run All Acceptance Criteria Tests
# =============================================================================
# Executes all 6 AC test scripts and reports aggregate results.
# =============================================================================

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"

TOTAL_PASS=0
TOTAL_FAIL=0

run_test() {
    local test_file="$1"
    local test_name="$2"
    echo ""
    echo "======================================================================"
    echo "  Running: ${test_name}"
    echo "======================================================================"
    if bash "${SCRIPT_DIR}/${test_file}"; then
        TOTAL_PASS=$((TOTAL_PASS + 1))
    else
        TOTAL_FAIL=$((TOTAL_FAIL + 1))
    fi
}

run_test "test_ac1_treelint_function_discovery.sh" "AC#1: Treelint Function Discovery"
run_test "test_ac2_json_parsing.sh"                "AC#2: JSON Parsing"
run_test "test_ac3_grep_fallback.sh"               "AC#3: Grep Fallback"
run_test "test_ac4_test_source_mapping.sh"         "AC#4: Test-Source Mapping"
run_test "test_ac5_performance.sh"                 "AC#5: Performance Validation"
run_test "test_ac6_line_count.sh"                  "AC#6: Line Count Compliance"

echo ""
echo "======================================================================"
echo "  STORY-363 AGGREGATE RESULTS"
echo "======================================================================"
echo "  ACs Passed: ${TOTAL_PASS}/6"
echo "  ACs Failed: ${TOTAL_FAIL}/6"
echo "======================================================================"

if [[ "$TOTAL_FAIL" -gt 0 ]]; then
    echo "  OVERALL STATUS: FAILED (RED phase - expected)"
    exit 1
else
    echo "  OVERALL STATUS: PASSED"
    exit 0
fi
