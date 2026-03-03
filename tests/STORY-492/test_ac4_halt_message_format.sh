#!/bin/bash
# Test: AC#4 - Checkpoint HALT prevents phase progression
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

echo "=== AC#4: HALT Message Format Tests ==="
echo ""

# --- Test 1: Phase 2-3 Gate HALT includes checkpoint name ---
GATE_23=$(sed -n '/^## Phase 2 - Phase 3 Gate/,/^## /p' "$TARGET_FILE" | head -n -1)
echo "$GATE_23" | grep "HALT" | grep -q "Phase 2.*3\|2-3"
run_test "Phase 2-3 Gate HALT includes checkpoint name" $?

# --- Test 2: Phase 5-6 Gate HALT includes checkpoint name ---
GATE_56=$(sed -n '/^## Phase 5 - Phase 6 Gate/,/^## /p' "$TARGET_FILE" | head -n -1)
echo "$GATE_56" | grep "HALT" | grep -q "Phase 5.*6\|5-6"
run_test "Phase 5-6 Gate HALT includes checkpoint name" $?

# --- Test 3: Phase 7-8 Gate HALT includes checkpoint name ---
GATE_78=$(sed -n '/^## Phase 7 - Phase 8 Gate/,/^## /p' "$TARGET_FILE" | head -n -1)
echo "$GATE_78" | grep "HALT" | grep -q "Phase 7.*8\|7-8"
run_test "Phase 7-8 Gate HALT includes checkpoint name" $?

# --- Test 4: Phase 2-3 HALT lists missing items ---
echo "$GATE_23" | grep -qi "missing.*section\|missing.*item\|list.*missing"
run_test "Phase 2-3 HALT references missing section list" $?

# --- Test 5: Phase 5-6 HALT lists missing items ---
echo "$GATE_56" | grep -qi "missing.*section\|missing.*item\|list.*missing"
run_test "Phase 5-6 HALT references missing section list" $?

# --- Test 6: Phase 7-8 HALT lists missing items ---
echo "$GATE_78" | grep -qi "missing.*section\|missing.*item\|missing.*validation\|no.*evidence"
run_test "Phase 7-8 HALT references missing validation evidence" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed out of 6 tests"
[ $FAILED -eq 0 ] && exit 0 || exit 1
