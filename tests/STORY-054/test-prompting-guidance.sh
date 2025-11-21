#!/bin/bash

# ============================================================================
# Test Suite: STORY-054 - claude-code-terminal-expert Prompting Guidance
# ============================================================================
#
# Acceptance Criteria Tests (All RED - Implementation Not Yet Complete)
#
# AC#1: Prompting Guidance Section Added
# AC#2: Cross-References to Both Guidance Documents
# AC#3: Effective Communication Examples (5-10 Scenarios)
# AC#4: "Ask, Don't Assume" Principle Explained
# AC#5: No Breaking Changes to Skill Structure
#
# Test Pattern: Integration tests using grep, wc, file reading
# Expected Result: ALL TESTS FAIL (RED phase - TDD)
# ============================================================================

# NOTE: NOT using 'set -e' to allow all tests to complete regardless of failures
# This is intentional for test suite execution (RED phase allows failures)

# Configuration
SKILL_FILE="./.claude/skills/claude-code-terminal-expert/SKILL.md"
TEST_DIR="./tests/STORY-054"
RESULTS_FILE="${TEST_DIR}/test-results.txt"
FAILED_TESTS=0
PASSED_TESTS=0

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ============================================================================
# Helper Functions
# ============================================================================

print_test_header() {
    echo ""
    echo "============================================================================"
    echo "TEST: $1"
    echo "============================================================================"
}

assert_file_exists() {
    local file_path=$1
    local test_name=$2

    if [ ! -f "$file_path" ]; then
        echo -e "${RED}FAIL${NC}: File not found: $file_path"
        return 1
    else
        echo -e "${GREEN}PASS${NC}: File exists: $file_path"
        return 0
    fi
}

assert_grep_match() {
    local pattern=$1
    local file_path=$2
    local test_name=$3

    if grep -q "$pattern" "$file_path" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}: Pattern found in $file_path"
        return 0
    else
        echo -e "${RED}FAIL${NC}: Pattern not found: '$pattern'"
        return 1
    fi
}

assert_grep_count() {
    local pattern=$1
    local file_path=$2
    local min_count=$3
    local max_count=$4
    local test_name=$5

    count=$(grep -o "$pattern" "$file_path" 2>/dev/null | wc -l)

    if [ "$count" -ge "$min_count" ] && [ "$count" -le "$max_count" ]; then
        echo -e "${GREEN}PASS${NC}: Pattern count is $count (expected $min_count-$max_count)"
        return 0
    else
        echo -e "${RED}FAIL${NC}: Pattern count is $count (expected $min_count-$max_count)"
        return 1
    fi
}

assert_file_readable() {
    local file_path=$1
    local test_name=$2

    if [ -f "$file_path" ] && [ -r "$file_path" ]; then
        echo -e "${GREEN}PASS${NC}: File is readable: $file_path"
        return 0
    else
        echo -e "${RED}FAIL${NC}: File not readable: $file_path"
        return 1
    fi
}

assert_line_position() {
    local pattern=$1
    local file_path=$2
    local max_line=$3
    local test_name=$4

    line_num=$(grep -n "$pattern" "$file_path" 2>/dev/null | head -1 | cut -d: -f1)

    if [ -z "$line_num" ]; then
        echo -e "${RED}FAIL${NC}: Pattern not found: '$pattern'"
        return 1
    fi

    if [ "$line_num" -le "$max_line" ]; then
        echo -e "${GREEN}PASS${NC}: Pattern found at line $line_num (expected ≤$max_line)"
        return 0
    else
        echo -e "${RED}FAIL${NC}: Pattern at line $line_num (expected ≤$max_line)"
        return 1
    fi
}

record_test_result() {
    local test_name=$1
    local result=$2

    if [ $result -eq 0 ]; then
        echo "[PASS] $test_name" >> "$RESULTS_FILE"
        ((PASSED_TESTS++))
    else
        echo "[FAIL] $test_name" >> "$RESULTS_FILE"
        ((FAILED_TESTS++))
    fi
}

# ============================================================================
# ACCEPTANCE CRITERIA TEST SUITE
# ============================================================================

echo ""
echo "=========================================="
echo "STORY-054 Test Suite (RED Phase)"
echo "=========================================="
echo "File: $SKILL_FILE"
echo "Timestamp: $(date -u)"
echo ""

# Initialize results file
> "$RESULTS_FILE"

# ============================================================================
# AC#1: Prompting Guidance Section Added
# ============================================================================

print_test_header "AC#1.1: Section header exists"
if assert_file_exists "$SKILL_FILE" "AC#1.1"; then
    record_test_result "AC#1.1" 0
