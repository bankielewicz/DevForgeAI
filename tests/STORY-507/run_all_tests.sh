#!/bin/bash
# Run all tests for STORY-507
# Story: STORY-507 - Add Decision Context Section to Epic Template
# Generated: 2026-02-28

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOTAL_PASS=0
TOTAL_FAIL=0

echo "=========================================="
echo "  STORY-507: Test Suite"
echo "=========================================="
echo ""

for test_file in "$SCRIPT_DIR"/test_ac*.sh; do
    echo "------------------------------------------"
    bash "$test_file"
    if [ $? -ne 0 ]; then
        ((TOTAL_FAIL++))
    else
        ((TOTAL_PASS++))
    fi
    echo ""
done

echo "=========================================="
echo "  Overall: $TOTAL_PASS test files passed, $TOTAL_FAIL test files failed"
echo "=========================================="

[ $TOTAL_FAIL -eq 0 ] && exit 0 || exit 1
