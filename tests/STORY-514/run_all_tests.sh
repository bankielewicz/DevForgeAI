#!/bin/bash
# Test Runner: STORY-514 - Snapshot File Existence Verification
# Generated: 2026-02-28

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOTAL_PASS=0
TOTAL_FAIL=0

echo "============================================"
echo "  STORY-514: Snapshot File Existence Check"
echo "============================================"
echo ""

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

echo "============================================"
echo "  Final: $TOTAL_PASS test files passed, $TOTAL_FAIL test files failed"
echo "============================================"
[ $TOTAL_FAIL -eq 0 ] && exit 0 || exit 1
