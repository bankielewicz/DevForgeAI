#!/bin/bash
# Test: AC#1 - Snapshot section appears BEFORE Validation Checkpoint
# Story: STORY-513
# Generated: 2026-02-28

# === Test Configuration ===
PASSED=0
FAILED=0
TARGET_FILE="src/claude/skills/implementing-stories/phases/phase-02-test-first.md"

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

echo "=== AC#1: Snapshot Section Position ==="

# === Arrange ===
SNAPSHOT_LINE=$(grep -n "### Test Integrity Snapshot" "$TARGET_FILE" | head -1 | cut -d: -f1)
CHECKPOINT_LINE=$(grep -n "## Validation Checkpoint" "$TARGET_FILE" | head -1 | cut -d: -f1)

# === Act & Assert ===

# Test 1: Snapshot section exists
test -n "$SNAPSHOT_LINE"
run_test "Snapshot section exists in file" $?

# Test 2: Validation Checkpoint exists
test -n "$CHECKPOINT_LINE"
run_test "Validation Checkpoint exists in file" $?

# Test 3: Snapshot line number is LESS THAN checkpoint line number
if [ -n "$SNAPSHOT_LINE" ] && [ -n "$CHECKPOINT_LINE" ]; then
    test "$SNAPSHOT_LINE" -lt "$CHECKPOINT_LINE"
    run_test "Snapshot (line $SNAPSHOT_LINE) appears BEFORE Validation Checkpoint (line $CHECKPOINT_LINE)" $?
else
    run_test "Snapshot appears BEFORE Validation Checkpoint (missing section)" 1
fi

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
