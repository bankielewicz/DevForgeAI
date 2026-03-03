#!/bin/bash
# Run all STORY-494 tests
# Story: STORY-494 - Add Full Read Mandatory Markers
# Generated: 2026-02-23

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOTAL_PASS=0
TOTAL_FAIL=0

echo "============================================"
echo "  STORY-494: Full Read Mandatory Markers"
echo "============================================"
echo ""

for test_file in "$SCRIPT_DIR"/test_ac*.sh; do
    echo "Running: $(basename "$test_file")"
    echo "--------------------------------------------"
    if bash "$test_file"; then
        ((TOTAL_PASS++))
    else
        ((TOTAL_FAIL++))
    fi
    echo ""
done

echo "============================================"
echo "  Overall: $TOTAL_PASS test files passed, $TOTAL_FAIL failed"
echo "============================================"

[ "$TOTAL_FAIL" -eq 0 ] && exit 0 || exit 1