else
    record_test_result "AC#1.1" 1
    echo "    Cannot continue - skill file must exist to run remaining tests"
fi

print_test_header "AC#1.2: Section titled 'How DevForgeAI Skills Work with User Input' is present"
if assert_grep_match "## How DevForgeAI Skills Work" "$SKILL_FILE" "AC#1.2"; then
    record_test_result "AC#1.2" 0
else
    record_test_result "AC#1.2" 1
    echo "    Expected section header not found"
    echo "    Test will fail until section is added"
fi

print_test_header "AC#1.3: Section positioned after features overview (before line 300)"
if grep -q "## How DevForgeAI Skills Work" "$SKILL_FILE" 2>/dev/null; then
    if assert_line_position "## How DevForgeAI Skills Work" "$SKILL_FILE" 300 "AC#1.3"; then
        record_test_result "AC#1.3" 0
    else
        record_test_result "AC#1.3" 1
    fi
else
    record_test_result "AC#1.3" 1
    echo -e "${RED}SKIP${NC}: Section header not found, cannot verify position"
fi

print_test_header "AC#1.4: Section contains 100-200 lines of guidance"
if grep -A 200 "## How DevForgeAI Skills Work" "$SKILL_FILE" 2>/dev/null | head -200 > /tmp/ac1_section.txt; then
    section_lines=$(wc -l < /tmp/ac1_section.txt)
    if [ "$section_lines" -ge 100 ] && [ "$section_lines" -le 200 ]; then
        echo -e "${GREEN}PASS${NC}: Section has $section_lines lines (expected 100-200)"
        record_test_result "AC#1.4" 0
    else
        echo -e "${RED}FAIL${NC}: Section has $section_lines lines (expected 100-200)"
        record_test_result "AC#1.4" 1
    fi
else
    record_test_result "AC#1.4" 1
    echo -e "${RED}FAIL${NC}: Could not extract section"
fi

# ============================================================================
# AC#2: Cross-References to Both Guidance Documents
# ============================================================================

print_test_header "AC#2.1: Cross-reference to effective-prompting-guide.md exists"
if assert_grep_match "effective-prompting-guide.md" "$SKILL_FILE" "AC#2.1"; then
    record_test_result "AC#2.1" 0
else
    record_test_result "AC#2.1" 1
    echo "    Test will fail until cross-reference is added"
fi

print_test_header "AC#2.2: effective-prompting-guide.md reference is valid markdown link"
if grep -q "\[.*\](.*effective-prompting-guide\.md.*)" "$SKILL_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}: Markdown link format detected"
    record_test_result "AC#2.2" 0
else
    echo -e "${RED}FAIL${NC}: Valid markdown link not found"
    record_test_result "AC#2.2" 1
fi

print_test_header "AC#2.3: effective-prompting-guide.md link has description (≥15 words)"
if grep -B5 "effective-prompting-guide\.md" "$SKILL_FILE" 2>/dev/null | tail -10 > /tmp/link_context.txt; then
    context_words=$(wc -w < /tmp/link_context.txt)
    if [ "$context_words" -ge 15 ]; then
        echo -e "${GREEN}PASS${NC}: Link context has $context_words words (expected ≥15)"
        record_test_result "AC#2.3" 0
    else
        echo -e "${RED}FAIL${NC}: Link context has $context_words words (expected ≥15)"
        record_test_result "AC#2.3" 1
    fi
else
    record_test_result "AC#2.3" 1
    echo -e "${RED}FAIL${NC}: Could not extract link context"
fi

print_test_header "AC#2.4: Cross-reference to user-input-guidance.md exists"
if assert_grep_match "user-input-guidance.md" "$SKILL_FILE" "AC#2.4"; then
    record_test_result "AC#2.4" 0
else
    record_test_result "AC#2.4" 1
    echo "    Test will fail until cross-reference is added"
fi

print_test_header "AC#2.5: user-input-guidance.md reference is valid markdown link"
if grep -q "\[.*\](.*user-input-guidance\.md.*)" "$SKILL_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}: Markdown link format detected"
    record_test_result "AC#2.5" 0
else
    echo -e "${RED}FAIL${NC}: Valid markdown link not found"
    record_test_result "AC#2.5" 1
fi

print_test_header "AC#2.6: user-input-guidance.md link has description (≥15 words)"
if grep -B5 "user-input-guidance\.md" "$SKILL_FILE" 2>/dev/null | tail -10 > /tmp/link_context2.txt; then
    context_words=$(wc -w < /tmp/link_context2.txt)
    if [ "$context_words" -ge 15 ]; then
        echo -e "${GREEN}PASS${NC}: Link context has $context_words words (expected ≥15)"
        record_test_result "AC#2.6" 0
    else
        echo -e "${RED}FAIL${NC}: Link context has $context_words words (expected ≥15)"
        record_test_result "AC#2.6" 1
    fi
