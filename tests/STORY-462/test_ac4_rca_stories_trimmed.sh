#!/bin/bash
# Test: AC#4 - create-stories-from-rca.md trimmed to <=180 lines
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

echo "=== AC#4: create-stories-from-rca.md trimmed to <=180 lines ==="

RCA_CMD="$PROJECT_ROOT/src/claude/commands/create-stories-from-rca.md"

# --- Test 1: create-stories-from-rca.md exists ---
[ -f "$RCA_CMD" ]
run_test "create-stories-from-rca.md exists" $?

# --- Test 2: create-stories-from-rca.md is <=180 lines ---
if [ -f "$RCA_CMD" ]; then
    LINE_COUNT=$(wc -l < "$RCA_CMD")
    [ "$LINE_COUNT" -le 180 ]
    run_test "create-stories-from-rca.md is <=180 lines (current: $LINE_COUNT)" $?
else
    echo "  FAIL: create-stories-from-rca.md not found, cannot check line count"
    ((FAILED++))
fi

# --- Summary ---
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
