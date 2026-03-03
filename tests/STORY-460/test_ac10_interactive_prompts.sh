#!/bin/bash
# Test: AC#10 - AskUserQuestion prompts preserved in commands
# Story: STORY-460
# Generated: 2026-02-21
# Expected: FAIL (TDD Red phase - commands not yet refactored)

set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

# === Test Configuration ===
PASSED=0
FAILED=0
TOTAL=0

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

echo "=============================================="
echo "  AC#10: Interactive Prompts Preserved"
echo "  Story: STORY-460"
echo "=============================================="
echo ""

# === qa.md: AskUserQuestion prompts (7 expected) ===
echo "  --- qa.md AskUserQuestion prompts ---"

QA_ASK_COUNT=$(grep -c 'AskUserQuestion' "$CMD_QA" || true)
test_result=0
if [ "$QA_ASK_COUNT" -ge 7 ]; then
    test_result=0
else
    test_result=1
fi
run_test "qa.md: >= 7 AskUserQuestion references (actual: ${QA_ASK_COUNT})" "$test_result"

# qa: story ID validation prompt
test_result=0
if grep -qi 'story.*id\|which.*story\|enter.*story' "$CMD_QA" && grep -q 'AskUserQuestion' "$CMD_QA"; then
    test_result=0
else
    test_result=1
fi
run_test "qa.md: Story ID validation prompt present" "$test_result"

# qa: mode selection / inference
test_result=0
if grep -qi 'mode.*select\|mode.*infer\|Dev Complete\|In Development' "$CMD_QA"; then
    test_result=0
else
    test_result=1
fi
run_test "qa.md: Mode inference from story status (Dev Complete/In Development)" "$test_result"

# === create-ui.md: AskUserQuestion references (7 expected) ===
echo ""
echo "  --- create-ui.md AskUserQuestion prompts ---"

UI_ASK_COUNT=$(grep -c 'AskUserQuestion' "$CMD_UI" || true)
test_result=0
if [ "$UI_ASK_COUNT" -ge 7 ]; then
    test_result=0
else
    test_result=1
fi
run_test "create-ui.md: >= 7 AskUserQuestion references (actual: ${UI_ASK_COUNT})" "$test_result"

# create-ui: placeholder resolution
test_result=0
if grep -qi 'placeholder.*resolut\|resolve.*placeholder' "$CMD_UI"; then
    test_result=0
else
    test_result=1
fi
run_test "create-ui.md: Placeholder resolution flow present" "$test_result"

# === ideate.md: AskUserQuestion prompts (3 expected) ===
echo ""
echo "  --- ideate.md AskUserQuestion prompts ---"

IDEATE_ASK_COUNT=$(grep -c 'AskUserQuestion' "$CMD_IDEATE" || true)
test_result=0
if [ "$IDEATE_ASK_COUNT" -ge 3 ]; then
    test_result=0
else
    test_result=1
fi
run_test "ideate.md: >= 3 AskUserQuestion references (actual: ${IDEATE_ASK_COUNT})" "$test_result"

# ideate: brainstorm resume prompt
test_result=0
if grep -qi 'brainstorm.*resume\|resume.*brainstorm' "$CMD_IDEATE"; then
    test_result=0
else
    test_result=1
fi
run_test "ideate.md: Brainstorm resume prompt present" "$test_result"

# ideate: business idea capture
test_result=0
if grep -qi 'business.*idea\|idea.*capture\|describe.*idea' "$CMD_IDEATE"; then
    test_result=0
else
    test_result=1
fi
run_test "ideate.md: Business idea capture prompt present" "$test_result"

# === Summary ===
echo ""
echo "----------------------------------------------"
echo "Results: $PASSED passed, $FAILED failed out of $TOTAL tests"
echo "----------------------------------------------"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
