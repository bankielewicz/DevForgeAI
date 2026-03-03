#!/bin/bash
# Test Runner: STORY-524 - Memory File Graceful Fallback
# Generated: 2026-03-02

echo "========================================"
echo "  STORY-524: Memory File Graceful Fallback"
echo "========================================"
echo ""

TOTAL_PASS=0
TOTAL_FAIL=0
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

for test_file in "$SCRIPT_DIR"/test_ac*.sh; do
    echo "--- Running: $(basename "$test_file") ---"
    bash "$test_file"
    if [ $? -ne 0 ]; then
        ((TOTAL_FAIL++))
    else
        ((TOTAL_PASS++))
    fi
    echo ""
done

echo "========================================"
echo "  Overall: $TOTAL_PASS suites passed, $TOTAL_FAIL suites failed"
echo "========================================"
[ $TOTAL_FAIL -eq 0 ] && exit 0 || exit 1
