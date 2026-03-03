#!/bin/bash
# Run all STORY-406 tests
# STORY-406: Create Batch Sibling Story Session Template

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TEST_DIR="$PROJECT_ROOT/tests/STORY-406"

echo "=============================================="
echo "STORY-406: Create Batch Sibling Story Session Template"
echo "Running all acceptance criteria tests"
echo "=============================================="
echo ""

TOTAL_PASS=0
TOTAL_FAIL=0

for test_file in "$TEST_DIR"/test_ac*.sh; do
    echo "--- Running: $(basename "$test_file") ---"
    bash "$test_file"
    if [ $? -eq 0 ]; then
        TOTAL_PASS=$((TOTAL_PASS + 1))
    else
        TOTAL_FAIL=$((TOTAL_FAIL + 1))
    fi
    echo ""
done

echo "=============================================="
echo "Overall Summary: $TOTAL_PASS AC passed, $TOTAL_FAIL AC failed"
echo "=============================================="

if [ "$TOTAL_FAIL" -gt 0 ]; then
    echo "Overall Status: FAILED"
    exit 1
else
    echo "Overall Status: PASSED"
    exit 0
fi
