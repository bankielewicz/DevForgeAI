#!/usr/bin/env bash
# =============================================================================
# STORY-407: Run All Acceptance Criteria Tests
# =============================================================================
# Runs all 5 AC test scripts and reports aggregate results.
#
# Usage:
#   bash tests/STORY-407/run_all_tests.sh
#
# Exit Codes:
#   0 - All tests passed
#   1 - One or more tests failed
# =============================================================================

set -uo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
TEST_DIR="${PROJECT_ROOT}/tests/STORY-407"

TOTAL_PASS=0
TOTAL_FAIL=0
SUITE_RESULTS=()

run_test() {
    local test_file="$1"
    local test_name="$2"

    echo ""
    echo "================================================================"
    echo "  Running: ${test_name}"
    echo "================================================================"
    echo ""

    if bash "${TEST_DIR}/${test_file}"; then
        SUITE_RESULTS+=("PASS: ${test_name}")
        TOTAL_PASS=$((TOTAL_PASS + 1))
    else
        SUITE_RESULTS+=("FAIL: ${test_name}")
        TOTAL_FAIL=$((TOTAL_FAIL + 1))
    fi
}

echo "================================================================"
echo "  STORY-407: Add Treelint JSON Schema Validation"
echo "  Full Test Suite Execution"
echo "================================================================"

# Run each AC test
run_test "test_ac1_non_treelint_skip.sh" "AC#1: Non-Treelint Stories Skip Validation"
run_test "test_ac2_keyword_detection_triggers_schema.sh" "AC#2: Keyword Detection Triggers Schema Loading"
run_test "test_ac3_field_mismatch_warnings.sh" "AC#3: Field Mismatches Produce Non-Blocking Warnings"
run_test "test_ac4_valid_fields_silent_pass.sh" "AC#4: Valid Field References Pass Silently"
run_test "test_ac5_content_only_contract.sh" "AC#5: Content-Only Output Contract Preserved"

# Summary
echo ""
echo "================================================================"
echo "  STORY-407: Full Suite Results"
echo "================================================================"
echo ""

for result in "${SUITE_RESULTS[@]}"; do
    echo "  ${result}"
done

echo ""
echo "  Total: $((TOTAL_PASS + TOTAL_FAIL)) suites"
echo "  Passed: ${TOTAL_PASS}"
echo "  Failed: ${TOTAL_FAIL}"
echo ""

if [[ "$TOTAL_FAIL" -gt 0 ]]; then
    echo "  OVERALL STATUS: FAILED"
    exit 1
else
    echo "  OVERALL STATUS: PASSED"
    exit 0
fi
