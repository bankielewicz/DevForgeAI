#!/usr/bin/env bash
# =============================================================================
# STORY-367: Run All Acceptance Criteria Tests
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

run_test "test_ac1_treelint_structure_analysis.sh"  "AC#1: Treelint Integration for Code Structure Analysis"
run_test "test_ac2_json_parsing.sh"                  "AC#2: JSON Parsing of Treelint Search Results"
run_test "test_ac3_grep_fallback.sh"                 "AC#3: Grep Fallback for Unsupported Languages"
run_test "test_ac4_refactoring_patterns.sh"          "AC#4: Refactoring-Specific Treelint Patterns"
run_test "test_ac5_line_count.sh"                    "AC#5: Progressive Disclosure Compliance"
run_test "test_ac6_ranked_file_map.sh"               "AC#6: Ranked File Map for Refactoring Prioritization"

echo ""
echo "======================================================================"
echo "  STORY-367 AGGREGATE RESULTS"
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
