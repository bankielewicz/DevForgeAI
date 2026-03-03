#!/bin/bash
# Test: AC#3 - Phase Plan Display to User
# Story: STORY-498
# Generated: 2026-02-24

PASSED=0
FAILED=0
TARGET_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-release/SKILL.md"

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

echo "=== AC#3: Phase Plan Display to User ==="

# Test 1: Phase 0.3 has output/display section showing project type
grep -A20 "Phase 0\.3" "$TARGET_FILE" | grep -qi "display.*project type\|project type.*display\|detected.*type\|Project Type:"
run_test "Phase 0.3 displays detected project type" $?

# Test 2: Phase 0.3 output includes phase status table
grep -A30 "Phase 0\.3" "$TARGET_FILE" | grep -qi "active.*skipped\|status.*table\|phase.*status\|Active\|Skipped"
run_test "Phase 0.3 shows phase status table with active/skipped" $?

# Test 3: Display happens before Phase 1
PHASE_03_LINE=$(grep -n "Phase 0\.3" "$TARGET_FILE" | head -1 | cut -d: -f1)
PHASE_1_LINE=$(grep -n "^## Phase 1\b\|^### Phase 1\b" "$TARGET_FILE" | head -1 | cut -d: -f1)
if [ -n "$PHASE_03_LINE" ] && [ -n "$PHASE_1_LINE" ] && [ "$PHASE_03_LINE" -lt "$PHASE_1_LINE" ]; then
    run_test "Phase 0.3 display occurs before Phase 1" 0
else
    run_test "Phase 0.3 display occurs before Phase 1" 1
fi

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
