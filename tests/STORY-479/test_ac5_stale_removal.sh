#!/bin/bash
# Test: AC#5 - Stale File Removal with User Confirmation
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

echo "=== AC#5: Stale File Removal with User Confirmation ==="

# Test 1: AskUserQuestion used for stale file removal
grep -A 40 '\-\-generate-refs' "$TARGET_FILE" | grep -q 'AskUserQuestion'
run_test "test_should_use_askuserquestion_when_stale_file_detected" $?

# Test 2: Stale file concept documented
grep -A 40 '\-\-generate-refs' "$TARGET_FILE" | grep -qi 'stale'
run_test "test_should_detect_stale_files_when_heuristic_no_longer_triggers" $?

# Test 3: User given option to keep or remove
grep -A 40 '\-\-generate-refs' "$TARGET_FILE" | grep -qi 'remove.*keep\|keep.*remove'
run_test "test_should_offer_keep_or_remove_options_when_stale_detected" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
