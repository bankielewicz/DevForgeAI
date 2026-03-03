#!/bin/bash
# Test: AC#8 - Backward-compatible output: error handling sections preserved
# Story: STORY-460
# Generated: 2026-02-21
# Expected: FAIL (TDD Red phase - sections may be lost during refactoring)

set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

# === Test Configuration ===
PASSED=0
FAILED=0
TOTAL=0

CMD_QA="${PROJECT_ROOT}/src/claude/commands/qa.md"
CMD_UI="${PROJECT_ROOT}/src/claude/commands/create-ui.md"
CMD_IDEATE="${PROJECT_ROOT}/src/claude/commands/ideate.md"
QA_SKILL="${PROJECT_ROOT}/src/claude/skills/devforgeai-qa/SKILL.md"
QA_REFS="${PROJECT_ROOT}/src/claude/skills/devforgeai-qa/references"
UI_SKILL="${PROJECT_ROOT}/src/claude/skills/devforgeai-ui-generator/SKILL.md"
UI_REFS="${PROJECT_ROOT}/src/claude/skills/devforgeai-ui-generator/references"
IDEATE_SKILL="${PROJECT_ROOT}/src/claude/skills/discovering-requirements/SKILL.md"
IDEATE_REFS="${PROJECT_ROOT}/src/claude/skills/discovering-requirements/references"

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

# Search in command AND skill AND skill references for a pattern
search_qa_files() {
    local pattern="$1"
    if grep -rqi "$pattern" "$CMD_QA" 2>/dev/null; then return 0; fi
    if grep -rqi "$pattern" "$QA_SKILL" 2>/dev/null; then return 0; fi
    if [ -d "$QA_REFS" ] && grep -rqi "$pattern" "$QA_REFS" 2>/dev/null; then return 0; fi
    return 1
}

search_ui_files() {
    local pattern="$1"
    if grep -rqi "$pattern" "$CMD_UI" 2>/dev/null; then return 0; fi
    if grep -rqi "$pattern" "$UI_SKILL" 2>/dev/null; then return 0; fi
    if [ -d "$UI_REFS" ] && grep -rqi "$pattern" "$UI_REFS" 2>/dev/null; then return 0; fi
    return 1
}

search_ideate_files() {
    local pattern="$1"
    if grep -rqi "$pattern" "$CMD_IDEATE" 2>/dev/null; then return 0; fi
    if grep -rqi "$pattern" "$IDEATE_SKILL" 2>/dev/null; then return 0; fi
    if [ -d "$IDEATE_REFS" ] && grep -rqi "$pattern" "$IDEATE_REFS" 2>/dev/null; then return 0; fi
    return 1
}

echo "=============================================="
echo "  AC#8: Backward-Compatible Output"
echo "  Story: STORY-460"
echo "=============================================="
echo ""

# === QA: 4 error types preserved ===
echo "  --- qa.md Error Types (4 required) ---"

test_result=0
if search_qa_files 'story.*id.*invalid\|invalid.*story.*id'; then test_result=0; else test_result=1; fi
run_test "qa: Error type 1 - Story ID Invalid" "$test_result"

test_result=0
if search_qa_files 'story.*file.*not found\|not found.*story.*file\|story.*not.*exist'; then test_result=0; else test_result=1; fi
run_test "qa: Error type 2 - Story File Not Found" "$test_result"

test_result=0
if search_qa_files 'invalid.*mode\|mode.*invalid\|unrecognized.*mode'; then test_result=0; else test_result=1; fi
run_test "qa: Error type 3 - Invalid Mode" "$test_result"

test_result=0
if search_qa_files 'qa.*skill.*fail\|skill.*fail\|validation.*fail'; then test_result=0; else test_result=1; fi
run_test "qa: Error type 4 - QA Skill Failed" "$test_result"

echo ""
echo "  --- qa.md Sections Preserved ---"

test_result=0
if search_qa_files 'quick reference\|Quick Reference'; then test_result=0; else test_result=1; fi
run_test "qa: Quick Reference section preserved" "$test_result"

test_result=0
if search_qa_files 'error handling\|Error Handling'; then test_result=0; else test_result=1; fi
run_test "qa: Error Handling section preserved" "$test_result"

test_result=0
if search_qa_files 'success criteria\|Success Criteria'; then test_result=0; else test_result=1; fi
run_test "qa: Success Criteria section preserved" "$test_result"

test_result=0
if search_qa_files 'integration.*framework\|Integration.*Framework\|integration with'; then test_result=0; else test_result=1; fi
run_test "qa: Integration with Framework section preserved" "$test_result"

test_result=0
if search_qa_files 'related commands\|Related Commands'; then test_result=0; else test_result=1; fi
run_test "qa: Related Commands section preserved" "$test_result"

test_result=0
if search_qa_files 'performance.*target\|Performance.*Target'; then test_result=0; else test_result=1; fi
run_test "qa: Performance Targets section preserved" "$test_result"

# === create-ui: 5 error types preserved ===
echo ""
echo "  --- create-ui.md Error Types (5 required) ---"

test_result=0
if search_ui_files 'story.*not found\|not found.*story'; then test_result=0; else test_result=1; fi
run_test "create-ui: Error type 1 - Story Not Found" "$test_result"

test_result=0
if search_ui_files 'context.*files.*missing\|missing.*context.*file'; then test_result=0; else test_result=1; fi
run_test "create-ui: Error type 2 - Context Files Missing" "$test_result"

test_result=0
if search_ui_files 'frontend.*stack.*not.*defined\|stack.*not.*defined\|frontend.*not.*defined'; then test_result=0; else test_result=1; fi
run_test "create-ui: Error type 3 - Frontend Stack Not Defined" "$test_result"

test_result=0
if search_ui_files 'ui.*generator.*fail\|skill.*fail\|generator.*fail'; then test_result=0; else test_result=1; fi
run_test "create-ui: Error type 4 - UI Generator Skill Failed" "$test_result"

test_result=0
if search_ui_files 'specification.*validation.*fail\|validation.*fail.*spec'; then test_result=0; else test_result=1; fi
run_test "create-ui: Error type 5 - Specification Validation Failed" "$test_result"

echo ""
echo "  --- create-ui.md Sections Preserved ---"

test_result=0
if search_ui_files 'success criteria\|Success Criteria'; then test_result=0; else test_result=1; fi
run_test "create-ui: Success Criteria section preserved" "$test_result"

test_result=0
if search_ui_files 'token efficiency\|Token Efficiency'; then test_result=0; else test_result=1; fi
run_test "create-ui: Token Efficiency section preserved" "$test_result"

test_result=0
if search_ui_files 'integration point\|Integration Point'; then test_result=0; else test_result=1; fi
run_test "create-ui: Integration Points section preserved" "$test_result"

# === ideate: Error section preserved ===
echo ""
echo "  --- ideate.md Error Handling ---"

test_result=0
if search_ideate_files 'error handling\|Error Handling'; then test_result=0; else test_result=1; fi
run_test "ideate: Error Handling section preserved" "$test_result"

test_result=0
if search_ideate_files 'brainstorm.*detect\|brainstorm.*auto\|auto.*detect.*brainstorm'; then test_result=0; else test_result=1; fi
run_test "ideate: Brainstorm auto-detection UX flow preserved" "$test_result"

# === Summary ===
echo ""
echo "----------------------------------------------"
echo "Results: $PASSED passed, $FAILED failed out of $TOTAL tests"
echo "----------------------------------------------"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
