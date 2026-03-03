#!/usr/bin/env bash
# =============================================================================
# STORY-372: Run All Acceptance Criteria Tests
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

run_test "test_ac1_source_discovery.sh"     "AC#1: Source Function Discovery via Treelint"
run_test "test_ac2_test_discovery.sh"        "AC#2: Test Function Discovery and Name Pattern Extraction"
run_test "test_ac3_correlation.sh"           "AC#3: Semantic Correlation Between Test and Source Functions"
run_test "test_ac4_gap_report.sh"            "AC#4: Coverage Gap Identification at Function Level"
run_test "test_ac5_report_integration.sh"    "AC#5: Integration with Coverage Analyzer Reports"
run_test "test_ac6_multi_file.sh"            "AC#6: Handle Multiple Test Files per Source File"

echo ""
echo "======================================================================"
echo "  STORY-372 AGGREGATE RESULTS"
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
