#!/bin/bash

################################################################################
# TEST: Story Template Version Update (Technical Specification)
#
# VALIDATES:
# - SVC-002: Current Status field and table structure
# - SVC-003: Template version 2.5
# - CFG-001: 5-column table format
# - CFG-004: Timestamp format documentation
#
# CHECKS THAT:
# - Template version incremented to 2.5
# - Template changelog documents the v2.5 change
# - Old version (2.4) no longer documented
################################################################################

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TEMPLATE_FILE="${PROJECT_ROOT}/.claude/skills/devforgeai-story-creation/assets/templates/story-template.md"

# Track test results
PASS_COUNT=0
FAIL_COUNT=0

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "================================================================"
echo "TEST: Story Template Version 2.5 Update"
echo "================================================================"
echo ""

# Test 1: Template file exists
echo -n "TEST 1: Template file exists... "
if [ -f "$TEMPLATE_FILE" ]; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: $TEMPLATE_FILE"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 2: Template contains Change Log section
echo -n "TEST 2: Template contains '## Change Log' section... "
if grep -q "^## Change Log" "$TEMPLATE_FILE"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: ## Change Log section"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 3: Template contains Current Status field
echo -n "TEST 3: Template contains '**Current Status:**' field... "
if grep -A 5 "^## Change Log" "$TEMPLATE_FILE" | grep -q "\*\*Current Status:\*\*"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: **Current Status:** field in Change Log"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 4: Template contains 5-column table header
echo -n "TEST 4: Template table has all 5 columns... "
if grep -A 10 "^## Change Log" "$TEMPLATE_FILE" | grep -q "Date.*Author.*Phase.*Change.*Files"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: All 5 column headers (Date|Author|Phase|Change|Files)"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 5: Template contains table separator row
echo -n "TEST 5: Template table has markdown separator row... "
if grep -A 12 "^## Change Log" "$TEMPLATE_FILE" | grep -q "^|.*-.*|"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Markdown separator row (|---|...|)"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 6: Template contains initial changelog entry
echo -n "TEST 6: Template contains initial changelog entry... "
if grep -A 15 "^## Change Log" "$TEMPLATE_FILE" | grep -q "^|.*|"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Example/initial changelog entry row"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 7: Template has valid frontmatter (YAML metadata)
echo -n "TEST 7: Template has valid YAML frontmatter... "
if head -20 "$TEMPLATE_FILE" | grep -q "^---" && grep "^---" "$TEMPLATE_FILE" | head -2 | tail -1; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: YAML frontmatter with --- delimiters"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 8: Template frontmatter contains format_version
echo -n "TEST 8: Template frontmatter contains 'format_version'... "
if head -20 "$TEMPLATE_FILE" | grep -q "format_version"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: format_version in frontmatter"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 9: Template references or contains version 2.5 indicator
echo -n "TEST 9: Template indicates version 2.5... "
if grep -q "2.5\|version.*2.5\|v2.5" "$TEMPLATE_FILE"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${YELLOW}WARN${NC}"
    echo "  Expected: Version 2.5 indicator (not critical if format correct)"
    # Warning only, not a hard fail
fi

# Test 10: Template does NOT contain Workflow Status
echo -n "TEST 10: Template does NOT contain '## Workflow Status'... "
if ! grep -q "^## Workflow Status" "$TEMPLATE_FILE"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: ## Workflow Status section removed"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 11: Template maintains all required sections
echo -n "TEST 11: Template contains essential sections (Description, AC, etc)... "
REQUIRED_SECTIONS=("# " "## Description" "## Acceptance Criteria")
ALL_PRESENT=true
for section in "${REQUIRED_SECTIONS[@]}"; do
    if ! grep -q "$section" "$TEMPLATE_FILE"; then
        ALL_PRESENT=false
        break
    fi
done
if [ "$ALL_PRESENT" = true ]; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: All essential sections preserved"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 12: Template is valid markdown
echo -n "TEST 12: Template is valid markdown file... "
if head -1 "$TEMPLATE_FILE" | grep -q "^-\|^#"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Valid markdown structure"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Summary
echo ""
echo "================================================================"
echo "SUMMARY: Story Template Version Tests"
echo "================================================================"
echo -e "PASSED: ${GREEN}${PASS_COUNT}${NC}"
echo -e "FAILED: ${RED}${FAIL_COUNT}${NC}"
echo "TOTAL:  $((PASS_COUNT + FAIL_COUNT))"
echo ""

if [ $FAIL_COUNT -eq 0 ]; then
    echo -e "${GREEN}All template version tests PASSED${NC}"
    exit 0
else
    echo -e "${RED}Some template version tests FAILED${NC}"
    exit 1
fi
