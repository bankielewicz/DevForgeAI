#!/bin/bash

################################################################################
# TEST: AC#1 - Story Template Updated with Change Log Section
#
# GIVEN the story template at
#   .claude/skills/devforgeai-story-creation/assets/templates/story-template.md
#   contains the current "## Workflow Status" section
# WHEN a developer creates a new story using the updated template
# THEN the "## Workflow Status" section is replaced with "## Change Log" containing:
#   - `**Current Status:** Backlog` header
#   - Table with columns: Date | Author | Phase/Action | Change | Files Affected
#   - Initial entry with author `claude/story-requirements-analyst` and action "Created"
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
echo "TEST: AC#1 - Story Template Updated with Change Log Section"
echo "================================================================"
echo ""

# Test 1: Template file exists
echo -n "TEST 1: Template file exists at expected location... "
if [ -f "$TEMPLATE_FILE" ]; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected file: $TEMPLATE_FILE"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 2: Template contains "## Change Log" section
echo -n "TEST 2: Template contains '## Change Log' header... "
if grep -q "^## Change Log" "$TEMPLATE_FILE"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: ## Change Log section not found"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 3: Template does NOT contain "## Workflow Status" section
echo -n "TEST 3: Template does NOT contain '## Workflow Status'... "
if ! grep -q "^## Workflow Status" "$TEMPLATE_FILE"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: ## Workflow Status should be removed"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 4: Change Log section contains "**Current Status:**" field
echo -n "TEST 4: Change Log contains '**Current Status:** Backlog'... "
if grep -A 5 "^## Change Log" "$TEMPLATE_FILE" | grep -q "\*\*Current Status:\*\*"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: **Current Status:** field in Change Log section"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 5: Change Log contains table with Date column header
echo -n "TEST 5: Change Log table has 'Date' column... "
if grep -A 10 "^## Change Log" "$TEMPLATE_FILE" | grep -q "^|.*Date.*|"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Table with Date column header"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 6: Change Log contains table with Author column header
echo -n "TEST 6: Change Log table has 'Author' column... "
if grep -A 10 "^## Change Log" "$TEMPLATE_FILE" | grep -q "^|.*Author.*|"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Table with Author column header"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 7: Change Log contains table with Phase/Action column header
echo -n "TEST 7: Change Log table has 'Phase/Action' column... "
if grep -A 10 "^## Change Log" "$TEMPLATE_FILE" | grep -q "^|.*Phase.*|"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Table with Phase/Action column header"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 8: Change Log contains table with Change column header
echo -n "TEST 8: Change Log table has 'Change' column... "
if grep -A 10 "^## Change Log" "$TEMPLATE_FILE" | grep -q "^|.*Change.*|"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Table with Change column header"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 9: Change Log contains table with Files Affected column header
echo -n "TEST 9: Change Log table has 'Files Affected' column... "
if grep -A 10 "^## Change Log" "$TEMPLATE_FILE" | grep -q "^|.*Files.*|"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Table with Files Affected column header"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 10: Change Log contains initial entry with claude/story-requirements-analyst author
echo -n "TEST 10: Initial entry has author 'claude/story-requirements-analyst'... "
if grep -A 20 "^## Change Log" "$TEMPLATE_FILE" | grep -q "claude/story-requirements-analyst"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Initial changelog entry with author claude/story-requirements-analyst"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 11: Change Log contains initial entry with action "Created"
echo -n "TEST 11: Initial entry has action 'Created'... "
if grep -A 20 "^## Change Log" "$TEMPLATE_FILE" | grep -q "Created"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Initial changelog entry with action 'Created'"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 12: Table has proper markdown formatting with separators
echo -n "TEST 12: Change Log table has markdown separators (|---|)... "
if grep -A 10 "^## Change Log" "$TEMPLATE_FILE" | grep -q "^|.*-.*|"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Markdown table with separator row"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Summary
echo ""
echo "================================================================"
echo "SUMMARY: AC#1 Tests"
echo "================================================================"
echo -e "PASSED: ${GREEN}${PASS_COUNT}${NC}"
echo -e "FAILED: ${RED}${FAIL_COUNT}${NC}"
echo "TOTAL:  $((PASS_COUNT + FAIL_COUNT))"
echo ""

if [ $FAIL_COUNT -eq 0 ]; then
    echo -e "${GREEN}All AC#1 tests PASSED${NC}"
    exit 0
else
    echo -e "${RED}Some AC#1 tests FAILED${NC}"
    exit 1
fi
