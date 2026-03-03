#!/bin/bash
# Test: AC#8 - Derivation Purity Verification
# Story: STORY-478
# Generated: 2026-02-23
set -uo pipefail

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TARGET="$PROJECT_ROOT/src/claude/skills/designing-systems/references/domain-reference-generation.md"
PASSED=0
FAILED=0

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        ((PASSED++))
    else
        echo "  FAIL: $name"
        ((FAILED++))
    fi
}

echo "=== AC#8: Derivation Purity Verification ==="

# Test 1: Contains verification step (Step 4)
grep -q "Step 4" "$TARGET" && grep -iq "verif" "$TARGET"
run_test "test_should_contain_step4_verification_when_reference_checked" $?

# Test 2: Documents 100% content derivation requirement
grep -q "100%" "$TARGET"
run_test "test_should_document_100_percent_derivation_when_checked" $?

# Test 3: Verification failure halts with warning
grep -iq "halt" "$TARGET" && grep -iq "warning" "$TARGET"
run_test "test_should_halt_on_verification_failure_when_checked" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
