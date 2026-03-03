#!/bin/bash

################################################################################
# TEST: AC#2 - Shared Changelog Reference Guide Created
#
# GIVEN the changelog-update-guide.md file is created at
#   .claude/references/changelog-update-guide.md
# WHEN devforgeai-development, devforgeai-qa, and devforgeai-release skills
#   execute their workflows
# THEN each skill references this shared guide and appends entries with
#   consistent format where author matches pattern
#   ^(claude/[a-z-]+|user/[a-zA-Z0-9_-]+|claude/opus)$
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
echo "TEST: AC#2 - Shared Changelog Reference Guide Created"
echo "================================================================"
echo ""

# Test 1: Guide file exists
echo -n "TEST 1: Guide file exists at '.claude/references/changelog-update-guide.md'... "
if [ -f "$GUIDE_FILE" ]; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected file: $GUIDE_FILE"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 2: Guide contains format specification section
echo -n "TEST 2: Guide contains 'Format Specification' section... "
if grep -q "Format Specification\|Table Format\|Column Format" "$GUIDE_FILE"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Format specification documentation"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 3: Guide documents 5-column table format
echo -n "TEST 3: Guide documents 5-column table (Date|Author|Phase|Change|Files)... "
if grep -q "Date.*Author.*Phase.*Change.*Files" "$GUIDE_FILE"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of 5-column table format"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 4: Guide contains author pattern regex or specification
echo -n "TEST 4: Guide contains author pattern specification... "
if grep -q "author\|pattern\|regex\|format" "$GUIDE_FILE" | head -1; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Author pattern specification in guide"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 5: Guide specifies valid author patterns (claude/...)
echo -n "TEST 5: Guide documents valid author pattern: claude/{subagent}... "
if grep -q "claude/" "$GUIDE_FILE"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Example of claude/{subagent} author pattern"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 6: Guide specifies valid author patterns (user/...)
echo -n "TEST 6: Guide documents valid author pattern: user/{name}... "
if grep -q "user/" "$GUIDE_FILE"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Example of user/{name} author pattern"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 7: Guide specifies valid author pattern (claude/opus)
echo -n "TEST 7: Guide documents valid author pattern: claude/opus... "
if grep -q "claude/opus" "$GUIDE_FILE"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Example of claude/opus author pattern"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 8: Guide contains Edit tool snippet for appending entries
echo -n "TEST 8: Guide contains Edit tool snippet for appending... "
if grep -q "Edit\|append\|add.*entry" "$GUIDE_FILE"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Edit tool snippet for appending changelog entries"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 9: Guide documents timestamp format (YYYY-MM-DD HH:MM or similar)
echo -n "TEST 9: Guide documents timestamp format... "
if grep -q "YYYY-MM-DD\|[0-9][0-9][0-9][0-9]-\|timestamp\|date.*time\|HH:MM" "$GUIDE_FILE"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Timestamp format documentation"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 10: Guide contains example changelog entry
echo -n "TEST 10: Guide contains example changelog entry... "
if grep -q "^|.*|.*|.*|.*|" "$GUIDE_FILE"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Example markdown table entry in guide"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 11: Guide is readable markdown file
echo -n "TEST 11: Guide is valid markdown file... "
if head -1 "$GUIDE_FILE" | grep -q "^#\|^---"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Valid markdown structure"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 12: Guide contains instruction for skills/subagents
echo -n "TEST 12: Guide contains instructions for skills/subagents... "
if grep -q "skill\|workflow\|subagent\|phase\|development\|qa\|release" "$GUIDE_FILE"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Instructions for skills to follow guide"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Summary
echo ""
echo "================================================================"
echo "SUMMARY: AC#2 Tests"
echo "================================================================"
echo -e "PASSED: ${GREEN}${PASS_COUNT}${NC}"
echo -e "FAILED: ${RED}${FAIL_COUNT}${NC}"
echo "TOTAL:  $((PASS_COUNT + FAIL_COUNT))"
echo ""

if [ $FAIL_COUNT -eq 0 ]; then
    echo -e "${GREEN}All AC#2 tests PASSED${NC}"
    exit 0
else
    echo -e "${RED}Some AC#2 tests FAILED${NC}"
    exit 1
fi
