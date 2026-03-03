#!/bin/bash
# Test: AC#4 - devforgeai-feedback skill extended with triage mode
# Story: STORY-458
# Generated: 2026-02-20
# Expected: FAIL (TDD Red phase - skill extension not yet done)

set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

# === Test Configuration ===
PASSED=0
FAILED=0
TOTAL=0

TRIAGE_WORKFLOW="${PROJECT_ROOT}/src/claude/skills/devforgeai-feedback/references/triage-workflow.md"
SKILL_MD="${PROJECT_ROOT}/src/claude/skills/devforgeai-feedback/SKILL.md"

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

echo "=============================================="
echo "  AC#4: devforgeai-feedback Triage Mode"
echo "  Story: STORY-458"
echo "=============================================="
echo ""

# === Test 1: triage-workflow.md exists ===
test_result=0
if [ -f "$TRIAGE_WORKFLOW" ]; then
    test_result=0
else
    test_result=1
fi
run_test "triage-workflow.md exists" "$test_result"

# === Test 2: Contains all 6 phases ===
# Check for each phase keyword (case insensitive)
PHASE_COUNT=0
if [ -f "$TRIAGE_WORKFLOW" ]; then
    grep -qi 'read queue' "$TRIAGE_WORKFLOW" && ((PHASE_COUNT++)) || true
    grep -qi 'display' "$TRIAGE_WORKFLOW" && ((PHASE_COUNT++)) || true
    grep -qi 'selection' "$TRIAGE_WORKFLOW" && ((PHASE_COUNT++)) || true
    grep -qi 'story creation' "$TRIAGE_WORKFLOW" && ((PHASE_COUNT++)) || true
    grep -qi 'queue update' "$TRIAGE_WORKFLOW" && ((PHASE_COUNT++)) || true
    grep -qi 'summary' "$TRIAGE_WORKFLOW" && ((PHASE_COUNT++)) || true
fi
test_result=0
if [ "$PHASE_COUNT" -eq 6 ]; then
    test_result=0
else
    test_result=1
fi
run_test "Contains all 6 phases (found: ${PHASE_COUNT}/6)" "$test_result"

# === Test 3: SKILL.md <=500 lines ===
if [ -f "$SKILL_MD" ]; then
    SKILL_LINES=$(wc -l < "$SKILL_MD")
    test_result=0
    if [ "$SKILL_LINES" -le 500 ]; then
        test_result=0
    else
        test_result=1
    fi
    run_test "SKILL.md <= 500 lines (actual: ${SKILL_LINES})" "$test_result"
else
    run_test "SKILL.md <= 500 lines (file not found)" 1
fi

# === Test 4: SKILL.md contains triage mode marker ===
test_result=0
if [ -f "$SKILL_MD" ] && grep -qi 'triage' "$SKILL_MD"; then
    test_result=0
else
    test_result=1
fi
run_test "SKILL.md contains triage mode marker" "$test_result"

# === Summary ===
echo ""
echo "----------------------------------------------"
echo "Results: $PASSED passed, $FAILED failed out of $TOTAL tests"
echo "----------------------------------------------"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
