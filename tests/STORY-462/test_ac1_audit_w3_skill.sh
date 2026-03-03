#!/bin/bash
# Test: AC#1 - audit-w3.md refactored with new auditing-w3-compliance skill
# Story: STORY-462
# Generated: 2026-02-21
# TDD Phase: RED (all tests expected to FAIL before implementation)
# set -e removed: tests use run_test pattern that captures exit codes

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

echo "=== AC#1: audit-w3.md refactored with new auditing-w3-compliance skill ==="

AUDIT_W3_CMD="$PROJECT_ROOT/src/claude/commands/audit-w3.md"
SKILL_FILE="$PROJECT_ROOT/src/claude/skills/auditing-w3-compliance/SKILL.md"
SKILL_DIR="$PROJECT_ROOT/src/claude/skills/auditing-w3-compliance"

# --- Test 1: audit-w3.md exists ---
[ -f "$AUDIT_W3_CMD" ]
run_test "audit-w3.md exists" $?

# --- Test 2: audit-w3.md is <=120 lines ---
if [ -f "$AUDIT_W3_CMD" ]; then
    LINE_COUNT=$(wc -l < "$AUDIT_W3_CMD")
    [ "$LINE_COUNT" -le 120 ]
    run_test "audit-w3.md is <=120 lines (current: $LINE_COUNT)" $?
else
    echo "  FAIL: audit-w3.md not found, cannot check line count"
    ((FAILED++))
fi

# --- Test 3: audit-w3.md has <=4 code blocks before Skill() call ---
if [ -f "$AUDIT_W3_CMD" ]; then
    # Find line number of first Skill() call
    SKILL_LINE=$(grep -n "Skill(" "$AUDIT_W3_CMD" | head -1 | cut -d: -f1 || echo "99999")
    if [ -z "$SKILL_LINE" ] || [ "$SKILL_LINE" = "99999" ]; then
        echo "  FAIL: No Skill() call found in audit-w3.md"
        ((FAILED++))
    else
        # Count ``` occurrences before SKILL_LINE (each code block is 2 backtick lines)
        BACKTICK_COUNT=$(head -n "$SKILL_LINE" "$AUDIT_W3_CMD" | grep -c '^\s*```' || true)
        BLOCK_COUNT=$(( BACKTICK_COUNT / 2 ))
        [ "$BLOCK_COUNT" -le 4 ]
        run_test "audit-w3.md has <=4 code blocks before Skill() call (found: $BLOCK_COUNT)" $?
    fi
else
    echo "  FAIL: audit-w3.md not found, cannot check code blocks"
    ((FAILED++))
fi

# --- Test 4: auditing-w3-compliance SKILL.md exists ---
[ -f "$SKILL_FILE" ]
run_test "auditing-w3-compliance/SKILL.md exists" $?

# --- Test 5: Skill directory uses gerund naming (auditing-w3-compliance) ---
[ -d "$SKILL_DIR" ]
run_test "Skill directory auditing-w3-compliance exists (gerund naming per ADR-017)" $?

# --- Test 6: Skill directory name starts with gerund 'auditing' ---
SKILL_DIRNAME=$(basename "$SKILL_DIR")
echo "$SKILL_DIRNAME" | grep -q "^auditing"
run_test "Skill directory name starts with gerund 'auditing' (got: $SKILL_DIRNAME)" $?

# --- Summary ---
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
