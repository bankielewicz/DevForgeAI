#!/bin/bash
# Test: AC#11 - AskUserQuestion calls reside in commands only, not in skill references
# Story: STORY-458
# Generated: 2026-02-20
# Expected: FAIL (TDD Red phase - reference files do not exist yet)

set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

# === Test Configuration ===
PASSED=0
FAILED=0
TOTAL=0

SPRINT_WORKFLOW="${PROJECT_ROOT}/src/claude/skills/devforgeai-orchestration/references/sprint-command-workflow.md"
TRIAGE_WORKFLOW="${PROJECT_ROOT}/src/claude/skills/devforgeai-feedback/references/triage-workflow.md"

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
echo "  Story: STORY-458"
echo "=============================================="
echo ""

# === Test 1: sprint-command-workflow.md contains ZERO AskUserQuestion ===
if [ -f "$SPRINT_WORKFLOW" ]; then
    ASK_COUNT=$(grep -c 'AskUserQuestion' "$SPRINT_WORKFLOW" || true)
    test_result=0
    if [ "$ASK_COUNT" -eq 0 ]; then
        test_result=0
    else
        test_result=1
    fi
    run_test "sprint-command-workflow.md: ZERO AskUserQuestion calls (actual: ${ASK_COUNT})" "$test_result"
else
    # File does not exist yet - this is a failure because the file should be created
    run_test "sprint-command-workflow.md: file does not exist (must be created)" 1
fi

# === Test 2: triage-workflow.md contains ZERO AskUserQuestion ===
if [ -f "$TRIAGE_WORKFLOW" ]; then
    ASK_COUNT=$(grep -c 'AskUserQuestion' "$TRIAGE_WORKFLOW" || true)
    test_result=0
    if [ "$ASK_COUNT" -eq 0 ]; then
        test_result=0
    else
        test_result=1
    fi
    run_test "triage-workflow.md: ZERO AskUserQuestion calls (actual: ${ASK_COUNT})" "$test_result"
else
    # File does not exist yet - this is a failure because the file should be created
    run_test "triage-workflow.md: file does not exist (must be created)" 1
fi

# === Summary ===
echo ""
echo "----------------------------------------------"
echo "Results: $PASSED passed, $FAILED failed out of $TOTAL tests"
echo "----------------------------------------------"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
