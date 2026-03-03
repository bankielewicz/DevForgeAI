#!/bin/bash
# Test: AC#3 - Verification step positioned AFTER snapshot creation, BEFORE Validation Checkpoint
# Story: STORY-514
# Generated: 2026-02-28

# === Test Configuration ===
PASSED=0
FAILED=0
TARGET_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/skills/implementing-stories/phases/phase-02-test-first.md"

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

echo "=== AC#3: Verification Step Positioning ==="

# === Test 1: Glob check appears AFTER "Execute snapshot creation" line ===
SNAPSHOT_LINE=$(grep -n 'Execute snapshot creation per the reference' "$TARGET_FILE" | head -1 | cut -d: -f1)
GLOB_LINE=$(grep -n 'Glob.*red-phase-checksums\.json' "$TARGET_FILE" | head -1 | cut -d: -f1)
if [ -n "$SNAPSHOT_LINE" ] && [ -n "$GLOB_LINE" ] && [ "$GLOB_LINE" -gt "$SNAPSHOT_LINE" ]; then
    run_test "Glob verification appears AFTER snapshot creation instruction" 0
else
    run_test "Glob verification appears AFTER snapshot creation instruction" 1
fi

# === Test 2: Glob check appears BEFORE "Validation Checkpoint" heading ===
CHECKPOINT_LINE=$(grep -n '## Validation Checkpoint' "$TARGET_FILE" | head -1 | cut -d: -f1)
if [ -n "$GLOB_LINE" ] && [ -n "$CHECKPOINT_LINE" ] && [ "$GLOB_LINE" -lt "$CHECKPOINT_LINE" ]; then
    run_test "Glob verification appears BEFORE Validation Checkpoint heading" 0
else
    run_test "Glob verification appears BEFORE Validation Checkpoint heading" 1
fi

# === Test 3: Sequence order is Create -> Verify -> Checkpoint ===
if [ -n "$SNAPSHOT_LINE" ] && [ -n "$GLOB_LINE" ] && [ -n "$CHECKPOINT_LINE" ] && \
   [ "$SNAPSHOT_LINE" -lt "$GLOB_LINE" ] && [ "$GLOB_LINE" -lt "$CHECKPOINT_LINE" ]; then
    run_test "Correct sequence: Create -> Verify -> Checkpoint" 0
else
    run_test "Correct sequence: Create -> Verify -> Checkpoint" 1
fi

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
