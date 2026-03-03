#!/usr/bin/env bash
# =============================================================================
# STORY-362: Run All Acceptance Criteria Tests
# =============================================================================
# Runs all 6 AC test scripts for STORY-362:
#   AC#1: Language Support Detection
#   AC#2: Automatic Grep Fallback
#   AC#3: Warning Message (Not Error)
#   AC#4: Binary Unavailable Handling
#   AC#5: Runtime Error Fallback
#   AC#6: Reusable Fallback Pattern
#
# Usage: bash tests/STORY-362/run_all_tests.sh
# =============================================================================

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
export PROJECT_ROOT

TOTAL_PASS=0
TOTAL_FAIL=0

run_test() {
    local test_file="$1"
    local test_name="$2"

    echo ""
    echo "================================================================"
    echo "  Running: ${test_name}"
    echo "================================================================"

    if bash "${SCRIPT_DIR}/${test_file}"; then
        TOTAL_PASS=$((TOTAL_PASS + 1))
        echo "  >>> ${test_name}: PASSED"
    else
        TOTAL_FAIL=$((TOTAL_FAIL + 1))
        echo "  >>> ${test_name}: FAILED"
    fi
}

echo "================================================================"
echo "  STORY-362: Hybrid Fallback Logic - Test Suite"
echo "================================================================"

run_test "test_ac1_language_detection.sh"      "AC#1: Language Support Detection"
run_test "test_ac2_grep_fallback.sh"           "AC#2: Automatic Grep Fallback"
run_test "test_ac3_warning_not_error.sh"       "AC#3: Warning Message (Not Error)"
run_test "test_ac4_binary_unavailable.sh"      "AC#4: Binary Unavailable Handling"
run_test "test_ac5_runtime_error_fallback.sh"  "AC#5: Runtime Error Fallback"
run_test "test_ac6_reusable_pattern.sh"        "AC#6: Reusable Fallback Pattern"

echo ""
echo "================================================================"
echo "  STORY-362 Overall Results"
echo "================================================================"
echo "  ACs Passed: ${TOTAL_PASS}/6"
echo "  ACs Failed: ${TOTAL_FAIL}/6"
echo "================================================================"

if [[ "$TOTAL_FAIL" -gt 0 ]]; then
    echo "  OVERALL STATUS: FAILED"
    exit 1
else
    echo "  OVERALL STATUS: PASSED"
    exit 0
fi
