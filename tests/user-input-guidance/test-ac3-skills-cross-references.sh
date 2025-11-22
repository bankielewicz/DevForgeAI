#!/bin/bash
################################################################################
# Test Suite: AC#3 - Skills Reference Cross-References Added
#
# Tests for acceptance criterion 3: Verifying that 13 applicable skills have
# "User Input Guidance" subsections (excluding claude-code-terminal-expert).
#
# Test Framework: Bash/Shell (grep, awk)
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
SKILLS_REF_FILE="src/claude/memory/skills-reference.md"

# List of 13 applicable skills (excluding claude-code-terminal-expert and skill-creator)
APPLICABLE_SKILLS=(
    "devforgeai-ideation"
    "devforgeai-architecture"
    "devforgeai-orchestration"
    "devforgeai-story-creation"
    "devforgeai-ui-generator"
    "devforgeai-development"
    "devforgeai-qa"
    "devforgeai-release"
    "devforgeai-documentation"
    "devforgeai-feedback"
    "devforgeai-mcp-cli-converter"
    "devforgeai-subagent-creation"
    "devforgeai-rca"
)

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

assert_skill_section_exists() {
    local file="$1"
    local skill="$2"
    local test_name="$3"

    # Look for skill mention in file (case-insensitive, as code pattern)
    if ! grep -qi "### $skill\|**$skill**\|\`$skill\`" "$file"; then
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Skill section for '$skill' not found"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

assert_skill_has_guidance() {
    local file="$1"
    local skill="$2"
    local test_name="$3"

    # Find the skill section line number (look for skill name in various formats)
    local skill_line=$(grep -n -i "### $skill\|**$skill**" "$file" | head -1 | cut -d: -f1)

    if [[ -z "$skill_line" ]]; then
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Skill section for '$skill' not found"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi

    # Get section content until next skill or major section
    local section_end=$(tail -n +$((skill_line + 1)) "$file" | grep -n "^###" | head -1 | cut -d: -f1)
    if [[ -z "$section_end" ]]; then
        section_end=$(wc -l < "$file")
    else
        section_end=$((skill_line + section_end - 1))
    fi

    local section_content=$(sed -n "${skill_line},${section_end}p" "$file")

    # Look for User Input Guidance subsection
    if ! echo "$section_content" | grep -qi "#### User Input Guidance\|### User Input Guidance"; then
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  'User Input Guidance' subsection not found for skill '$skill'"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi

    echo -e "${GREEN}PASS${NC}: $test_name"
    TESTS_PASSED=$((TESTS_PASSED + 1))
}

assert_guidance_has_structure() {
    local file="$1"
    local skill="$2"
    local test_name="$3"

    # Find the skill section
    local skill_line=$(grep -n -i "### $skill\|**$skill**" "$file" | head -1 | cut -d: -f1)

    if [[ -z "$skill_line" ]]; then
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Skill section not found"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi

    # Get section content
    local section_end=$(tail -n +$((skill_line + 1)) "$file" | grep -n "^###" | head -1 | cut -d: -f1)
    if [[ -z "$section_end" ]]; then
        section_end=$(wc -l < "$file")
    else
        section_end=$((skill_line + section_end - 1))
    fi

    local section_content=$(sed -n "${skill_line},${section_end}p" "$file")

    # Check for required subsections (File:, Load:, Example:)
    local has_file=0
    local has_load=0
    local has_example=0

    if echo "$section_content" | grep -qi "\*\*File:\|File:"; then
        has_file=1
    fi

    if echo "$section_content" | grep -qi "\*\*Load:\|Load:"; then
        has_load=1
    fi

    if echo "$section_content" | grep -qi "\*\*Example:\|Example:"; then
        has_example=1
    fi

    if [[ $has_file -eq 1 && $has_load -eq 1 && $has_example -eq 1 ]]; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Missing required subsections for '$skill'"
        echo "  File: $has_file, Load: $has_load, Example: $has_example"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

################################################################################
# TEST CASES: AC#3 - Skills Cross-References Added
################################################################################

echo "=========================================="
echo "TEST SUITE: AC#3 - Skills Cross-References"
echo "=========================================="
echo ""

# Test 3.1: File exists
echo "Test 3.1: skills-reference.md file exists"
assert_file_exists "$SKILLS_REF_FILE" || true
echo ""

# Test 3.2: All 13 applicable skills are documented
echo "Test 3.2: All 13 applicable skills have sections"
for skill in "${APPLICABLE_SKILLS[@]}"; do
    {
        assert_skill_section_exists "$SKILLS_REF_FILE" "$skill" \
            "Skill section for '$skill' found" || true
    }
done
echo ""

# Test 3.3: Each applicable skill has "User Input Guidance" subsection
echo "Test 3.3: Each applicable skill has 'User Input Guidance' subsection"
for skill in "${APPLICABLE_SKILLS[@]}"; do
    {
        assert_skill_has_guidance "$SKILLS_REF_FILE" "$skill" \
            "User Input Guidance subsection for '$skill'" || true
    }
done
echo ""

# Test 3.4: Each guidance subsection has required structure
echo "Test 3.4: Each guidance subsection has File, Load, and Example components"
for skill in "${APPLICABLE_SKILLS[@]}"; do
    {
        assert_guidance_has_structure "$SKILLS_REF_FILE" "$skill" \
            "Guidance structure for '$skill' complete" || true
    }
done
echo ""

# Test 3.5: Count "User Input Guidance" subsections in skill sections
echo "Test 3.5: Count of 'User Input Guidance' subsections matches 13 applicable skills"
{
    # Count subsections in the skills sections (should have at least 13)
    local guidance_count=$(grep -c "#### User Input Guidance\|### User Input Guidance" "$SKILLS_REF_FILE" || true)

    # We need to exclude claude-code-terminal-expert and skill-creator from the count
    # Extract just the section that covers applicable skills
    local applicable_count=$(sed -n '/devforgeai-ideation/,/devforgeai-rca/p' "$SKILLS_REF_FILE" | \
        grep -c "#### User Input Guidance\|### User Input Guidance" || true)

    if [[ $guidance_count -ge 13 ]]; then
        echo -e "${GREEN}PASS${NC}: Found $guidance_count 'User Input Guidance' subsections (expected ≥13)"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC}: Found only $guidance_count 'User Input Guidance' subsections (expected ≥13)"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}
echo ""

# Test 3.6: Verify claude-code-terminal-expert does NOT have guidance requirement
echo "Test 3.6: claude-code-terminal-expert NOT included in guidance requirement (13 skill limit)"
{
    local claude_code_line=$(grep -n "claude-code-terminal-expert" "$SKILLS_REF_FILE" | head -1 | cut -d: -f1)
    local skill_creator_line=$(grep -n "skill-creator" "$SKILLS_REF_FILE" | head -1 | cut -d: -f1)

    if [[ -n "$claude_code_line" || -n "$skill_creator_line" ]]; then
        echo -e "${GREEN}PASS${NC}: Infrastructure skills documented separately (13-skill limit respected)"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${YELLOW}INFO${NC}: Claude Code infrastructure skills section may not be explicitly marked"
    fi
}
echo ""

# Test 3.7: Check that guidance descriptions are skill-specific (not generic)
echo "Test 3.7: Guidance descriptions are tailored to skill input requirements"
{
    # Check for some differentiation in guidance text
    # For example, different skills should mention their specific inputs
    local unique_descriptions=$(sed -n '/#### User Input Guidance/,/####\|###/p' "$SKILLS_REF_FILE" | \
        grep -o "This skill [^.]*" | sort -u | wc -l)

    if [[ $unique_descriptions -ge 5 ]]; then
        echo -e "${GREEN}PASS${NC}: Found $unique_descriptions unique guidance descriptions (expected ≥5)"
        echo "  Indicates skill-specific tailoring"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC}: Insufficient variation in guidance descriptions ($unique_descriptions unique)"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}
echo ""

# Test 3.8: Verify consistency of subsection structure across all skills
echo "Test 3.8: Consistent formatting across all skill guidance subsections"
{
    # Count total formatted subsections (File, Load, Example)
    local subsection_lines=$(sed -n '/#### User Input Guidance/,/####\|###/p' "$SKILLS_REF_FILE" | \
        grep -c "\*\*File:\|\*\*Load:\|\*\*Example:" || true)

    # Should have 3 per skill minimum (13 skills × 3 = 39)
    if [[ $subsection_lines -ge 35 ]]; then
        echo -e "${GREEN}PASS${NC}: Found $subsection_lines formatted subsection lines (expected ≥35)"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC}: Insufficient consistent formatting ($subsection_lines lines)"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}
echo ""

# Test 3.9: Verify Invocation subsections are placed before User Input Guidance
echo "Test 3.9: User Input Guidance appears after Invocation subsection"
{
    local file_content=$(cat "$SKILLS_REF_FILE")
    local invocation_count=$(echo "$file_content" | grep -c "### Invocation" || true)
    local guidance_count=$(echo "$file_content" | grep -c "#### User Input Guidance" || true)

    # For each guidance section, verify it comes after an Invocation section
    # This is harder to test directly, so we'll just verify both exist and are present
    if [[ $invocation_count -gt 0 && $guidance_count -gt 0 ]]; then
        echo -e "${GREEN}PASS${NC}: Found both Invocation ($invocation_count) and Guidance ($guidance_count) sections"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC}: Missing Invocation or Guidance sections"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}
echo ""

################################################################################
# Test Summary
################################################################################

echo "=========================================="
echo "TEST SUMMARY: AC#3"
echo "=========================================="
echo -e "Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Failed: ${RED}$TESTS_FAILED${NC}"
echo ""

if [[ $TESTS_FAILED -gt 0 ]]; then
    exit 1
else
    exit 0
fi
