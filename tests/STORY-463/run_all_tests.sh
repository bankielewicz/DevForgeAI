#!/bin/bash
# Run all STORY-463 tests
# Story: STORY-463 - Refactor feedback-search.md to lean orchestration pattern
# Generated: 2026-02-21

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Run from project root so relative paths (src/claude/...) work
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_ROOT"

TOTAL_PASSED=0
TOTAL_FAILED=0
SUITE_FAILURES=0

run_suite() {
    local script="$1"
    local name="$2"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  $name"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    bash "$script"
    local exit_code=$?
    if [ $exit_code -ne 0 ]; then
        ((SUITE_FAILURES++))
    fi
    return $exit_code
}

echo "======================================================"
echo "  STORY-463 Test Suite"
echo "  Refactor feedback-search.md to lean orchestration"
echo "  Running from: $PROJECT_ROOT"
echo "======================================================"

run_suite "$SCRIPT_DIR/test_ac1_feedback_search_lean.sh"     "AC#1: feedback-search.md Lean File Constraints"
run_suite "$SCRIPT_DIR/test_ac2_reference_complete.sh"        "AC#2: Reference File Complete"
run_suite "$SCRIPT_DIR/test_ac3_orchestration_structure.sh"   "AC#3: Orchestration Structure"
run_suite "$SCRIPT_DIR/test_ac4_setup_unchanged.sh"           "AC#4: setup-github-actions.md Unchanged"
run_suite "$SCRIPT_DIR/test_ac5_gold_standard.sh"             "AC#5: Gold Standard Pattern"
run_suite "$SCRIPT_DIR/test_ac6_backward_compat_output.sh"    "AC#6: Backward Compatibility (Reference)"
run_suite "$SCRIPT_DIR/test_ac7_errors_in_command.sh"         "AC#7: Error Blocks in Command"

echo ""
echo "======================================================"
echo "  STORY-463 Suite Summary"
echo "  Test suites failed: $SUITE_FAILURES / 7"
echo "======================================================"

[ $SUITE_FAILURES -eq 0 ] && exit 0 || exit 1