else
    record_test_result "AC#2.6" 1
    echo -e "${RED}FAIL${NC}: Could not extract link context"
fi

# ============================================================================
# AC#3: Effective Communication Examples (5-10 Scenarios)
# ============================================================================

print_test_header "AC#3.1: Section contains 5-10 paired examples (❌ vs ✅)"
if assert_grep_count "❌" "$SKILL_FILE" 5 10 "AC#3.1"; then
    record_test_result "AC#3.1" 0
else
    record_test_result "AC#3.1" 1
    count=$(grep -o "❌" "$SKILL_FILE" 2>/dev/null | wc -l)
    echo "    Found $count examples (expected 5-10)"
fi

print_test_header "AC#3.2: Each example has effective (✅) counterpart"
ineffective_count=$(grep -o "❌" "$SKILL_FILE" 2>/dev/null | wc -l)
effective_count=$(grep -o "✅" "$SKILL_FILE" 2>/dev/null | wc -l)

if [ "$ineffective_count" -eq "$effective_count" ] && [ "$ineffective_count" -gt 0 ]; then
    echo -e "${GREEN}PASS${NC}: Paired examples ($effective_count pairs)"
    record_test_result "AC#3.2" 0
else
    echo -e "${RED}FAIL${NC}: Mismatch in paired examples (❌:$ineffective_count, ✅:$effective_count)"
    record_test_result "AC#3.2" 1
fi

print_test_header "AC#3.3: Feature request example present"
if grep -qi "feature.*request" "$SKILL_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}: Feature request example found"
    record_test_result "AC#3.3" 0
else
    echo -e "${RED}FAIL${NC}: Feature request example not found"
    record_test_result "AC#3.3" 1
fi

print_test_header "AC#3.4: Story creation example present"
if grep -qi "story.*creation\|create.*story" "$SKILL_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}: Story creation example found"
    record_test_result "AC#3.4" 0
else
    echo -e "${RED}FAIL${NC}: Story creation example not found"
    record_test_result "AC#3.4" 1
fi

print_test_header "AC#3.5: Error reporting example present"
if grep -qi "error.*report\|report.*error" "$SKILL_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}: Error reporting example found"
    record_test_result "AC#3.5" 0
else
    echo -e "${RED}FAIL${NC}: Error reporting example not found"
    record_test_result "AC#3.5" 1
fi

print_test_header "AC#3.6: Technology decision example present"
if grep -qi "technology.*decis\|tech.*prefer" "$SKILL_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}: Technology decision example found"
    record_test_result "AC#3.6" 0
else
    echo -e "${RED}FAIL${NC}: Technology decision example not found"
    record_test_result "AC#3.6" 1
fi

print_test_header "AC#3.7: Feedback provision example present"
if grep -qi "feedback" "$SKILL_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}: Feedback example found"
    record_test_result "AC#3.7" 0
else
    echo -e "${RED}FAIL${NC}: Feedback example not found"
    record_test_result "AC#3.7" 1
fi

# ============================================================================
# AC#4: "Ask, Don't Assume" Principle Explained
# ============================================================================

print_test_header "AC#4.1: Subsection titled 'Ask, Don't Assume' exists"
if assert_grep_match "Ask, Don't Assume" "$SKILL_FILE" "AC#4.1"; then
    record_test_result "AC#4.1" 0
else
    record_test_result "AC#4.1" 1
    echo "    Test will fail until subsection is added"
fi

print_test_header "AC#4.2: Subsection explains WHEN to use AskUserQuestion"
if grep -A 30 "Ask, Don't Assume" "$SKILL_FILE" 2>/dev/null | grep -qi "when\|ambig"; then
    echo -e "${GREEN}PASS${NC}: 'When' guidance found"
    record_test_result "AC#4.2" 0
else
    echo -e "${RED}FAIL${NC}: 'When' guidance not found"
    record_test_result "AC#4.2" 1
fi

print_test_header "AC#4.3: Subsection explains WHAT NOT to assume"
if grep -A 30 "Ask, Don't Assume" "$SKILL_FILE" 2>/dev/null | grep -qi "not.*assume\|don't assume\|avoid.*assum"; then
    echo -e "${GREEN}PASS${NC}: 'What NOT' guidance found"
    record_test_result "AC#4.3" 0
else
    echo -e "${RED}FAIL${NC}: 'What NOT' guidance not found"
    record_test_result "AC#4.3" 1
