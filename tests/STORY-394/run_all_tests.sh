#!/usr/bin/env bash
# =============================================================================
# STORY-394: Run All Acceptance Criteria Tests
#
# Executes all 6 AC test files and reports aggregate results.
# TDD Phase: RED (all tests should FAIL before implementation)
# =============================================================================

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TOTAL_PASS=0
TOTAL_FAIL=0
TOTAL_FILES=0
FAILED_FILES=()

echo "================================================================"
echo "STORY-394: Build Before/After Evaluation Pipeline"
echo "Running All Acceptance Criteria Tests"
echo "================================================================"
echo ""

for test_file in "$SCRIPT_DIR"/test_ac*.sh; do
    if [ ! -f "$test_file" ]; then
        continue
    fi

    TOTAL_FILES=$((TOTAL_FILES + 1))
    TEST_NAME=$(basename "$test_file" .sh)

    echo "--- Running: ${TEST_NAME} ---"
    if bash "$test_file"; then
        TOTAL_PASS=$((TOTAL_PASS + 1))
    else
        TOTAL_FAIL=$((TOTAL_FAIL + 1))
        FAILED_FILES+=("$TEST_NAME")
    fi
    echo ""
done

echo "================================================================"
echo "STORY-394 Aggregate Results"
echo "================================================================"
echo "Test files passed: ${TOTAL_PASS}/${TOTAL_FILES}"
echo "Test files failed: ${TOTAL_FAIL}/${TOTAL_FILES}"

if [ ${#FAILED_FILES[@]} -gt 0 ]; then
    echo ""
    echo "Failed test files:"
    for f in "${FAILED_FILES[@]}"; do
        echo "  - ${f}"
    done
fi

echo "================================================================"

if [ "$TOTAL_FAIL" -gt 0 ]; then
    exit 1
else
    exit 0
fi
