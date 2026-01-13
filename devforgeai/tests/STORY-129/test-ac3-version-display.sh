#!/bin/bash
# STORY-129 AC#3: Verify CLI version display format when CLI available

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

TARGET_FILE=".claude/skills/devforgeai-development/references/preflight/_index.md"

echo -e "${BLUE}=== STORY-129 AC#3: Version Display ===${NC}"
echo ""

# Test 3.1: Success message format
((TESTS_RUN++))
echo -n "Test 3.1: Contains '✓ devforgeai CLI:' pattern... "
if grep -q "✓ devforgeai CLI:" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    ((TESTS_FAILED++))
fi

# Test 3.2: Version retrieval command
((TESTS_RUN++))
echo -n "Test 3.2: Contains '--version' check... "
if grep -q "devforgeai --version\|--version" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    ((TESTS_FAILED++))
fi

# Summary
echo ""
echo -e "${BLUE}=== Results ===${NC}"
echo "Tests run: $TESTS_RUN"
echo -e "Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Failed: ${RED}$TESTS_FAILED${NC}"

if [ "$TESTS_FAILED" -eq 0 ]; then
    echo -e "${GREEN}✓ AC#3 PASSED${NC}"
    exit 0
else
    echo -e "${RED}✗ AC#3 FAILED${NC}"
    exit 1
fi
