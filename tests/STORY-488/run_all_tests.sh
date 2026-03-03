#!/bin/bash
# Run all STORY-488 tests
# Story: STORY-488 - Create-Story Skill Dual-Path Translation Rule
# Generated: 2026-02-23

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TOTAL_PASSED=0
TOTAL_FAILED=0

echo "============================================"
echo "  STORY-488: Dual-Path Translation Rule"
echo "  Running all acceptance criteria tests"
echo "============================================"
echo ""

for test_file in "$SCRIPT_DIR"/test_ac*.sh; do
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
echo "  Overall: $TOTAL_PASSED test files passed, $TOTAL_FAILED test files failed"
echo "============================================"

[ $TOTAL_FAILED -eq 0 ] && exit 0 || exit 1
