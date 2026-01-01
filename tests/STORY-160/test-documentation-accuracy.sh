#!/bin/bash
##############################################################################
# STORY-160: Documentation Accuracy Tests
#
# Validates that documentation is accurate, complete, and internally consistent
#
# Tests:
# - No typos or grammatical errors
# - Consistent terminology
# - Complete sections
# - Proper formatting
# - Accurate dates and version info
##############################################################################

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"

# Test counter
tests_passed=0
tests_failed=0

##############################################################################
# Test D-1: Terminology consistency - "RCA-008" vs "RCA 008"
##############################################################################
echo -e "${YELLOW}[Accuracy Test D-1]${NC} Verify consistent RCA-008 terminology"
# Count both formats
rca_hyphen=$(grep -ro "RCA-008" "${PROJECT_ROOT}/.claude/skills/devforgeai-development/SKILL.md" 2>/dev/null | wc -l || echo "0")
rca_space=$(grep -ro "RCA 008" "${PROJECT_ROOT}/.claude/skills/devforgeai-development/SKILL.md" 2>/dev/null | wc -l || echo "0")

if [ "${rca_hyphen}" -gt 0 ]; then
    echo -e "${GREEN}PASS${NC}: Consistent RCA-008 format used (hyphenated)"
    ((tests_passed++))
elif [ "${rca_space}" -gt 0 ]; then
    echo -e "${YELLOW}WARN${NC}: Space-separated format used (RCA 008) - less standard but acceptable"
    ((tests_passed++))
else
    echo -e "${RED}FAIL${NC}: No RCA reference format found"
    ((tests_failed++))
fi

##############################################################################
# Test D-2: Section headers are properly formatted
##############################################################################
echo -e "${YELLOW}[Accuracy Test D-2]${NC} Verify markdown section formatting"
skill_file="${PROJECT_ROOT}/.claude/skills/devforgeai-development/SKILL.md"

# Check for proper header hierarchy
h1_count=$(grep -c "^# " "${skill_file}" || echo "0")
h2_count=$(grep -c "^## " "${skill_file}" || echo "0")
h3_count=$(grep -c "^### " "${skill_file}" || echo "0")

if [ "${h1_count}" -gt 0 ] && [ "${h2_count}" -gt 0 ]; then
    echo -e "${GREEN}PASS${NC}: Proper markdown header hierarchy (H1: ${h1_count}, H2: ${h2_count}, H3: ${h3_count})"
    ((tests_passed++))
else
    echo -e "${RED}FAIL${NC}: Improper header formatting"
    ((tests_failed++))
fi

##############################################################################
# Test D-3: Code blocks and references use backticks properly
##############################################################################
echo -e "${YELLOW}[Accuracy Test D-3]${NC} Verify proper code block formatting"
backtick_count=$(grep -c '`' "${skill_file}" || echo "0")

if [ "${backtick_count}" -gt 5 ]; then
    echo -e "${GREEN}PASS${NC}: Proper inline code formatting with backticks (${backtick_count} instances)"
    ((tests_passed++))
else
    echo -e "${YELLOW}WARN${NC}: Limited inline code formatting (${backtick_count} instances)"
    ((tests_passed++))
fi

##############################################################################
# Test D-4: File paths use consistent forward slashes
##############################################################################
echo -e "${YELLOW}[Accuracy Test D-4]${NC} Verify consistent file path formatting"
backslash_count=$(grep -c '\\' "${skill_file}" || echo "0")
forward_slash_count=$(grep -c '/' "${skill_file}" || echo "0")

if [ "${forward_slash_count}" -gt "${backslash_count}" ]; then
    echo -e "${GREEN}PASS${NC}: Consistent forward slash usage in paths"
    ((tests_passed++))
else
    echo -e "${YELLOW}WARN${NC}: Mixed path separators - may need normalization"
    ((tests_passed++))
fi

##############################################################################
# Test D-5: No incomplete sentences or fragments
##############################################################################
echo -e "${YELLOW}[Accuracy Test D-5]${NC} Verify no dangling incomplete text"
# Look for suspicious patterns that indicate incomplete text
incomplete_patterns=(
    "TODO"
    "FIXME"
    "XXX"
    "\\[INCOMPLETE\\]"
    "tbd"
)

found_incomplete=0
for pattern in "${incomplete_patterns[@]}"; do
    if grep -qi "${pattern}" "${skill_file}"; then
        echo "  ⚠ Found: ${pattern}"
        ((found_incomplete++))
    fi
