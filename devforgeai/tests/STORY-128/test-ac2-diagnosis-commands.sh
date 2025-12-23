#!/bin/bash
################################################################################
# Test AC#2: Diagnosis Commands Documented
#
# Test that diagnosis steps include:
# - ls -la .git/index.lock  # Check if lock exists
# - ps aux | grep git       # Check for running git processes
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
echo "TEST AC#2: Diagnosis Commands Documented"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test 1: ls -la .git/index.lock command documented
echo -n "Test 1: Command 'ls -la .git/index.lock' documented... "
if grep -q "ls -la .git/index.lock" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Command 'ls -la .git/index.lock' in Diagnosis section"
    echo "  Actual: Command not found in file"
    exit 1
fi

# Test 2: ps aux | grep git command documented
echo -n "Test 2: Command 'ps aux | grep git' documented... "
if grep -q "ps aux | grep git" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Command 'ps aux | grep git' in Diagnosis section"
    echo "  Actual: Command not found in file"
    exit 1
fi

# Test 3: Both commands in code block
echo -n "Test 3: Both commands are in a bash code block... "
if grep -A5 "^### Diagnosis" "$TARGET_FILE" 2>/dev/null | grep -q '```bash'; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Bash code block in Diagnosis section"
    echo "  Actual: No bash code block found"
    exit 1
fi

# Test 4: Comment explaining ls command
echo -n "Test 4: Comment explaining 'ls' command intent... "
if grep -q "Check if lock" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Comment explaining 'Check if lock' intent"
    echo "  Actual: Comment not found"
    exit 1
fi

# Test 5: Comment explaining ps command
echo -n "Test 5: Comment explaining 'ps' command intent... "
if grep -q "Check for running git" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Comment explaining git process check intent"
    echo "  Actual: Comment not found"
    exit 1
fi

echo ""
echo -e "${GREEN}All AC#2 tests PASSED${NC}"
echo ""
