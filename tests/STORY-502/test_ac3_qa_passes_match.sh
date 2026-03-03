#!/bin/bash
# Test: AC#3 - QA Phase Passes When Checksums Match
# Story: STORY-502
# Generated: 2026-02-27

# === Test Configuration ===
PASSED=0
FAILED=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
QA_REF="${PROJECT_ROOT}/src/claude/skills/devforgeai-qa/references/diff-regression-detection.md"

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

echo "=== AC#3: QA Passes When Checksums Match ==="

# === Test 1: Documents PASS verdict when all checksums match ===
grep -q -i "verdict.*PASS\|PASS.*all.*match\|checksums.*match.*PASS" "$QA_REF" 2>/dev/null
run_test "QA reference documents PASS verdict when checksums match" $?

# === Test 2: Documents mismatched_files empty on pass ===
grep -q -i "mismatched_files.*empty\|mismatched.*empty\|no.*mismatched" "$QA_REF" 2>/dev/null
run_test "Documents mismatched_files empty on pass" $?

# === Test 3: Documents tampering_patterns empty on pass ===
grep -q -i "tampering_patterns.*empty\|tampering.*empty\|no.*tampering" "$QA_REF" 2>/dev/null
run_test "Documents tampering_patterns empty on pass" $?

# === Test 4: Documents graceful degradation for missing snapshot (red-phase-checksums) ===
grep -q -i "red-phase-checksums.*missing\|missing.*red-phase-checksums\|snapshot.*absent.*WARNING.*integrity" "$QA_REF" 2>/dev/null
run_test "Documents graceful degradation for missing red-phase-checksums snapshot" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
