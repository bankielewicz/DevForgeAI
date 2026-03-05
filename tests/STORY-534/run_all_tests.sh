#!/bin/bash
# Test Runner: STORY-534 - Dual-Mode /business-plan Command
# Generated: 2026-03-04
#
# Runs all acceptance criteria tests and integration tests
# Reports comprehensive test summary

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOTAL_PASS=0
TOTAL_FAIL=0
AC_PASS=0
AC_FAIL=0
INTEGRATION_PASS=0
INTEGRATION_FAIL=0

echo "=============================================="
echo " STORY-534: Dual-Mode /business-plan Command"
echo "=============================================="
echo ""

# Run Unit Tests (Acceptance Criteria)
echo "======== UNIT TESTS: Acceptance Criteria ========"
echo ""

for test_file in "$SCRIPT_DIR"/test_ac*.sh; do
    echo "----------------------------------------------"
    bash "$test_file"
    if [ $? -ne 0 ]; then
        ((AC_FAIL++))
        ((TOTAL_FAIL++))
    else
        ((AC_PASS++))
        ((TOTAL_PASS++))
    fi
    echo ""
done

# Run Integration Tests
echo "======== INTEGRATION TESTS ========"
echo ""
echo "----------------------------------------------"
bash "$SCRIPT_DIR/test_integration.sh"
if [ $? -ne 0 ]; then
    ((INTEGRATION_FAIL++))
    ((TOTAL_FAIL++))
else
    ((INTEGRATION_PASS++))
    ((TOTAL_PASS++))
fi
echo ""

# Summary Report
echo "=============================================="
echo " TEST SUMMARY: STORY-534"
echo "=============================================="
echo ""
echo "Unit Tests (AC):        $AC_PASS passed, $AC_FAIL failed"
echo "Integration Tests:      $INTEGRATION_PASS passed, $INTEGRATION_FAIL failed"
echo ""
echo "OVERALL:                $TOTAL_PASS passed, $TOTAL_FAIL failed"
echo "=============================================="

[ $TOTAL_FAIL -eq 0 ] && exit 0 || exit 1
