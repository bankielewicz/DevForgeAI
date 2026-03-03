#!/bin/bash
# Test: AC#1 - --generate-refs Flag Triggers Regeneration
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

echo "=== AC#1: --generate-refs Flag Triggers Regeneration ==="

# Test 1: --generate-refs flag is documented in command file
grep -q '\-\-generate-refs' "$TARGET_FILE"
run_test "test_should_contain_generate_refs_flag_when_file_inspected" $?

# Test 2: --generate-refs triggers Task() delegation for regeneration
grep -q '\-\-generate-refs' "$TARGET_FILE" && grep -A 30 '\-\-generate-refs' "$TARGET_FILE" | grep -q 'Task('
run_test "test_should_delegate_via_task_when_generate_refs_invoked" $?

# Test 3: Regeneration targets project-*.md files
grep -q '\-\-generate-refs' "$TARGET_FILE" && grep -A 30 '\-\-generate-refs' "$TARGET_FILE" | grep -q 'project-\*\.md'
run_test "test_should_target_project_md_files_when_regeneration_triggered" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
