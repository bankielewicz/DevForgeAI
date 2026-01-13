#!/bin/bash
# STORY-129 AC#1: Verify Step 0.0.5 (Phase 01.0.5) exists in preflight-validation.md

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

TARGET_FILE=".claude/skills/devforgeai-development/references/preflight/_index.md"

echo -e "${BLUE}=== STORY-129 AC#1: Step Exists ===${NC}"
echo ""

# Test 1.1: Section header exists
((TESTS_RUN++))
echo -n "Test 1.1: Phase 01.0.5 header exists... "
if grep -q "## Phase 01.0.5: CLI Availability Check" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    ((TESTS_FAILED++))
fi

# Test 1.2: Contains command -v check
((TESTS_RUN++))
echo -n "Test 1.2: Contains 'command -v devforgeai'... "
if grep -q "command -v devforgeai" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    ((TESTS_FAILED++))
fi

# Test 1.3: Sets CLI_AVAILABLE variable
((TESTS_RUN++))
echo -n "Test 1.3: Sets CLI_AVAILABLE variable... "
if grep -q "CLI_AVAILABLE" "$TARGET_FILE" 2>/dev/null; then
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
    echo -e "${GREEN}✓ AC#1 PASSED${NC}"
    exit 0
else
    echo -e "${RED}✗ AC#1 FAILED${NC}"
    exit 1
fi