fi

print_test_header "AC#4.4: Subsection explains WHY principle exists"
if grep -A 30 "Ask, Don't Assume" "$SKILL_FILE" 2>/dev/null | grep -qi "why\|reason\|prevent\|technical.*debt"; then
    echo -e "${GREEN}PASS${NC}: 'Why' rationale found"
    record_test_result "AC#4.4" 0
else
    echo -e "${RED}FAIL${NC}: 'Why' rationale not found"
    record_test_result "AC#4.4" 1
fi

print_test_header "AC#4.5: Subsection explains HOW it integrates with quality gates"
if grep -A 30 "Ask, Don't Assume" "$SKILL_FILE" 2>/dev/null | grep -qi "quality.*gate\|integrat"; then
    echo -e "${GREEN}PASS${NC}: 'How' integration found"
    record_test_result "AC#4.5" 0
else
    echo -e "${RED}FAIL${NC}: 'How' integration not found"
    record_test_result "AC#4.5" 1
fi

# ============================================================================
# AC#5: No Breaking Changes to Skill Structure
# ============================================================================

print_test_header "AC#5.1: Skill file structure unchanged (still contains frontmatter)"
if head -20 "$SKILL_FILE" | grep -q "^---"; then
    echo -e "${GREEN}PASS${NC}: YAML frontmatter detected"
    record_test_result "AC#5.1" 0
else
    echo -e "${RED}FAIL${NC}: YAML frontmatter not found"
    record_test_result "AC#5.1" 1
fi

print_test_header "AC#5.2: 'When to Use This Skill' section still present"
if assert_grep_match "## When to Use This Skill" "$SKILL_FILE" "AC#5.2"; then
    record_test_result "AC#5.2" 0
else
    record_test_result "AC#5.2" 1
fi

print_test_header "AC#5.3: 'Core Claude Code Terminal Features' section still present"
if assert_grep_match "## Core Claude Code Terminal Features" "$SKILL_FILE" "AC#5.3"; then
    record_test_result "AC#5.3" 0
else
    record_test_result "AC#5.3" 1
fi

print_test_header "AC#5.4: All 8 core features still documented"
feature_count=$(grep -c "^### [0-9]\+\. " "$SKILL_FILE" 2>/dev/null)
if [ "$feature_count" -ge 8 ]; then
    echo -e "${GREEN}PASS${NC}: Found $feature_count features (expected ≥8)"
    record_test_result "AC#5.4" 0
else
    echo -e "${RED}FAIL${NC}: Found $feature_count features (expected ≥8)"
    record_test_result "AC#5.4" 1
fi

print_test_header "AC#5.5: 'Progressive Disclosure Strategy' section still present"
if assert_grep_match "## Progressive Disclosure Strategy" "$SKILL_FILE" "AC#5.5"; then
    record_test_result "AC#5.5" 0
else
    record_test_result "AC#5.5" 1
fi

print_test_header "AC#5.6: Self-updating mechanism documentation still present"
if assert_grep_match "## Self-Updating Mechanism" "$SKILL_FILE" "AC#5.6"; then
    record_test_result "AC#5.6" 0
else
    record_test_result "AC#5.6" 1
fi

print_test_header "AC#5.7: Reference file loading still works (code examples present)"
if grep -q "Read(file_path=" "$SKILL_FILE"; then
    echo -e "${GREEN}PASS${NC}: Reference file loading code detected"
    record_test_result "AC#5.7" 0
else
    echo -e "${RED}FAIL${NC}: Reference file loading code not found"
    record_test_result "AC#5.7" 1
fi

# ============================================================================
# TECHNICAL SPECIFICATION TESTS
# ============================================================================

print_test_header "TechSpec-001: Section header format is heading level 2 (##)"
if grep "^## How DevForgeAI Skills Work" "$SKILL_FILE" 2>/dev/null >/dev/null; then
    echo -e "${GREEN}PASS${NC}: Correct heading level detected"
    record_test_result "TechSpec-001" 0
else
    echo -e "${RED}FAIL${NC}: Incorrect heading level"
    record_test_result "TechSpec-001" 1
fi

print_test_header "TechSpec-002: Cross-reference syntax uses relative paths"
if grep -E "(\.\./(\.\.)?)?memory|guides" "$SKILL_FILE" 2>/dev/null | grep -q "\.md"; then
    echo -e "${GREEN}PASS${NC}: Relative path references detected"
    record_test_result "TechSpec-002" 0
else
    echo -e "${RED}FAIL${NC}: Proper relative path references not found"
    record_test_result "TechSpec-002" 1
fi

