#!/bin/bash
# Test Runner: STORY-512 - Epic Completeness Scorecard Display
# Generated: 2026-02-28

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOTAL_PASSED=0
TOTAL_FAILED=0

echo "============================================"
echo "  STORY-512: Epic Completeness Scorecard"
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
echo "  Overall: $TOTAL_PASSED test files passed, $TOTAL_FAILED test files failed"
echo "============================================"
[ $TOTAL_FAILED -eq 0 ] && exit 0 || exit 1
