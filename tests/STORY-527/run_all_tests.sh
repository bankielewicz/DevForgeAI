#!/bin/bash
# Test Runner: STORY-527 - TaskCompleted Hook Step Validation Gate
# Generated: 2026-03-03

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOTAL_PASS=0
TOTAL_FAIL=0

echo "=================================================="
echo "  STORY-527: TaskCompleted Hook Step Validation Gate"
echo "  Running all acceptance criteria and integration tests"
echo "=================================================="
echo ""

# Run unit tests (AC tests)
for test_file in "$SCRIPT_DIR"/test_ac*.sh; do
    echo "--------------------------------------------------"
    echo "Running: $(basename "$test_file")"
    echo "--------------------------------------------------"
    if bash "$test_file"; then
        ((TOTAL_PASS++))
    else
        ((TOTAL_FAIL++))
    fi
    echo ""
done

# Run integration tests
for test_file in "$SCRIPT_DIR"/test_integration*.sh; do
    echo "--------------------------------------------------"
    echo "Running: $(basename "$test_file")"
    echo "--------------------------------------------------"
    if bash "$test_file"; then
        ((TOTAL_PASS++))
    else
        ((TOTAL_FAIL++))
    fi
    echo ""
done

echo "=================================================="
echo "  OVERALL: $TOTAL_PASS test files passed, $TOTAL_FAIL test files failed"
echo "=================================================="

[ "$TOTAL_FAIL" -eq 0 ] && exit 0 || exit 1
