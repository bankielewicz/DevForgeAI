#!/bin/bash
# Runner: Execute all STORY-544 tests
# Story: STORY-544 - Business Structure Decision Tree
# Generated: 2026-03-04

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOTAL_PASSED=0
TOTAL_FAILED=0

echo "============================================"
echo "  STORY-544: Business Structure Decision Tree"
echo "  Test Suite Runner"
echo "============================================"
echo ""

for test_file in "$SCRIPT_DIR"/test_ac*.sh; do
    echo "--------------------------------------------"
    echo "Running: $(basename "$test_file")"
    echo "--------------------------------------------"
    bash "$test_file"
    if [ $? -ne 0 ]; then
        ((TOTAL_FAILED++))
    else
        ((TOTAL_PASSED++))
    fi
    echo ""
done

echo "============================================"
echo "  Suite Results: $TOTAL_PASSED files passed, $TOTAL_FAILED files failed"
echo "============================================"

[ $TOTAL_FAILED -eq 0 ] && exit 0 || exit 1
