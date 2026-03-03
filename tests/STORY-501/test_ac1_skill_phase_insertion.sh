#!/bin/bash
# Test: AC#1 - New phase executes between Phase 1 and Phase 2 in SKILL.md
# Story: STORY-501
# Generated: 2026-02-27

# === Test Configuration ===
PASSED=0
FAILED=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SKILL_FILE="${PROJECT_ROOT}/src/claude/skills/devforgeai-qa/SKILL.md"
REF_FILE="${PROJECT_ROOT}/src/claude/skills/devforgeai-qa/references/diff-regression-detection.md"

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

echo "=== AC#1: New Phase Between Phase 1 and Phase 2 ==="

# === Test 1: SKILL.md contains diff regression phase section ===
grep -q -i "diff.*regression" "$SKILL_FILE" 2>/dev/null
run_test "SKILL.md contains diff regression phase section" $?

# === Test 2: Phase references diff-regression-detection.md ===
grep -q "diff-regression-detection.md" "$SKILL_FILE" 2>/dev/null
run_test "Phase references diff-regression-detection.md" $?

# === Test 3: Phase appears after Phase 1 content ===
# Verify the diff regression phase is positioned between Phase 1 and Phase 2
# by checking that line number of diff regression is between Phase 1 and Phase 2
PHASE1_LINE=$(grep -n "^## Phase 1:" "$SKILL_FILE" 2>/dev/null | head -1 | cut -d: -f1)
DIFF_LINE=$(grep -n -i "diff.*regression" "$SKILL_FILE" 2>/dev/null | head -1 | cut -d: -f1)
PHASE2_LINE=$(grep -n "^## Phase 2:" "$SKILL_FILE" 2>/dev/null | head -1 | cut -d: -f1)

if [ -n "$PHASE1_LINE" ] && [ -n "$DIFF_LINE" ] && [ -n "$PHASE2_LINE" ]; then
    if [ "$DIFF_LINE" -gt "$PHASE1_LINE" ] && [ "$DIFF_LINE" -lt "$PHASE2_LINE" ]; then
        run_test "Diff regression phase positioned between Phase 1 and Phase 2" 0
    else
        run_test "Diff regression phase positioned between Phase 1 and Phase 2" 1
    fi
else
    run_test "Diff regression phase positioned between Phase 1 and Phase 2" 1
fi

# === Test 4: Phase excludes test files in diff regression context ===
# Must find exclusion patterns specifically in the diff regression section
grep -i -A 20 "diff.*regression" "$SKILL_FILE" 2>/dev/null | grep -q "exclu.*test\|test.*exclu\|tests/.*exclude\|skip.*test"
run_test "Diff regression phase documents test file exclusions" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
