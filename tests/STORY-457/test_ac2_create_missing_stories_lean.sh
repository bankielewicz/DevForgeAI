#!/usr/bin/env bash
# STORY-457 AC#2: Refactored /create-missing-stories meets lean orchestration targets
# Tests run against src/ tree per CLAUDE.md
set -euo pipefail

COMMAND_FILE="src/claude/commands/create-missing-stories.md"
PASS=0
FAIL=0

assert_true() {
    local desc="$1"; shift
    if "$@" >/dev/null 2>&1; then
        echo "  PASS: $desc"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: $desc"
        FAIL=$((FAIL + 1))
    fi
}

assert_less_equal() {
    local desc="$1" actual="$2" max="$3"
    if [ "$actual" -le "$max" ]; then
        echo "  PASS: $desc ($actual <= $max)"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: $desc ($actual > $max)"
        FAIL=$((FAIL + 1))
    fi
}

assert_equal() {
    local desc="$1" actual="$2" expected="$3"
    if [ "$actual" = "$expected" ]; then
        echo "  PASS: $desc ($actual = $expected)"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: $desc ($actual != $expected)"
        FAIL=$((FAIL + 1))
    fi
}

echo "=== AC#2: create-missing-stories Lean Orchestration ==="
echo ""

# Test 1: File exists
echo "--- File Existence ---"
assert_true "Command file exists" test -f "$COMMAND_FILE"

# Test 2: Line count <= 100
echo "--- Line Count ---"
if [ -f "$COMMAND_FILE" ]; then
    LINE_COUNT=$(wc -l < "$COMMAND_FILE")
    assert_less_equal "Line count <= 100" "$LINE_COUNT" 100
else
    echo "  FAIL: Cannot count lines - file missing"
    FAIL=$((FAIL + 1))
fi

# Test 3: Character count <= 12000 (target) and <= 15000 (hard limit)
echo "--- Character Count ---"
if [ -f "$COMMAND_FILE" ]; then
    CHAR_COUNT=$(wc -c < "$COMMAND_FILE")
    assert_less_equal "Character count <= 15000 (hard limit)" "$CHAR_COUNT" 15000
    assert_less_equal "Character count <= 12000 (target)" "$CHAR_COUNT" 12000
else
    echo "  FAIL: Cannot count chars - file missing"
    FAIL=$((FAIL + 1))
fi

# Test 4: Code blocks before Skill() <= 2
echo "--- Code Blocks Before Skill ---"
if [ -f "$COMMAND_FILE" ]; then
    SKILL_LINE=$(grep -n 'Skill(command=' "$COMMAND_FILE" | head -1 | cut -d: -f1)
    if [ -n "$SKILL_LINE" ]; then
        BLOCKS_BEFORE=$(head -n "$SKILL_LINE" "$COMMAND_FILE" | grep -c '^```' || true)
        CODE_BLOCK_COUNT=$((BLOCKS_BEFORE / 2))
        assert_less_equal "Code blocks before Skill() <= 2" "$CODE_BLOCK_COUNT" 2
    else
        echo "  FAIL: No Skill() invocation found"
        FAIL=$((FAIL + 1))
    fi
else
    echo "  FAIL: Cannot check code blocks - file missing"
    FAIL=$((FAIL + 1))
fi

# Test 5: Zero forbidden patterns
echo "--- Forbidden Patterns ---"
if [ -f "$COMMAND_FILE" ]; then
    BASH_COUNT=$(grep -c 'Bash(command=' "$COMMAND_FILE" || true)
    assert_equal "Zero Bash(command= patterns" "$BASH_COUNT" "0"

    TASK_COUNT=$(grep -c 'Task(' "$COMMAND_FILE" || true)
    assert_equal "Zero Task( patterns" "$TASK_COUNT" "0"

    FOR_IN_COUNT=$(grep -c 'FOR.*in ' "$COMMAND_FILE" || true)
    assert_equal "Zero FOR...in patterns" "$FOR_IN_COUNT" "0"
else
    echo "  FAIL: Cannot check patterns - file missing"
    FAIL=$((FAIL + 1))
fi

# Test 6: Invocation syntax unchanged
echo "--- Invocation Syntax ---"
if [ -f "$COMMAND_FILE" ]; then
    assert_true "Has argument-hint with EPIC-NNN" grep -q 'argument-hint:.*EPIC-NNN' "$COMMAND_FILE"
    assert_true "Supports --help flag" grep -q '\-\-help' "$COMMAND_FILE"
else
    echo "  FAIL: Cannot check syntax - file missing"
    FAIL=$((FAIL + 1))
fi

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
