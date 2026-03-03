#!/bin/bash
# Test: AC#3 - Zero Open RCAs Handled
# Story: STORY-490 - RCA Status Dashboard in /audit-deferrals
# Generated: 2026-02-23
# TDD Phase: RED (tests expected to FAIL before implementation)

TARGET_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/commands/audit-deferrals.md"

PASSED=0
FAILED=0

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

echo "=== AC#3: Zero Open RCAs Handled ==="
echo "Target: $TARGET_FILE"
echo ""

# Test 1: Zero open RCAs message uses "Open RCAs: 0" format
grep -q "Open RCAs: 0" "$TARGET_FILE"; run_test "test_zero_rcas_displays_count_as_zero" $?

# Test 2: Zero state message includes "All RCAs resolved" text
grep -q "All RCAs resolved" "$TARGET_FILE"; run_test "test_zero_rcas_message_says_all_rcas_resolved" $?

# Test 3: Zero state message includes the checkmark indicator (✅)
grep -qE "All RCAs resolved.*✅|✅.*All RCAs resolved" "$TARGET_FILE"
run_test "test_zero_rcas_message_includes_checkmark_indicator" $?

# Test 4: Zero state has an explicit conditional handling block
grep -qE "IF.*0|== 0|= 0|ELSE|else|no open|zero" "$TARGET_FILE"
run_test "test_zero_rcas_has_explicit_conditional_handling" $?

# Test 5: Both "Open RCAs" section and "All RCAs resolved" message appear together (non-empty section)
grep -q "Open RCAs" "$TARGET_FILE" && grep -q "All RCAs resolved" "$TARGET_FILE"
run_test "test_zero_rcas_section_is_not_empty_when_zero" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
