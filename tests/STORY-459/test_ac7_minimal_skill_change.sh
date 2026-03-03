#!/bin/bash
# Test: AC#7 - implementing-stories SKILL.md minimal change
# Story: STORY-459
# Generated: 2026-02-20
# Phase: TDD Red (tests MUST fail before implementation)
#
# Validates:
# - resume-detection.md referenced in SKILL.md
# - "Context Isolation Compliance" section in resume-detection.md

set -uo pipefail

# === Test Configuration ===
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SKILL_FILE="${PROJECT_ROOT}/src/claude/skills/implementing-stories/SKILL.md"
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
echo "  AC#7: Minimal SKILL.md Change Tests"
echo "  Story: STORY-459"
echo "=========================================="
echo ""

# --- Pre-condition: SKILL.md exists ---
if [ ! -f "$SKILL_FILE" ]; then
    echo "  FATAL: SKILL.md not found: $SKILL_FILE"
    exit 1
fi

# === Test 1: SKILL.md references resume-detection.md ===
grep -q 'resume-detection' "$SKILL_FILE"
run_test "SKILL.md references 'resume-detection' reference file" $?

# === Test 2: resume-detection.md exists ===
test -f "$REFERENCE_FILE"
run_test "resume-detection.md exists at expected path" $?

# === Test 3: resume-detection.md contains "Context Isolation Compliance" section ===
if [ -f "$REFERENCE_FILE" ]; then
    grep -q "Context Isolation Compliance" "$REFERENCE_FILE"
    run_test "resume-detection.md contains 'Context Isolation Compliance' section" $?
else
    ((TOTAL++)); ((FAILED++))
    echo "  FAIL: resume-detection.md contains 'Context Isolation Compliance' section (file missing)"
fi

# === Test 4: SKILL.md remains under 1000 lines (source-tree constraint) ===
SKILL_LINES=$(wc -l < "$SKILL_FILE")
echo "  [INFO] SKILL.md line count: $SKILL_LINES"
test "$SKILL_LINES" -le 1000
run_test "SKILL.md remains under 1000 lines (actual: $SKILL_LINES)" $?

# === Summary ===
echo ""
echo "=========================================="
echo "  Results: $PASSED passed, $FAILED failed out of $TOTAL tests"
echo "=========================================="
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
