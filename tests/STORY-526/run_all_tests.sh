#!/bin/bash
# Test Runner: STORY-526 - SubagentStop Hook Auto-Track Invocations
# Generated: 2026-03-02

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TOTAL_PASSED=0
TOTAL_FAILED=0
TOTAL_FILES=0
FAILED_FILES=()

echo "========================================"
echo "  STORY-526: SubagentStop Hook Tests"
echo "========================================"
echo ""

for test_file in "$SCRIPT_DIR"/test_ac*.sh; do
    ((TOTAL_FILES++))
    echo "--- Running: $(basename "$test_file") ---"
    if bash "$test_file"; then
        echo "  >>> FILE PASSED"
    else
        echo "  >>> FILE FAILED"
        FAILED_FILES+=("$(basename "$test_file")")
    fi
    echo ""
done

echo "========================================"
echo "  Summary: $TOTAL_FILES test files executed"
if [ ${#FAILED_FILES[@]} -gt 0 ]; then
    echo "  FAILED files: ${FAILED_FILES[*]}"
    echo "  Status: RED (tests failing as expected for TDD)"
    exit 1
else
    echo "  Status: ALL PASSED"
    exit 0
fi
echo "========================================"
