#!/bin/bash

# Test Runner: STORY-482 - Test Pyramid Exception Documentation
# Generated: 2026-02-23
#
# Runs all acceptance criteria tests for STORY-482

echo "========================================================================"
echo "STORY-482: Add Test Pyramid Exception Documentation to Test-Automator"
echo "========================================================================"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOTAL_PASSED=0
TOTAL_FAILED=0

# === Test AC#1 ===
echo "Running AC#1 tests..."
bash "$SCRIPT_DIR/test_ac1_exception_documented.sh"
AC1_EXIT=$?
if [ $AC1_EXIT -eq 0 ]; then
    ((TOTAL_PASSED+=4))
else
    ((TOTAL_FAILED+=4))
fi
echo ""

# === Test AC#2 ===
echo "Running AC#2 tests..."
bash "$SCRIPT_DIR/test_ac2_criteria_defined.sh"
AC2_EXIT=$?
if [ $AC2_EXIT -eq 0 ]; then
    ((TOTAL_PASSED+=6))
else
    ((TOTAL_FAILED+=6))
fi
echo ""

# === Test AC#3 ===
echo "Running AC#3 tests..."
bash "$SCRIPT_DIR/test_ac3_alternative_ratio.sh"
AC3_EXIT=$?
if [ $AC3_EXIT -eq 0 ]; then
    ((TOTAL_PASSED+=5))
else
    ((TOTAL_FAILED+=5))
fi
echo ""

# === Final Summary ===
echo "========================================================================"
echo "FINAL SUMMARY"
echo "========================================================================"
echo "AC#1: $([ $AC1_EXIT -eq 0 ] && echo 'PASS' || echo 'FAIL')"
echo "AC#2: $([ $AC2_EXIT -eq 0 ] && echo 'PASS' || echo 'FAIL')"
echo "AC#3: $([ $AC3_EXIT -eq 0 ] && echo 'PASS' || echo 'FAIL')"
echo ""
echo "Total: $TOTAL_PASSED passed, $TOTAL_FAILED failed"
echo "========================================================================"

if [ $AC1_EXIT -eq 0 ] && [ $AC2_EXIT -eq 0 ] && [ $AC3_EXIT -eq 0 ]; then
    exit 0
else
    exit 1
fi
