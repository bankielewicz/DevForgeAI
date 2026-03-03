#!/bin/bash
# Run all STORY-408 tests
# Story: STORY-408 - Restructure /create-story Command
# Generated: 2026-02-16

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOTAL_PASS=0
TOTAL_FAIL=0

echo "============================================"
echo "  STORY-408: Test Suite"
echo "============================================"
echo ""

for test_file in "$SCRIPT_DIR"/test_ac*.sh; do
    echo "--------------------------------------------"
    bash "$test_file"
    if [ $? -ne 0 ]; then
        ((TOTAL_FAIL++))
    else
        ((TOTAL_PASS++))
    fi
    echo ""
done

echo "============================================"
echo "  Summary: $TOTAL_PASS test files passed, $TOTAL_FAIL test files failed"
echo "============================================"

[ $TOTAL_FAIL -eq 0 ] && exit 0 || exit 1
