#!/bin/bash
# Run all STORY-492 tests
# Story: STORY-492 - Phase Completion Verification Checkpoints
# Generated: 2026-02-23

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOTAL_PASS=0
TOTAL_FAIL=0

echo "=========================================="
echo "  STORY-492: Phase Completion Verification"
echo "  Checkpoints Test Suite"
echo "=========================================="
echo ""

for test_file in "$SCRIPT_DIR"/test_ac*.sh; do
    echo "------------------------------------------"
    bash "$test_file"
    if [ $? -ne 0 ]; then
        ((TOTAL_FAIL++))
    else
        ((TOTAL_PASS++))
    fi
    echo ""
done

echo "=========================================="
echo "  Suite Results: $TOTAL_PASS suites passed, $TOTAL_FAIL suites failed"
echo "=========================================="

[ $TOTAL_FAIL -eq 0 ] && exit 0 || exit 1
