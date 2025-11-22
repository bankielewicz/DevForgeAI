#!/bin/bash
################################################################################
# Test Suite: AC#2 - Commands Reference Cross-References Added
#
# Tests for acceptance criterion 2: Verifying that all 11 commands have
# "User Input Guidance" subsections with consistent structure.
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
COMMANDS_REF_FILE="src/claude/memory/commands-reference.md"

# List of all 11 commands
COMMANDS=(
    "/ideate"
    "/create-context"
    "/create-epic"
    "/create-sprint"
    "/create-story"
    "/create-ui"
    "/dev"
    "/qa"
    "/release"
    "/orchestrate"
    "/audit-deferrals"
)

# Commands that might have "N/A" guidance (no feature descriptions required)
NA_COMMANDS=(
    "/audit-deferrals"
    "/audit-budget"
    "/rca"
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

assert_command_section_exists() {
    local file="$1"
    local command="$2"
    local test_name="$3"

    if ! grep -q "^### $command" "$file"; then
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Command section '### $command' not found"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

assert_command_has_guidance() {
    local file="$1"
    local command="$2"
    local test_name="$3"

    # Extract section for this command
    local section_start=$(grep -n "^### $command" "$file" | head -1 | cut -d: -f1)
    if [[ -z "$section_start" ]]; then
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Command section '### $command' not found"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi

    # Get the section from this command to the next ### header
    local section_end=$(tail -n +$((section_start + 1)) "$file" | grep -n "^###" | head -1 | cut -d: -f1)
    if [[ -z "$section_end" ]]; then
        section_end=$(wc -l < "$file")
    else
        section_end=$((section_start + section_end - 1))
    fi

    local section_content=$(sed -n "${section_start},${section_end}p" "$file")

    if ! echo "$section_content" | grep -q "#### User Input Guidance\|### User Input Guidance"; then
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  'User Input Guidance' subsection not found for command '$command'"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi

    echo -e "${GREEN}PASS${NC}: $test_name"
    TESTS_PASSED=$((TESTS_PASSED + 1))
}

assert_guidance_structure() {
    local file="$1"
    local command="$2"
    local test_name="$3"

    # Find the command section
    local section_start=$(grep -n "^### $command" "$file" | head -1 | cut -d: -f1)
    if [[ -z "$section_start" ]]; then
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Command section not found for '$command'"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi

    local section_end=$(tail -n +$((section_start + 1)) "$file" | grep -n "^###" | head -1 | cut -d: -f1)
    if [[ -z "$section_end" ]]; then
        section_end=$(wc -l < "$file")
    else
        section_end=$((section_start + section_end - 1))
    fi

    local section_content=$(sed -n "${section_start},${section_end}p" "$file")

    # Check for required subsections within User Input Guidance
    local has_file_subsection=0
    local has_load_subsection=0
    local has_example_subsection=0

    # Look for File:, Load:, Example: within the User Input Guidance section
    if echo "$section_content" | grep -q "\*\*File:\*\|**File:\|File:"; then
        has_file_subsection=1
    fi

    if echo "$section_content" | grep -q "\*\*Load:\*\|**Load:\|Load:"; then
        has_load_subsection=1
    fi

    if echo "$section_content" | grep -q "\*\*Example:\*\|**Example:\|Example:"; then
        has_example_subsection=1
    fi

    if [[ $has_file_subsection -eq 1 && $has_load_subsection -eq 1 && $has_example_subsection -eq 1 ]]; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        echo "  File, Load, and Example subsections found"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Missing required subsections in guidance for '$command'"
        echo "  File: $has_file_subsection, Load: $has_load_subsection, Example: $has_example_subsection"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

################################################################################
# TEST CASES: AC#2 - Commands Cross-References Added
################################################################################

echo "=========================================="
echo "TEST SUITE: AC#2 - Commands Cross-References"
echo "=========================================="
echo ""

# Test 2.1: File exists
echo "Test 2.1: commands-reference.md file exists"
assert_file_exists "$COMMANDS_REF_FILE" || true
echo ""

# Test 2.2: All 11 commands are defined
echo "Test 2.2: All 11 commands have section headers"
for command in "${COMMANDS[@]}"; do
    {
        assert_command_section_exists "$COMMANDS_REF_FILE" "$command" \
            "Command section '### $command' found" || true
    }
done
echo ""

# Test 2.3: Each command has "User Input Guidance" subsection
echo "Test 2.3: Each command has 'User Input Guidance' subsection"
for command in "${COMMANDS[@]}"; do
    {
        assert_command_has_guidance "$COMMANDS_REF_FILE" "$command" \
            "User Input Guidance subsection for '$command'" || true
    }
done
echo ""

# Test 2.4: Each guidance subsection has required structure
echo "Test 2.4: Each guidance subsection has File, Load, and Example components"
for command in "${COMMANDS[@]}"; do
    {
        assert_guidance_structure "$COMMANDS_REF_FILE" "$command" \
            "Guidance structure for '$command' complete" || true
    }
done
echo ""

# Test 2.5: Count "User Input Guidance" subsections (should be 11)
echo "Test 2.5: Total count of 'User Input Guidance' subsections is 11"
actual_count=$(grep -c "#### User Input Guidance\|### User Input Guidance" "$COMMANDS_REF_FILE" || true)
if [[ $actual_count -eq 11 ]]; then
    echo -e "${GREEN}PASS${NC}: Found exactly 11 'User Input Guidance' subsections"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC}: Expected 11 'User Input Guidance' subsections, found $actual_count"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
echo ""

# Test 2.6: Check for consistent formatting across all guidance sections
echo "Test 2.6: Consistent formatting across all guidance subsections"
{
    # Extract all guidance subsections and check for consistent indentation
    local guidance_sections=$(grep -A 20 "#### User Input Guidance\|### User Input Guidance" "$COMMANDS_REF_FILE" | \
        grep "**File:\|**Load:\|**Example:" | wc -l)

    # Should have at least 3 (File, Load, Example) per command × commands = minimum 33 total
    if [[ $guidance_sections -ge 30 ]]; then
        echo -e "${GREEN}PASS${NC}: Consistent subsections found across guidance sections"
        echo "  Found $guidance_sections formatted subsection lines"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC}: Insufficient consistent formatting found"
        echo "  Expected at least 30 formatted subsection lines, found $guidance_sections"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}
echo ""

# Test 2.7: Check that guidance descriptions exist (non-empty)
echo "Test 2.7: All guidance subsections have descriptions (1-2 sentences)"
{
    local command_count=0
    for command in "${COMMANDS[@]}"; do
        local section_start=$(grep -n "^### $command" "$COMMANDS_REF_FILE" | head -1 | cut -d: -f1)
        if [[ -n "$section_start" ]]; then
            local section_end=$(tail -n +$((section_start + 1)) "$COMMANDS_REF_FILE" | grep -n "^###" | head -1 | cut -d: -f1)
            if [[ -z "$section_end" ]]; then
                section_end=$(wc -l < "$COMMANDS_REF_FILE")
            else
                section_end=$((section_start + section_end - 1))
            fi

            # Look for guidance subsection
            local guidance_start=$(sed -n "${section_start},${section_end}p" "$COMMANDS_REF_FILE" | \
                grep -n "#### User Input Guidance\|### User Input Guidance" | head -1 | cut -d: -f1)

            if [[ -n "$guidance_start" ]]; then
                guidance_start=$((section_start + guidance_start))
                # Check if there's non-empty content after the heading (description)
                if sed -n "$((guidance_start + 1)),$((section_end))p" "$COMMANDS_REF_FILE" | \
                   grep -q "[A-Za-z0-9]" | head -1; then
                    command_count=$((command_count + 1))
                fi
            fi
        fi
    done

    if [[ $command_count -ge 8 ]]; then
        echo -e "${GREEN}PASS${NC}: At least 8 commands have guidance descriptions"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC}: Only $command_count commands have descriptions (expected ≥8)"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}
echo ""

################################################################################
# Test Summary
################################################################################

echo "=========================================="
echo "TEST SUMMARY: AC#2"
echo "=========================================="
echo -e "Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Failed: ${RED}$TESTS_FAILED${NC}"
echo ""

if [[ $TESTS_FAILED -gt 0 ]]; then
    exit 1
else
    exit 0
fi
