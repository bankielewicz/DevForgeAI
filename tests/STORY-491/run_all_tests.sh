#!/bin/bash
# Test Runner: STORY-491 - Root Cause Diagnosis Foundation
# Generated: 2026-02-23

echo "========================================"
echo "  STORY-491 Test Suite"
echo "========================================"
echo ""

TOTAL_PASSED=0
TOTAL_FAILED=0
SUITE_FAILURES=0

TEST_DIR="$(cd "$(dirname "$0")" && pwd)"

for test_file in "$TEST_DIR"/test_ac*.sh; do
    echo "----------------------------------------"
    echo "Running: $(basename "$test_file")"
    echo "----------------------------------------"
    bash "$test_file"
    if [ $? -ne 0 ]; then
        ((SUITE_FAILURES++))
    fi
    echo ""
done

echo "========================================"
echo "  Suite Summary: $SUITE_FAILURES / 5 test files had failures"
echo "========================================"

[ $SUITE_FAILURES -eq 0 ] && exit 0 || exit 1
