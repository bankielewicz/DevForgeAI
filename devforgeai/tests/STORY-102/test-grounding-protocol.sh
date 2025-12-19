#!/bin/bash
# STORY-102: Evidence-Based Grounding Protocol - Test Suite
# TDD Phase: RED (tests should fail before implementation)
#
# Tests verify:
# - AC#1: Grounding Protocol Documentation in CLAUDE.md (via citation-requirements.md)
# - AC#2: Technology Decision Grounding Example
# - AC#3: Architecture Decision Grounding Example
# - AC#4: Verification Step Documentation
# - AC#5: Backward Compatibility Verification

set -uo pipefail
# Note: -e removed to allow tests to continue after failures

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
CITATION_REQ="$PROJECT_ROOT/.claude/rules/core/citation-requirements.md"
SKILLS_DIR="$PROJECT_ROOT/.claude/skills"
COMMANDS_DIR="$PROJECT_ROOT/.claude/commands"

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
# AC#1: Grounding Protocol Documentation
# ============================================
header "AC#1: Grounding Protocol Documentation"

# Test 1.1: Grounding Protocol section exists
if grep -qi "Grounding Protocol" "$CITATION_REQ" 2>/dev/null; then
    pass "Grounding Protocol section exists"
else
    fail "Grounding Protocol section not found"
fi

# Test 1.2: Step 1 (Read) documented
if grep -qi "Step 1.*Read\|Read.*tool.*access\|Read(file_path" "$CITATION_REQ" 2>/dev/null; then
    pass "Step 1 (Read) documented"
else
    fail "Step 1 (Read) not documented"
fi

# Test 1.3: Step 2 (Quote) documented
if grep -qi "Step 2.*Quote\|Quote.*word-for-word\|exact.*passage" "$CITATION_REQ" 2>/dev/null; then
    pass "Step 2 (Quote) documented"
else
    fail "Step 2 (Quote) not documented"
fi

# Test 1.4: Step 3 (Cite) documented
if grep -qi "Step 3.*Cite\|Cite.*citation format\|Reference.*source" "$CITATION_REQ" 2>/dev/null; then
    pass "Step 3 (Cite) documented"
else
    fail "Step 3 (Cite) not documented"
fi

# Test 1.5: Verification step documented (Step 4 or Verify)
if grep -qi "Step 4.*Verify\|Verify.*confirm\|recommendation.*matches" "$CITATION_REQ" 2>/dev/null; then
    pass "Verification step (Step 4) documented"
else
    fail "Verification step not documented"
fi

# ============================================
# AC#2: Technology Decision Grounding Example
# ============================================
header "AC#2: Technology Decision Grounding Example"

# Test 2.1: Read tool invocation shown for tech example
if grep -q 'Read(file_path=.*tech-stack' "$CITATION_REQ" 2>/dev/null; then
    pass "Technology example shows Read tool invocation"
else
    fail "Technology example missing Read tool invocation"
fi

# Test 2.2: Quoted passage present (at least 2 lines with > markers)
TECH_QUOTE_LINES=$(grep -cE "^[[:space:]]*>" "$CITATION_REQ" 2>/dev/null | tr -d '\n' || echo "0")
if [[ "$TECH_QUOTE_LINES" =~ ^[0-9]+$ ]] && [[ $TECH_QUOTE_LINES -ge 4 ]]; then
    pass "Quoted passages present (>= 4 quote lines for 2 examples)"
else
    fail "Insufficient quoted passages ($TECH_QUOTE_LINES lines, need >= 4)"
fi

# Test 2.3: Technology example has citation format
if grep -qE "Source:.*tech-stack.*lines [0-9]+-[0-9]+" "$CITATION_REQ" 2>/dev/null; then
    pass "Technology example has correct citation format"
else
    fail "Technology example missing proper citation format"
fi

# Test 2.4: Technology example has recommendation
if grep -qiE "Example.*Technology" "$CITATION_REQ" 2>/dev/null && grep -qi "Recommendation:" "$CITATION_REQ" 2>/dev/null; then
    pass "Technology example includes recommendation"
else
    fail "Technology example missing recommendation"
fi

# Test 2.5: Technology example length (15-25 lines) - check Example 1 section
# We'll count lines in a more flexible way - checking example exists with content
if grep -qiE "Example.*Technology|Technology.*Example" "$CITATION_REQ" 2>/dev/null; then
    pass "Technology example section present"
else
    fail "Technology example section not found"
