#!/bin/bash

###############################################################################
# TEST: AC#4 - Handle Story Creation Failure
###############################################################################
#
# Validates that .claude/commands/create-stories-from-rca.md documents
# error handling for individual story creation failures.
#
# AC#4: Given story creation fails for a recommendation (e.g., validation error)
#       When the failure occurs
#       Then log the error, continue to next recommendation (BR-004),
#       and include in failure report
#
# Test Strategy:
# 1. Verify command file exists
# 2. Verify AC#4 pseudocode section exists
# 3. Verify error logging is documented
# 4. Verify continuation logic is documented (BR-004)
# 5. Verify failure tracking is documented
# 6. Verify failure report inclusion is documented
###############################################################################

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

COMMAND_FILE="./.claude/commands/create-stories-from-rca.md"
TEST_NAME="AC#4: Handle Story Creation Failure"

echo -e "${YELLOW}Testing: ${TEST_NAME}${NC}"
echo "=================================================="

# Test 1: Command file exists
echo -n "Test 4.1: Command file exists... "
if [ ! -f "$COMMAND_FILE" ]; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: $COMMAND_FILE"
    echo "  Actual: File not found"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 2: AC#4 section exists
echo -n "Test 4.2: AC#4 pseudocode section exists... "
if ! grep -q -i "## AC#4\|### AC#4\|^## AC#4\|^### AC#4" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Section '## AC#4' or '### AC#4' documenting error handling"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 3: Error handling documented
echo -n "Test 4.3: Error handling documented... "
if ! grep -q -i "error\|catch\|exception\|fail" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of error handling for story creation failures"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 4: Error logging documented
echo -n "Test 4.4: Error logging documented... "
if ! grep -q -i "log\|record\|capture.*error" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of logging the error message"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 5: Continuation logic documented (BR-004)
echo -n "Test 4.5: Continuation logic documented (BR-004)... "
if ! grep -q -i "continue\|next\|proceed\|br-004" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of continuing to next recommendation (BR-004)"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 6: Failure tracking documented
echo -n "Test 4.6: Failure tracking documented... "
if ! grep -q -i "fail.*track\|track.*fail\|failed.*array\|fail.*list" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of tracking failed stories"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 7: Failure report inclusion documented
echo -n "Test 4.7: Failure report inclusion documented... "
if ! grep -q -i "report\|summary\|include.*fail" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of including failed stories in final report"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 8: BR-004 referenced
echo -n "Test 4.8: Business rule BR-004 referenced... "
if ! grep -q -i "BR-004\|br-004\|failure.*isolation" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Reference to BR-004 (Failure Isolation)"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

echo ""
echo -e "${GREEN}✅ AC#4 Tests Passed${NC}"
exit 0
