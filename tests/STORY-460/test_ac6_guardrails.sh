#!/bin/bash
# Test: AC#6 - DO NOT guardrail sections in all three commands
# Story: STORY-460
# Generated: 2026-02-21
# Expected: FAIL (TDD Red phase - guardrail sections not yet added)

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
echo "  AC#6: DO NOT Guardrail Sections"
echo "  Story: STORY-460"
echo "=============================================="
echo ""

# Each command must have a Lean Orchestration Enforcement section with >=4 DO NOT items

# === qa.md: >=4 DO NOT items ===
QA_DONOT_COUNT=$(grep -c 'DO NOT' "$CMD_QA" || true)
test_result=0
if [ "$QA_DONOT_COUNT" -ge 4 ]; then
    test_result=0
else
    test_result=1
fi
run_test "qa.md: >= 4 DO NOT items (actual: ${QA_DONOT_COUNT})" "$test_result"

# === qa.md: Has Lean Orchestration Enforcement section ===
test_result=0
if grep -qi 'Lean Orchestration Enforcement\|## .*DO NOT\|Orchestration Enforcement' "$CMD_QA"; then
    test_result=0
else
    test_result=1
fi
run_test "qa.md: Has Lean Orchestration Enforcement section" "$test_result"

# === create-ui.md: >=4 DO NOT items ===
UI_DONOT_COUNT=$(grep -c 'DO NOT' "$CMD_UI" || true)
test_result=0
if [ "$UI_DONOT_COUNT" -ge 4 ]; then
    test_result=0
else
    test_result=1
fi
run_test "create-ui.md: >= 4 DO NOT items (actual: ${UI_DONOT_COUNT})" "$test_result"

# === create-ui.md: Has Lean Orchestration Enforcement section ===
test_result=0
if grep -qi 'Lean Orchestration Enforcement\|## .*DO NOT\|Orchestration Enforcement' "$CMD_UI"; then
    test_result=0
else
    test_result=1
fi
run_test "create-ui.md: Has Lean Orchestration Enforcement section" "$test_result"

# === ideate.md: >=4 DO NOT items ===
IDEATE_DONOT_COUNT=$(grep -c 'DO NOT' "$CMD_IDEATE" || true)
test_result=0
if [ "$IDEATE_DONOT_COUNT" -ge 4 ]; then
    test_result=0
else
    test_result=1
fi
run_test "ideate.md: >= 4 DO NOT items (actual: ${IDEATE_DONOT_COUNT})" "$test_result"

# === ideate.md: Has Lean Orchestration Enforcement section ===
test_result=0
if grep -qi 'Lean Orchestration Enforcement\|## .*DO NOT\|Orchestration Enforcement' "$CMD_IDEATE"; then
    test_result=0
else
    test_result=1
fi
run_test "ideate.md: Has Lean Orchestration Enforcement section" "$test_result"

# === Summary ===
echo ""
echo "----------------------------------------------"
echo "Results: $PASSED passed, $FAILED failed out of $TOTAL tests"
echo "----------------------------------------------"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
