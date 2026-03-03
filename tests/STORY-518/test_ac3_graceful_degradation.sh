#!/bin/bash
# Test: AC#3 - Graceful Degradation
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

echo "=== AC#3: Graceful Degradation ==="
echo ""

# Verify target file exists
if [ ! -f "$TARGET_FILE" ]; then
    echo "  FAIL: Target file not found: $TARGET_FILE"
    echo "Results: 0 passed, 1 failed"
    exit 1
fi

# Test 1: WARNING message about missing snapshot
grep -q "Test integrity snapshot not found" "$TARGET_FILE"
run_test "Contains WARNING: Test integrity snapshot not found" $?

# Test 2: Graceful degradation text
grep -q "graceful degradation" "$TARGET_FILE"
run_test "Contains graceful degradation instruction" $?

# Test 3: QA continues without blocking on missing snapshot (pre-STORY-502 reference)
grep -q "pre-STORY-502" "$TARGET_FILE"
run_test "References pre-STORY-502 stories for backward compatibility" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
