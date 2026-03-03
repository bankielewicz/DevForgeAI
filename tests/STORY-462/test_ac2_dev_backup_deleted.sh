#!/bin/bash
# Test: AC#2 - dev.backup.md deleted from both trees
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

echo "=== AC#2: dev.backup.md deleted from both trees ==="

OPERATIONAL_BACKUP="$PROJECT_ROOT/src/claude/commands/dev.backup.md"
SRC_BACKUP="$PROJECT_ROOT/src/claude/commands/dev.backup.md"
OPERATIONAL_DEV="$PROJECT_ROOT/src/claude/commands/dev.md"

# --- Test 1: .claude/commands/dev.backup.md does NOT exist ---
[ ! -f "$OPERATIONAL_BACKUP" ]
run_test ".claude/commands/dev.backup.md does NOT exist (deleted)" $?

# --- Test 2: src/claude/commands/dev.backup.md does NOT exist ---
[ ! -f "$SRC_BACKUP" ]
run_test "src/claude/commands/dev.backup.md does NOT exist (deleted)" $?

# --- Test 3: .claude/commands/dev.md still exists (unaffected) ---
[ -f "$OPERATIONAL_DEV" ]
run_test ".claude/commands/dev.md still exists (unaffected)" $?

# --- Summary ---
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
