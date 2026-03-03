#!/bin/bash
# Test: AC#5 - Output Argument
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

echo "=== AC#5: --output Argument ==="

# Test 1: Target file exists
test -f "$TARGET_FILE"
run_test "audit-alignment.md file exists" $?

# Test 2: --output argument documented
grep -q "\-\-output" "$TARGET_FILE"
run_test "--output argument is documented" $?

# Test 3: Console mode supported
grep -qE "\bconsole\b" "$TARGET_FILE"
run_test "Console output mode supported" $?

# Test 4: File mode supported
grep -qE "\bfile\b" "$TARGET_FILE"
run_test "File output mode supported" $?

# Test 5: Console is default
grep -qE "default.*console|console.*default" "$TARGET_FILE"
run_test "Console is default output mode" $?

# Test 6: File mode writes to alignment-audit path
grep -qE "alignment-audit-.*\.md|devforgeai/qa/alignment-audit" "$TARGET_FILE"
run_test "File mode writes to devforgeai/qa/alignment-audit-{date}.md" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
