#!/bin/bash
# Test Runner: STORY-474 - Audit Alignment Command
# Generated: 2026-02-23

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOTAL_PASS=0
TOTAL_FAIL=0
SUITE_FAILURES=0

echo "=============================================="
echo "  STORY-474: Audit Alignment Command Tests"
echo "=============================================="
echo ""

for test_file in "$SCRIPT_DIR"/test_ac*.sh; do
    echo "--- Running: $(basename "$test_file") ---"
    bash "$test_file"
    if [ $? -ne 0 ]; then
        ((SUITE_FAILURES++))
    fi
    echo ""
done

echo "=============================================="
echo "  Suite Summary: $SUITE_FAILURES test file(s) with failures"
echo "=============================================="

[ $SUITE_FAILURES -eq 0 ] && exit 0 || exit 1
