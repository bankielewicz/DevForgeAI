#!/bin/bash
# Test: AC#3 - devforgeai-orchestration skill extended with sprint planning logic
# Story: STORY-458
# Generated: 2026-02-20
# Expected: FAIL (TDD Red phase - skill extension not yet done)

set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

# === Test Configuration ===
PASSED=0
FAILED=0
TOTAL=0

SPRINT_WORKFLOW="${PROJECT_ROOT}/src/claude/skills/devforgeai-orchestration/references/sprint-command-workflow.md"
SKILL_MD="${PROJECT_ROOT}/src/claude/skills/devforgeai-orchestration/SKILL.md"

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
echo "  AC#3: devforgeai-orchestration Extended"
echo "  Story: STORY-458"
echo "=============================================="
echo ""

# === Test 1: sprint-command-workflow.md exists ===
test_result=0
if [ -f "$SPRINT_WORKFLOW" ]; then
    test_result=0
else
    test_result=1
fi
run_test "sprint-command-workflow.md exists" "$test_result"

# === Test 2: Contains epic discovery section ===
test_result=0
if [ -f "$SPRINT_WORKFLOW" ] && grep -qi 'epic discovery' "$SPRINT_WORKFLOW"; then
    test_result=0
else
    test_result=1
fi
run_test "Contains epic discovery section" "$test_result"

# === Test 3: Contains story filtering section ===
test_result=0
if [ -f "$SPRINT_WORKFLOW" ] && grep -qi 'story filter' "$SPRINT_WORKFLOW"; then
    test_result=0
else
    test_result=1
fi
run_test "Contains story filtering section" "$test_result"

# === Test 4: Contains capacity validation section ===
test_result=0
if [ -f "$SPRINT_WORKFLOW" ] && grep -qi 'capacity' "$SPRINT_WORKFLOW"; then
    test_result=0
else
    test_result=1
fi
run_test "Contains capacity validation section" "$test_result"

# === Test 5: SKILL.md <=500 lines ===
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

# === Test 6: SKILL.md contains sprint mode routing ===
test_result=0
if [ -f "$SKILL_MD" ] && grep -qi 'plan-sprint\|sprint.*mode\|sprint.*context' "$SKILL_MD"; then
    test_result=0
else
    test_result=1
fi
run_test "SKILL.md contains sprint mode routing" "$test_result"

# === Summary ===
echo ""
echo "----------------------------------------------"
echo "Results: $PASSED passed, $FAILED failed out of $TOTAL tests"
echo "----------------------------------------------"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
