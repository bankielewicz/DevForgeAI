#!/bin/bash
# Test: AC#4 - Session checkpoint detection extracted
# Story: STORY-459
# Generated: 2026-02-20
# Phase: TDD Red (tests MUST fail before implementation)
#
# Validates:
# - resume-detection.md contains "Session Checkpoint Detection" section
# - resume-dev.md does NOT contain checkpoint reading code (CHECKPOINT_FOUND, read_checkpoint)
# - resume-detection.md contains checkpoint-first, fallback-to-DoD behavior

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
echo "  AC#4: Checkpoint Detection Extraction Tests"
echo "  Story: STORY-459"
echo "=========================================="
echo ""

# === Test 1: resume-detection.md exists ===
test -f "$REFERENCE_FILE"
run_test "resume-detection.md exists" $?

# === Test 2: resume-detection.md contains "Session Checkpoint Detection" section ===
if [ -f "$REFERENCE_FILE" ]; then
    grep -q "Session Checkpoint Detection" "$REFERENCE_FILE"
    run_test "resume-detection.md contains 'Session Checkpoint Detection' section" $?
else
    ((TOTAL++)); ((FAILED++))
    echo "  FAIL: resume-detection.md contains 'Session Checkpoint Detection' section (file missing)"
fi

# === Test 3: resume-dev.md does NOT contain CHECKPOINT_FOUND ===
FOUND=$(grep -c 'CHECKPOINT_FOUND' "$COMMAND_FILE" || true)
test "$FOUND" -eq 0
run_test "resume-dev.md does NOT contain 'CHECKPOINT_FOUND' (found: $FOUND)" $?

# === Test 4: resume-dev.md does NOT contain read_checkpoint ===
FOUND=$(grep -c 'read_checkpoint' "$COMMAND_FILE" || true)
test "$FOUND" -eq 0
run_test "resume-dev.md does NOT contain 'read_checkpoint' (found: $FOUND)" $?

# === Test 5: resume-dev.md does NOT contain checkpoint file reading patterns ===
# Checkpoint reading typically involves phase-state.json or checkpoint parsing
FOUND=$(grep -c -E '(checkpoint.*Read\(|Read\(.*checkpoint|phase-state\.json.*checkpoint)' "$COMMAND_FILE" || true)
test "$FOUND" -eq 0
run_test "resume-dev.md does NOT contain checkpoint file reading patterns (found: $FOUND)" $?

# === Test 6: resume-detection.md contains fallback to DoD behavior ===
if [ -f "$REFERENCE_FILE" ]; then
    # Should mention fallback from checkpoint to DoD analysis
    grep -q -i -E '(fallback.*DoD|checkpoint.*DoD|DoD.*fallback)' "$REFERENCE_FILE"
    run_test "resume-detection.md contains checkpoint-to-DoD fallback behavior" $?
else
    ((TOTAL++)); ((FAILED++))
    echo "  FAIL: resume-detection.md contains checkpoint-to-DoD fallback behavior (file missing)"
fi

# === Summary ===
echo ""
echo "=========================================="
echo "  Results: $PASSED passed, $FAILED failed out of $TOTAL tests"
echo "=========================================="
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
