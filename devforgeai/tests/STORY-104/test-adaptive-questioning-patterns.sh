#!/bin/bash
# STORY-104: Adaptive Questioning Patterns - Test Suite
# TDD Phase: RED (tests should fail before implementation)
#
# Tests verify:
# - AC#1: Context-Aware Question Templates Documentation
# - AC#2: Template Pre-Population Pattern
# - AC#3: Adaptive Question Selection Pattern
# - AC#4: Context Variables in Prompts
# - AC#5: Graceful Fallback Pattern

set -uo pipefail
# Note: -e removed to allow tests to continue after failures

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
ADAPTIVE_QUESTIONING="$PROJECT_ROOT/.claude/skills/devforgeai-feedback/references/adaptive-questioning.md"
QUESTION_TEMPLATES="$PROJECT_ROOT/.claude/skills/devforgeai-feedback/references/feedback-question-templates.md"

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test helper functions
pass() {
    ((TESTS_PASSED++))
    ((TESTS_RUN++))
    echo -e "${GREEN}PASS${NC}: $1"
}

fail() {
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
    echo -e "${RED}FAIL${NC}: $1"
}

header() {
    echo ""
    echo -e "${YELLOW}=== $1 ===${NC}"
}

# ============================================
# AC#1: Context-Aware Question Templates Documentation
# ============================================
header "AC#1: Context-Aware Question Templates Documentation"

# Test 1.1: adaptive-questioning.md file exists
if [[ -f "$ADAPTIVE_QUESTIONING" ]]; then
    pass "adaptive-questioning.md file exists"
else
    fail "adaptive-questioning.md file does not exist"
fi

# Test 1.2: Operation type templates documented (dev, qa, release)
if grep -qiE "(operation.type|operation_type).*(dev|qa|release)" "$ADAPTIVE_QUESTIONING" 2>/dev/null && \
   grep -qiE "(template|question).*(operation|type)" "$ADAPTIVE_QUESTIONING" 2>/dev/null; then
    pass "Operation type templates documented (dev, qa, release)"
else
    fail "Operation type templates not documented"
fi

# Test 1.3: Todo-referencing templates documented
if grep -qiE "(todo.*count|todo_count|completed.*count|completed_count)" "$ADAPTIVE_QUESTIONING" 2>/dev/null && \
   grep -qiE "(\{todo_count\}|\{completed_count\}|todo.*reference)" "$ADAPTIVE_QUESTIONING" 2>/dev/null; then
    pass "Todo-referencing templates documented"
else
    fail "Todo-referencing templates not documented"
fi

# Test 1.4: Error-referencing templates documented
if grep -qiE "(error.*message|error_message|failed.*todo|failed_todo)" "$ADAPTIVE_QUESTIONING" 2>/dev/null && \
   grep -qiE "(\{error_message\}|\{failed_todo\}|error.*reference)" "$ADAPTIVE_QUESTIONING" 2>/dev/null; then
    pass "Error-referencing templates documented"
else
    fail "Error-referencing templates not documented"
fi

# Test 1.5: Phase duration templates documented
if grep -qiE "(phase.*duration|longest.*phase|longest_phase)" "$ADAPTIVE_QUESTIONING" 2>/dev/null; then
    pass "Phase duration templates documented"
else
    fail "Phase duration templates not documented"
fi

# ============================================
# AC#2: Template Pre-Population Pattern
# ============================================
header "AC#2: Template Pre-Population Pattern"

# Test 2.1: Context metadata inclusion documented
if grep -qiE "(context.*metadata|pre.?popul|metadata.*inclus)" "$ADAPTIVE_QUESTIONING" 2>/dev/null; then
    pass "Context metadata inclusion documented"
else
    fail "Context metadata inclusion not documented"
fi

# Test 2.2: operation_type, duration, status pre-fill documented
if grep -qiE "operation_type" "$ADAPTIVE_QUESTIONING" 2>/dev/null && \
   grep -qiE "duration" "$ADAPTIVE_QUESTIONING" 2>/dev/null && \
   grep -qiE "status" "$ADAPTIVE_QUESTIONING" 2>/dev/null; then
    pass "Pre-fill fields documented (operation_type, duration, status)"
else
    fail "Pre-fill fields not documented"
fi

# Test 2.3: Error message inclusion documented
if grep -qiE "(error.*message.*inclus|includ.*error|error.*context)" "$ADAPTIVE_QUESTIONING" 2>/dev/null; then
    pass "Error message inclusion documented"
else
    fail "Error message inclusion not documented"
fi

# Test 2.4: Longest-running phase identification documented
if grep -qiE "(longest.*phase|phase.*longest|max.*duration.*phase)" "$ADAPTIVE_QUESTIONING" 2>/dev/null; then
    pass "Longest-running phase identification documented"
else
    fail "Longest-running phase identification not documented"
fi

# ============================================
# AC#3: Adaptive Question Selection Pattern
# ============================================
header "AC#3: Adaptive Question Selection Pattern"

# Test 3.1: Success operations question selection documented
if grep -qiE "(success.*question|question.*success|success.*select)" "$ADAPTIVE_QUESTIONING" 2>/dev/null && \
   grep -qiE "(improvement|went.*well|pattern)" "$ADAPTIVE_QUESTIONING" 2>/dev/null; then
    pass "Success operations question selection documented"
else
    fail "Success operations question selection not documented"
fi

