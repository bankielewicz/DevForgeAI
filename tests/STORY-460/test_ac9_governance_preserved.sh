#!/bin/bash
# Test: AC#9 - Governance, integration, and hook sections preserved in skills or references
# Story: STORY-460
# Generated: 2026-02-21
# Expected: FAIL (TDD Red phase - governance sections must survive refactoring)

set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

# === Test Configuration ===
PASSED=0
FAILED=0
TOTAL=0

QA_SKILL="${PROJECT_ROOT}/src/claude/skills/devforgeai-qa/SKILL.md"
QA_REFS="${PROJECT_ROOT}/src/claude/skills/devforgeai-qa/references"
UI_SKILL="${PROJECT_ROOT}/src/claude/skills/devforgeai-ui-generator/SKILL.md"
UI_REFS="${PROJECT_ROOT}/src/claude/skills/devforgeai-ui-generator/references"
IDEATE_SKILL="${PROJECT_ROOT}/src/claude/skills/discovering-requirements/SKILL.md"
IDEATE_REFS="${PROJECT_ROOT}/src/claude/skills/discovering-requirements/references"
CMD_QA="${PROJECT_ROOT}/src/claude/commands/qa.md"
CMD_UI="${PROJECT_ROOT}/src/claude/commands/create-ui.md"
CMD_IDEATE="${PROJECT_ROOT}/src/claude/commands/ideate.md"

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

# Search in skill + references + command for a pattern
search_all() {
    local skill="$1"
    local refs="$2"
    local cmd="$3"
    local pattern="$4"
    if grep -rqi "$pattern" "$skill" 2>/dev/null; then return 0; fi
    if [ -d "$refs" ] && grep -rqi "$pattern" "$refs" 2>/dev/null; then return 0; fi
    if grep -rqi "$pattern" "$cmd" 2>/dev/null; then return 0; fi
    return 1
}

echo "=============================================="
echo "  AC#9: Governance Sections Preserved"
echo "  Story: STORY-460"
echo "=============================================="
echo ""

# === create-ui: Feedback Hook Integration ===
echo "  --- create-ui Governance ---"

test_result=0
if search_all "$UI_SKILL" "$UI_REFS" "$CMD_UI" 'feedback.*hook\|hook.*integration\|invoke.hooks\|check.hooks'; then
    test_result=0
else
    test_result=1
fi
run_test "create-ui: Feedback Hook Integration preserved" "$test_result"

test_result=0
if search_all "$UI_SKILL" "$UI_REFS" "$CMD_UI" 'integration point\|Integration Point\|prerequisite\|invokes\|creates\|enables'; then
    test_result=0
else
    test_result=1
fi
run_test "create-ui: Integration Points section preserved" "$test_result"

# === ideate: Hook Integration and project mode detection ===
echo ""
echo "  --- ideate Governance ---"

test_result=0
if search_all "$IDEATE_SKILL" "$IDEATE_REFS" "$CMD_IDEATE" 'hook.*integration\|invoke.hooks\|devforgeai.validate.*invoke'; then
    test_result=0
else
    test_result=1
fi
run_test "ideate: Hook Integration preserved" "$test_result"

test_result=0
if search_all "$IDEATE_SKILL" "$IDEATE_REFS" "$CMD_IDEATE" 'greenfield\|brownfield\|brainstorm.resume\|project.*mode.*detect'; then
    test_result=0
else
    test_result=1
fi
run_test "ideate: Project mode detection decision tree preserved" "$test_result"

# === qa: Integration with Framework ===
echo ""
echo "  --- qa Governance ---"

test_result=0
if search_all "$QA_SKILL" "$QA_REFS" "$CMD_QA" 'invoked.by\|invoked by'; then
    test_result=0
else
    test_result=1
fi
run_test "qa: Integration 'invoked by' section preserved" "$test_result"

test_result=0
if search_all "$QA_SKILL" "$QA_REFS" "$CMD_QA" 'quality.*gate\|Quality.*Gate'; then
    test_result=0
else
    test_result=1
fi
run_test "qa: Quality gates section preserved" "$test_result"

test_result=0
if search_all "$QA_SKILL" "$QA_REFS" "$CMD_QA" 'result.*handling\|Result.*Handling\|light.*deep\|deep.*light'; then
    test_result=0
else
    test_result=1
fi
run_test "qa: Result handling (light/deep modes) preserved" "$test_result"

# === Summary ===
echo ""
echo "----------------------------------------------"
echo "Results: $PASSED passed, $FAILED failed out of $TOTAL tests"
echo "----------------------------------------------"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
