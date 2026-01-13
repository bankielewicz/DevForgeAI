#!/bin/bash
# STORY-129 AC#5: Verify fallback validation patterns are documented

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

TARGET_FILE=".claude/skills/devforgeai-development/references/preflight/_index.md"

echo -e "${BLUE}=== STORY-129 AC#5: Fallback Documentation ===${NC}"
echo ""

# Test 5.1: Manual validation section exists
((TESTS_RUN++))
echo -n "Test 5.1: Contains 'Manual Validation' section... "
if grep -qi "Manual Validation\|Fallback Validation" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    ((TESTS_FAILED++))
fi

# Test 5.2: Grep-based fallback for hooks
((TESTS_RUN++))
echo -n "Test 5.2: Documents Grep-based hook validation... "
if grep -q "Grep.*hook\|grep.*hook" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    ((TESTS_FAILED++))
fi

# Test 5.3: Read-based fallback for context
((TESTS_RUN++))
echo -n "Test 5.3: Documents Read-based context validation... "
if grep -q "Read.*context\|context.*Read" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    ((TESTS_FAILED++))
fi

# Test 5.4: Documents risks of skipped validations
((TESTS_RUN++))
echo -n "Test 5.4: Documents risks or limitations... "
if grep -qi "risk\|limitation\|skip" "$TARGET_FILE" 2>/dev/null; then
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
    echo -e "${GREEN}✓ AC#5 PASSED${NC}"
    exit 0
else
    echo -e "${RED}✗ AC#5 FAILED${NC}"
    exit 1
fi
