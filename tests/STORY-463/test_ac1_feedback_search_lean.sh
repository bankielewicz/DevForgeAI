#!/bin/bash
# Test: AC#1 - feedback-search.md is lean (<=120 lines, <=12000 chars, <=4 code blocks before Skill())
# Story: STORY-463
# Generated: 2026-02-21
# TDD Phase: RED - these tests MUST FAIL before refactoring

PASSED=0
FAILED=0
TARGET="src/claude/commands/feedback-search.md"

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

echo "=== AC#1: feedback-search.md Lean File Constraints ==="
echo "Target: $TARGET"
echo ""

# === Test 1: File exists ===
[ -f "$TARGET" ]
run_test "feedback-search.md exists at src/claude/commands/feedback-search.md" $?

# === Test 2: Line count <= 120 ===
if [ -f "$TARGET" ]; then
    LINE_COUNT=$(wc -l < "$TARGET")
    echo "  INFO: Current line count = $LINE_COUNT (must be <= 120)"
    [ "$LINE_COUNT" -le 120 ]
    run_test "Line count <= 120 (actual: $LINE_COUNT)" $?
else
    echo "  SKIP: Line count check (file missing)"
    ((FAILED++))
fi

# === Test 3: Character count <= 12000 ===
if [ -f "$TARGET" ]; then
    CHAR_COUNT=$(wc -c < "$TARGET")
    echo "  INFO: Current char count = $CHAR_COUNT (must be <= 12000)"
    [ "$CHAR_COUNT" -le 12000 ]
    run_test "Character count <= 12000 (actual: $CHAR_COUNT)" $?
else
    echo "  SKIP: Character count check (file missing)"
    ((FAILED++))
fi

# === Test 4: Code block count before Skill() invocation <= 4 ===
# Extract content before first Skill() call, count ``` occurrences (each block = 2)
if [ -f "$TARGET" ]; then
    # Get content before Skill( line
    BEFORE_SKILL=$(sed '/Skill(/q' "$TARGET" | head -n -1)
    # Count triple-backtick markers (pairs = code blocks, so count/2)
    BACKTICK_COUNT=$(echo "$BEFORE_SKILL" | grep -c '^```' || true)
    CODE_BLOCK_COUNT=$((BACKTICK_COUNT / 2))
    echo "  INFO: Code blocks before Skill() = $CODE_BLOCK_COUNT (must be <= 4)"
    [ "$CODE_BLOCK_COUNT" -le 4 ]
    run_test "Code block count before Skill() <= 4 (actual: $CODE_BLOCK_COUNT)" $?
else
    echo "  SKIP: Code block count check (file missing)"
    ((FAILED++))
fi

echo ""
echo "=== Results: $PASSED passed, $FAILED failed ==="
[ $FAILED -eq 0 ] && exit 0 || exit 1