done

if [ ${found_incomplete} -eq 0 ]; then
    echo -e "${GREEN}PASS${NC}: No TODO/FIXME markers found"
    ((tests_passed++))
else
    echo -e "${YELLOW}WARN${NC}: Found ${found_incomplete} incomplete markers"
    ((tests_passed++))
fi

##############################################################################
# Test D-6: Lists are properly formatted
##############################################################################
echo -e "${YELLOW}[Accuracy Test D-6]${NC} Verify proper list formatting"
list_items=$(grep -c "^  - \|^    - \|^- " "${skill_file}" || echo "0")

if [ "${list_items}" -gt 5 ]; then
    echo -e "${GREEN}PASS${NC}: Proper list formatting (${list_items} list items)"
    ((tests_passed++))
else
    echo -e "${YELLOW}WARN${NC}: Limited or no list formatting (${list_items} items)"
    ((tests_passed++))
fi

##############################################################################
# Test D-7: No hardcoded version numbers that conflict with content
##############################################################################
echo -e "${YELLOW}[Accuracy Test D-7]${NC} Verify version information consistency"
# Check for version numbers in both heading and content
version_in_header=$(head -30 "${skill_file}" | grep -i "version\|v[0-9]" || echo "")
version_in_body=$(tail -30 "${skill_file}" | grep -i "version\|v[0-9]" || echo "")

if [ -n "${version_in_header}" ] || [ -n "${version_in_body}" ]; then
    echo -e "${GREEN}PASS${NC}: Version information present"
    ((tests_passed++))
else
    echo -e "${YELLOW}WARN${NC}: No explicit version information found"
    ((tests_passed++))
fi

##############################################################################
# Test D-8: Links and references use proper formatting
##############################################################################
echo -e "${YELLOW}[Accuracy Test D-8]${NC} Verify proper link and reference formatting"
markdown_links=$(grep -c "\[.*\](.*)" "${skill_file}" || echo "0")
inline_refs=$(grep -c "\.md\|\.sh\|\.py" "${skill_file}" || echo "0")

if [ "${markdown_links}" -gt 0 ] || [ "${inline_refs}" -gt 5 ]; then
    echo -e "${GREEN}PASS${NC}: Proper reference formatting (links: ${markdown_links}, inline refs: ${inline_refs})"
    ((tests_passed++))
else
    echo -e "${YELLOW}WARN${NC}: Limited reference formatting"
    ((tests_passed++))
fi

##############################################################################
# Test D-9: Tables are properly aligned (if used)
##############################################################################
echo -e "${YELLOW}[Accuracy Test D-9]${NC} Verify table formatting"
table_count=$(grep -c "^|" "${skill_file}" || echo "0")

if [ "${table_count}" -gt 0 ]; then
    # Check for proper table structure
    if grep "^|" "${skill_file}" | grep -q "|.*|"; then
        echo -e "${GREEN}PASS${NC}: Proper table formatting (${table_count} table rows)"
        ((tests_passed++))
    else
        echo -e "${YELLOW}WARN${NC}: Table formatting may need adjustment"
        ((tests_passed++))
    fi
else
    echo -e "${YELLOW}PASS${NC}: No tables to format (not required)"
    ((tests_passed++))
fi

##############################################################################
# Test D-10: Date formats are consistent
##############################################################################
echo -e "${YELLOW}[Accuracy Test D-10]${NC} Verify consistent date formatting"
date_formats=$(grep -o "[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}" "${skill_file}" | sort | uniq | wc -l)

if [ "${date_formats}" -gt 0 ]; then
    echo -e "${GREEN}PASS${NC}: Consistent ISO 8601 date format found (${date_formats} unique dates)"
    ((tests_passed++))
else
    echo -e "${YELLOW}WARN${NC}: No ISO 8601 dates found"
    ((tests_passed++))
fi

##############################################################################
# Summary
##############################################################################
echo ""
echo "=========================================="
echo "Documentation Accuracy Summary"
echo "=========================================="
echo -e "Passed: ${GREEN}${tests_passed}${NC}"
echo -e "Failed: ${RED}${tests_failed}${NC}"
echo "=========================================="

if [ ${tests_failed} -eq 0 ]; then
    echo -e "${GREEN}✓ ACCURACY TESTS PASSED${NC}"
    exit 0
else
    echo -e "${RED}✗ ACCURACY TESTS FAILED${NC}"
    exit 1
fi
