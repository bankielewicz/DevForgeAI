#!/bin/bash

###############################################################################
# TEST: AC#5 - Report Success and Failure Summary
###############################################################################
#
# Validates that .claude/commands/create-stories-from-rca.md documents
# the summary report output format and content.
#
# AC#5: Given all selected recommendations have been processed
#       When batch creation completes
#       Then display summary: "✅ Created: N stories" and
#       "❌ Failed: M stories" with story IDs and failure reasons
#
# Test Strategy:
# 1. Verify command file exists
# 2. Verify AC#5 pseudocode section exists
# 3. Verify success message format is documented
# 4. Verify failure message format is documented
# 5. Verify story ID inclusion is documented
# 6. Verify failure reason inclusion is documented
###############################################################################

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

COMMAND_FILE="./.claude/commands/create-stories-from-rca.md"
TEST_NAME="AC#5: Report Success and Failure Summary"

echo -e "${YELLOW}Testing: ${TEST_NAME}${NC}"
echo "=================================================="

# Test 1: Command file exists
echo -n "Test 5.1: Command file exists... "
if [ ! -f "$COMMAND_FILE" ]; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: $COMMAND_FILE"
    echo "  Actual: File not found"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 2: AC#5 section exists
echo -n "Test 5.2: AC#5 pseudocode section exists... "
if ! grep -q -i "## AC#5\|### AC#5\|^## AC#5\|^### AC#5" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Section '## AC#5' or '### AC#5' documenting summary report"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 3: Success message format documented
echo -n "Test 5.3: Success message format documented... "
if ! grep -q "Created\|✅\|success.*N\|created.*stories" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of success message '✅ Created: N stories'"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 4: Failure message format documented
echo -n "Test 5.4: Failure message format documented... "
if ! grep -q "Failed\|❌\|failed.*M\|failed.*stories" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of failure message '❌ Failed: M stories'"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 5: Story ID inclusion documented
echo -n "Test 5.5: Story ID inclusion in report documented... "
if ! grep -q -i "story.*id\|STORY-\|story ids" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of including story IDs in report"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 6: Failure reason inclusion documented
echo -n "Test 5.6: Failure reason inclusion in report documented... "
if ! grep -q -i "reason\|error.*message\|cause" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of including failure reasons in report"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 7: Report display documented
echo -n "Test 5.7: Report display/output documented... "
if ! grep -q -i "display\|print\|output\|report.*display" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of how report is displayed"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 8: Completion documentation
echo -n "Test 5.8: Batch completion state documented... "
if ! grep -q -i "complet\|finish\|all.*processed" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of batch creation completion"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

echo ""
echo -e "${GREEN}✅ AC#5 Tests Passed${NC}"
exit 0
