#!/bin/bash
# Test: AC#9 - Governance and architecture sections preserved in skill or references
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
echo "  AC#9: Governance Sections Preserved"
echo "  Story: STORY-458"
echo "=============================================="
echo ""

# === Sprint Workflow Governance ===
echo "  --- sprint-command-workflow.md ---"

# Test 1: Contains Feedback Hook section
test_result=0
if [ -f "$SPRINT_WORKFLOW" ] && grep -qi 'feedback hook' "$SPRINT_WORKFLOW"; then
    test_result=0
else
    test_result=1
fi
run_test "Contains Feedback Hook section" "$test_result"

# Test 2: Contains Architecture section
test_result=0
if [ -f "$SPRINT_WORKFLOW" ] && grep -qi 'architecture' "$SPRINT_WORKFLOW"; then
    test_result=0
else
    test_result=1
fi
run_test "Contains Architecture section" "$test_result"

# Test 3: Contains Design Philosophy
test_result=0
if [ -f "$SPRINT_WORKFLOW" ] && grep -qi 'design philosophy' "$SPRINT_WORKFLOW"; then
    test_result=0
else
    test_result=1
fi
run_test "Contains Design Philosophy" "$test_result"

# Test 4: Contains Framework Integration
test_result=0
if [ -f "$SPRINT_WORKFLOW" ] && grep -qi 'framework integration' "$SPRINT_WORKFLOW"; then
    test_result=0
else
    test_result=1
fi
run_test "Contains Framework Integration" "$test_result"

echo ""
echo "  --- triage-workflow.md ---"

# Test 5: Contains data flow documentation
test_result=0
if [ -f "$TRIAGE_WORKFLOW" ] && grep -qi 'data flow' "$TRIAGE_WORKFLOW"; then
    test_result=0
else
    test_result=1
fi
run_test "Contains data flow documentation" "$test_result"

# Test 6: Contains at least 3 reference file paths
REF_COUNT=0
if [ -f "$TRIAGE_WORKFLOW" ]; then
    # Count lines that look like file paths (containing / and .md or .json or .yaml)
    REF_COUNT=$(grep -cE '[a-zA-Z0-9_/-]+\.(md|json|yaml|yml)' "$TRIAGE_WORKFLOW" || true)
fi
test_result=0
if [ "$REF_COUNT" -ge 3 ]; then
    test_result=0
else
    test_result=1
fi
run_test "Contains >= 3 reference file paths (found: ${REF_COUNT})" "$test_result"

# === Summary ===
echo ""
echo "----------------------------------------------"
echo "Results: $PASSED passed, $FAILED failed out of $TOTAL tests"
echo "----------------------------------------------"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
