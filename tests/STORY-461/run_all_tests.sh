#!/bin/bash
# Test Runner: STORY-461 - Trim Documentation-Heavy Commands to Lean Orchestration Pattern
# Generated: 2026-02-21
# Runs all 9 AC test scripts and reports overall pass/fail

SUITE_PASS=0
SUITE_FAIL=0
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

run_suite() {
    local script="$1"
    local label="$2"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  Running: $label"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    bash "$SCRIPT_DIR/$script"
    if [[ $? -eq 0 ]]; then
        echo "  SUITE RESULT: PASS - $label"
        ((SUITE_PASS++))
    else
        echo "  SUITE RESULT: FAIL - $label"
        ((SUITE_FAIL++))
    fi
}

echo "======================================================="
echo "  STORY-461 Test Suite"
echo "  Lean Orchestration Pattern Validation"
echo "======================================================="

run_suite "test_ac1_create_epic_lean.sh"       "AC#1: create-epic.md lean targets"
run_suite "test_ac2_document_lean.sh"           "AC#2: document.md lean targets"
run_suite "test_ac3_create_agent_lean.sh"       "AC#3: create-agent.md lean targets"
run_suite "test_ac4_rca_lean.sh"               "AC#4: rca.md lean targets"
run_suite "test_ac5_insights_lean.sh"           "AC#5: insights.md lean targets"
run_suite "test_ac6_backward_compat_output.sh"  "AC#6: Backward compatibility"
run_suite "test_ac7_governance_preserved.sh"    "AC#7: Governance sections preserved"
run_suite "test_ac8_interactive_prompts.sh"     "AC#8: AskUserQuestion prompts preserved"
run_suite "test_ac9_askuser_placement.sh"       "AC#9: No new AskUserQuestion in skills"

echo ""
echo "======================================================="
echo "  FINAL RESULTS: $SUITE_PASS suites passed, $SUITE_FAIL suites failed"
echo "======================================================="
[[ $SUITE_FAIL -eq 0 ]] && exit 0 || exit 1
