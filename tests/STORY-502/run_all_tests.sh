#!/bin/bash
# Test Runner: STORY-502 - Red-Phase Test Integrity Checksums
# Story: STORY-502
# Generated: 2026-02-27

echo "=============================================="
echo "  STORY-502: Red-Phase Test Integrity Checksums"
echo "  Running all acceptance criteria tests"
echo "=============================================="
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOTAL_PASS=0
TOTAL_FAIL=0
TESTS_RUN=0

for test_file in "$SCRIPT_DIR"/test_ac*.sh; do
    if [ -f "$test_file" ]; then
        ((TESTS_RUN++))
        echo "--- $(basename "$test_file") ---"
        bash "$test_file"
        if [ $? -ne 0 ]; then
            ((TOTAL_FAIL++))
        else
            ((TOTAL_PASS++))
        fi
        echo ""
    fi
done

echo "=============================================="
echo "  SUMMARY: $TOTAL_PASS/$TESTS_RUN test files passed"
echo "=============================================="

[ $TOTAL_FAIL -eq 0 ] && exit 0 || exit 1
