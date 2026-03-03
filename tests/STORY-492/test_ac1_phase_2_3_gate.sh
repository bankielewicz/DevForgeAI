#!/bin/bash
# Test: AC#1 - Phase 2-3 Checkpoint verifies requirements analysis outputs exist
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

echo "=== AC#1: Phase 2-3 Gate Tests ==="
echo ""

# --- Test 1: Phase 2-3 Gate header exists ---
grep -q "^## Phase 2 - Phase 3 Gate" "$TARGET_FILE"
run_test "Phase 2-3 Gate header exists with ## level" $?

# --- Test 2: Gate checks for ## User Story ---
grep -A 50 "^## Phase 2 - Phase 3 Gate" "$TARGET_FILE" | grep -q "User Story"
run_test "Gate checks for User Story section" $?

# --- Test 3: Gate checks for ## Acceptance Criteria ---
grep -A 50 "^## Phase 2 - Phase 3 Gate" "$TARGET_FILE" | grep -q "Acceptance Criteria"
run_test "Gate checks for Acceptance Criteria section" $?

# --- Test 4: Gate checks for ## Edge Cases ---
grep -A 50 "^## Phase 2 - Phase 3 Gate" "$TARGET_FILE" | grep -q "Edge Cases"
run_test "Gate checks for Edge Cases section" $?

# --- Test 5: Gate checks for ## Non-Functional Requirements ---
grep -A 50 "^## Phase 2 - Phase 3 Gate" "$TARGET_FILE" | grep -q "Non-Functional Requirements"
run_test "Gate checks for Non-Functional Requirements section" $?

# --- Test 6: Gate contains HALT directive ---
grep -A 50 "^## Phase 2 - Phase 3 Gate" "$TARGET_FILE" | grep -q "HALT"
run_test "Gate contains HALT directive" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed out of 6 tests"
[ $FAILED -eq 0 ] && exit 0 || exit 1
