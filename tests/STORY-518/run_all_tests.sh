#!/bin/bash
# Run all STORY-518 tests
# Generated: 2026-03-01

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOTAL_PASS=0
TOTAL_FAIL=0

echo "========================================"
echo "  STORY-518 Test Suite"
echo "========================================"
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

echo "========================================"
echo "  Suite Results: $TOTAL_PASS passed, $TOTAL_FAIL failed"
echo "========================================"
[ $TOTAL_FAIL -eq 0 ] && exit 0 || exit 1
