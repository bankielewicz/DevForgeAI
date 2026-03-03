#!/bin/bash
# Test: AC#4 - Fix Mutability Rules
# Story: STORY-474
# Generated: 2026-02-23

PASSED=0
FAILED=0
TARGET_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/commands/audit-alignment.md"

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

echo "=== AC#4: --fix Mutability Rules ==="

# Test 1: Target file exists
test -f "$TARGET_FILE"
run_test "audit-alignment.md file exists" $?

# Test 2: --fix argument documented
grep -q "\-\-fix" "$TARGET_FILE"
run_test "--fix argument is documented" $?

# Test 3: IMMUTABLE files recommend ADR
grep -qE "IMMUTABLE.*ADR|ADR.*IMMUTABLE" "$TARGET_FILE"
run_test "IMMUTABLE files get ADR recommendation" $?

# Test 4: MUTABLE files use AskUserQuestion
grep -qE "MUTABLE.*AskUserQuestion|AskUserQuestion.*MUTABLE" "$TARGET_FILE"
run_test "MUTABLE files use AskUserQuestion" $?

# Test 5: APPEND-ONLY files create new ADR
grep -qE "APPEND.ONLY.*ADR|ADR.*APPEND.ONLY" "$TARGET_FILE"
run_test "APPEND-ONLY files create new ADR" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
