#!/bin/bash
# Test: AC#6 - Backward compatibility preserved
# Story: STORY-459
# Generated: 2026-02-20
# Phase: TDD Red (tests MUST fail before implementation)
#
# Validates:
# - Both manual mode (/resume-dev STORY-057 2) and auto-detect (/resume-dev STORY-057)
#   invocation patterns are described in the refactored command
# - Skill() invocation present with correct context markers

set -uo pipefail

# === Test Configuration ===
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
COMMAND_FILE="${PROJECT_ROOT}/src/claude/commands/resume-dev.md"
REFERENCE_FILE="${PROJECT_ROOT}/src/claude/skills/implementing-stories/references/resume-detection.md"
PASSED=0
FAILED=0
TOTAL=0

run_test() {
    local name="$1"
    local result="$2"
    ((TOTAL++))
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        ((PASSED++))
    else
        echo "  FAIL: $name"
        ((FAILED++))
    fi
}

echo "=========================================="
echo "  AC#6: Backward Compatibility Tests"
echo "  Story: STORY-459"
echo "=========================================="
echo ""

# --- Pre-condition: File exists ---
if [ ! -f "$COMMAND_FILE" ]; then
    echo "  FATAL: Target file not found: $COMMAND_FILE"
    exit 1
fi

# === Test 1: Manual mode syntax documented (STORY-XXX N) ===
grep -q -E '/resume-dev.*STORY-[0-9]+.*[0-9]' "$COMMAND_FILE"
run_test "Manual mode invocation syntax documented (/resume-dev STORY-XXX N)" $?

# === Test 2: Auto-detect mode syntax documented (STORY-XXX without phase) ===
grep -q -E '/resume-dev.*STORY-[0-9]+' "$COMMAND_FILE"
run_test "Auto-detect mode invocation syntax documented (/resume-dev STORY-XXX)" $?

# === Test 3: Skill() invocation present in command ===
grep -q 'Skill(' "$COMMAND_FILE"
run_test "Skill() invocation present in command" $?

# === Test 4: Command is lean (<=120 lines) per AC#1 cross-check ===
LINE_COUNT=$(wc -l < "$COMMAND_FILE")
test "$LINE_COUNT" -le 120
run_test "Command is lean (<=120 lines) enabling backward compat through delegation (actual: $LINE_COUNT)" $?

# === Test 5: resume-detection.md handles both modes ===
if [ -f "$REFERENCE_FILE" ]; then
    # Reference should mention both manual and auto-detect paths
    MANUAL=$(grep -c -i 'manual' "$REFERENCE_FILE" || true)
    AUTO=$(grep -c -i 'auto-detect\|auto.*detect' "$REFERENCE_FILE" || true)
    test "$MANUAL" -ge 1 -a "$AUTO" -ge 1
    run_test "resume-detection.md describes both manual and auto-detect modes" $?
else
    ((TOTAL++)); ((FAILED++))
    echo "  FAIL: resume-detection.md describes both manual and auto-detect modes (file missing)"
fi

# === Summary ===
echo ""
echo "=========================================="
echo "  Results: $PASSED passed, $FAILED failed out of $TOTAL tests"
echo "=========================================="
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
