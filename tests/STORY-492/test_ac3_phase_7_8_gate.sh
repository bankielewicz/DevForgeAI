#!/bin/bash
# Test: AC#3 - Phase 7-8 Checkpoint verifies validation was executed
# Story: STORY-492
# Generated: 2026-02-23

# === Test Configuration ===
PASSED=0
FAILED=0
TARGET_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-story-creation/SKILL.md"

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

echo "=== AC#3: Phase 7-8 Gate Tests ==="
echo ""

# --- Test 1: Phase 7-8 Gate header exists ---
grep -q "^## Phase 7 - Phase 8 Gate" "$TARGET_FILE"
run_test "Phase 7-8 Gate header exists with ## level" $?

# Extract gate block
GATE_BLOCK=$(sed -n '/^## Phase 7 - Phase 8 Gate/,/^## /p' "$TARGET_FILE" | head -n -1)

# --- Test 2: Gate references validation evidence ---
echo "$GATE_BLOCK" | grep -qi "validation.*evidence\|evidence.*validation"
run_test "Gate verifies validation evidence exists" $?

# --- Test 3: Gate references validation-checklists.md ---
echo "$GATE_BLOCK" | grep -q "validation-checklists"
run_test "Gate references validation-checklists.md" $?

# --- Test 4: Gate contains HALT for missing validation ---
echo "$GATE_BLOCK" | grep -q "HALT"
run_test "Gate contains HALT for missing validation evidence" $?

# --- Test 5: Gate checks for validation findings or all-passed statement ---
echo "$GATE_BLOCK" | grep -qi "finding\|all.*check.*passed\|validation.*result"
run_test "Gate checks for validation findings or all-checks-passed" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed out of 5 tests"
[ $FAILED -eq 0 ] && exit 0 || exit 1
