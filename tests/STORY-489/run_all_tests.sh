#!/bin/bash
# Run all STORY-489 tests
# Generated: 2026-02-23

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOTAL_PASS=0
TOTAL_FAIL=0

echo "============================================"
echo "  STORY-489: RCA Recommendation Tracking"
echo "============================================"
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

echo "============================================"
echo "  Suite Results: $TOTAL_PASS suites passed, $TOTAL_FAIL suites failed"
echo "============================================"

[ $TOTAL_FAIL -eq 0 ] && exit 0 || exit 1