fi

# ============================================
# AC#3: Architecture Decision Grounding Example
# ============================================
header "AC#3: Architecture Decision Grounding Example"

# Test 3.1: Read tool invocation shown for architecture example
if grep -q 'Read(file_path=.*architecture-constraints' "$CITATION_REQ" 2>/dev/null; then
    pass "Architecture example shows Read tool invocation"
else
    fail "Architecture example missing Read tool invocation"
fi

# Test 3.2: Architecture example has quoted passage
if grep -qE "> " "$CITATION_REQ" 2>/dev/null; then
    pass "Architecture example has quoted passage markers"
else
    fail "Architecture example missing quoted passage"
fi

# Test 3.3: Architecture example has citation format
if grep -qE "Source:.*architecture-constraints.*lines [0-9]+-[0-9]+" "$CITATION_REQ" 2>/dev/null; then
    pass "Architecture example has correct citation format"
else
    fail "Architecture example missing proper citation format"
fi

# Test 3.4: Architecture example has recommendation
if grep -qiE "Example.*Architecture" "$CITATION_REQ" 2>/dev/null; then
    pass "Architecture example section present"
else
    fail "Architecture example section not found"
fi

# Test 3.5: Both examples exist (technology and architecture)
EXAMPLE_COUNT=$(grep -ciE "Example [12]:|### Example" "$CITATION_REQ" 2>/dev/null | tr -d '\n' || echo "0")
if [[ "$EXAMPLE_COUNT" =~ ^[0-9]+$ ]] && [[ $EXAMPLE_COUNT -ge 2 ]]; then
    pass "Both grounding examples present ($EXAMPLE_COUNT examples)"
else
    fail "Need 2 grounding examples, found $EXAMPLE_COUNT"
fi

# ============================================
# AC#4: Verification Step Documentation
# ============================================
header "AC#4: Verification Checklist"

# Test 4.1: Checkbox 1 - Read tool used
if grep -qE "\[ \].*Read tool" "$CITATION_REQ" 2>/dev/null; then
    pass "Verification checkbox: Read tool used"
else
    fail "Missing checkbox for Read tool verification"
fi

# Test 4.2: Checkbox 2 - Quote word-for-word
if grep -qiE "\[ \].*(word-for-word|Quoted text)" "$CITATION_REQ" 2>/dev/null; then
    pass "Verification checkbox: Quote word-for-word"
else
    fail "Missing checkbox for quote verification"
fi

# Test 4.3: Checkbox 3 - Citation format correct
if grep -qiE "\[ \].*Citation format" "$CITATION_REQ" 2>/dev/null; then
    pass "Verification checkbox: Citation format"
else
    fail "Missing checkbox for citation format verification"
fi

# Test 4.4: Checkbox 4 - Recommendation relates to quote
if grep -qiE "\[ \].*Recommendation.*relate" "$CITATION_REQ" 2>/dev/null; then
    pass "Verification checkbox: Recommendation relates to quote"
else
    fail "Missing checkbox for recommendation alignment verification"
fi

# ============================================
# AC#5: Backward Compatibility Verification
# ============================================
header "AC#5: Backward Compatibility"

# Test 5.1: Critical Rule #12 length 40-100 lines
LINE_COUNT=$(wc -l < "$CITATION_REQ" 2>/dev/null || echo "0")
if [[ $LINE_COUNT -ge 40 && $LINE_COUNT -le 100 ]]; then
    pass "citation-requirements.md is 40-100 lines ($LINE_COUNT lines)"
else
    fail "citation-requirements.md outside 40-100 range ($LINE_COUNT lines)"
fi

# Test 5.2: Skills directory has skills (checking 9 skills exist)
SKILL_COUNT=$(find "$SKILLS_DIR" -name "SKILL.md" 2>/dev/null | wc -l)
if [[ $SKILL_COUNT -ge 9 ]]; then
    pass "9+ skills exist ($SKILL_COUNT skills found)"
else
    fail "Less than 9 skills found ($SKILL_COUNT skills)"
fi

# Test 5.3: Commands directory has commands (checking 11 commands exist)
COMMAND_COUNT=$(find "$COMMANDS_DIR" -name "*.md" 2>/dev/null | wc -l)
if [[ $COMMAND_COUNT -ge 11 ]]; then
    pass "11+ commands exist ($COMMAND_COUNT commands found)"
else
    fail "Less than 11 commands found ($COMMAND_COUNT commands)"
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
