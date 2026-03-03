#!/bin/bash
# Test: AC#1 - Sibling Reuse Protocol Added to Observation-Capture
# Story: STORY-486
# Generated: 2026-02-23
# TDD Phase: RED (tests expected to FAIL before implementation)

PASSED=0
FAILED=0
TARGET_FILE="src/claude/skills/implementing-stories/references/observation-capture.md"

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

echo "AC#1: Sibling Reuse Protocol Added to Observation-Capture"
echo "Target: $TARGET_FILE"
echo ""

# Arrange: verify target file exists
if [ ! -f "$TARGET_FILE" ]; then
    echo "  ERROR: Target file not found: $TARGET_FILE"
    exit 1
fi

# Test 1: Section heading exists
grep -q "Sibling Story Pattern Reuse" "$TARGET_FILE"
run_test "Section 'Sibling Story Pattern Reuse' exists in observation-capture.md" $?

# Test 2: Documents WHEN to reuse (batch workflows)
grep -qi "batch" "$TARGET_FILE"
run_test "Section documents when to reuse (batch workflows)" $?

# Test 3: Documents WHAT to reuse - test structure
grep -qi "test structure" "$TARGET_FILE"
run_test "Section documents what to reuse: test structure" $?

# Test 4: Documents WHAT to reuse - fixtures
grep -qi "fixture" "$TARGET_FILE"
run_test "Section documents what to reuse: fixtures" $?

# Test 5: Documents WHAT to reuse - patterns (must appear near "reuse" context)
grep -A20 "Sibling Story Pattern Reuse" "$TARGET_FILE" | grep -qi "reuse.*pattern\|pattern.*reuse"
run_test "Section documents what to reuse: patterns (within Sibling Reuse section)" $?

# Test 6: Documents HOW to reference (cite first story as pattern source)
grep -qi "pattern source" "$TARGET_FILE"
run_test "Section documents how to reference (cite first story as pattern source)" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
