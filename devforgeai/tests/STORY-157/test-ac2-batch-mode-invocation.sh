#!/bin/bash

###############################################################################
# TEST: AC#2 - Invoke Story Creation Skill in Batch Mode
###############################################################################
#
# Validates that .claude/commands/create-stories-from-rca.md documents
# how the devforgeai-story-creation skill is invoked in batch mode.
#
# AC#2: Given batch context markers are set for a recommendation
#       When invoking devforgeai-story-creation skill
#       Then the skill executes in batch mode (skipping Phase 1 questions,
#       executing Phases 2-7)
#
# Test Strategy:
# 1. Verify command file exists
# 2. Verify AC#2 pseudocode section exists
# 3. Verify batch mode invocation is documented
# 4. Verify Skill() call syntax documented
# 5. Verify Phase 1 skipping is documented
# 6. Verify Phases 2-7 execution is documented
###############################################################################

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

COMMAND_FILE="./.claude/commands/create-stories-from-rca.md"
TEST_NAME="AC#2: Invoke Story Creation Skill in Batch Mode"

echo -e "${YELLOW}Testing: ${TEST_NAME}${NC}"
echo "=================================================="

# Test 1: Command file exists
echo -n "Test 2.1: Command file exists... "
if [ ! -f "$COMMAND_FILE" ]; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: $COMMAND_FILE"
    echo "  Actual: File not found"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 2: AC#2 section exists
echo -n "Test 2.2: AC#2 pseudocode section exists... "
if ! grep -q -i "## AC#2\|### AC#2\|^## AC#2\|^### AC#2" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Section '## AC#2' or '### AC#2' documenting skill invocation"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 3: Batch mode invocation documented
echo -n "Test 2.3: Batch mode invocation documented... "
if ! grep -q -i "batch.*mode\|batch mode\|batch_mode" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of batch mode invocation"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 4: Skill invocation documented (Skill() API call)
echo -n "Test 2.4: Skill() invocation documented... "
if ! grep -q "Skill\|skill\|devforgeai-story-creation" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of Skill() API call to devforgeai-story-creation"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 5: Phase 1 skipping documented
echo -n "Test 2.5: Phase 1 skipping documented... "
if ! grep -q -i "phase.*1\|phase 1\|skip.*phase" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation that Phase 1 questions are skipped in batch mode"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 6: Phases 2-7 execution documented
echo -n "Test 2.6: Phases 2-7 execution documented... "
if ! grep -q -i "phase.*2\|phase 2\|phase.*3\|phase.*7\|execute" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation that Phases 2-7 execute in batch mode"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 7: Context markers mentioned
echo -n "Test 2.7: Context markers passed to skill... "
if ! grep -q -i "context.*marker\|batch.*context\|marker" "$COMMAND_FILE"; then
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of context markers passed to devforgeai-story-creation"
    exit 1
fi
echo -e "${GREEN}PASS${NC}"

echo ""
echo -e "${GREEN}✅ AC#2 Tests Passed${NC}"
exit 0
