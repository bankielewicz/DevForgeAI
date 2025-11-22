#!/bin/bash
################################################################################
# Test Suite: AC#1 - CLAUDE.md Learning Section Added
#
# Tests for acceptance criterion 1: Section existence, positioning, subsections
# and example count in the "Learning DevForgeAI" section.
#
# Test Framework: Bash/Shell (grep, test operators)
# Test Pattern: AAA (Arrange, Act, Assert)
#
# Status: RED PHASE - All tests should FAIL (implementation not started)
################################################################################

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

TESTS_PASSED=0
TESTS_FAILED=0
CLAUDEMD_FILE="src/CLAUDE.md"

################################################################################
# Helper Functions
################################################################################

assert_file_exists() {
    local file="$1"
    if [[ ! -f "$file" ]]; then
        echo -e "${RED}FAIL${NC}: File does not exist: $file"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

assert_section_exists() {
    local file="$1"
    local section_header="$2"
    local test_name="$3"

    if ! grep -q "^## $section_header" "$file"; then
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Expected section header '## $section_header' not found in $file"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
    echo -e "${GREEN}PASS${NC}: $test_name"
    TESTS_PASSED=$((TESTS_PASSED + 1))
}

assert_section_contains() {
    local file="$1"
    local section_header="$2"
    local search_pattern="$3"
    local test_name="$4"

    # Extract content between section header and next ## header
    local section_content=$(awk "/^## $section_header/,/^##/ {print}" "$file" | head -n -1)

    if ! echo "$section_content" | grep -q "$search_pattern"; then
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Pattern '$search_pattern' not found in section '$section_header'"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
    echo -e "${GREEN}PASS${NC}: $test_name"
    TESTS_PASSED=$((TESTS_PASSED + 1))
}

count_pattern_in_section() {
    local file="$1"
    local section_header="$2"
    local pattern="$3"

    # Extract content between section header and next ## header
    local section_content=$(awk "/^## $section_header/,/^##/ {print}" "$file" | head -n -1)

    echo "$section_content" | grep -c "$pattern" || echo 0
}

assert_section_position() {
    local file="$1"
    local section_name="$2"
    local before_section="$3"
    local after_section="$4"
    local test_name="$5"

    local line_section=$(grep -n "^## $section_name" "$file" | cut -d: -f1)
    local line_before=$(grep -n "^## $before_section" "$file" | cut -d: -f1)
    local line_after=$(grep -n "^## $after_section" "$file" | cut -d: -f1)

    if [[ -z "$line_section" ]] || [[ -z "$line_before" ]] || [[ -z "$line_after" ]]; then
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  One or more required sections not found"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi

    if [[ $line_section -gt $line_before && $line_section -lt $line_after ]]; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Section '$section_name' is not positioned correctly"
        echo "  Found on line $line_section, but should be after line $line_before and before line $line_after"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

assert_count_in_range() {
    local file="$1"
    local section_header="$2"
    local pattern="$3"
    local min_count="$4"
    local max_count="$5"
    local test_name="$6"

    local actual_count=$(count_pattern_in_section "$file" "$section_header" "$pattern")

    if [[ $actual_count -ge $min_count && $actual_count -le $max_count ]]; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        echo "  Found $actual_count occurrences (expected $min_count-$max_count)"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Found $actual_count occurrences of pattern '$pattern'"
        echo "  Expected between $min_count and $max_count occurrences"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

################################################################################
# TEST CASES: AC#1 - CLAUDE.md Learning Section Added
################################################################################

echo "================================"
echo "TEST SUITE: AC#1 - CLAUDE.md Learning Section"
echo "================================"
echo ""

# Test 1.1: CLAUDE.md file exists
echo "Test 1.1: CLAUDE.md file exists"
assert_file_exists "$CLAUDEMD_FILE" || true
echo ""

# Test 1.2: "Learning DevForgeAI" section header exists
echo "Test 1.2: 'Learning DevForgeAI' section header exists"
assert_section_exists "$CLAUDEMD_FILE" "Learning DevForgeAI" \
    "Section header '## Learning DevForgeAI' found" || true
echo ""

# Test 1.3: Section is positioned after "Quick Reference - Progressive Disclosure"
echo "Test 1.3: Section positioned correctly between Quick Reference and Development Workflow"
assert_section_position "$CLAUDEMD_FILE" "Learning DevForgeAI" \
    "Quick Reference - Progressive Disclosure" "Development Workflow Overview" \
    "Learning DevForgeAI section positioned correctly" || true
echo ""

# Test 1.4: "Writing Effective Feature Descriptions" subsection exists
echo "Test 1.4: 'Writing Effective Feature Descriptions' subsection exists"
assert_section_contains "$CLAUDEMD_FILE" "Learning DevForgeAI" \
    "### Writing Effective Feature Descriptions" \
    "Subsection 'Writing Effective Feature Descriptions' found" || true
echo ""

# Test 1.5: "User Input Guidance Resources" subsection exists
echo "Test 1.5: 'User Input Guidance Resources' subsection exists"
assert_section_contains "$CLAUDEMD_FILE" "Learning DevForgeAI" \
    "### User Input Guidance Resources" \
    "Subsection 'User Input Guidance Resources' found" || true
echo ""

# Test 1.6: "Progressive Learning Path" subsection exists
echo "Test 1.6: 'Progressive Learning Path' subsection exists"
assert_section_contains "$CLAUDEMD_FILE" "Learning DevForgeAI" \
    "### Progressive Learning Path" \
    "Subsection 'Progressive Learning Path' found" || true
echo ""

# Test 1.7: "Writing Effective Feature Descriptions" has 3-5 examples
echo "Test 1.7: 'Writing Effective Feature Descriptions' has 3-5 good vs bad examples"
assert_count_in_range "$CLAUDEMD_FILE" "Learning DevForgeAI" \
    "❌.*✅\|✅.*❌" 3 5 \
    "Found 3-5 example pairs of bad vs good (❌ vs ✅) examples" || true
echo ""

# Test 1.8: "User Input Guidance Resources" lists 3 Read commands
echo "Test 1.8: 'User Input Guidance Resources' lists all 3 guidance documents"
assert_count_in_range "$CLAUDEMD_FILE" "Learning DevForgeAI" \
    'Read(file_path=' 3 3 \
    "Found exactly 3 Read(file_path=...) commands" || true
echo ""

# Test 1.9: "Progressive Learning Path" mentions learning levels
echo "Test 1.9: 'Progressive Learning Path' mentions basic, advanced, and framework-specific"
assert_section_contains "$CLAUDEMD_FILE" "Learning DevForgeAI" \
    "basic" "Learning levels include 'basic'" || true
assert_section_contains "$CLAUDEMD_FILE" "Learning DevForgeAI" \
    "advanced" "Learning levels include 'advanced'" || true
assert_section_contains "$CLAUDEMD_FILE" "Learning DevForgeAI" \
    "framework-specific\|framework specific" "Learning levels include 'framework-specific'" || true
echo ""

# Test 1.10: All three subsections exist in correct order
echo "Test 1.10: All three subsections exist in correct order"
{
    grep -n "### Writing Effective Feature Descriptions" "$CLAUDEMD_FILE" && \
    grep -n "### User Input Guidance Resources" "$CLAUDEMD_FILE" && \
    grep -n "### Progressive Learning Path" "$CLAUDEMD_FILE"
} >/dev/null 2>&1
if [[ $? -eq 0 ]]; then
    line_write=$(grep -n "### Writing Effective Feature Descriptions" "$CLAUDEMD_FILE" | cut -d: -f1)
    line_resources=$(grep -n "### User Input Guidance Resources" "$CLAUDEMD_FILE" | cut -d: -f1)
    line_learning=$(grep -n "### Progressive Learning Path" "$CLAUDEMD_FILE" | cut -d: -f1)

    if [[ $line_write -lt $line_resources && $line_resources -lt $line_learning ]]; then
        echo -e "${GREEN}PASS${NC}: All three subsections in correct order"
        echo "  Line $line_write: Writing Effective Feature Descriptions"
        echo "  Line $line_resources: User Input Guidance Resources"
        echo "  Line $line_learning: Progressive Learning Path"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC}: Subsections not in correct order"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
else
    echo -e "${RED}FAIL${NC}: Not all three subsections found"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
echo ""

################################################################################
# Test Summary
################################################################################

echo "================================"
echo "TEST SUMMARY: AC#1"
echo "================================"
echo -e "Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Failed: ${RED}$TESTS_FAILED${NC}"
echo ""

if [[ $TESTS_FAILED -gt 0 ]]; then
    exit 1
else
    exit 0
fi
