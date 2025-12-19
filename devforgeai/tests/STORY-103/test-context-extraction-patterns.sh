#!/bin/bash
# STORY-103: Context Extraction Pattern - Test Suite
# TDD Phase: RED (tests should fail before implementation)
#
# Tests verify:
# - AC#1: Context Extraction Pattern Documentation
# - AC#2: Context Sanitization Pattern
# - AC#3: Performance Requirements Documentation
# - AC#4: Graceful Degradation Pattern
# - AC#5: Data Model Documentation

set -uo pipefail
# Note: -e removed to allow tests to continue after failures

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
CONTEXT_EXTRACTION="$PROJECT_ROOT/.claude/skills/devforgeai-feedback/references/context-extraction.md"
CONTEXT_SANITIZATION="$PROJECT_ROOT/.claude/skills/devforgeai-feedback/references/context-sanitization.md"

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
# AC#1: Context Extraction Pattern Documentation
# ============================================
header "AC#1: Context Extraction Pattern Documentation"

# Test 1.1: context-extraction.md file exists
if [[ -f "$CONTEXT_EXTRACTION" ]]; then
    pass "context-extraction.md file exists"
else
    fail "context-extraction.md file does not exist"
fi

# Test 1.2: Todo extraction pattern documented (content, status, time)
if grep -qiE "todo.*(content|status|time)|TodoContext" "$CONTEXT_EXTRACTION" 2>/dev/null; then
    pass "Todo extraction pattern documented"
else
    fail "Todo extraction pattern not documented (content, status, time)"
fi

# Test 1.3: Operation status extraction documented (success/failure/partial)
if grep -qiE "(success|failure|partial)" "$CONTEXT_EXTRACTION" 2>/dev/null && \
   grep -qiE "(operation.*status|status.*extraction|determine.*status)" "$CONTEXT_EXTRACTION" 2>/dev/null; then
    pass "Operation status extraction documented (success/failure/partial)"
else
    fail "Operation status extraction not documented"
fi

# Test 1.4: Timing extraction documented (start, end, duration)
if grep -qiE "(start_time|end_time|duration)" "$CONTEXT_EXTRACTION" 2>/dev/null && \
   grep -qiE "(timing|calculate.*time)" "$CONTEXT_EXTRACTION" 2>/dev/null; then
    pass "Timing extraction documented (start, end, duration)"
else
    fail "Timing extraction not documented"
fi

# Test 1.5: Error context extraction documented (message, failed todo)
if grep -qiE "(error.*context|ErrorContext)" "$CONTEXT_EXTRACTION" 2>/dev/null && \
   grep -qiE "(error.*message|failed.*todo|stack.*trace)" "$CONTEXT_EXTRACTION" 2>/dev/null; then
    pass "Error context extraction documented"
else
    fail "Error context extraction not documented"
fi

# ============================================
# AC#2: Context Sanitization Pattern
# ============================================
header "AC#2: Context Sanitization Pattern"

# Test 2.1: context-sanitization.md file exists
if [[ -f "$CONTEXT_SANITIZATION" ]]; then
    pass "context-sanitization.md file exists"
else
    fail "context-sanitization.md file does not exist"
fi

# Test 2.2: Secret removal documented (KEY, SECRET, TOKEN, PASSWORD)
if grep -qiE "KEY|SECRET|TOKEN|PASSWORD" "$CONTEXT_SANITIZATION" 2>/dev/null && \
   grep -qiE "(secret.*removal|remove.*secret|environment.*variable)" "$CONTEXT_SANITIZATION" 2>/dev/null; then
    pass "Secret removal patterns documented (KEY, SECRET, TOKEN, PASSWORD)"
else
    fail "Secret removal patterns not documented"
fi

# Test 2.3: File path credential removal documented
if grep -qiE "(file.*path|credential.*path|path.*credential)" "$CONTEXT_SANITIZATION" 2>/dev/null; then
    pass "File path credential removal documented"
else
    fail "File path credential removal not documented"
fi

# Test 2.4: PII removal documented (email, phone, SSN)
if grep -qiE "(email|phone|SSN)" "$CONTEXT_SANITIZATION" 2>/dev/null && \
   grep -qiE "(PII|personal.*identif)" "$CONTEXT_SANITIZATION" 2>/dev/null; then
    pass "PII removal patterns documented (email, phone, SSN)"
else
    fail "PII removal patterns not documented"
fi

# Test 2.5: Sanitization logging documented
if grep -qiE "(sanitization.*log|log.*sanitization|logging)" "$CONTEXT_SANITIZATION" 2>/dev/null; then
    pass "Sanitization logging documented"
else
    fail "Sanitization logging not documented"
fi

# ============================================
# AC#3: Performance Requirements Documentation
# ============================================
header "AC#3: Performance Requirements Documentation"

# Test 3.1: 200ms target documented
if grep -qE "200\s*ms|200ms" "$CONTEXT_EXTRACTION" 2>/dev/null; then
    pass "200ms extraction target documented"
else
    fail "200ms extraction target not documented"
fi

# Test 3.2: 50KB size limit documented
if grep -qE "50\s*KB|50KB" "$CONTEXT_EXTRACTION" 2>/dev/null; then
    pass "50KB size limit documented"
else
    fail "50KB size limit not documented"
fi

# Test 3.3: Summarization for >100 todos documented (first 50, last 10)
if grep -qiE "(100.*todos|todos.*100|summariz)" "$CONTEXT_EXTRACTION" 2>/dev/null && \
   grep -qiE "(first.*50|last.*10|50.*10)" "$CONTEXT_EXTRACTION" 2>/dev/null; then
    pass "Todo summarization pattern documented (>100 todos, first 50, last 10)"
