#!/bin/bash
# Test: AC#8 - AskUserQuestion calls remain in commands, zero in new skill
# Story: STORY-462
# Generated: 2026-02-21
# TDD Phase: RED (all tests expected to FAIL before implementation)
# Requirement: >=7 AskUserQuestion in commands combined; 0 in new skill

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
PASSED=0
FAILED=0

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

echo "=== AC#8: AskUserQuestion placement ==="

AUDIT_W3_CMD="$PROJECT_ROOT/src/claude/commands/audit-w3.md"
ORCHESTRATE_CMD="$PROJECT_ROOT/src/claude/commands/orchestrate.md"
RCA_CMD="$PROJECT_ROOT/src/claude/commands/create-stories-from-rca.md"
SKILL_FILE="$PROJECT_ROOT/src/claude/skills/auditing-w3-compliance/SKILL.md"

# --- Count AskUserQuestion in all three command files combined ---
TOTAL_COUNT=0

if [ -f "$AUDIT_W3_CMD" ]; then
    COUNT=$(grep -c "AskUserQuestion" "$AUDIT_W3_CMD" 2>/dev/null || true)
    TOTAL_COUNT=$(( TOTAL_COUNT + ${COUNT:-0} ))
    echo "  INFO: audit-w3.md AskUserQuestion count: ${COUNT:-0}"
else
    echo "  WARN: audit-w3.md not found"
fi

if [ -f "$ORCHESTRATE_CMD" ]; then
    COUNT=$(grep -c "AskUserQuestion" "$ORCHESTRATE_CMD" 2>/dev/null || true)
    TOTAL_COUNT=$(( TOTAL_COUNT + ${COUNT:-0} ))
    echo "  INFO: orchestrate.md AskUserQuestion count: $COUNT"
else
    echo "  WARN: orchestrate.md not found"
fi

if [ -f "$RCA_CMD" ]; then
    COUNT=$(grep -c "AskUserQuestion" "$RCA_CMD" 2>/dev/null || true)
    TOTAL_COUNT=$(( TOTAL_COUNT + ${COUNT:-0} ))
    echo "  INFO: create-stories-from-rca.md AskUserQuestion count: $COUNT"
else
    echo "  WARN: create-stories-from-rca.md not found"
fi

echo "  INFO: Total AskUserQuestion across commands: $TOTAL_COUNT (need >=7)"

# --- Test 1: Combined AskUserQuestion count in commands >= 7 ---
[ "$TOTAL_COUNT" -ge 7 ]
run_test "Commands combined: >=7 AskUserQuestion calls preserved (found: $TOTAL_COUNT)" $?

# --- Test 2: auditing-w3-compliance SKILL.md has 0 AskUserQuestion ---
if [ -f "$SKILL_FILE" ]; then
    SKILL_COUNT=$(grep -c "AskUserQuestion" "$SKILL_FILE" 2>/dev/null || true)
    [ "${SKILL_COUNT:-0}" -eq 0 ]
    run_test "auditing-w3-compliance SKILL.md has 0 AskUserQuestion (found: $SKILL_COUNT)" $?
else
    echo "  FAIL: auditing-w3-compliance/SKILL.md does not exist"
    ((FAILED++))
fi

# --- Summary ---
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
