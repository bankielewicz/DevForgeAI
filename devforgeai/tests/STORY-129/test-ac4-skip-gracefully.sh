#!/bin/bash
# STORY-129 AC#4: Verify downstream steps skip CLI calls gracefully

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

TARGET_FILE=".claude/skills/devforgeai-development/references/preflight/_index.md"

echo -e "${BLUE}=== STORY-129 AC#4: Skip Gracefully ===${NC}"
echo ""

# Test 4.1: Skip message format
((TESTS_RUN++))
echo -n "Test 4.1: Contains 'Skipping:' pattern for CLI calls... "
if grep -q "Skipping:" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    ((TESTS_FAILED++))
fi

# Test 4.2: CLI not available message
((TESTS_RUN++))
echo -n "Test 4.2: Contains 'CLI not available' message... "
if grep -q "CLI not available" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    ((TESTS_FAILED++))
fi

# Test 4.3: Lists CLI commands that get skipped
((TESTS_RUN++))
echo -n "Test 4.3: Lists commands to skip (check-hooks, validate-dod, validate-context)... "
skip_count=0
grep -q "check-hooks" "$TARGET_FILE" 2>/dev/null && ((skip_count++))
grep -q "validate-dod" "$TARGET_FILE" 2>/dev/null && ((skip_count++))
grep -q "validate-context" "$TARGET_FILE" 2>/dev/null && ((skip_count++))
if [ "$skip_count" -ge 2 ]; then
    echo -e "${GREEN}PASS${NC} (found $skip_count/3)"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC} (found $skip_count/3)"
    ((TESTS_FAILED++))
fi

# Summary
echo ""
echo -e "${BLUE}=== Results ===${NC}"
echo "Tests run: $TESTS_RUN"
echo -e "Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Failed: ${RED}$TESTS_FAILED${NC}"

if [ "$TESTS_FAILED" -eq 0 ]; then
    echo -e "${GREEN}✓ AC#4 PASSED${NC}"
    exit 0
else
    echo -e "${RED}✗ AC#4 FAILED${NC}"
    exit 1
fi
