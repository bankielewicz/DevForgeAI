#!/bin/bash
# Test Runner: STORY-393 - Pilot: Apply Unified Template to requirements-analyst Subagent
# Generated: 2026-02-12

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOTAL_PASS=0
TOTAL_FAIL=0
TESTS_RUN=0

echo "=============================================="
echo "  STORY-393: Requirements-Analyst Template Migration"
echo "  Test Suite Runner"
echo "=============================================="
echo ""

for test_file in "$SCRIPT_DIR"/test_ac*.sh; do
    test_name=$(basename "$test_file")
    echo "--- Running: $test_name ---"
    ((TESTS_RUN++))

    if bash "$test_file"; then
        ((TOTAL_PASS++))
    else
        ((TOTAL_FAIL++))
    fi
    echo ""
done

echo "=============================================="
echo "  Suite Results: $TOTAL_PASS/$TESTS_RUN test files passed"
if [ "$TOTAL_FAIL" -gt 0 ]; then
    echo "  Status: FAILING (TDD Red phase confirmed)"
else
    echo "  Status: ALL PASSING"
fi
echo "=============================================="

[ "$TOTAL_FAIL" -eq 0 ] && exit 0 || exit 1
