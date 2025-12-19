#!/bin/bash
# STORY-101: Citation Format Standards - Test Suite
# TDD Phase: RED (tests should fail before implementation)
#
# Tests verify:
# - AC#1: Critical Rule #12 in CLAUDE.md
# - AC#2: Framework file citation format
# - AC#3: Memory file citation format
# - AC#4: Code example citation format
# - AC#5: MUST cite categories documented
# - AC#6: SHOULD cite categories documented

set -uo pipefail
# Note: -e removed to allow tests to continue after failures

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
CLAUDE_MD="$PROJECT_ROOT/CLAUDE.md"
CRITICAL_RULES="$PROJECT_ROOT/.claude/rules/core/critical-rules.md"
CITATION_REQ="$PROJECT_ROOT/.claude/rules/core/citation-requirements.md"

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
# AC#1: Critical Rule #12 Documentation
# ============================================
header "AC#1: Critical Rule #12 Documentation"

# Test 1.1: CLAUDE.md has "Summary (12 rules)"
if grep -q "Summary (12 rules)" "$CLAUDE_MD" 2>/dev/null; then
    pass "CLAUDE.md has 'Summary (12 rules)'"
else
    fail "CLAUDE.md missing 'Summary (12 rules)' (still shows 11)"
fi

# Test 1.2: CLAUDE.md lists Rule #12 in summary
if grep -q "^12\. " "$CLAUDE_MD" 2>/dev/null; then
    pass "CLAUDE.md lists Rule #12 in summary"
else
    fail "CLAUDE.md missing Rule #12 entry in summary list"
fi

# Test 1.3: citation-requirements.md file exists
if [[ -f "$CITATION_REQ" ]]; then
    pass "citation-requirements.md file exists"
else
    fail "citation-requirements.md file does not exist"
fi

# Test 1.4: critical-rules.md has Rule #12 section
if grep -q "## 12\." "$CRITICAL_RULES" 2>/dev/null; then
    pass "critical-rules.md has Rule #12 section"
else
    fail "critical-rules.md missing Rule #12 section"
fi

# Test 1.5: Section length 40-80 lines (citation-requirements.md)
if [[ -f "$CITATION_REQ" ]]; then
    LINE_COUNT=$(wc -l < "$CITATION_REQ")
    if [[ $LINE_COUNT -ge 40 && $LINE_COUNT -le 80 ]]; then
        pass "citation-requirements.md is 40-80 lines ($LINE_COUNT lines)"
    else
        fail "citation-requirements.md length outside 40-80 range ($LINE_COUNT lines)"
    fi
else
    fail "Cannot check line count - file does not exist"
fi

# ============================================
# AC#2: Framework File Citation Format
# ============================================
header "AC#2: Framework File Citation Format"

# Test 2.1: Format template documented
if grep -q "Source:.*lines" "$CITATION_REQ" 2>/dev/null; then
    pass "Framework citation format template documented"
else
    fail "Framework citation format template not found"
fi

# Test 2.2: tech-stack.md example provided
if grep -q "tech-stack.md" "$CITATION_REQ" 2>/dev/null; then
    pass "tech-stack.md example provided"
else
    fail "tech-stack.md example not found"
fi

# Test 2.3: Line range limit documented (20 lines for framework)
if grep -qE "(20 lines|≤20)" "$CITATION_REQ" 2>/dev/null; then
    pass "20-line range limit documented for framework files"
else
    fail "20-line range limit not documented"
fi

# ============================================
# AC#3: Memory File Citation Format
# ============================================
header "AC#3: Memory File Citation Format"

# Test 3.1: Section format template documented
if grep -q "Source:.*section" "$CITATION_REQ" 2>/dev/null; then
    pass "Memory citation format template documented"
else
    fail "Memory citation format template not found"
fi

# Test 3.2: Section identifier format explained
if grep -qiE "(section|heading)" "$CITATION_REQ" 2>/dev/null; then
    pass "Section identifier format explained"
else
    fail "Section identifier format not explained"
fi

# Test 3.3: Memory file path example
if grep -qE "\.claude/memory|memory/" "$CITATION_REQ" 2>/dev/null; then
    pass "Memory file path example provided"
else
    fail "Memory file path example not found"
fi

# ============================================
# AC#4: Code Example Citation Format
# ============================================
header "AC#4: Code Example Citation Format"

# Test 4.1: Code citation format documented
if grep -qE "Code.*Citation|code.*citation" "$CITATION_REQ" 2>/dev/null; then
    pass "Code citation format section exists"
else
    fail "Code citation format section not found"
fi

# Test 4.2: 50-line maximum documented
if grep -qE "(50 lines|≤50|50-line)" "$CITATION_REQ" 2>/dev/null; then
    pass "50-line maximum documented for code citations"
else
    fail "50-line maximum not documented"
fi

# ============================================
# AC#5: MUST Citation Categories Documented
# ============================================
header "AC#5: MUST Citation Categories"

# Test 5.1: tech-stack.md MUST cite
if grep -qE "MUST.*tech-stack|tech-stack.*MUST" "$CITATION_REQ" 2>/dev/null; then
    pass "tech-stack.md MUST cite requirement documented"
else
    fail "tech-stack.md MUST cite requirement not documented"
fi

# Test 5.2: architecture-constraints.md MUST cite
if grep -qE "MUST.*architecture-constraints|architecture-constraints.*MUST" "$CITATION_REQ" 2>/dev/null; then
    pass "architecture-constraints.md MUST cite requirement documented"
else
    fail "architecture-constraints.md MUST cite requirement not documented"
fi

# Test 5.3: anti-patterns.md MUST cite
if grep -qE "MUST.*anti-patterns|anti-patterns.*MUST" "$CITATION_REQ" 2>/dev/null; then
    pass "anti-patterns.md MUST cite requirement documented"
else
    fail "anti-patterns.md MUST cite requirement not documented"
fi

# Test 5.4: source-tree.md MUST cite
if grep -qE "MUST.*source-tree|source-tree.*MUST" "$CITATION_REQ" 2>/dev/null; then
    pass "source-tree.md MUST cite requirement documented"
else
    fail "source-tree.md MUST cite requirement not documented"
fi

# ============================================
# AC#6: SHOULD Citation Categories Documented
# ============================================
header "AC#6: SHOULD Citation Categories"

# Test 6.1: coding-standards.md SHOULD cite
if grep -qE "SHOULD.*coding-standards|coding-standards.*SHOULD" "$CITATION_REQ" 2>/dev/null; then
    pass "coding-standards.md SHOULD cite requirement documented"
else
    fail "coding-standards.md SHOULD cite requirement not documented"
fi

# Test 6.2: SKILL.md SHOULD cite
if grep -qiE "SHOULD.*skill|skill.*SHOULD" "$CITATION_REQ" 2>/dev/null; then
    pass "SKILL.md SHOULD cite requirement documented"
else
    fail "SKILL.md SHOULD cite requirement not documented"
fi

# Test 6.3: commands-reference SHOULD cite
if grep -qiE "SHOULD.*command|command.*SHOULD" "$CITATION_REQ" 2>/dev/null; then
    pass "commands-reference SHOULD cite requirement documented"
else
    fail "commands-reference SHOULD cite requirement not documented"
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
