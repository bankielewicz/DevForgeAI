#!/bin/bash
# Test: AC#2 - Library Projects Skip Deployment Phases
# Story: STORY-498
# Generated: 2026-02-24

PASSED=0
FAILED=0
TARGET_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-release/SKILL.md"

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

echo "=== AC#2: Library Projects Skip Deployment Phases ==="

# Test 1: SKIP_PHASES defined for library type containing phases 2, 2.5, 3, 3.5, 4, 6
grep -q "SKIP_PHASES" "$TARGET_FILE"
run_test "SKIP_PHASES variable defined in SKILL.md" $?

# Test 2: Skip phases list contains phase 2
grep -A5 "SKIP_PHASES" "$TARGET_FILE" | grep -q "2"
run_test "SKIP_PHASES contains phase 2" $?

# Test 3: Skip phases list contains phase 2.5
grep -A5 "SKIP_PHASES" "$TARGET_FILE" | grep -q "2\.5"
run_test "SKIP_PHASES contains phase 2.5" $?

# Test 4: Skip phases list contains phase 3
grep -A5 "SKIP_PHASES" "$TARGET_FILE" | grep -q "3"
run_test "SKIP_PHASES contains phase 3" $?

# Test 5: Skip phases list contains phase 3.5
grep -A5 "SKIP_PHASES" "$TARGET_FILE" | grep -q "3\.5"
run_test "SKIP_PHASES contains phase 3.5" $?

# Test 6: Skip phases list contains phase 4
grep -A5 "SKIP_PHASES" "$TARGET_FILE" | grep -q "4"
run_test "SKIP_PHASES contains phase 4" $?

# Test 7: Skip phases list contains phase 6
grep -A5 "SKIP_PHASES" "$TARGET_FILE" | grep -q "6"
run_test "SKIP_PHASES contains phase 6" $?

# Test 8: ACTIVE_PHASES defined for library type
grep -q "ACTIVE_PHASES" "$TARGET_FILE"
run_test "ACTIVE_PHASES variable defined in SKILL.md" $?

# Test 9: Active phases contains phase 1
grep -A5 "ACTIVE_PHASES" "$TARGET_FILE" | grep -q "1"
run_test "ACTIVE_PHASES contains phase 1" $?

# Test 10: Active phases contains phase 5
grep -A5 "ACTIVE_PHASES" "$TARGET_FILE" | grep -q "5"
run_test "ACTIVE_PHASES contains phase 5" $?

# Test 11: Active phases contains phase 7
grep -A5 "ACTIVE_PHASES" "$TARGET_FILE" | grep -q "7"
run_test "ACTIVE_PHASES contains phase 7" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
