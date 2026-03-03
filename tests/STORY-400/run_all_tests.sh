#!/usr/bin/env bash
# STORY-400: Run all AC test suites
# Usage: bash tests/STORY-400/run_all_tests.sh

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TOTAL_SUITES=0
PASSED_SUITES=0
FAILED_SUITES=0

echo "=============================================="
echo "STORY-400: Add Inline Observation Capture"
echo "Running all AC test suites"
echo "=============================================="
echo ""

for test_file in "$SCRIPT_DIR"/test_ac*.sh; do
    TOTAL_SUITES=$((TOTAL_SUITES + 1))
    echo "--- Running: $(basename "$test_file") ---"
    if bash "$test_file"; then
        PASSED_SUITES=$((PASSED_SUITES + 1))
    else
        FAILED_SUITES=$((FAILED_SUITES + 1))
    fi
    echo ""
done

echo "=============================================="
echo "Summary: $PASSED_SUITES/$TOTAL_SUITES suites passed, $FAILED_SUITES failed"
echo "=============================================="

if [ "$FAILED_SUITES" -gt 0 ]; then
    exit 1
fi
exit 0
