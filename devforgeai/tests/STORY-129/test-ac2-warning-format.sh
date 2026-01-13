#!/bin/bash
# STORY-129 AC#2: Verify warning message format when CLI not installed

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

TARGET_FILE=".claude/skills/devforgeai-development/references/preflight/_index.md"

echo -e "${BLUE}=== STORY-129 AC#2: Warning Format ===${NC}"
echo ""

# Test 2.1: Warning message exists
((TESTS_RUN++))
echo -n "Test 2.1: Contains 'WARN: devforgeai CLI not installed'... "
if grep -q "WARN: devforgeai CLI not installed" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    ((TESTS_FAILED++))
fi

# Test 2.2: Hook skip message exists
((TESTS_RUN++))
echo -n "Test 2.2: Contains 'Hook checks will be skipped'... "
if grep -q "Hook checks will be skipped" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    ((TESTS_FAILED++))
fi

# Test 2.3: Manual validation message exists
((TESTS_RUN++))
echo -n "Test 2.3: Contains 'Manual validation required'... "
if grep -q "Manual validation required" "$TARGET_FILE" 2>/dev/null; then
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
    echo -e "${GREEN}✓ AC#2 PASSED${NC}"
    exit 0
else
    echo -e "${RED}✗ AC#2 FAILED${NC}"
    exit 1
fi