# Test 3.2: Failure operations question selection documented
if grep -qiE "(failure.*question|question.*failure|failure.*select)" "$ADAPTIVE_QUESTIONING" 2>/dev/null && \
   grep -qiE "(root.*cause|prevent|block)" "$ADAPTIVE_QUESTIONING" 2>/dev/null; then
    pass "Failure operations question selection documented"
else
    fail "Failure operations question selection not documented"
fi

# Test 3.3: Partial operations question selection documented
if grep -qiE "(partial.*question|question.*partial|partial.*select|partial.*complet)" "$ADAPTIVE_QUESTIONING" 2>/dev/null; then
    pass "Partial operations question selection documented"
else
    fail "Partial operations question selection not documented"
fi

# Test 3.4: Long operations (>10 min) question selection documented
if grep -qiE "(long.*running|long.*operation|>.*10.*min|600.*second|10.*minute)" "$ADAPTIVE_QUESTIONING" 2>/dev/null && \
   grep -qiE "(duration|time.*expect|took)" "$ADAPTIVE_QUESTIONING" 2>/dev/null; then
    pass "Long operations (>10 min) question selection documented"
else
    fail "Long operations question selection not documented"
fi

# ============================================
# AC#4: Context Variables in Prompts
# ============================================
header "AC#4: Context Variables in Prompts"

# Test 4.1: AskUserQuestion variable usage documented
if grep -qiE "(AskUserQuestion|variable.*prompt|prompt.*variable)" "$ADAPTIVE_QUESTIONING" 2>/dev/null; then
    pass "AskUserQuestion variable usage documented"
else
    fail "AskUserQuestion variable usage not documented"
fi

# Test 4.2: Context passing pattern documented
if grep -qiE "(context.*pass|pass.*context|devforgeai-feedback)" "$ADAPTIVE_QUESTIONING" 2>/dev/null; then
    pass "Context passing pattern documented"
else
    fail "Context passing pattern not documented"
fi

# Test 4.3: Variable list documented ({operation_type}, {duration}, {error_message}, {todo_count})
if grep -qE "\{operation_type\}" "$ADAPTIVE_QUESTIONING" 2>/dev/null && \
   grep -qE "\{duration\}" "$ADAPTIVE_QUESTIONING" 2>/dev/null && \
   grep -qE "\{error_message\}" "$ADAPTIVE_QUESTIONING" 2>/dev/null && \
   grep -qE "\{todo_count\}" "$ADAPTIVE_QUESTIONING" 2>/dev/null; then
    pass "Variable list documented ({operation_type}, {duration}, {error_message}, {todo_count})"
else
    fail "Variable list not fully documented"
fi

# ============================================
# AC#5: Graceful Fallback Pattern
# ============================================
header "AC#5: Graceful Fallback Pattern"

# Test 5.1: Generic fallback questions documented
if grep -qiE "(generic.*fallback|fallback.*generic|fallback.*question)" "$ADAPTIVE_QUESTIONING" 2>/dev/null; then
    pass "Generic fallback questions documented"
else
    fail "Generic fallback questions not documented"
fi

# Test 5.2: Partial context handling documented (no errors)
if grep -qiE "(partial.*context|context.*partial|graceful|no.*error)" "$ADAPTIVE_QUESTIONING" 2>/dev/null; then
    pass "Partial context handling documented"
else
    fail "Partial context handling not documented"
fi

# Test 5.3: Context field logging documented
if grep -qiE "(log.*context|context.*log|field.*available|available.*field)" "$ADAPTIVE_QUESTIONING" 2>/dev/null; then
    pass "Context field logging documented"
else
    fail "Context field logging not documented"
fi

# ============================================
# Quality Checks
# ============================================
header "Quality Checks"

# Test Q.1: YAML frontmatter present
if head -5 "$ADAPTIVE_QUESTIONING" 2>/dev/null | grep -q "^---"; then
    pass "YAML frontmatter present"
else
    fail "YAML frontmatter missing"
fi

# Test Q.2: File within 500-line limit
if [[ -f "$ADAPTIVE_QUESTIONING" ]]; then
    LINE_COUNT=$(wc -l < "$ADAPTIVE_QUESTIONING")
    if [[ $LINE_COUNT -le 500 ]]; then
        pass "File within 500-line limit ($LINE_COUNT lines)"
    else
        fail "File exceeds 500-line limit ($LINE_COUNT lines)"
    fi
else
    fail "Cannot check line count - file does not exist"
fi

# Test Q.3: No Python code in document
if ! grep -qE "^(def |class |import |from .* import |if __name__|    def )" "$ADAPTIVE_QUESTIONING" 2>/dev/null; then
    pass "No Python code in document (framework-agnostic)"
else
    fail "Python code detected in document"
fi

# Test Q.4: Context variable section added to feedback-question-templates.md
if grep -qiE "(context.*variable|variable.*support|STORY-104)" "$QUESTION_TEMPLATES" 2>/dev/null; then
    pass "Context variable section added to feedback-question-templates.md"
else
    fail "Context variable section not added to feedback-question-templates.md"
fi

# ============================================
# Summary
# ============================================
echo ""
echo "============================================"
echo -e "Test Summary: ${TESTS_PASSED}/${TESTS_RUN} passed"
if [[ $TESTS_FAILED -eq 0 ]]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}${TESTS_FAILED} tests failed${NC}"
    exit 1
fi
