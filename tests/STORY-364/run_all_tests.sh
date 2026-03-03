#!/usr/bin/env bash
# =============================================================================
# STORY-364: Run All Acceptance Criteria Tests
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

run_test "test_ac1_reference_file_created.sh"  "AC#1: Code-Reviewer Reference File Created"
run_test "test_ac2_god_class_detection.sh"      "AC#2: God Class Detection via Treelint"
run_test "test_ac3_long_method_detection.sh"    "AC#3: Long Method Detection via Treelint"
run_test "test_ac4_grep_fallback.sh"            "AC#4: Grep Fallback for Unsupported Languages"
run_test "test_ac5_review_prioritization.sh"    "AC#5: Review Prioritization via Treelint Map"
run_test "test_ac6_json_parsing.sh"             "AC#6: JSON Parsing of Treelint Results"

echo ""
echo "======================================================================"
echo "  STORY-364 AGGREGATE RESULTS"
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
