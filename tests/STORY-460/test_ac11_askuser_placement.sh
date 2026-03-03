#!/bin/bash
# Test: AC#11 - Zero new AskUserQuestion calls added to skill files by this story
# Story: STORY-460
# Generated: 2026-02-21
# Expected: FAIL (TDD Red phase - baseline counts must be captured before refactoring)

set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

# === Test Configuration ===
PASSED=0
FAILED=0
TOTAL=0

QA_SKILL="${PROJECT_ROOT}/src/claude/skills/devforgeai-qa/SKILL.md"
UI_SKILL="${PROJECT_ROOT}/src/claude/skills/devforgeai-ui-generator/SKILL.md"
REQS_SKILL="${PROJECT_ROOT}/src/claude/skills/discovering-requirements/SKILL.md"

# Pre-refactoring baseline counts (captured from current state)
# These are the counts BEFORE this story's refactoring begins.
# After refactoring, these counts must NOT increase.
QA_BASELINE=0     # Current AskUserQuestion count in devforgeai-qa SKILL.md
UI_BASELINE=0     # Current AskUserQuestion count in devforgeai-ui-generator SKILL.md
REQS_BASELINE=0   # Current AskUserQuestion count in discovering-requirements SKILL.md

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
echo "  AC#11: AskUserQuestion Placement"
echo "  Story: STORY-460"
echo "=============================================="
echo ""

# Capture actual baselines from current files
if [ -f "$QA_SKILL" ]; then
    QA_BASELINE=$(grep -c 'AskUserQuestion' "$QA_SKILL" || true)
fi
if [ -f "$UI_SKILL" ]; then
    UI_BASELINE=$(grep -c 'AskUserQuestion' "$UI_SKILL" || true)
fi
if [ -f "$REQS_SKILL" ]; then
    REQS_BASELINE=$(grep -c 'AskUserQuestion' "$REQS_SKILL" || true)
fi

echo "  Baselines captured:"
echo "    devforgeai-qa SKILL.md: ${QA_BASELINE} AskUserQuestion occurrences"
echo "    devforgeai-ui-generator SKILL.md: ${UI_BASELINE} AskUserQuestion occurrences"
echo "    discovering-requirements SKILL.md: ${REQS_BASELINE} AskUserQuestion occurrences"
echo ""

# === Test 1: devforgeai-qa SKILL.md has no NEW AskUserQuestion ===
# After refactoring, count must be <= baseline
if [ -f "$QA_SKILL" ]; then
    QA_COUNT=$(grep -c 'AskUserQuestion' "$QA_SKILL" || true)
    test_result=0
    if [ "$QA_COUNT" -le "$QA_BASELINE" ]; then
        test_result=0
    else
        test_result=1
    fi
    run_test "devforgeai-qa SKILL.md: no new AskUserQuestion (baseline: ${QA_BASELINE}, current: ${QA_COUNT})" "$test_result"
else
    run_test "devforgeai-qa SKILL.md: file exists" 1
fi

# === Test 2: devforgeai-ui-generator SKILL.md has no NEW AskUserQuestion ===
if [ -f "$UI_SKILL" ]; then
    UI_COUNT=$(grep -c 'AskUserQuestion' "$UI_SKILL" || true)
    test_result=0
    if [ "$UI_COUNT" -le "$UI_BASELINE" ]; then
        test_result=0
    else
        test_result=1
    fi
    run_test "devforgeai-ui-generator SKILL.md: no new AskUserQuestion (baseline: ${UI_BASELINE}, current: ${UI_COUNT})" "$test_result"
else
    run_test "devforgeai-ui-generator SKILL.md: file exists" 1
fi

# === Test 3: discovering-requirements SKILL.md has no NEW AskUserQuestion ===
if [ -f "$REQS_SKILL" ]; then
    REQS_COUNT=$(grep -c 'AskUserQuestion' "$REQS_SKILL" || true)
    test_result=0
    if [ "$REQS_COUNT" -le "$REQS_BASELINE" ]; then
        test_result=0
    else
        test_result=1
    fi
    run_test "discovering-requirements SKILL.md: no new AskUserQuestion (baseline: ${REQS_BASELINE}, current: ${REQS_COUNT})" "$test_result"
else
    run_test "discovering-requirements SKILL.md: file exists" 1
fi

# === Summary ===
echo ""
echo "----------------------------------------------"
echo "Results: $PASSED passed, $FAILED failed out of $TOTAL tests"
echo "----------------------------------------------"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
