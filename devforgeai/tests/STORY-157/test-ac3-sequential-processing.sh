#!/bin/bash

###############################################################################
# TEST: AC#3 - Create Stories Sequentially with Progress Display
###############################################################################
#
# Validates that .claude/commands/create-stories-from-rca.md documents
# sequential processing of recommendations with progress display.
#
# AC#3: Given multiple recommendations are selected for story creation
#       When creating stories
#       Then each story is created sequentially with progress display:
#       "[N/Total] Creating: {title}"
#
# Test Strategy:
# 1. Verify command file exists
# 2. Verify AC#3 pseudocode section exists
# 3. Verify sequential processing is documented
# 4. Verify progress display format is documented
# 5. Verify loop/iteration logic is documented
# 6. Verify title substitution is documented
###############################################################################

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

COMMAND_FILE="./.claude/commands/create-stories-from-rca.md"
TEST_NAME="AC#3: Create Stories Sequentially with Progress Display"

echo -e "${YELLOW}Testing: ${TEST_NAME}${NC}"
echo "=================================================="

# Test 1: Command file exists
echo -n "Test 3.1: Command file exists... "
if [ ! -f "$COMMAND_FILE" ]; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: $COMMAND_FILE"
    echo "  Actual: File not found"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 2: AC#3 section exists
echo -n "Test 3.2: AC#3 pseudocode section exists... "
if ! grep -q -i "## AC#3\|### AC#3\|^## AC#3\|^### AC#3" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Section '## AC#3' or '### AC#3' documenting sequential processing"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 3: Sequential processing documented
echo -n "Test 3.3: Sequential processing documented... "
if ! grep -q -i "sequen\|serial\|one.*at.*time\|loop\|for.*each" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of sequential (not parallel) story creation"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 4: Progress display format documented
echo -n "Test 3.4: Progress display format documented... "
if ! grep -q "\[.*\/.*\]\|Progress\|Creating" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of progress format '[N/Total] Creating: {title}'"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 5: Counter/iteration documented
echo -n "Test 3.5: Counter/iteration tracking documented... "
if ! grep -q -i "counter\|index\|count\|iteration\|N/Total" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of counter tracking (N/Total)"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 6: Title substitution documented
echo -n "Test 3.6: Title substitution documented... "
if ! grep -q -i "title\|feature.*name" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of substituting recommendation title in progress display"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 7: Display output documented
echo -n "Test 3.7: Display/output step documented... "
if ! grep -q -i "display\|print\|output\|echo\|log" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of how progress is displayed to user"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

echo ""
echo -e "${GREEN}✅ AC#3 Tests Passed${NC}"
exit 0
