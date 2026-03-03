#!/bin/bash
# Test: AC#2 - Checklist Positioned Before Phase Marker Write
# Story: STORY-520
# Generated: 2026-03-01

set -euo pipefail

# === Test Configuration ===
PASSED=0
FAILED=0
TARGET_FILE="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-qa/SKILL.md"

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        PASSED=$((PASSED + 1))
    else
        echo "  FAIL: $name"
        FAILED=$((FAILED + 1))
    fi
}

echo "=== AC#2: Checklist Positioned Before Phase Marker Write ==="
echo ""

# === Test 1: Checklist header line number ===
CHECKLIST_LINE=$(grep -n "### Phase 1.5 Completion Checklist" "$TARGET_FILE" | head -1 | cut -d: -f1 || true)
if [ -z "$CHECKLIST_LINE" ]; then
    run_test "Phase 1.5 Completion Checklist header found (prerequisite)" 1
    echo ""
    echo "Results: $PASSED passed, $FAILED failed"
    exit 1
fi
run_test "Phase 1.5 Completion Checklist header found at line $CHECKLIST_LINE" 0

# === Test 2: phase-complete or CLI gate call exists after checklist for Phase 1.5 ===
# Look for phase-complete with phase 1.5 reference AFTER the checklist
GATE_LINE=$(awk -v start="$CHECKLIST_LINE" '
    NR > start && /phase-complete.*1\.5|phase-complete.*phase=1\.5|phase.*1\.5.*complete/ { print NR; exit }
' "$TARGET_FILE")

if [ -z "$GATE_LINE" ]; then
    # No CLI gate found after checklist - test FAILS because there should be one
    run_test "CLI gate/phase-complete call exists after Phase 1.5 Completion Checklist" 1
else
    run_test "CLI gate/phase-complete call exists after Phase 1.5 Completion Checklist at line $GATE_LINE" 0
fi

# === Test 3: Checklist appears BEFORE the gate call ===
if [ -n "$GATE_LINE" ] && [ "$CHECKLIST_LINE" -lt "$GATE_LINE" ]; then
    run_test "Checklist (line $CHECKLIST_LINE) appears before CLI gate (line $GATE_LINE)" 0
else
    run_test "Checklist appears before CLI gate call (checklist=$CHECKLIST_LINE, gate=${GATE_LINE:-not_found})" 1
fi

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
