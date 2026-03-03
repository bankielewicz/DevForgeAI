#!/bin/bash
# Test Runner: STORY-528 - Stop Hook Phase Completion Gate
# Runs all test files and reports aggregate results

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOTAL_PASS=0
TOTAL_FAIL=0
TOTAL_FILES=0
FAILED_FILES=()

echo "============================================="
echo "  STORY-528: Phase Completion Gate Tests"
echo "============================================="
echo ""

for test_file in "$SCRIPT_DIR"/test_*.sh; do
    ((TOTAL_FILES++))
    echo "--- Running: $(basename "$test_file") ---"
    if bash "$test_file"; then
        ((TOTAL_PASS++))
    else
        ((TOTAL_FAIL++))
        FAILED_FILES+=("$(basename "$test_file")")
    fi
    echo ""
done

echo "============================================="
echo "  Aggregate: $TOTAL_PASS/$TOTAL_FILES files passed"
echo "============================================="

if [ ${#FAILED_FILES[@]} -gt 0 ]; then
    echo "Failed files:"
    for f in "${FAILED_FILES[@]}"; do
        echo "  - $f"
    done
    exit 1
fi

exit 0
