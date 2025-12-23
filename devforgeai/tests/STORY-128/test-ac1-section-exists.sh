#!/bin/bash
################################################################################
# Test AC#1: Lock File Recovery Section Exists
#
# Test that a "Lock File Recovery" section exists in git-workflow-conventions.md
# with diagnosis commands, recovery commands, and safety warnings
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
echo "TEST AC#1: Lock File Recovery Section Exists"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test 1: Section header exists
echo -n "Test 1: Section header '## Lock File Recovery' exists... "
if grep -q "^## Lock File Recovery" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Section header '## Lock File Recovery' in file"
    echo "  Actual: Section header not found"
    exit 1
fi

# Test 2: Problem subsection exists
echo -n "Test 2: Problem subsection exists... "
if grep -q "^### Problem" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Subsection '### Problem' under Lock File Recovery"
    echo "  Actual: Problem subsection not found"
    exit 1
fi

# Test 3: Diagnosis subsection exists
echo -n "Test 3: Diagnosis subsection exists... "
if grep -q "^### Diagnosis" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Subsection '### Diagnosis' under Lock File Recovery"
    echo "  Actual: Diagnosis subsection not found"
    exit 1
fi

# Test 4: Recovery subsection exists
echo -n "Test 4: Recovery subsection exists... "
if grep -q "^### Recovery" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Subsection '### Recovery' under Lock File Recovery"
    echo "  Actual: Recovery subsection not found"
    exit 1
fi

# Test 5: WSL2-Specific Notes subsection exists
echo -n "Test 5: WSL2-Specific Notes subsection exists... "
if grep -q "^### WSL2-Specific" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Subsection '### WSL2-Specific Notes' under Lock File Recovery"
    echo "  Actual: WSL2-Specific Notes subsection not found"
    exit 1
fi

# Test 6: Safety warning exists
echo -n "Test 6: Safety warning exists... "
if grep -q "WARNING" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: WARNING text in recovery section"
    echo "  Actual: Warning not found"
    exit 1
fi

echo ""
echo -e "${GREEN}All AC#1 tests PASSED${NC}"
echo ""
