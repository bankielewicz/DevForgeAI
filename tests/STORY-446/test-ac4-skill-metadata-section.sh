#!/bin/bash
# Test: AC#4 - SKILL.md Includes Metadata Section
# Story: STORY-446
# Generated: 2026-02-18
# Expected: FAIL (TDD Red) - current file has no metadata: section

PASSED=0
FAILED=0
TARGET="/mnt/c/Projects/DevForgeAI2/src/claude/skills/discovering-requirements/SKILL.md"

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

echo "=== AC#4: SKILL.md Includes Metadata Section ==="

FRONTMATTER=$(awk '/^---$/{n++; if(n==2) exit} n==1{print}' "$TARGET")

# Test 1: frontmatter contains metadata: key
echo "$FRONTMATTER" | grep -q '^metadata:'
run_test "Frontmatter contains metadata: key" $?

# Test 2: metadata section has author field
echo "$FRONTMATTER" | grep -q 'author:'
run_test "Metadata contains author field" $?

# Test 3: metadata section has version field
echo "$FRONTMATTER" | grep -q 'version:'
run_test "Metadata contains version field" $?

# Test 4: metadata section has category field
echo "$FRONTMATTER" | grep -q 'category:'
run_test "Metadata contains category field" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
