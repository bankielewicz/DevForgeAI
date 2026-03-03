#!/bin/bash
# Test Runner: STORY-509 - Add design_decisions Field to F4 Requirements Schema
# Generated: 2026-02-28

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOTAL_PASS=0
TOTAL_FAIL=0

echo "========================================"
echo "  STORY-509 Test Suite"
echo "========================================"
echo ""

for test_file in "$SCRIPT_DIR"/test_ac*.sh; do
    echo "--- Running: $(basename "$test_file") ---"
    if bash "$test_file"; then
        ((TOTAL_PASS++))
    else
        ((TOTAL_FAIL++))
    fi
    echo ""
done

echo "========================================"
echo "  Suite Results: $TOTAL_PASS suites passed, $TOTAL_FAIL suites failed"
echo "========================================"

[ "$TOTAL_FAIL" -eq 0 ] && exit 0 || exit 1
