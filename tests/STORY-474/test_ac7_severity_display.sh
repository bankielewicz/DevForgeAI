#!/bin/bash
# Test: AC#7 - Severity-Based Display Formatting
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

echo "=== AC#7: Severity-Based Display Formatting ==="

# Test 1: Target file exists
test -f "$TARGET_FILE"
run_test "audit-alignment.md file exists" $?

# Test 2: CRITICAL severity referenced
grep -q "CRITICAL" "$TARGET_FILE"
run_test "CRITICAL severity level present" $?

# Test 3: HIGH severity referenced
grep -q "HIGH" "$TARGET_FILE"
run_test "HIGH severity level present" $?

# Test 4: MEDIUM severity referenced
grep -q "MEDIUM" "$TARGET_FILE"
run_test "MEDIUM severity level present" $?

# Test 5: LOW severity referenced
grep -q "LOW" "$TARGET_FILE"
run_test "LOW severity level present" $?

# Test 6: Severity ordering documented (CRITICAL > HIGH > MEDIUM > LOW)
grep -qE "CRITICAL.*HIGH.*MEDIUM.*LOW" "$TARGET_FILE"
run_test "Severity ordering CRITICAL > HIGH > MEDIUM > LOW documented" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
