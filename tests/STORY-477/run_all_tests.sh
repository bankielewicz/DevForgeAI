#!/bin/bash
# Test Runner: STORY-477 - Detection Heuristic Engine and Reference File Template
# Generated: 2026-02-23
# Runs all 12 AC test files and reports aggregate results

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOTAL_PASSED=0
TOTAL_FAILED=0
SUITE_FAILURES=0

echo "============================================================"
echo "  STORY-477: Detection Heuristic Engine and Reference File"
echo "  Test Suite Runner"
echo "============================================================"
echo ""

run_suite() {
    local script="$1"
    local name="$2"
    echo "------------------------------------------------------------"
    echo "Running: $name"
    echo "------------------------------------------------------------"
    bash "$script"
    local exit_code=$?
    if [ "$exit_code" -ne 0 ]; then
        ((SUITE_FAILURES++))
    fi
    echo ""
}

run_suite "$SCRIPT_DIR/test_ac1_four_heuristics.sh"   "AC#1: Four Detection Heuristics Implemented"
run_suite "$SCRIPT_DIR/test_ac2_dh01_trigger.sh"       "AC#2: DH-01 Triggers on Hardware/Platform Keywords"
run_suite "$SCRIPT_DIR/test_ac3_dh02_trigger.sh"       "AC#3: DH-02 Triggers on Multi-Language/Build-System"
run_suite "$SCRIPT_DIR/test_ac4_dh03_trigger.sh"       "AC#4: DH-03 Triggers on Anti-Pattern Count"
run_suite "$SCRIPT_DIR/test_ac5_dh04_trigger.sh"       "AC#5: DH-04 Triggers on Multi-Language Coding Standards"
run_suite "$SCRIPT_DIR/test_ac6_readonly.sh"            "AC#6: Heuristics Are Read-Only"
run_suite "$SCRIPT_DIR/test_ac7_structured_output.sh"  "AC#7: Structured Output with Triggered Heuristics"
run_suite "$SCRIPT_DIR/test_ac8_skip_signal.sh"         "AC#8: Skip Signal When No Heuristics Trigger"
run_suite "$SCRIPT_DIR/test_ac9_header.sh"              "AC#9: Auto-Generation Header in Template"
run_suite "$SCRIPT_DIR/test_ac10_sections.sh"           "AC#10: Template Contains All Required Sections"
run_suite "$SCRIPT_DIR/test_ac11_derivation_purity.sh" "AC#11: Derivation Purity"
run_suite "$SCRIPT_DIR/test_ac12_naming.sh"             "AC#12: project-*.md Naming Convention"

echo "============================================================"
echo "  SUITE SUMMARY"
echo "============================================================"
echo "  Test suites failed: $SUITE_FAILURES / 12"
echo ""

if [ "$SUITE_FAILURES" -eq 0 ]; then
    echo "  ALL SUITES PASSED"
    exit 0
else
    echo "  FAILURES DETECTED - $SUITE_FAILURES suite(s) failed"
    exit 1
fi
