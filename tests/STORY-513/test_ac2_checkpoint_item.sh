#!/bin/bash
# Test: AC#2 - Validation Checkpoint includes snapshot verification item
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

echo "=== AC#2: Checkpoint Includes Snapshot Verification Item ==="

# === Arrange ===
# Extract the Validation Checkpoint section (from ## Validation Checkpoint to next --- or ## heading)
CHECKPOINT_START=$(grep -n "## Validation Checkpoint" "$TARGET_FILE" | head -1 | cut -d: -f1)

# === Act & Assert ===

# Test 1: Validation Checkpoint section exists
test -n "$CHECKPOINT_START"
run_test "Validation Checkpoint section exists" $?

# Test 2: Extract checkpoint section and look for snapshot verification item
# The checkpoint checklist items are between ## Validation Checkpoint and the next ### or ---
if [ -n "$CHECKPOINT_START" ]; then
    # Get lines from checkpoint start to the HALT line (end of checklist)
    CHECKPOINT_SECTION=$(sed -n "${CHECKPOINT_START},$((CHECKPOINT_START + 10))p" "$TARGET_FILE")
    echo "$CHECKPOINT_SECTION" | grep -q "Test integrity snapshot created"
    run_test "Checkpoint contains 'Test integrity snapshot created' item" $?
else
    run_test "Checkpoint contains 'Test integrity snapshot created' item (section missing)" 1
fi

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
