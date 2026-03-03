#!/bin/bash
# STORY-218 Test Runner
# Run all AC tests for Phase Execution Status Display in TodoWrite

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/../../.." || exit 1

echo "========================================"
echo "STORY-218: Phase Execution Status Display Tests"
echo "========================================"

PASS_COUNT=0
FAIL_COUNT=0
TESTS_DIR="tests/results/STORY-218"

for test_file in "$TESTS_DIR"/test_*.sh; do
    echo ""
    bash "$test_file"
    if [ $? -eq 0 ]; then
        ((PASS_COUNT++))
    else
        ((FAIL_COUNT++))
    fi
done

echo ""
echo "========================================"
echo "Results: $PASS_COUNT passed, $FAIL_COUNT failed"
echo "========================================"

if [ "$FAIL_COUNT" -gt 0 ]; then
    exit 1
fi
exit 0
