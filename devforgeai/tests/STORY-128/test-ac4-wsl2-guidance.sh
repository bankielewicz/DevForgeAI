#!/bin/bash
################################################################################
# Test AC#4: WSL2-Specific Guidance
#
# Test that section documents:
# - Common causes in WSL2 (VS Code, cross-filesystem, crashes)
# - Prevention tips (close VS Code Git panels, use native paths)
################################################################################

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test file location
TARGET_FILE=".claude/skills/devforgeai-development/references/git-workflow-conventions.md"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST AC#4: WSL2-Specific Guidance"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test 1: WSL2-Specific Notes section exists
echo -n "Test 1: WSL2-Specific Notes section exists... "
if grep -q "^### WSL2-Specific" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Section '### WSL2-Specific Notes'"
    echo "  Actual: Section not found"
    exit 1
fi

# Test 2: Common Causes subsection
echo -n "Test 2: Common Causes subsection exists... "
if grep -q "^\\*\\*Common Causes:" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Subsection '**Common Causes:**'"
    echo "  Actual: Common Causes section not found"
    exit 1
fi

# Test 3: VS Code mentioned as cause
echo -n "Test 3: VS Code with Git extension mentioned... "
if grep -q "VS Code" "$TARGET_FILE" 2>/dev/null && grep -q "Git extension" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: 'VS Code' and 'Git extension' mentioned in causes"
    echo "  Actual: One or both not found"
    exit 1
fi

# Test 4: Cross-filesystem cause mentioned
echo -n "Test 4: Cross-filesystem cause mentioned... "
if grep -q "Cross-filesystem" "$TARGET_FILE" 2>/dev/null || grep -q "cross-filesystem" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Cross-filesystem cause documented"
    echo "  Actual: Cross-filesystem not mentioned"
    exit 1
fi

# Test 5: Crash without cleanup mentioned
echo -n "Test 5: Git crash cause mentioned... "
if grep -q "crashed without cleanup" "$TARGET_FILE" 2>/dev/null || grep -q "crash without cleanup" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Crash without cleanup cause documented"
    echo "  Actual: Crash cause not mentioned"
    exit 1
fi

# Test 6: Prevention section exists
echo -n "Test 6: Prevention section exists... "
if grep -q "^\\*\\*Prevention:" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Subsection '**Prevention:**'"
    echo "  Actual: Prevention section not found"
    exit 1
fi

# Test 7: Close VS Code Git panels prevention tip
echo -n "Test 7: Close VS Code Git panels mentioned... "
if grep -q "Close VS Code" "$TARGET_FILE" 2>/dev/null && grep -q "Git panel" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Prevention tip about closing VS Code Git panels"
    echo "  Actual: Not found"
    exit 1
fi

# Test 8: Native WSL paths mentioned
echo -n "Test 8: Native WSL paths (/mnt/c/) mentioned... "
if grep -q "/mnt/c/" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Native WSL path '/mnt/c/' example"
    echo "  Actual: Not found"
    exit 1
fi

# Test 9: Windows paths (C:\) mentioned as anti-pattern
echo -n "Test 9: Windows paths (C:\\) mentioned as anti-pattern... "
if grep -q "C:\\\\" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Windows path example 'C:\\' as anti-pattern"
    echo "  Actual: Not found"
    exit 1
fi

echo ""
echo -e "${GREEN}All AC#4 tests PASSED${NC}"
echo ""
