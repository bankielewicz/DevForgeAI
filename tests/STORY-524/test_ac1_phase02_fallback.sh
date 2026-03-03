#!/bin/bash
# Test: AC#1 - Phase 02 handles missing tdd-patterns.md with fallback
# Story: STORY-524
# Generated: 2026-03-02

PASSED=0
FAILED=0
TARGET_FILE="src/claude/skills/implementing-stories/phases/phase-02-test-first.md"

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

echo "=== AC#1: Phase 02 fallback for missing tdd-patterns.md ==="

# Arrange
cd "$(dirname "$0")/../.." || exit 1

# Test 1: Fallback message "No TDD patterns in long-term memory yet" exists
grep -q "No TDD patterns in long-term memory yet" "$TARGET_FILE"
run_test "test_phase02_step01_contains_fallback_message_when_file_absent" $?

# Test 2: Glob check specifically for tdd-patterns.md (not just any Glob)
# Must find Glob(...tdd-patterns...) pattern
grep -q 'Glob.*tdd-patterns' "$TARGET_FILE"
run_test "test_phase02_step01_has_glob_check_for_tdd_patterns_file" $?

# Test 3: "Proceeding without memory context" message present
grep -q "Proceeding without memory context" "$TARGET_FILE"
run_test "test_phase02_step01_contains_proceeding_without_memory_message" $?

# Test 4: Step 0.1 has conditional fallback (IF.*no match or similar near tdd-patterns)
# Extract Step 0.1 block and check for conditional logic about absent file
sed -n '/Step 0\.1/,/Step 0\.2/p' "$TARGET_FILE" | grep -qE "(IF|If|if).*(absent|no match|empty|not found)"
run_test "test_phase02_step01_block_contains_conditional_fallback_logic" $?

# Summary
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
