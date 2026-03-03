#!/bin/bash
# Test: AC#3 - No existing content modified (only marker additions)
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

echo "=== AC#3: No Existing Content Modified ==="
echo ""

# --- Arrange ---
EXPECTED_READ_COUNT=25
EXPECTED_MARKER_COUNT=25

# --- Act ---
ACTUAL_READ_COUNT=$(tr -d '\r' < "$TARGET_FILE" | grep -c "Read(file_path=" || true)
ACTUAL_MARKER_COUNT=$(tr -d '\r' < "$TARGET_FILE" | grep -c "FULL READ MANDATORY" || true)
EMPTY_READS=$(tr -d '\r' < "$TARGET_FILE" | grep "Read(file_path=" | grep -c 'Read(file_path="")' || true)

# --- Assert ---

# Test 1: Read directive count preserved at 25
if [ "$ACTUAL_READ_COUNT" -eq "$EXPECTED_READ_COUNT" ]; then
    run_test "Read directive count preserved at $EXPECTED_READ_COUNT (found: $ACTUAL_READ_COUNT)" 0
else
    run_test "Read directive count preserved at $EXPECTED_READ_COUNT (found: $ACTUAL_READ_COUNT)" 1
fi

# Test 2: All markers present (25)
if [ "$ACTUAL_MARKER_COUNT" -eq "$EXPECTED_MARKER_COUNT" ]; then
    run_test "All $EXPECTED_MARKER_COUNT FULL READ MANDATORY markers present (found: $ACTUAL_MARKER_COUNT)" 0
else
    run_test "All $EXPECTED_MARKER_COUNT FULL READ MANDATORY markers present (found: $ACTUAL_MARKER_COUNT)" 1
fi

# Test 3: No Read directives have empty file paths
if [ "$EMPTY_READS" -eq 0 ]; then
    run_test "No Read directives have empty file paths" 0
else
    run_test "No Read directives have empty file paths ($EMPTY_READS found empty)" 1
fi

# Test 4: No lines containing ONLY "FULL READ MANDATORY" without context
BARE_MARKERS=$(tr -d '\r' < "$TARGET_FILE" | grep -c "^FULL READ MANDATORY$" || true)
if [ "$BARE_MARKERS" -eq 0 ]; then
    run_test "No bare FULL READ MANDATORY markers (all have context/formatting)" 0
else
    run_test "No bare FULL READ MANDATORY markers (all have context/formatting) - found $BARE_MARKERS bare" 1
fi

# --- Summary ---
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
