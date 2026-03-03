#!/bin/bash
# Test: AC#7 - Skill size compliance after absorption
# Story: STORY-460
# Generated: 2026-02-21
# Expected: FAIL (TDD Red phase - skills not yet modified)

set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

# === Test Configuration ===
PASSED=0
FAILED=0
TOTAL=0

QA_SKILL="${PROJECT_ROOT}/src/claude/skills/devforgeai-qa/SKILL.md"
UI_SKILL="${PROJECT_ROOT}/src/claude/skills/devforgeai-ui-generator/SKILL.md"
REQS_SKILL="${PROJECT_ROOT}/src/claude/skills/discovering-requirements/SKILL.md"

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
echo "  AC#7: Skill Size Compliance"
echo "  Story: STORY-460"
echo "=============================================="
echo ""

# === Test 1: devforgeai-qa SKILL.md <=800 lines ===
if [ -f "$QA_SKILL" ]; then
    QA_LINES=$(wc -l < "$QA_SKILL")
    test_result=0
    if [ "$QA_LINES" -le 800 ]; then
        test_result=0
    else
        test_result=1
    fi
    run_test "devforgeai-qa SKILL.md <= 800 lines (actual: ${QA_LINES})" "$test_result"
else
    run_test "devforgeai-qa SKILL.md exists" 1
fi

# === Test 2: devforgeai-ui-generator SKILL.md <=500 lines ===
if [ -f "$UI_SKILL" ]; then
    UI_LINES=$(wc -l < "$UI_SKILL")
    test_result=0
    if [ "$UI_LINES" -le 500 ]; then
        test_result=0
    else
        test_result=1
    fi
    run_test "devforgeai-ui-generator SKILL.md <= 500 lines (actual: ${UI_LINES})" "$test_result"
else
    run_test "devforgeai-ui-generator SKILL.md exists" 1
fi

# === Test 3: discovering-requirements SKILL.md <=500 lines ===
if [ -f "$REQS_SKILL" ]; then
    REQS_LINES=$(wc -l < "$REQS_SKILL")
    test_result=0
    if [ "$REQS_LINES" -le 500 ]; then
        test_result=0
    else
        test_result=1
    fi
    run_test "discovering-requirements SKILL.md <= 500 lines (actual: ${REQS_LINES})" "$test_result"
else
    run_test "discovering-requirements SKILL.md exists" 1
fi

# === Test 4: All 3 skills under 1000-line maximum ===
ALL_UNDER=0
for skill_file in "$QA_SKILL" "$UI_SKILL" "$REQS_SKILL"; do
    if [ -f "$skill_file" ]; then
        lines=$(wc -l < "$skill_file")
        if [ "$lines" -gt 1000 ]; then
            ALL_UNDER=1
        fi
    else
        ALL_UNDER=1
    fi
done
run_test "All 3 skills under 1000-line maximum" "$ALL_UNDER"

# === Summary ===
echo ""
echo "----------------------------------------------"
echo "Results: $PASSED passed, $FAILED failed out of $TOTAL tests"
echo "----------------------------------------------"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
