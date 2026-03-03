#!/bin/bash
# Test: AC#4 - All 4 Heuristics Re-Evaluated
# Story: STORY-479
# Generated: 2026-02-23

PASSED=0
FAILED=0
TARGET_FILE="src/claude/commands/audit-alignment.md"

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

echo "=== AC#4: All 4 Heuristics Re-Evaluated ==="

# Test 1: References to all 4 detection heuristics (DH-01 through DH-04)
grep -q 'DH-01' "$TARGET_FILE" && grep -q 'DH-02' "$TARGET_FILE" && grep -q 'DH-03' "$TARGET_FILE" && grep -q 'DH-04' "$TARGET_FILE"
run_test "test_should_reference_all_four_heuristics_when_regenerating" $?

# Test 2: Re-evaluation of all heuristics documented in --generate-refs context
grep -A 40 '\-\-generate-refs' "$TARGET_FILE" | grep -qi 'all.*4.*heuristic\|re-evaluat\|DH-0[1-4]'
run_test "test_should_re_evaluate_all_heuristics_when_generate_refs_invoked" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
