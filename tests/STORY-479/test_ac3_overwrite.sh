#!/bin/bash
# Test: AC#3 - Regeneration Overwrites Existing Files
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

echo "=== AC#3: Regeneration Overwrites Existing Files ==="

# Test 1: Overwrite behavior documented (not append)
grep -qi 'overwrite\|overwritten\|replace' "$TARGET_FILE" && grep -A 5 'generate-refs' "$TARGET_FILE" | grep -qi 'overwrite\|overwritten\|replace'
run_test "test_should_specify_overwrite_behavior_when_regenerating" $?

# Test 2: Auto-generation header with current date mentioned
grep -A 30 '\-\-generate-refs' "$TARGET_FILE" | grep -qi 'auto-generat\|header.*date\|generation.*header'
run_test "test_should_include_auto_generation_header_when_files_created" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
