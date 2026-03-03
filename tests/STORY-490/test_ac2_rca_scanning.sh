#!/bin/bash
# Test: AC#2 - RCA Scanning Logic
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

echo "=== AC#2: RCA Scanning Logic ==="
echo "Target: $TARGET_FILE"
echo ""

# Test 1: Command references devforgeai/RCA/ directory for scanning
grep -q "devforgeai/RCA" "$TARGET_FILE"; run_test "test_rca_scanning_targets_devforgeai_rca_directory" $?

# Test 2: Scanner checks for "Status" field (capital S)
grep -qE '"Status"|Status:' "$TARGET_FILE"; run_test "test_rca_scanning_checks_Status_field_uppercase" $?

# Test 3: Scanner checks for "status" field (lowercase s)
grep -qE '"status"|status:' "$TARGET_FILE"; run_test "test_rca_scanning_checks_status_field_lowercase" $?

# Test 4: RCAs counted as open when status is NOT "RESOLVED"
grep -q "RESOLVED" "$TARGET_FILE"; run_test "test_rca_scanning_excludes_RESOLVED_status" $?

# Test 5: RCAs counted as open when status is NOT "CLOSED"
grep -q "CLOSED" "$TARGET_FILE"; run_test "test_rca_scanning_excludes_CLOSED_status" $?

# Test 6: Unchecked implementation checklist items are counted
grep -qE "unchecked|implementation checklist|\- \[ \]|checklist items" "$TARGET_FILE"
run_test "test_rca_scanning_counts_unchecked_checklist_items" $?

# Test 7: Scanning references framework file tools (Glob/Grep/Read) in the context of RCA scanning
grep -qE "Glob.*RCA|RCA.*Glob|Grep.*RCA|RCA.*Grep|Read.*RCA|RCA.*Read" "$TARGET_FILE"
run_test "test_rca_scanning_references_framework_file_tools" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
