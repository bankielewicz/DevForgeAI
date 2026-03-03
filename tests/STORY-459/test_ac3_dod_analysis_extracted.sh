#!/bin/bash
# Test: AC#3 - DoD analysis and auto-detect logic extracted
# Story: STORY-459
# Generated: 2026-02-20
# Phase: TDD Red (tests MUST fail before implementation)
#
# Validates:
# - resume-detection.md contains "DoD-Based Resumption Point Detection" section
# - resume-detection.md contains phase determination logic (implementation_unchecked, quality_unchecked)
# - resume-dev.md delegates to skill for DoD analysis (does not contain inline DoD parsing)

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
echo "  AC#3: DoD Analysis Extraction Tests"
echo "  Story: STORY-459"
echo "=========================================="
echo ""

# === Test 1: resume-detection.md exists ===
test -f "$REFERENCE_FILE"
run_test "resume-detection.md exists" $?

# === Test 2: resume-detection.md contains "DoD-Based Resumption Point Detection" section ===
if [ -f "$REFERENCE_FILE" ]; then
    grep -q "DoD-Based Resumption Point Detection" "$REFERENCE_FILE"
    run_test "resume-detection.md contains 'DoD-Based Resumption Point Detection' section" $?
else
    ((TOTAL++)); ((FAILED++))
    echo "  FAIL: resume-detection.md contains 'DoD-Based Resumption Point Detection' section (file missing)"
fi

# === Test 3: resume-detection.md contains implementation_unchecked logic ===
if [ -f "$REFERENCE_FILE" ]; then
    grep -q 'implementation_unchecked' "$REFERENCE_FILE"
    run_test "resume-detection.md contains 'implementation_unchecked' phase determination" $?
else
    ((TOTAL++)); ((FAILED++))
    echo "  FAIL: resume-detection.md contains 'implementation_unchecked' (file missing)"
fi

# === Test 4: resume-detection.md contains quality_unchecked logic ===
if [ -f "$REFERENCE_FILE" ]; then
    grep -q 'quality_unchecked' "$REFERENCE_FILE"
    run_test "resume-detection.md contains 'quality_unchecked' phase determination" $?
else
    ((TOTAL++)); ((FAILED++))
    echo "  FAIL: resume-detection.md contains 'quality_unchecked' (file missing)"
fi

# === Test 5: resume-dev.md does NOT contain inline DoD parsing (DoD section reading) ===
# The original command contains DoD counting logic with patterns like
# implementation_unchecked, quality_unchecked, or DoD item counting
FOUND=$(grep -c -E '(implementation_unchecked|quality_unchecked|count.*DoD|DoD.*count)' "$COMMAND_FILE" || true)
test "$FOUND" -eq 0
run_test "resume-dev.md does NOT contain inline DoD parsing logic (found: $FOUND)" $?

# === Summary ===
echo ""
echo "=========================================="
echo "  Results: $PASSED passed, $FAILED failed out of $TOTAL tests"
echo "=========================================="
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
