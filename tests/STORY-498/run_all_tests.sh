#!/bin/bash
# Test Runner: STORY-498 - Add Library Crate Adaptive Path to Release Skill
# Generated: 2026-02-24

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOTAL_PASSED=0
TOTAL_FAILED=0
SUITE_FAILURES=0

echo "=============================================="
echo "  STORY-498: Library Crate Adaptive Path Tests"
echo "=============================================="
echo ""

for test_file in "$SCRIPT_DIR"/test_ac*.sh; do
    echo "----------------------------------------------"
    echo "Running: $(basename "$test_file")"
    echo "----------------------------------------------"
    bash "$test_file"
    if [ $? -ne 0 ]; then
        ((SUITE_FAILURES++))
    fi
    echo ""
done

echo "=============================================="
echo "  Suite Summary"
echo "=============================================="
echo "  Test files with failures: $SUITE_FAILURES"
echo ""

if [ $SUITE_FAILURES -eq 0 ]; then
    echo "  RESULT: ALL TESTS PASSED"
    exit 0
else
    echo "  RESULT: $SUITE_FAILURES test file(s) had failures"
    exit 1
fi
