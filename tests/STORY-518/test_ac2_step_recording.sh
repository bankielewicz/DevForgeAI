#!/bin/bash
# Test: AC#2 - Step Recording
# Story: STORY-518
# Generated: 2026-03-01

# === Test Configuration ===
PASSED=0
FAILED=0
TARGET_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-qa/SKILL.md"

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

echo "=== AC#2: Step Recording ==="
echo ""

# Verify target file exists
if [ ! -f "$TARGET_FILE" ]; then
    echo "  FAIL: Target file not found: $TARGET_FILE"
    echo "Results: 0 passed, 1 failed"
    exit 1
fi

# Test 1: Instruction to record test_integrity_verification in steps_completed
grep -q "test_integrity_verification" "$TARGET_FILE"
run_test "Contains test_integrity_verification step name" $?

# Test 2: References qa-phase-state.json steps_completed array
grep -q "steps_completed" "$TARGET_FILE"
run_test "References steps_completed array in qa-phase-state.json" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
