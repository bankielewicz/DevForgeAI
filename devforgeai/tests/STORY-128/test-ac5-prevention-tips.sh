#!/bin/bash
################################################################################
# Test AC#5: Prevention Tips Documented
#
# Test that prevention guidance includes:
# - Close VS Code Git panels before terminal git operations
# - Use native WSL paths (/mnt/c/) not Windows paths (C:\)
# - Avoid running git from both Windows and WSL simultaneously
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
echo "TEST AC#5: Prevention Tips Documented"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test 1: Prevention section exists
echo -n "Test 1: Prevention section exists... "
if grep -q "^\\*\\*Prevention:" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Section '**Prevention:**'"
    echo "  Actual: Prevention section not found"
    exit 1
fi

# Test 2: Numbered list format (1., 2., 3., etc.)
echo -n "Test 2: Prevention tips in numbered list format... "
if grep -q "^1\\." "$TARGET_FILE" 2>/dev/null && grep -q "^2\\." "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Numbered list (1., 2., 3., etc.) for prevention tips"
    echo "  Actual: Numbered list format not found"
    exit 1
fi

# Test 3: First tip - Close VS Code Git panels
echo -n "Test 3: Tip 1 - Close VS Code Git panels before terminal git... "
if grep -q "1\\. Close VS Code" "$TARGET_FILE" 2>/dev/null && grep -q "terminal git" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Tip 1 about closing VS Code before terminal git"
    echo "  Actual: Not found or misformatted"
    exit 1
fi

# Test 4: Second tip - Use native WSL paths
echo -n "Test 4: Tip 2 - Use native WSL paths (/mnt/c/) not Windows... "
if grep -q "2\\." "$TARGET_FILE" 2>/dev/null && grep -q "native WSL" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Tip 2 about using native WSL paths vs Windows paths"
    echo "  Actual: Not found or misformatted"
    exit 1
fi

# Test 5: Third tip - Avoid running git from both Windows and WSL
echo -n "Test 5: Tip 3 - Avoid running git from both Windows and WSL... "
if grep -q "3\\." "$TARGET_FILE" 2>/dev/null && grep -q "Avoid running git from both" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Tip 3 about avoiding simultaneous git operations"
    echo "  Actual: Not found or misformatted"
    exit 1
fi

# Test 6: Path examples in tips
echo -n "Test 6: Example path /mnt/c/ in native paths tip... "
if grep -q "/mnt/c/" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Example '/mnt/c/' in native paths prevention tip"
    echo "  Actual: Path example not found"
    exit 1
fi

# Test 7: Windows path anti-pattern shown
echo -n "Test 7: Windows path anti-pattern (C:\\) shown... "
if grep -q "C:\\\\" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Windows path anti-pattern 'C:\\' shown"
    echo "  Actual: Not found"
    exit 1
fi

# Test 8: Same repo mentioned in Windows/WSL tip
echo -n "Test 8: 'same repo' mentioned in Windows/WSL simultaneous tip... "
if grep -q "same repo" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Mention of 'same repo' in Windows/WSL tip"
    echo "  Actual: Not found"
    exit 1
fi

echo ""
echo -e "${GREEN}All AC#5 tests PASSED${NC}"
echo ""
