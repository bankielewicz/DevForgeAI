#!/bin/bash
# Test Runner: STORY-479 - /audit-alignment --generate-refs Integration
# Generated: 2026-02-23

TOTAL_PASSED=0
TOTAL_FAILED=0
SCRIPTS_PASSED=0
SCRIPTS_FAILED=0

DIR="$(cd "$(dirname "$0")" && pwd)"

echo "============================================="
echo "  STORY-479 Test Suite"
echo "============================================="
echo ""

for test_file in "$DIR"/test_ac*.sh; do
    echo "--- $(basename "$test_file") ---"
    bash "$test_file"
    if [ $? -eq 0 ]; then
        ((SCRIPTS_PASSED++))
    else
        ((SCRIPTS_FAILED++))
    fi
    echo ""
done

echo "============================================="
echo "  Summary: $SCRIPTS_PASSED scripts passed, $SCRIPTS_FAILED scripts failed"
echo "============================================="
[ $SCRIPTS_FAILED -eq 0 ] && exit 0 || exit 1
