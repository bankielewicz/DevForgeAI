#!/bin/bash
# Test: AC#11 - AskUserQuestion calls and interactive logic placement per lean orchestration
# Story: STORY-459
# Generated: 2026-02-20
# Phase: TDD Red (tests MUST fail before implementation)
#
# Validates:
# - resume-detection.md contains ZERO AskUserQuestion calls
# - Any user interaction remains in command, not reference file

set -uo pipefail

# === Test Configuration ===
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
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
echo "  AC#11: AskUserQuestion Placement Tests"
echo "  Story: STORY-459"
echo "=========================================="
echo ""

# === Test 1: resume-detection.md exists ===
test -f "$REFERENCE_FILE"
run_test "resume-detection.md exists" $?

# === Test 2: resume-detection.md contains ZERO AskUserQuestion calls ===
if [ -f "$REFERENCE_FILE" ]; then
    ASK_COUNT=$(grep -c 'AskUserQuestion' "$REFERENCE_FILE" || true)
    echo "  [INFO] AskUserQuestion occurrences in resume-detection.md: $ASK_COUNT"
    test "$ASK_COUNT" -eq 0
    run_test "resume-detection.md contains ZERO AskUserQuestion calls (found: $ASK_COUNT)" $?
else
    ((TOTAL++)); ((FAILED++))
    echo "  FAIL: resume-detection.md contains ZERO AskUserQuestion calls (file missing)"
fi

# === Test 3: resume-detection.md contains no interactive prompt patterns ===
if [ -f "$REFERENCE_FILE" ]; then
    # Check for common interactive prompt patterns that should stay in command
    PROMPT_COUNT=$(grep -c -i -E '(AskUser|prompt.*user|user.*confirm|interactive.*prompt)' "$REFERENCE_FILE" || true)
    test "$PROMPT_COUNT" -eq 0
    run_test "resume-detection.md contains no interactive prompt patterns (found: $PROMPT_COUNT)" $?
else
    ((TOTAL++)); ((FAILED++))
    echo "  FAIL: resume-detection.md contains no interactive prompt patterns (file missing)"
fi

# === Summary ===
echo ""
echo "=========================================="
echo "  Results: $PASSED passed, $FAILED failed out of $TOTAL tests"
echo "=========================================="
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
