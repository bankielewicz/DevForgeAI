#!/bin/bash
# Test: AC#1 - qa-phase-state.json Preserved After QA PASS
# Story: STORY-519
# Generated: 2026-03-01
# Tests run against src/ tree per CLAUDE.md

PASSED=0
FAILED=0
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

SKILL_FILE="$PROJECT_ROOT/src/claude/skills/devforgeai-qa/SKILL.md"
REF_FILE="$PROJECT_ROOT/src/claude/skills/devforgeai-qa/references/phase-4-cleanup-workflow.md"

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

echo "=== AC#1: qa-phase-state.json Preserved After QA PASS ==="
echo ""

# --- Arrange ---
# Verify target files exist
if [ ! -f "$SKILL_FILE" ]; then
    echo "  FAIL: SKILL.md not found at $SKILL_FILE"
    exit 1
fi
if [ ! -f "$REF_FILE" ]; then
    echo "  FAIL: Reference file not found at $REF_FILE"
    exit 1
fi

# --- Act & Assert ---

# Test 1: Reference file Step 4.5 contains "DO NOT delete" for qa-phase-state.json
grep -q "DO NOT delete.*qa-phase-state\.json\|DO NOT.*remove.*qa-phase-state\.json" "$REF_FILE"
run_test "Reference file contains DO NOT delete qa-phase-state.json" $?

# Test 2: Reference file contains "preserve" for qa-phase-state.json
grep -qi "preserve.*qa-phase-state\.json\|qa-phase-state\.json.*preserve" "$REF_FILE"
run_test "Reference file contains preserve instruction for qa-phase-state.json" $?

# Test 3: SKILL.md Step 4.5 contains preserve/DO NOT delete for qa-phase-state.json
grep -q "DO NOT delete.*qa-phase-state\.json\|preserve.*qa-phase-state\.json" "$SKILL_FILE"
run_test "SKILL.md contains preserve/DO NOT delete for qa-phase-state.json" $?

# Test 4: Reference file states qa-phase-state.json remains after cleanup
grep -qi "qa-phase-state\.json.*remains\|qa-phase-state\.json.*retained\|qa-phase-state\.json.*kept" "$REF_FILE"
run_test "Reference file states qa-phase-state.json remains after cleanup" $?

# --- Summary ---
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
