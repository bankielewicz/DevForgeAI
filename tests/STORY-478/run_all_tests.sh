#!/bin/bash
# Test Runner: STORY-478 - Phase 5.7 Domain Reference Generation Workflow Integration
# Generated: 2026-02-23
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOTAL_PASSED=0
TOTAL_FAILED=0
TOTAL_ERRORS=0

echo "============================================="
echo "  STORY-478: Domain Reference Generation"
echo "  Running all acceptance criteria tests"
echo "============================================="
echo ""

for test_file in "$SCRIPT_DIR"/test_ac*.sh; do
    echo "--- Running: $(basename "$test_file") ---"
    if bash "$test_file"; then
        echo "  [SUITE PASS]"
    else
        EXIT_CODE=$?
        if [ $EXIT_CODE -eq 1 ]; then
            echo "  [SUITE FAIL]"
            ((TOTAL_FAILED++))
        else
            echo "  [SUITE ERROR] (exit code: $EXIT_CODE)"
            ((TOTAL_ERRORS++))
        fi
    fi
    echo ""
done

echo "============================================="
echo "  Summary: $TOTAL_FAILED suite(s) failed, $TOTAL_ERRORS error(s)"
echo "============================================="

[ $TOTAL_FAILED -eq 0 ] && [ $TOTAL_ERRORS -eq 0 ] && exit 0 || exit 1
