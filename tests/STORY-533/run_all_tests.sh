#!/bin/bash
# Test Runner: STORY-533 - Business Model Pattern Matching
# Story: STORY-533
# Generated: 2026-03-04

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOTAL_PASSED=0
TOTAL_FAILED=0
SUITE_FAILURES=0

echo "=============================================="
echo "  STORY-533: Business Model Pattern Matching"
echo "  Test Suite Runner"
echo "=============================================="
echo ""

for test_file in \
    "$SCRIPT_DIR/test_ac1_model_detection.sh" \
    "$SCRIPT_DIR/test_ac2_reference_loading.sh" \
    "$SCRIPT_DIR/test_ac3_viability_scoring.sh" \
    "$SCRIPT_DIR/test_ac4_disclaimer.sh" \
    "$SCRIPT_DIR/test_ac5_ambiguous_model.sh"; do

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
echo "  Test files with failures: $SUITE_FAILURES / 5"
echo "=============================================="

[ $SUITE_FAILURES -eq 0 ] && exit 0 || exit 1
