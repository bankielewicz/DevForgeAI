#!/bin/bash
# Test: AC#2 - Phase 03 handles missing friction-catalog.md with fallback
# Story: STORY-524
# Generated: 2026-03-02

PASSED=0
FAILED=0
TARGET_FILE="src/claude/skills/implementing-stories/phases/phase-03-implementation.md"

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

echo "=== AC#2: Phase 03 fallback for missing friction-catalog.md ==="

# Arrange
cd "$(dirname "$0")/../.." || exit 1

# Test 1: Fallback message "No friction patterns in long-term memory yet" exists
grep -q "No friction patterns in long-term memory yet" "$TARGET_FILE"
run_test "test_phase03_step01_contains_fallback_message_when_file_absent" $?

# Test 2: Glob check specifically for friction-catalog.md
grep -q 'Glob.*friction-catalog' "$TARGET_FILE"
run_test "test_phase03_step01_has_glob_check_for_friction_catalog_file" $?

# Test 3: "Proceeding without friction context" message present
grep -q "Proceeding without friction context" "$TARGET_FILE"
run_test "test_phase03_step01_contains_proceeding_without_friction_message" $?

# Test 4: Step 0.1 has conditional fallback logic
sed -n '/Step 0\.1/,/Step 0\.2/p' "$TARGET_FILE" | grep -qE "(IF|If|if).*(absent|no match|empty|not found)"
run_test "test_phase03_step01_block_contains_conditional_fallback_logic" $?

# Summary
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
