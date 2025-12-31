#!/bin/bash

###############################################################################
# TEST: Error Handling Section
###############################################################################
#
# Validates that .claude/commands/create-stories-from-rca.md includes
# comprehensive error handling documentation.
#
# Error Handling Requirements:
# - Handle story creation failure gracefully
# - Log detailed error messages
# - Continue processing remaining recommendations (BR-004)
# - Track failures for final report
# - Handle skill invocation failures
# - Handle context window limit errors
#
# Test Strategy:
# 1. Verify command file exists
# 2. Verify Error Handling section exists
# 3. Verify different error types are documented
# 4. Verify recovery mechanisms are documented
###############################################################################

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

COMMAND_FILE="./.claude/commands/create-stories-from-rca.md"
TEST_NAME="Error Handling Section"

echo -e "${YELLOW}Testing: ${TEST_NAME}${NC}"
echo "=================================================="

# Test 1: Command file exists
echo -n "Test EH.1: Command file exists... "
if [ ! -f "$COMMAND_FILE" ]; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: $COMMAND_FILE"
    echo "  Actual: File not found"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 2: Error Handling section exists
echo -n "Test EH.2: Error Handling section exists... "
if ! grep -q -i "## Error\|## error handling\|### Error\|## Edge Case" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Section documenting error handling"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 3: Story creation failure handling documented
echo -n "Test EH.3: Story creation failure handling documented... "
if ! grep -q -i "story.*creat.*fail\|creation.*fail\|validation.*error" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of handling story creation failures"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 4: Error logging documented
echo -n "Test EH.4: Error logging documented... "
if ! grep -q -i "log\|error.*message\|capture" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of logging error details"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 5: Graceful failure documented
echo -n "Test EH.5: Graceful failure documented... "
if ! grep -q -i "graceful\|continue\|proceed\|next" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of graceful failure and continuation"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 6: Failure tracking documented
echo -n "Test EH.6: Failure tracking documented... "
if ! grep -q -i "track\|record.*fail\|failed.*list\|failed.*array" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of tracking failed recommendations"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 7: Skill invocation failure handling documented
echo -n "Test EH.7: Skill invocation failure handling documented... "
if ! grep -q -i "skill.*fail\|invocation.*fail\|devforgeai-story-creation.*fail" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of handling skill invocation failures"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 8: Context window error documented
echo -n "Test EH.8: Context window error handling documented... "
if ! grep -q -i "context.*window\|too many\|batch.*size\|batch of 5" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of handling context window limits"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

echo ""
echo -e "${GREEN}✅ Error Handling Tests Passed${NC}"
exit 0