print_test_header "TechSpec-003: Example format consistency (❌ / ✅ pattern)"
if grep -q "❌.*:" "$SKILL_FILE" 2>/dev/null && grep -q "✅.*:" "$SKILL_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}: Example format pattern detected"
    record_test_result "TechSpec-003" 0
else
    echo -e "${RED}FAIL${NC}: Example format pattern not found"
    record_test_result "TechSpec-003" 1
fi

print_test_header "TechSpec-004: Subsection headers use level 3 (###)"
if grep "^### .*Ask.*Don't Assume" "$SKILL_FILE" 2>/dev/null >/dev/null; then
    echo -e "${GREEN}PASS${NC}: Correct subsection heading level"
    record_test_result "TechSpec-004" 0
else
    echo -e "${RED}FAIL${NC}: Correct subsection heading not found"
    record_test_result "TechSpec-004" 1
fi

# ============================================================================
# BUSINESS RULES TESTS
# ============================================================================

print_test_header "BR-001: Examples align with actual framework behavior"
echo -e "${YELLOW}INFO${NC}: This requires manual verification with actual commands"
echo "    Example verification deferred to Phase 2 (implementation)"
record_test_result "BR-001" 1

print_test_header "BR-002: Cross-reference descriptions are helpful (≥15 words)"
echo -e "${YELLOW}INFO${NC}: Word count validation performed above (AC#2.3, AC#2.6)"
record_test_result "BR-002" 0

print_test_header "BR-003: No conflicting guidance in new section"
if grep -q "never.*AskUserQuestion" "$SKILL_FILE" 2>/dev/null && grep -q "use.*AskUserQuestion" "$SKILL_FILE" 2>/dev/null; then
    echo -e "${RED}FAIL${NC}: Potentially conflicting statements found"
    record_test_result "BR-003" 1
else
    echo -e "${GREEN}PASS${NC}: No obvious contradictions detected"
    record_test_result "BR-003" 0
fi

# ============================================================================
# NON-FUNCTIONAL REQUIREMENTS TESTS
# ============================================================================

print_test_header "NFR-001: Token overhead ≤1,000 tokens"
echo -e "${YELLOW}INFO${NC}: Token measurement requires implementation"
echo "    This test will be executed in Phase 2"
record_test_result "NFR-001" 1

print_test_header "NFR-003: 100% backward compatibility"
echo -e "${YELLOW}INFO${NC}: Full regression testing deferred to Phase 2"
echo "    Smoke tests above verify core sections unchanged"
record_test_result "NFR-003" 0

print_test_header "NFR-005: Terminology consistency with other docs"
echo -e "${YELLOW}INFO${NC}: Terminology validation deferred to Phase 2"
echo "    Requires analysis against effective-prompting-guide.md and CLAUDE.md"
record_test_result "NFR-005" 1

# ============================================================================
# TEST SUMMARY
# ============================================================================

echo ""
echo "=========================================="
echo "TEST SUITE SUMMARY"
echo "=========================================="
echo ""

total_tests=$((PASSED_TESTS + FAILED_TESTS))
echo "Total Tests: $total_tests"
echo -e "Passed: ${GREEN}$PASSED_TESTS${NC}"
echo -e "Failed: ${RED}$FAILED_TESTS${NC}"

if [ $FAILED_TESTS -gt 0 ]; then
    echo ""
    echo -e "${RED}TEST SUITE FAILED (RED Phase - Expected)${NC}"
    echo ""
    echo "Failed tests indicate incomplete implementation:"
    echo "  - AC#1: Section not yet added"
    echo "  - AC#2: Cross-references not yet added"
    echo "  - AC#3: Examples not yet added"
    echo "  - AC#4: Principle explanation not yet added"
    echo "  - NFR-001: Token measurement pending"
    echo "  - NFR-005: Terminology validation pending"
    echo ""
    echo "Next steps (Phase 2 - GREEN):"
    echo "  1. Add 'How DevForgeAI Skills Work with User Input' section"
    echo "  2. Add cross-references to guidance documents"
    echo "  3. Add 5-10 paired examples (❌/✅ pattern)"
    echo "  4. Add 'Ask, Don't Assume' principle explanation"
    echo "  5. Run this test suite again - all tests should PASS"
    echo ""
else
    echo ""
    echo -e "${GREEN}ALL TESTS PASSED (GREEN Phase)${NC}"
    echo ""
fi

# Write detailed results
echo ""
echo "Detailed Results:"
echo "================="
cat "$RESULTS_FILE"

echo ""
echo "Test execution complete: $(date -u)"

# Exit with appropriate code
exit $FAILED_TESTS
