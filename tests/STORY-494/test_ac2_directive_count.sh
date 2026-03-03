#!/bin/bash
# Test: AC#2 - Read directive count unchanged and 1:1 ratio with markers
# Story: STORY-494
# Generated: 2026-02-23

set -euo pipefail

PASSED=0
FAILED=0
TARGET_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-story-creation/SKILL.md"

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        PASSED=$((PASSED + 1))
    else
        echo "  FAIL: $name"
        FAILED=$((FAILED + 1))
    fi
}

echo "=== AC#2: Read Directive Count and 1:1 Ratio ==="
echo ""

# --- Arrange ---
EXPECTED_READ_COUNT=25

# --- Act ---
ACTUAL_READ_COUNT=$(tr -d '\r' < "$TARGET_FILE" | grep -c "Read(file_path=" || true)
ACTUAL_MARKER_COUNT=$(tr -d '\r' < "$TARGET_FILE" | grep -c "FULL READ MANDATORY" || true)

# --- Assert ---

# Test 1: Read(file_path= count equals 25
if [ "$ACTUAL_READ_COUNT" -eq "$EXPECTED_READ_COUNT" ]; then
    run_test "Read(file_path= count equals $EXPECTED_READ_COUNT (found: $ACTUAL_READ_COUNT)" 0
else
    run_test "Read(file_path= count equals $EXPECTED_READ_COUNT (found: $ACTUAL_READ_COUNT)" 1
fi

# Test 2: 1:1 ratio of markers to Read directives
if [ "$ACTUAL_MARKER_COUNT" -eq "$ACTUAL_READ_COUNT" ] && [ "$ACTUAL_MARKER_COUNT" -gt 0 ]; then
    run_test "1:1 ratio of FULL READ MANDATORY markers ($ACTUAL_MARKER_COUNT) to Read directives ($ACTUAL_READ_COUNT)" 0
else
    run_test "1:1 ratio of FULL READ MANDATORY markers ($ACTUAL_MARKER_COUNT) to Read directives ($ACTUAL_READ_COUNT)" 1
fi

# --- Summary ---
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
