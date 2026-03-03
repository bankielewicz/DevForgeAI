#!/bin/bash
# Run All Tests for STORY-409
# Story: Move Batch Workflow Logic into devforgeai-story-creation Skill
# Generated: 2026-02-16

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOTAL_PASSED=0
TOTAL_FAILED=0

echo "============================================"
echo "  STORY-409: Batch Workflow Tests"
echo "============================================"
echo ""

for test_file in "$SCRIPT_DIR"/test_ac*.sh; do
    echo "--- Running: $(basename "$test_file") ---"
    bash "$test_file"
    if [ $? -ne 0 ]; then
        ((TOTAL_FAILED++))
    else
        ((TOTAL_PASSED++))
    fi
    echo ""
done

echo "============================================"
echo "  Summary: $TOTAL_PASSED test files passed, $TOTAL_FAILED test files failed"
echo "============================================"

[ $TOTAL_FAILED -eq 0 ] && exit 0 || exit 1
