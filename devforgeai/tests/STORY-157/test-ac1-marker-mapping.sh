#!/bin/bash

###############################################################################
# TEST: AC#1 - Map Recommendation Fields to Story Batch Markers
###############################################################################
#
# Validates that .claude/commands/create-stories-from-rca.md documents
# the mapping from RCA recommendation fields to story batch context markers.
#
# AC#1: Given selected recommendations with priority, title, description,
#       effort, and success criteria
#       When preparing for story creation
#       Then fields are mapped to devforgeai-story-creation batch context
#       markers (Story ID, Epic ID, Feature Name, Priority, Points, Type,
#       Sprint, Batch Mode: true)
#
# Test Strategy:
# 1. Verify command file exists
# 2. Verify YAML frontmatter has required fields
# 3. Verify AC#1 pseudocode section exists
# 4. Verify field mapping is documented
###############################################################################

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

COMMAND_FILE="./.claude/commands/create-stories-from-rca.md"
TEST_NAME="AC#1: Map Recommendation Fields to Story Batch Markers"

echo -e "${YELLOW}Testing: ${TEST_NAME}${NC}"
echo "=================================================="

# Test 1: Command file exists
echo -n "Test 1.1: Command file exists... "
if [ ! -f "$COMMAND_FILE" ]; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: $COMMAND_FILE"
    echo "  Actual: File not found"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 2: YAML frontmatter has name field
echo -n "Test 1.2: YAML frontmatter has 'name' field... "
if ! grep -q "^name:" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: YAML field 'name:' in frontmatter"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 3: YAML frontmatter has description field
echo -n "Test 1.3: YAML frontmatter has 'description' field... "
if ! grep -q "^description:" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: YAML field 'description:' in frontmatter"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 4: YAML frontmatter has argument-hint field
echo -n "Test 1.4: YAML frontmatter has 'argument-hint' field... "
if ! grep -q "^argument-hint:" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: YAML field 'argument-hint:' in frontmatter"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 5: AC#1 section exists
echo -n "Test 1.5: AC#1 pseudocode section exists... "
if ! grep -q -i "## AC#1\|### AC#1\|^## AC#1\|^### AC#1" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Section '## AC#1' or '### AC#1' documenting marker mapping"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 6: Priority mapping documented (CRITICAL/HIGH -> High)
echo -n "Test 1.6: Priority mapping documented... "
if ! grep -q -i "priority.*[Hh]igh\|CRITICAL\|HIGH" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of priority mapping (CRITICAL/HIGH -> High)"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 7: Story ID mapping documented
echo -n "Test 1.7: Story ID mapping documented... "
if ! grep -q -i "story.*id\|story-id\|STORY-" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of Story ID mapping (next available STORY-NNN)"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 8: Points/Effort mapping documented
echo -n "Test 1.8: Points/Effort mapping documented... "
if ! grep -q -i "point\|effort" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of effort_points mapping (or default 5)"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 9: Batch mode marker documented (batch_mode: true)
echo -n "Test 1.9: Batch mode marker documented... "
if ! grep -q -i "batch.*mode\|batch_mode" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of batch_mode: true setting"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

echo ""
echo -e "${GREEN}✅ AC#1 Tests Passed${NC}"
exit 0
