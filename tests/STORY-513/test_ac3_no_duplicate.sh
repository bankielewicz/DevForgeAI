#!/bin/bash
# Test: AC#3 - No duplicate snapshot section (exactly one occurrence)
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

echo "=== AC#3: No Duplicate Snapshot Section ==="

# === Arrange ===
SNAPSHOT_COUNT=$(grep -c "### Test Integrity Snapshot" "$TARGET_FILE")
CHECKPOINT_LINE=$(grep -n "## Validation Checkpoint" "$TARGET_FILE" | head -1 | cut -d: -f1)

# === Act & Assert ===

# Test 1: Exactly one occurrence of snapshot heading
test "$SNAPSHOT_COUNT" -eq 1
run_test "Exactly 1 occurrence of '### Test Integrity Snapshot' heading (found: $SNAPSHOT_COUNT)" $?

# Test 2: No snapshot content appears AFTER the Validation Checkpoint
if [ -n "$CHECKPOINT_LINE" ]; then
    AFTER_CHECKPOINT=$(tail -n +"$CHECKPOINT_LINE" "$TARGET_FILE")
    SNAPSHOT_AFTER=$(echo "$AFTER_CHECKPOINT" | grep -c "### Test Integrity Snapshot")
    test "$SNAPSHOT_AFTER" -eq 0
    run_test "No snapshot heading after Validation Checkpoint (found: $SNAPSHOT_AFTER)" $?
else
    run_test "No snapshot heading after Validation Checkpoint (checkpoint missing)" 1
fi

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
