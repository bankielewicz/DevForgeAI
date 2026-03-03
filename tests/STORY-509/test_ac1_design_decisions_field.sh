#!/bin/bash
# Test: AC#1 - design_decisions Field Added to F4 Schema
# Story: STORY-509
# Generated: 2026-02-28

PASSED=0
FAILED=0

TARGET_FILE="src/claude/skills/discovering-requirements/references/artifact-generation.md"

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        PASSED=$((PASSED + 1))
    else
        echo "  FAIL: $name"
        FAILED=$((FAILED + 1))
    fi
}

echo "=== AC#1: design_decisions Field in F4 Schema ==="
echo "Target: $TARGET_FILE"
echo ""

if [ ! -f "$TARGET_FILE" ]; then
    echo "  FAIL: Target file does not exist: $TARGET_FILE"
    echo "Results: 0 passed, 1 failed"
    exit 1
fi

# Test 1: design_decisions top-level section exists
grep -qi "design_decisions" "$TARGET_FILE" 2>/dev/null; run_test "design_decisions section exists in F4 schema" $?

# Test 2: id field under design_decisions
grep -A 30 -i "design_decisions" "$TARGET_FILE" 2>/dev/null | grep -qi "\bid\b" 2>/dev/null; run_test "design_decisions has 'id' field" $?

# Test 3: decision field
grep -A 30 -i "design_decisions" "$TARGET_FILE" 2>/dev/null | grep -qi "\bdecision\b" 2>/dev/null; run_test "design_decisions has 'decision' field" $?

# Test 4: rationale field
grep -A 30 -i "design_decisions" "$TARGET_FILE" 2>/dev/null | grep -qi "\brationale\b" 2>/dev/null; run_test "design_decisions has 'rationale' field" $?

# Test 5: alternatives_rejected field
grep -A 30 -i "design_decisions" "$TARGET_FILE" 2>/dev/null | grep -qi "alternatives_rejected" 2>/dev/null; run_test "design_decisions has 'alternatives_rejected' field" $?

# Test 6: alternatives_rejected has name sub-field
grep -A 50 -i "design_decisions" "$TARGET_FILE" 2>/dev/null | grep -A 10 -i "alternatives_rejected" 2>/dev/null | grep -qi "\bname\b" 2>/dev/null; run_test "alternatives_rejected has 'name' sub-field" $?

# Test 7: alternatives_rejected has reason sub-field
grep -A 50 -i "design_decisions" "$TARGET_FILE" 2>/dev/null | grep -A 10 -i "alternatives_rejected" 2>/dev/null | grep -qi "\breason\b" 2>/dev/null; run_test "alternatives_rejected has 'reason' sub-field" $?

# Test 8: user_observations field
grep -A 30 -i "design_decisions" "$TARGET_FILE" 2>/dev/null | grep -qi "user_observations" 2>/dev/null; run_test "design_decisions has 'user_observations' field" $?

# Test 9: constraints field
grep -A 30 -i "design_decisions" "$TARGET_FILE" 2>/dev/null | grep -qi "\bconstraints\b" 2>/dev/null; run_test "design_decisions has 'constraints' field" $?

# Summary
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
