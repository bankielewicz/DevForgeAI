#!/bin/bash
# Test Runner: STORY-546 - /legal-check Command and Skill Assembly
# Generated: 2026-03-05

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TOTAL_PASS=0
TOTAL_FAIL=0

echo "========================================"
echo "  STORY-546: /legal-check Tests"
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
echo "  Summary: $TOTAL_PASS suites passed, $TOTAL_FAIL suites failed"
echo "========================================"
[ $TOTAL_FAIL -eq 0 ] && exit 0 || exit 1