else
    fail "Todo summarization pattern not documented"
fi

# Test 3.4: Stack trace truncation for >5KB documented
if grep -qE "5\s*KB|5KB" "$CONTEXT_EXTRACTION" 2>/dev/null && \
   grep -qiE "(stack.*trace|truncat)" "$CONTEXT_EXTRACTION" 2>/dev/null; then
    pass "Stack trace truncation documented (>5KB)"
else
    fail "Stack trace truncation not documented"
fi

# ============================================
# AC#4: Graceful Degradation Pattern
# ============================================
header "AC#4: Graceful Degradation Pattern"

# Test 4.1: Partial context return documented
if grep -qiE "(partial.*context|return.*partial)" "$CONTEXT_EXTRACTION" 2>/dev/null; then
    pass "Partial context return documented"
else
    fail "Partial context return not documented"
fi

# Test 4.2: Warning (not error) logging documented
if grep -qiE "(warning|warn)" "$CONTEXT_EXTRACTION" 2>/dev/null && \
   grep -qiE "(not.*error|log)" "$CONTEXT_EXTRACTION" 2>/dev/null; then
    pass "Warning logging (not error) documented"
else
    fail "Warning logging not documented"
fi

# Test 4.3: No-exception guarantee documented
if grep -qiE "(no.*exception|never.*throw|exception|catch)" "$CONTEXT_EXTRACTION" 2>/dev/null; then
    pass "No-exception guarantee documented"
else
    fail "No-exception guarantee not documented"
fi

# Test 4.4: Empty dict fallback documented
if grep -qiE "(empty.*context|empty.*dict|fallback|\{\})" "$CONTEXT_EXTRACTION" 2>/dev/null; then
    pass "Empty context fallback documented"
else
    fail "Empty context fallback not documented"
fi

# ============================================
# AC#5: Data Model Documentation
# ============================================
header "AC#5: Data Model Documentation"

# Test 5.1: OperationContext model documented with required fields
REQUIRED_FIELDS=("operation_id" "operation_type" "story_id" "start_time" "end_time" "duration_seconds" "status" "todos" "error" "phases")
FIELDS_FOUND=0
for field in "${REQUIRED_FIELDS[@]}"; do
    if grep -q "$field" "$CONTEXT_EXTRACTION" 2>/dev/null; then
        ((FIELDS_FOUND++))
    fi
done

if [[ $FIELDS_FOUND -ge 8 ]]; then
    pass "OperationContext model documented ($FIELDS_FOUND/10 fields found)"
else
    fail "OperationContext model incomplete ($FIELDS_FOUND/10 fields found)"
fi

# Test 5.2: TodoContext model documented
if grep -qiE "TodoContext" "$CONTEXT_EXTRACTION" 2>/dev/null && \
   grep -qiE "(content.*status|todo.*model)" "$CONTEXT_EXTRACTION" 2>/dev/null; then
    pass "TodoContext model documented"
else
    fail "TodoContext model not documented"
fi

# Test 5.3: ErrorContext model documented
if grep -qiE "ErrorContext" "$CONTEXT_EXTRACTION" 2>/dev/null && \
   grep -qiE "(message|stack_trace|error_type)" "$CONTEXT_EXTRACTION" 2>/dev/null; then
    pass "ErrorContext model documented"
else
    fail "ErrorContext model not documented"
fi

# ============================================
# File Quality Checks
# ============================================
header "File Quality Checks"

# Test Q.1: context-extraction.md has YAML frontmatter
if grep -q "^---" "$CONTEXT_EXTRACTION" 2>/dev/null; then
    pass "context-extraction.md has YAML frontmatter"
else
    fail "context-extraction.md missing YAML frontmatter"
fi

# Test Q.2: context-sanitization.md has YAML frontmatter
if grep -q "^---" "$CONTEXT_SANITIZATION" 2>/dev/null; then
    pass "context-sanitization.md has YAML frontmatter"
else
    fail "context-sanitization.md missing YAML frontmatter"
fi

# Test Q.3: context-extraction.md within 600 lines
if [[ -f "$CONTEXT_EXTRACTION" ]]; then
    LINE_COUNT=$(wc -l < "$CONTEXT_EXTRACTION")
    if [[ $LINE_COUNT -le 600 ]]; then
        pass "context-extraction.md within 600-line limit ($LINE_COUNT lines)"
    else
        fail "context-extraction.md exceeds 600-line limit ($LINE_COUNT lines)"
    fi
else
    fail "Cannot check line count - file does not exist"
fi

# Test Q.4: context-sanitization.md within 600 lines
if [[ -f "$CONTEXT_SANITIZATION" ]]; then
    LINE_COUNT=$(wc -l < "$CONTEXT_SANITIZATION")
    if [[ $LINE_COUNT -le 600 ]]; then
        pass "context-sanitization.md within 600-line limit ($LINE_COUNT lines)"
    else
        fail "context-sanitization.md exceeds 600-line limit ($LINE_COUNT lines)"
    fi
else
    fail "Cannot check line count - file does not exist"
fi

# ============================================
# Summary
# ============================================
header "Test Summary"
echo "Tests Run: $TESTS_RUN"
echo "Passed: $TESTS_PASSED"
echo "Failed: $TESTS_FAILED"
echo ""

if [[ $TESTS_FAILED -eq 0 ]]; then
    echo -e "${GREEN}ALL TESTS PASSED${NC}"
    exit 0
else
    echo -e "${RED}$TESTS_FAILED TEST(S) FAILED${NC}"
    exit 1
fi
