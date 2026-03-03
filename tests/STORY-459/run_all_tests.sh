#!/bin/bash
# Test Runner: STORY-459 - Extract Resume Dev Pre-Flight Logic
# Story: STORY-459
# Generated: 2026-02-20
#
# Runs all 11 AC test scripts and reports aggregate results.
# Exit 0 = all tests pass, Exit 1 = any test failed.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TOTAL_SUITES=0
PASSED_SUITES=0
FAILED_SUITES=0
FAILED_NAMES=()

echo "============================================================"
echo "  STORY-459: Extract Resume Dev Pre-Flight Logic"
echo "  Test Suite Runner - All 11 Acceptance Criteria"
echo "============================================================"
echo ""

run_suite() {
    local script="$1"
    local name="$2"
    ((TOTAL_SUITES++))
    echo "------------------------------------------------------------"
    echo "  Running: $name"
    echo "------------------------------------------------------------"
    if bash "$SCRIPT_DIR/$script" 2>&1; then
        echo "  >>> SUITE PASSED: $name"
        ((PASSED_SUITES++))
    else
        echo "  >>> SUITE FAILED: $name"
        ((FAILED_SUITES++))
        FAILED_NAMES+=("$name")
    fi
    echo ""
}

run_suite "test_ac1_resume_dev_lean.sh"        "AC#1: Command Line/Block Reduction"
run_suite "test_ac2_preflight_extracted.sh"     "AC#2: Pre-Flight Logic Extracted"
run_suite "test_ac3_dod_analysis_extracted.sh"  "AC#3: DoD Analysis Extracted"
run_suite "test_ac4_checkpoint_extracted.sh"    "AC#4: Checkpoint Detection Extracted"
run_suite "test_ac5_guardrails.sh"              "AC#5: Lean Orchestration Guardrails"
run_suite "test_ac6_backward_compat.sh"         "AC#6: Backward Compatibility"
run_suite "test_ac7_minimal_skill_change.sh"    "AC#7: Minimal SKILL.md Change"
run_suite "test_ac8_backward_compat_output.sh"  "AC#8: Backward-Compatible Output"
run_suite "test_ac9_governance_preserved.sh"    "AC#9: Governance Preserved"
run_suite "test_ac10_display_formats.sh"        "AC#10: Display Formats Preserved"
run_suite "test_ac11_askuser_placement.sh"      "AC#11: AskUserQuestion Placement"

echo "============================================================"
echo "  AGGREGATE RESULTS"
echo "============================================================"
echo "  Suites: $PASSED_SUITES passed, $FAILED_SUITES failed out of $TOTAL_SUITES"
echo ""

if [ "${#FAILED_NAMES[@]}" -gt 0 ]; then
    echo "  Failed suites:"
    for name in "${FAILED_NAMES[@]}"; do
        echo "    - $name"
    done
    echo ""
fi

if [ "$FAILED_SUITES" -eq 0 ]; then
    echo "  STATUS: ALL TESTS PASSED"
    exit 0
else
    echo "  STATUS: $FAILED_SUITES SUITE(S) FAILED"
    exit 1
fi
