#!/bin/bash
# Test: AC#2 - --generate-refs Requires --fix Flag
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

echo "=== AC#2: --generate-refs Requires --fix Flag ==="

# Test 1: Validation logic exists that requires --fix with --generate-refs
grep -q '\-\-generate-refs requires \-\-fix' "$TARGET_FILE"
run_test "test_should_document_fix_requirement_when_generate_refs_used" $?

# Test 2: Error message defined for missing --fix
grep -q 'regeneration is a fix action' "$TARGET_FILE"
run_test "test_should_show_error_message_when_fix_flag_missing" $?

# Test 3: Halt behavior when --fix absent
grep -A 5 '\-\-generate-refs requires' "$TARGET_FILE" | grep -qi 'halt\|stop\|error\|abort'
run_test "test_should_halt_execution_when_fix_flag_absent" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
