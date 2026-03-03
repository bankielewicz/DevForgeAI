#!/bin/bash
# Test: AC#3 - Layer Argument Validation
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

echo "=== AC#3: --layer Argument ==="

# Test 1: Target file exists
test -f "$TARGET_FILE"
run_test "audit-alignment.md file exists" $?

# Test 2: --layer argument documented
grep -q "\-\-layer" "$TARGET_FILE"
run_test "--layer argument is documented" $?

# Test 3: Accepts 'all' value
grep -q "all" "$TARGET_FILE"
run_test "Accepts 'all' layer value" $?

# Test 4: Accepts 'claudemd' value
grep -q "claudemd" "$TARGET_FILE"
run_test "Accepts 'claudemd' layer value" $?

# Test 5: Accepts 'prompt' value
grep -qE "\bprompt\b" "$TARGET_FILE"
run_test "Accepts 'prompt' layer value" $?

# Test 6: Accepts 'context' value
grep -qE "\bcontext\b" "$TARGET_FILE"
run_test "Accepts 'context' layer value" $?

# Test 7: Accepts 'rules' value
grep -qE "\brules\b" "$TARGET_FILE"
run_test "Accepts 'rules' layer value" $?

# Test 8: Accepts 'adrs' value
grep -qE "\badrs\b" "$TARGET_FILE"
run_test "Accepts 'adrs' layer value" $?

# Test 9: Default is 'all'
grep -qE "default.*all|all.*default" "$TARGET_FILE"
run_test "Default layer value is 'all'" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
