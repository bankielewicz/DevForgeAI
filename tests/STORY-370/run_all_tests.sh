#!/bin/bash
##############################################################################
# STORY-370: Run all acceptance criteria test suites
# Usage: bash tests/STORY-370/run_all_tests.sh
##############################################################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOTAL_SUITES=0
SUITES_PASSED=0
SUITES_FAILED=0

echo "============================================================"
echo "STORY-370: Integrate Dependency Graph Analysis via Treelint deps"
echo "Running all AC test suites..."
echo "============================================================"

for test_file in "$SCRIPT_DIR"/test_ac*.sh; do
    TOTAL_SUITES=$((TOTAL_SUITES + 1))
    echo ""
    echo "------------------------------------------------------------"
    echo "Running: $(basename "$test_file")"
    echo "------------------------------------------------------------"
    bash "$test_file"
    if [ $? -eq 0 ]; then
        SUITES_PASSED=$((SUITES_PASSED + 1))
    else
        SUITES_FAILED=$((SUITES_FAILED + 1))
    fi
done

echo ""
echo "============================================================"
echo "STORY-370 OVERALL: $SUITES_PASSED/$TOTAL_SUITES suites passed, $SUITES_FAILED failed"
echo "============================================================"

if [ $SUITES_FAILED -gt 0 ]; then
    echo "STATUS: RED (TDD Red phase - tests correctly failing)"
    exit 1
else
    echo "STATUS: GREEN (all tests passing)"
    exit 0
fi
