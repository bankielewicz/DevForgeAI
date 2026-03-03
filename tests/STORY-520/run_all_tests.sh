#!/bin/bash
# Test Runner: STORY-520 - Add Phase 1.5 Completion Checklist to QA SKILL.md
# Generated: 2026-03-01

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOTAL_PASS=0
TOTAL_FAIL=0

echo "=============================================="
echo "  STORY-520: Phase 1.5 Completion Checklist"
echo "=============================================="
echo ""

for test_file in "$SCRIPT_DIR"/test_ac*.sh; do
    echo "----------------------------------------------"
    echo "Running: $(basename "$test_file")"
    echo "----------------------------------------------"
    if bash "$test_file"; then
        ((TOTAL_PASS++))
    else
        ((TOTAL_FAIL++))
    fi
    echo ""
done

echo "=============================================="
echo "  FINAL: $TOTAL_PASS test files passed, $TOTAL_FAIL test files failed"
echo "=============================================="

[ "$TOTAL_FAIL" -eq 0 ] && exit 0 || exit 1
