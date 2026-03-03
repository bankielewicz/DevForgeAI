#!/bin/bash
# Test Runner: STORY-481 - Resolve Subagent Reference Loading Mechanism
# Generated: 2026-02-23
# Usage: bash src/tests/STORY-481/run_all_tests.sh

SCRIPT_DIR="/mnt/c/Projects/DevForgeAI2/src/tests/STORY-481"
TOTAL_PASSED=0
TOTAL_FAILED=0
SUITE_FAILURES=0

run_suite() {
    local suite_name="$1"
    local suite_file="$2"

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Running: $suite_name"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    bash "$suite_file"
    local exit_code=$?

    if [ "$exit_code" -ne 0 ]; then
        echo "  [SUITE FAILED] $suite_name"
        ((SUITE_FAILURES++))
    else
        echo "  [SUITE PASSED] $suite_name"
    fi
    echo ""
}

echo ""
echo "====================================================="
echo "  STORY-481 Test Suite"
echo "  Resolve Subagent Reference Loading Mechanism"
echo "====================================================="
echo ""

run_suite "AC#1: Decision Documented in EPIC-082" "$SCRIPT_DIR/test_ac1_decision_documented.sh"
run_suite "AC#2: ADR Created for Decision"         "$SCRIPT_DIR/test_ac2_adr_created.sh"
run_suite "AC#3: Implementation Guidance Added"    "$SCRIPT_DIR/test_ac3_guidance_added.sh"

echo "====================================================="
if [ "$SUITE_FAILURES" -eq 0 ]; then
    echo "  ALL SUITES PASSED"
    exit 0
else
    echo "  $SUITE_FAILURES SUITE(S) FAILED"
    exit 1
fi
