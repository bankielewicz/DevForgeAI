#!/bin/bash
# Test Runner: All STORY-460 Acceptance Criteria Tests
# Story: STORY-460 - Slim Skill-Invoking Commands (qa, create-ui, ideate)
# Generated: 2026-02-21
# Runs all 11 AC test files and reports aggregate results

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

TOTAL_SUITES=0
PASSED_SUITES=0
FAILED_SUITES=0
FAILED_NAMES=()

echo "============================================================"
echo "  STORY-460: Slim Skill-Invoking Commands"
echo "  Test Suite Runner - All 11 Acceptance Criteria"
echo "============================================================"
echo ""

run_suite() {
    local test_file="$1"
    local test_name="$2"
    ((TOTAL_SUITES++))

    echo "------------------------------------------------------------"
    echo "  Running: ${test_name}"
    echo "------------------------------------------------------------"

    if bash "$SCRIPT_DIR/$test_file"; then
        ((PASSED_SUITES++))
        echo "  >>> SUITE PASSED <<<"
    else
        ((FAILED_SUITES++))
        FAILED_NAMES+=("$test_name")
        echo "  >>> SUITE FAILED <<<"
    fi
    echo ""
}

# Run all 11 test suites
run_suite "test_ac1_qa_lean.sh"                "AC#1: qa.md Lean Orchestration"
run_suite "test_ac2_create_ui_lean.sh"         "AC#2: create-ui.md Lean Orchestration"
run_suite "test_ac3_ideate_lean.sh"            "AC#3: ideate.md Lean Orchestration"
run_suite "test_ac4_qa_skill_reduced.sh"       "AC#4: devforgeai-qa SKILL.md Prerequisite"
run_suite "test_ac5_backward_compat.sh"        "AC#5: Backward Compatibility"
run_suite "test_ac6_guardrails.sh"             "AC#6: DO NOT Guardrail Sections"
run_suite "test_ac7_skill_sizes.sh"            "AC#7: Skill Size Compliance"
run_suite "test_ac8_backward_compat_output.sh" "AC#8: Backward-Compatible Output"
run_suite "test_ac9_governance_preserved.sh"   "AC#9: Governance Sections Preserved"
run_suite "test_ac10_interactive_prompts.sh"   "AC#10: Interactive Prompts Functional"
run_suite "test_ac11_askuser_placement.sh"     "AC#11: AskUserQuestion Placement"

# === Aggregate Summary ===
echo "============================================================"
echo "  AGGREGATE RESULTS"
echo "============================================================"
echo ""
echo "  Suites: ${PASSED_SUITES} passed, ${FAILED_SUITES} failed out of ${TOTAL_SUITES}"
echo ""

if [ ${#FAILED_NAMES[@]} -gt 0 ]; then
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
    echo "  STATUS: ${FAILED_SUITES} SUITE(S) FAILED (TDD Red phase expected)"
    exit 1
fi
