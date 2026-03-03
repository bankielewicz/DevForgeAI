#!/bin/bash
# Test Runner: STORY-487 - Dual-Path Architecture Validation Function
# Generated: 2026-02-23
# RED PHASE: All tests expected to FAIL before implementation.

STORY_DIR="$(cd "$(dirname "$0")" && pwd)"
TOTAL_PASSED=0
TOTAL_FAILED=0
AC_RESULTS=()

run_ac_test() {
    local script="$1"
    local ac_label="$2"

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    bash "$STORY_DIR/$script"
    local exit_code=$?

    if [ $exit_code -eq 0 ]; then
        echo "  $ac_label: PASS"
        AC_RESULTS+=("PASS: $ac_label")
        ((TOTAL_PASSED++))
    else
        echo "  $ac_label: FAIL"
        AC_RESULTS+=("FAIL: $ac_label")
        ((TOTAL_FAILED++))
    fi
}

echo "========================================================="
echo "  STORY-487: Dual-Path Architecture Validation Function"
echo "  Test Suite - TDD RED Phase"
echo "========================================================="

run_ac_test "test_ac1_function_exists.sh"             "AC#1 Function exists in correct position"
run_ac_test "test_ac2_detects_missing_sync_block.sh"  "AC#2 Detects .claude/ paths without dual_path_sync"
run_ac_test "test_ac3_passes_src_with_sync_block.sh"  "AC#3 Passes src/ paths with dual_path_sync block"
run_ac_test "test_ac4_exempts_non_dual_path_files.sh" "AC#4 Exempts non-dual-path files"
run_ac_test "test_ac5_graceful_skip_no_dual_arch_section.sh" "AC#5 Graceful skip when no Dual-Location Architecture section"
run_ac_test "test_ac6_command_invocation.sh"          "AC#6 /validate-stories Phase 2 invokes as 7th check"

echo ""
echo "========================================================="
echo "  Summary"
echo "========================================================="
for result in "${AC_RESULTS[@]}"; do
    echo "  $result"
done
echo ""
echo "  ACs Passed: $TOTAL_PASSED / $((TOTAL_PASSED + TOTAL_FAILED))"
echo "  ACs Failed: $TOTAL_FAILED / $((TOTAL_PASSED + TOTAL_FAILED))"
echo ""

if [ $TOTAL_FAILED -eq 0 ]; then
    echo "  ALL TESTS PASS - GREEN phase achieved"
    exit 0
else
    echo "  TESTS FAILING - RED phase confirmed (expected before implementation)"
    exit 1
fi
