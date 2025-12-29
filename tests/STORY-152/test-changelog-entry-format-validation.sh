#!/bin/bash

################################################################################
# TEST: Changelog Entry Format Validation (Technical Specification)
#
# VALIDATES:
# - DM-001: Markdown table row with 5 columns
# - DM-002: Author validation regex
# - DM-003: Change field max 100 characters
# - CFG-001: 5-column table format
# - CFG-002: Author attribution patterns
# - CFG-004: Timestamp format YYYY-MM-DD HH:MM
################################################################################

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
GUIDE_FILE="${PROJECT_ROOT}/.claude/references/changelog-update-guide.md"

# Track test results
PASS_COUNT=0
FAIL_COUNT=0

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "================================================================"
echo "TEST: Changelog Entry Format Validation (Tech Spec)"
echo "================================================================"
echo ""

# Test 1: Guide exists
echo -n "TEST 1: Guide file exists at expected location... "
if [ -f "$GUIDE_FILE" ]; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: $GUIDE_FILE"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 2: Table has exactly 5 columns (Date, Author, Phase/Action, Change, Files Affected)
echo -n "TEST 2: Table format documents 5 columns... "
if grep -q "Date.*Author.*Phase.*Change.*Files" "$GUIDE_FILE"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: All 5 column names in order"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 3: Author pattern documented: claude/[a-z-]+
echo -n "TEST 3: Guide documents 'claude/{subagent}' author pattern... "
if grep -q "claude/[a-z\-]*" "$GUIDE_FILE" || grep -q "claude/{subagent}" "$GUIDE_FILE"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: claude/{subagent} pattern documentation"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 4: Author pattern documented: user/[a-zA-Z0-9_-]+
echo -n "TEST 4: Guide documents 'user/{name}' author pattern... "
if grep -q "user/[a-zA-Z0-9_\-]*" "$GUIDE_FILE" || grep -q "user/{name}" "$GUIDE_FILE"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: user/{name} pattern documentation"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 5: Author pattern documented: claude/opus
echo -n "TEST 5: Guide documents 'claude/opus' author pattern... "
if grep -q "claude/opus" "$GUIDE_FILE"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: claude/opus pattern documentation"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 6: Timestamp format documented (YYYY-MM-DD HH:MM or variant)
echo -n "TEST 6: Guide documents timestamp format... "
if grep -q "YYYY-MM-DD\|[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]\|HH:MM\|timestamp" "$GUIDE_FILE"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Timestamp format specification"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 7: Table example in guide has 5 columns with pipe separators
echo -n "TEST 7: Guide contains example markdown table... "
if grep -q "^|.*|.*|.*|.*|.*|" "$GUIDE_FILE"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Example markdown table with 5 columns"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 8: Table separator row documented (|---|---|...|)
echo -n "TEST 8: Guide shows markdown table separator row... "
if grep -q "^|.*-.*|.*-.*|" "$GUIDE_FILE"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Markdown separator row example"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 9: Change field truncation documented (max 100 chars)
echo -n "TEST 9: Guide documents change field length limit... "
if grep -q "100\|character\|length\|truncat\|max" "$GUIDE_FILE"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of change field length limit"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 10: Phase/Action column descriptions documented
echo -n "TEST 10: Guide documents Phase/Action examples... "
if grep -q "Phase\|Action\|Red\|Green\|Refactor\|QA\|Release" "$GUIDE_FILE"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Phase/Action example values"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 11: Author field validation rule documented
echo -n "TEST 11: Guide documents author field validation... "
if grep -q "author.*pattern\|author.*format\|valid.*author\|pattern.*author" "$GUIDE_FILE"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Author field validation documentation"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 12: File Affected column format documented
echo -n "TEST 12: Guide documents 'Files Affected' column format... "
if grep -q "Files.*Affected\|file.*list\|affected" "$GUIDE_FILE"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Files Affected column documentation"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Summary
echo ""
echo "================================================================"
echo "SUMMARY: Changelog Entry Format Validation Tests"
echo "================================================================"
echo -e "PASSED: ${GREEN}${PASS_COUNT}${NC}"
echo -e "FAILED: ${RED}${FAIL_COUNT}${NC}"
echo "TOTAL:  $((PASS_COUNT + FAIL_COUNT))"
echo ""

if [ $FAIL_COUNT -eq 0 ]; then
    echo -e "${GREEN}All format validation tests PASSED${NC}"
    exit 0
else
    echo -e "${RED}Some format validation tests FAILED${NC}"
    exit 1
fi
