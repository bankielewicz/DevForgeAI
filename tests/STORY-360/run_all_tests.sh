#!/usr/bin/env bash
# =============================================================================
# STORY-360: Run All AC Tests
# =============================================================================
# Executes all 5 acceptance criteria test scripts and reports aggregate results.
# =============================================================================

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"

AC_PASS=0
AC_FAIL=0
RESULTS=()

run_test() {
    local test_file="$1"
    local ac_name="$2"
    echo ""
    echo "================================================================"
    echo "  Running: ${ac_name}"
    echo "================================================================"
    echo ""

    if bash "${SCRIPT_DIR}/${test_file}"; then
        AC_PASS=$((AC_PASS + 1))
        RESULTS+=("  PASS: ${ac_name}")
    else
        AC_FAIL=$((AC_FAIL + 1))
        RESULTS+=("  FAIL: ${ac_name}")
    fi
}

echo "================================================================"
echo "  STORY-360: Context File Validation - Full Test Suite"
echo "================================================================"

run_test "test_ac1_syntax_validation.sh"       "AC#1: Syntax Validation"
run_test "test_ac2_locked_markers.sh"          "AC#2: LOCKED Markers"
run_test "test_ac3_version_numbers.sh"         "AC#3: Version Numbers"
run_test "test_ac4_last_updated_dates.sh"      "AC#4: Last Updated Dates"
run_test "test_ac5_cross_file_consistency.sh"  "AC#5: Cross-File Consistency"

echo ""
echo "================================================================"
echo "  STORY-360 Aggregate Results"
echo "================================================================"
for result in "${RESULTS[@]}"; do
    echo "$result"
done
echo ""
echo "  Total: $((AC_PASS + AC_FAIL)) ACs | ${AC_PASS} passed | ${AC_FAIL} failed"
echo "================================================================"

if [[ "$AC_FAIL" -gt 0 ]]; then
    echo "  OVERALL STATUS: FAILED"
    exit 1
else
    echo "  OVERALL STATUS: PASSED"
    exit 0
fi
