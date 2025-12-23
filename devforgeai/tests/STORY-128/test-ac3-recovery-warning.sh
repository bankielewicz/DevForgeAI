#!/bin/bash
################################################################################
# Test AC#3: Recovery Commands with Safety Warning
#
# Test that recovery steps include:
# - rm -f .git/index.lock
# And warning: "Only run this if no git processes are running"
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
echo "TEST AC#3: Recovery Commands with Safety Warning"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test 1: Recovery section exists
echo -n "Test 1: Recovery section exists... "
if grep -q "^### Recovery" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Recovery section in Lock File Recovery"
    echo "  Actual: Recovery section not found"
    exit 1
fi

# Test 2: rm -f .git/index.lock command documented
echo -n "Test 2: Command 'rm -f .git/index.lock' documented... "
if grep -q "rm -f .git/index.lock" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Command 'rm -f .git/index.lock' in Recovery section"
    echo "  Actual: Command not found in file"
    exit 1
fi

# Test 3: Safety warning present
echo -n "Test 3: Safety warning about git processes present... "
if grep -q "no git processes are running" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Warning text 'no git processes are running'"
    echo "  Actual: Warning not found"
    exit 1
fi

# Test 4: WARNING marker prominent
echo -n "Test 4: WARNING marker present (emphasis)... "
if grep -q "^**WARNING:**" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Bold WARNING marker '**WARNING:**'"
    echo "  Actual: WARNING marker not properly formatted"
    exit 1
fi

# Test 5: Recovery command is in code block
echo -n "Test 5: Recovery command in code block... "
if grep -A3 "^### Recovery" "$TARGET_FILE" 2>/dev/null | grep -q '```bash'; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Bash code block in Recovery section"
    echo "  Actual: Code block not found"
    exit 1
fi

# Test 6: Comment explaining recovery command
echo -n "Test 6: Comment explaining recovery command... "
if grep -q "Remove stale lock" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Comment explaining recovery intent"
    echo "  Actual: Comment not found"
    exit 1
fi

echo ""
echo -e "${GREEN}All AC#3 tests PASSED${NC}"
echo ""
