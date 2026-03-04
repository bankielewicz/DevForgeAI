#!/bin/bash
# Test Runner: STORY-532 - Milestone-Based Plan Generator
# Generated: 2026-03-04
# Runs all 5 AC test files and reports aggregate results

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOTAL_PASS=0
TOTAL_FAIL=0

echo "========================================"
echo "  STORY-532: Milestone-Based Plan Generator"
echo "  Test Suite Runner"
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
echo "  AGGREGATE: $TOTAL_PASS test files passed, $TOTAL_FAIL test files failed"
echo "========================================"

[ "$TOTAL_FAIL" -eq 0 ] && exit 0 || exit 1
