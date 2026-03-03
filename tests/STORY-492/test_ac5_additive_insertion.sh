#!/bin/bash
# Test: AC#5 - All checkpoints are additive to existing SKILL.md
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

echo "=== AC#5: Additive Insertion Tests ==="
echo ""

# --- Test 1-8: All 8 original phase headers preserved ---
# The devforgeai-story-creation skill has 8 phases
PHASE_HEADERS=(
    "Phase 1"
    "Phase 2"
    "Phase 3"
    "Phase 4"
    "Phase 5"
    "Phase 6"
    "Phase 7"
    "Phase 8"
)

phase_count=0
for phase in "${PHASE_HEADERS[@]}"; do
    if grep -q "^### .*${phase}" "$TARGET_FILE"; then
        ((phase_count++))
    fi
done
[ "$phase_count" -eq 8 ]
run_test "All 8 original phase headers preserved (found $phase_count/8)" $?

# --- Test 9: Gate headers use ## level ---
GATE_COUNT=$(grep -c "^## Phase [0-9]\+ - Phase [0-9]\+ Gate" "$TARGET_FILE")
[ "$GATE_COUNT" -ge 3 ]
run_test "At least 3 gate headers exist at ## level (found $GATE_COUNT)" $?

# --- Test 10: Gates are between correct phases (2-3, 5-6, 7-8) ---
grep -q "^## Phase 2 - Phase 3 Gate" "$TARGET_FILE"
GATE_23=$?
grep -q "^## Phase 5 - Phase 6 Gate" "$TARGET_FILE"
GATE_56=$?
grep -q "^## Phase 7 - Phase 8 Gate" "$TARGET_FILE"
GATE_78=$?
[ "$GATE_23" -eq 0 ] && [ "$GATE_56" -eq 0 ] && [ "$GATE_78" -eq 0 ]
run_test "All 3 specific gate headers exist (2-3, 5-6, 7-8)" $?

# --- Test 11: Phase order preserved (Phase 2 before Phase 3, etc.) ---
P2_LINE=$(grep -n "^### .*Phase 2[^-]" "$TARGET_FILE" | head -1 | cut -d: -f1)
P3_LINE=$(grep -n "^### .*Phase 3[^-]" "$TARGET_FILE" | head -1 | cut -d: -f1)
if [ -n "$P2_LINE" ] && [ -n "$P3_LINE" ]; then
    [ "$P2_LINE" -lt "$P3_LINE" ]
    run_test "Phase 2 appears before Phase 3 (line $P2_LINE < $P3_LINE)" $?
else
    run_test "Phase 2 appears before Phase 3 (headers not found)" 1
fi

# --- Test 12: Gate 2-3 appears between Phase 2 and Phase 3 ---
GATE_23_LINE=$(grep -n "^## Phase 2 - Phase 3 Gate" "$TARGET_FILE" | head -1 | cut -d: -f1)
if [ -n "$GATE_23_LINE" ] && [ -n "$P2_LINE" ] && [ -n "$P3_LINE" ]; then
    [ "$GATE_23_LINE" -gt "$P2_LINE" ] && [ "$GATE_23_LINE" -lt "$P3_LINE" ]
    run_test "Gate 2-3 positioned between Phase 2 and Phase 3" $?
else
    run_test "Gate 2-3 positioned between Phase 2 and Phase 3 (not found)" 1
fi

# --- Test 13: No content removal (file has reasonable size) ---
LINE_COUNT=$(wc -l < "$TARGET_FILE")
[ "$LINE_COUNT" -gt 100 ]
run_test "SKILL.md has substantial content ($LINE_COUNT lines, no mass deletion)" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed out of 6 tests"
[ $FAILED -eq 0 ] && exit 0 || exit 1
