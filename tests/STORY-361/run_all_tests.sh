#!/usr/bin/env bash
# =============================================================================
# STORY-361: Run All Acceptance Criteria Tests
# =============================================================================
# Runs all 5 AC test scripts for STORY-361:
#   AC#1: Treelint Search Command Patterns
#   AC#2: JSON Output Parsing Examples
#   AC#3: Fallback Logic (Treelint to Grep)
#   AC#4: Language Support Matrix
#   AC#5: Error Handling Patterns
#
# Usage: bash tests/STORY-361/run_all_tests.sh
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
echo "  STORY-361: Treelint Skill Reference Files - Test Suite"
echo "================================================================"

run_test "test_ac1_command_patterns.sh" "AC#1: Command Patterns"
run_test "test_ac2_json_examples.sh"    "AC#2: JSON Examples"
run_test "test_ac3_fallback_logic.sh"   "AC#3: Fallback Logic"
run_test "test_ac4_language_matrix.sh"   "AC#4: Language Matrix"
run_test "test_ac5_error_handling.sh"    "AC#5: Error Handling"

echo ""
echo "================================================================"
echo "  STORY-361 Overall Results"
echo "================================================================"
echo "  ACs Passed: ${TOTAL_PASS}/5"
echo "  ACs Failed: ${TOTAL_FAIL}/5"
echo "================================================================"

if [[ "$TOTAL_FAIL" -gt 0 ]]; then
    echo "  OVERALL STATUS: FAILED"
    exit 1
else
    echo "  OVERALL STATUS: PASSED"
    exit 0
fi
