#!/bin/bash
# Test: AC#8 - Executive Summary Table
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

echo "=== AC#8: Executive Summary Table ==="

# Test 1: Target file exists
test -f "$TARGET_FILE"
run_test "audit-alignment.md file exists" $?

# Test 2: Executive summary section present
grep -qiE "executive.summary|summary.table" "$TARGET_FILE"
run_test "Executive summary section present" $?

# Test 3: Category counts referenced
grep -qE "category|categories" "$TARGET_FILE"
run_test "Category counts referenced" $?

# Test 4: PASS status documented
grep -q "PASS" "$TARGET_FILE"
run_test "PASS overall status documented" $?

# Test 5: WARN status documented
grep -q "WARN" "$TARGET_FILE"
run_test "WARN overall status documented" $?

# Test 6: FAIL status documented
grep -q "FAIL" "$TARGET_FILE"
run_test "FAIL overall status documented" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
