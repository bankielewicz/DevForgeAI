#!/bin/bash

###############################################################################
# TEST: Business Rules Documentation
###############################################################################
#
# Validates that .claude/commands/create-stories-from-rca.md documents
# all business rules (BR-001 to BR-004).
#
# Business Rules:
# - BR-001: Priority Mapping (CRITICAL/HIGH -> High, MEDIUM -> Medium, LOW -> Low)
# - BR-002: Points Calculation (use recommendation effort_points or default 5)
# - BR-003: Story ID Generation (sequential STORY-NNN IDs with no gaps)
# - BR-004: Failure Isolation (failure in story N doesn't affect N+1)
#
# Test Strategy:
# 1. Verify command file exists
# 2. Verify Business Rules section exists
# 3. Verify each BR is documented with description and test requirement
###############################################################################

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

COMMAND_FILE="./.claude/commands/create-stories-from-rca.md"
TEST_NAME="Business Rules Documentation (BR-001 to BR-004)"

echo -e "${YELLOW}Testing: ${TEST_NAME}${NC}"
echo "=================================================="

# Test 1: Command file exists
echo -n "Test BR.1: Command file exists... "
if [ ! -f "$COMMAND_FILE" ]; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: $COMMAND_FILE"
    echo "  Actual: File not found"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 2: Business Rules section exists
echo -n "Test BR.2: Business Rules section exists... "
if ! grep -q -i "business.*rule\|## BR\|### BR\|BR-001" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Section documenting business rules"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 3: BR-001 (Priority Mapping) documented
echo -n "Test BR.3: BR-001 (Priority Mapping) documented... "
if ! grep -q -i "BR-001\|br-001\|priority.*mapping\|critical.*high" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of BR-001 (Priority Mapping)"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 4: BR-001 maps CRITICAL/HIGH to High
echo -n "Test BR.4: BR-001 priority mappings documented... "
if ! grep -q -i "critical\|HIGH" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of CRITICAL/HIGH -> High mapping"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 5: BR-002 (Points Calculation) documented
echo -n "Test BR.5: BR-002 (Points Calculation) documented... "
if ! grep -q -i "BR-002\|br-002\|point.*calculation\|effort" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of BR-002 (Points Calculation)"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 6: BR-002 references default 5
echo -n "Test BR.6: BR-002 default value (5) documented... "
if ! grep -q "default.*5\|default to 5" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of default 5 points if effort_points not available"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 7: BR-003 (Story ID Generation) documented
echo -n "Test BR.7: BR-003 (Story ID Generation) documented... "
if ! grep -q -i "BR-003\|br-003\|story.*id.*generation\|sequential.*STORY" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of BR-003 (Story ID Generation)"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 8: BR-003 references no gaps requirement
echo -n "Test BR.8: BR-003 no-gaps requirement documented... "
if ! grep -q -i "sequential\|no.*gap\|continuous" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of sequential ID generation with no gaps"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 9: BR-004 (Failure Isolation) documented
echo -n "Test BR.9: BR-004 (Failure Isolation) documented... "
if ! grep -q -i "BR-004\|br-004\|failure.*isolation\|continue" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of BR-004 (Failure Isolation)"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 10: BR-004 documents failure doesn't affect next
echo -n "Test BR.10: BR-004 isolation requirement documented... "
if ! grep -q -i "doesn't affect\|does not affect\|isolated\|independent" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation that failure in story N doesn't affect N+1"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

echo ""
echo -e "${GREEN}✅ Business Rules Tests Passed${NC}"
exit 0
