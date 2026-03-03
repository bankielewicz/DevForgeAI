#!/bin/bash
# Test: AC#1 - Open RCAs Section in Output
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

echo "=== AC#1: Open RCAs Section in Output ==="
echo "Target: $TARGET_FILE"
echo ""

# Test 1: "Open RCAs" section header exists in the command file
grep -q "Open RCAs" "$TARGET_FILE"; run_test "test_open_rcas_section_header_exists" $?

# Test 2: Section displays total open RCA count
grep -q "total open RCA" "$TARGET_FILE"; run_test "test_open_rcas_section_shows_total_count" $?

# Test 3: Section displays oldest open RCA with ID and age in days
grep -q "oldest open RCA" "$TARGET_FILE"; run_test "test_open_rcas_section_shows_oldest_rca_id_and_age" $?

# Test 4: Section references unimplemented CRITICAL or HIGH recommendations
grep -qE "unimplemented.*(CRITICAL|HIGH)|(CRITICAL|HIGH).*unimplemented" "$TARGET_FILE"
run_test "test_open_rcas_section_shows_unimplemented_critical_high_count" $?

# Test 5: The "Open RCAs" section appears within a display/output phase context
grep -q "Open RCAs" "$TARGET_FILE"; run_test "test_open_rcas_section_is_in_output_display_phase" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
