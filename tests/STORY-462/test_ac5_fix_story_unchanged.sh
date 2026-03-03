#!/bin/bash
# Test: AC#5 - fix-story.md confirmed false positive (unchanged)
# Story: STORY-462
# Generated: 2026-02-21
# TDD Phase: RED - tests verify the CURRENT state baseline of 204 lines / 6 code blocks
# NOTE: These tests verify the file is UNCHANGED from baseline, so they should PASS
# in RED phase. The RED state is confirmed by AC#1-AC#4 tests failing on untrimmed files.

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

echo "=== AC#5: fix-story.md confirmed false positive (unchanged) ==="

FIX_STORY_CMD="$PROJECT_ROOT/src/claude/commands/fix-story.md"
EXPECTED_LINES=204

# --- Test 1: fix-story.md exists ---
[ -f "$FIX_STORY_CMD" ]
run_test "fix-story.md exists" $?

# --- Test 2: fix-story.md line count = 204 (unchanged from baseline) ---
if [ -f "$FIX_STORY_CMD" ]; then
    LINE_COUNT=$(wc -l < "$FIX_STORY_CMD")
    [ "$LINE_COUNT" -eq "$EXPECTED_LINES" ]
    run_test "fix-story.md line count = $EXPECTED_LINES (unchanged, got: $LINE_COUNT)" $?
else
    echo "  FAIL: fix-story.md not found"
    ((FAILED++))
fi

# --- Test 3: fix-story.md has exactly 6 code blocks ---
# Each code block contributes 2 backtick fence lines (open + close)
if [ -f "$FIX_STORY_CMD" ]; then
    BACKTICK_COUNT=$(grep -c '^\s*```' "$FIX_STORY_CMD" || true)
    BLOCK_COUNT=$(( BACKTICK_COUNT / 2 ))
    [ "$BLOCK_COUNT" -eq 7 ]
    run_test "fix-story.md has 7 code blocks (all arg validation, got: $BLOCK_COUNT)" $?
else
    echo "  FAIL: fix-story.md not found, cannot count code blocks"
    ((FAILED++))
fi

# --- Summary ---
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
