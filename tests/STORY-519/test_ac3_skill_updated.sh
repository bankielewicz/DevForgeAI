#!/bin/bash
# Test: AC#3 - SKILL.md Step 4.5 Updated with All 3 Requirements
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

echo "=== AC#3: SKILL.md Step 4.5 Updated with All 3 Requirements ==="
echo ""

# --- Arrange ---
if [ ! -f "$SKILL_FILE" ]; then
    echo "  FAIL: SKILL.md not found at $SKILL_FILE"
    exit 1
fi
if [ ! -f "$REF_FILE" ]; then
    echo "  FAIL: Reference file not found at $REF_FILE"
    exit 1
fi

# --- Act & Assert ---

# Requirement (a): DO NOT delete qa-phase-state.json
grep -q "DO NOT delete.*qa-phase-state\.json" "$SKILL_FILE"
run_test "SKILL.md: (a) DO NOT delete qa-phase-state.json" $?

# Requirement (b): DELETE .qa-phase-N.marker files (legacy cleanup)
grep -qi "delete.*\.qa-phase.*\.marker" "$SKILL_FILE"
run_test "SKILL.md: (b) DELETE .qa-phase-N.marker files" $?

# Requirement (c): qa-phase-state.json IS the permanent audit trail
grep -qi "qa-phase-state\.json.*permanent audit trail\|qa-phase-state\.json.*audit trail" "$SKILL_FILE"
run_test "SKILL.md: (c) qa-phase-state.json IS the permanent audit trail" $?

# Same 3 requirements in reference file
grep -q "DO NOT delete.*qa-phase-state\.json" "$REF_FILE"
run_test "Reference: (a) DO NOT delete qa-phase-state.json" $?

grep -qi "delete.*\.qa-phase.*\.marker" "$REF_FILE"
run_test "Reference: (b) DELETE .qa-phase-N.marker files" $?

grep -qi "qa-phase-state\.json.*permanent audit trail\|qa-phase-state\.json.*audit trail" "$REF_FILE"
run_test "Reference: (c) qa-phase-state.json IS the permanent audit trail" $?

# --- Summary ---
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
