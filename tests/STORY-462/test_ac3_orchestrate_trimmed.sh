#!/bin/bash
# Test: AC#3 - orchestrate.md trimmed to <=300 lines
# Story: STORY-462
# Generated: 2026-02-21
# TDD Phase: RED (all tests expected to FAIL before implementation)

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

echo "=== AC#3: orchestrate.md trimmed to <=300 lines ==="

ORCHESTRATE_CMD="$PROJECT_ROOT/src/claude/commands/orchestrate.md"

# --- Test 1: orchestrate.md exists ---
[ -f "$ORCHESTRATE_CMD" ]
run_test "orchestrate.md exists" $?

# --- Test 2: orchestrate.md is <=300 lines ---
if [ -f "$ORCHESTRATE_CMD" ]; then
    LINE_COUNT=$(wc -l < "$ORCHESTRATE_CMD")
    [ "$LINE_COUNT" -le 300 ]
    run_test "orchestrate.md is <=300 lines (current: $LINE_COUNT)" $?
else
    echo "  FAIL: orchestrate.md not found, cannot check line count"
    ((FAILED++))
fi

# --- Summary ---
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
