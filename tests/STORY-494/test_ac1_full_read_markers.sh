#!/bin/bash
# Test: AC#1 - FULL READ MANDATORY markers present for all Read directives
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

echo "=== AC#1: FULL READ MANDATORY Markers ==="
echo ""

# --- Arrange ---
EXPECTED_MARKER_COUNT=25

# --- Act ---
ACTUAL_MARKER_COUNT=$(tr -d '\r' < "$TARGET_FILE" | grep -c "FULL READ MANDATORY" || true)

# --- Assert ---

# Test 1: Marker count equals 25
if [ "$ACTUAL_MARKER_COUNT" -eq "$EXPECTED_MARKER_COUNT" ]; then
    run_test "FULL READ MANDATORY marker count equals $EXPECTED_MARKER_COUNT (found: $ACTUAL_MARKER_COUNT)" 0
else
    run_test "FULL READ MANDATORY marker count equals $EXPECTED_MARKER_COUNT (found: $ACTUAL_MARKER_COUNT)" 1
fi

# Test 2: Each Read(file_path= directive has an associated FULL READ MANDATORY marker
# Check that every line with Read(file_path= has "FULL READ MANDATORY" on the same line or the immediately preceding line
READ_LINES=$(tr -d '\r' < "$TARGET_FILE" | grep -n "Read(file_path=" | cut -d: -f1)
UNMATCHED=0
UNMATCHED_LINES=""

for line_num in $READ_LINES; do
    prev_line=$((line_num - 1))
    # Check current line for marker
    current_has=$(sed -n "${line_num}p" "$TARGET_FILE" | tr -d '\r' | grep -c "FULL READ MANDATORY" 2>/dev/null || true)
    # Check previous line for marker
    prev_has=$(sed -n "${prev_line}p" "$TARGET_FILE" | tr -d '\r' | grep -c "FULL READ MANDATORY" 2>/dev/null || true)

    if [ "$current_has" -eq 0 ] && [ "$prev_has" -eq 0 ]; then
        ((UNMATCHED++))
        UNMATCHED_LINES="$UNMATCHED_LINES $line_num"
    fi
done

if [ "$UNMATCHED" -eq 0 ]; then
    run_test "Every Read(file_path= has associated FULL READ MANDATORY marker" 0
else
    run_test "Every Read(file_path= has associated FULL READ MANDATORY marker ($UNMATCHED unmatched at lines:$UNMATCHED_LINES)" 1
fi

# --- Summary ---
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
