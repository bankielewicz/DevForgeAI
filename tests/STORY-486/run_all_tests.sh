#!/bin/bash
# Test Runner: STORY-486 - Document Sibling Story Pattern Reuse Protocol
# Generated: 2026-02-23

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOTAL_PASSED=0
TOTAL_FAILED=0

run_suite() {
    local script="$1"
    echo "========================================"
    echo "Running: $(basename $script)"
    echo "========================================"
    bash "$script"
    local exit_code=$?
    if [ $exit_code -eq 0 ]; then
        ((TOTAL_PASSED++))
    else
        ((TOTAL_FAILED++))
    fi
    echo ""
}

run_suite "$SCRIPT_DIR/test_ac1_protocol_added.sh"
run_suite "$SCRIPT_DIR/test_ac2_cross_reference.sh"

echo "========================================"
echo "STORY-486 Suite Summary"
echo "  Suites passed: $TOTAL_PASSED"
echo "  Suites failed: $TOTAL_FAILED"
echo "========================================"
[ $TOTAL_FAILED -eq 0 ] && exit 0 || exit 1
