#!/bin/bash
# STORY-220 Test Runner
# Run all AC tests for Document Mandatory Skill Execution Principle
# TDD Red Phase: All tests should FAIL before implementation

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/../../.." || exit 1

echo "========================================"
echo "STORY-220: Document Mandatory Skill Execution Principle Tests"
echo "========================================"
echo "Target File: src/CLAUDE.md"
echo "========================================"

PASS_COUNT=0
FAIL_COUNT=0
TESTS_DIR="tests/results/STORY-220"

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
    echo ""
    echo "TDD Red Phase: Tests are expected to FAIL before implementation."
    exit 1
fi
exit 0
