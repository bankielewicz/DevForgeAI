#!/bin/bash
#
# STORY-166: AC#3 - Historical Story Guidance
# Test validates that CLAUDE.md includes guidance for older story format
#
# AC#3 Requirements:
# - Documentation notes that older stories (template v2.0) may have ### 1. [ ] format
# - Guidance explains this format is vestigial
# - Clear explanation that these checkboxes should never be checked
#
# Expected: FAILS (RED state - historical guidance doesn't exist yet)

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

TEST_NAME="AC#3: Historical Story Guidance for Older Format"
CLAUDE_MD_PATH="CLAUDE.md"

echo "Running: $TEST_NAME"
echo "==========================================="
echo ""

# Test 1: CLAUDE.md file exists
if [ ! -f "$CLAUDE_MD_PATH" ]; then
    echo -e "${RED}FAIL${NC}: CLAUDE.md file not found at $CLAUDE_MD_PATH"
    exit 1
fi
echo -e "${GREEN}PASS${NC}: CLAUDE.md file exists"

# Test 2: Verify guidance about older stories exists
if ! grep -iq "older stories\|template v2\|historical\|vestigial" "$CLAUDE_MD_PATH"; then
    echo -e "${RED}FAIL${NC}: CLAUDE.md does not contain guidance about older stories"
    echo "Expected content mentioning: older stories, template v2.0, or vestigial format"
    exit 1
fi
echo -e "${GREEN}PASS${NC}: Historical story guidance section found"

# Test 3: Verify reference to ### 1. [ ] checkbox format
if ! grep -q "### 1\. \[ \]\|### 1\|checkbox syntax.*vestigial\|v2\.0.*checkbox" "$CLAUDE_MD_PATH"; then
    echo -e "${RED}FAIL${NC}: CLAUDE.md does not reference the ### 1. [ ] checkbox format"
    echo "Expected: mention of '### 1. [ ]' format or similar old template reference"
    exit 1
fi
echo -e "${GREEN}PASS${NC}: Reference to old ### 1. [ ] format found"

# Test 4: Verify explanation that these checkboxes are never meant to be checked
if ! grep -iq "never.*meant to be checked\|never.*check.*old\|checkboxes.*vestigial\|should not.*check" "$CLAUDE_MD_PATH"; then
    echo -e "${RED}FAIL${NC}: CLAUDE.md does not explain that old checkboxes should never be checked"
    echo "Expected: explanation that old checkbox format should never be marked"
    exit 1
fi
echo -e "${GREEN}PASS${NC}: Explanation that old checkboxes should not be marked found"

# Test 5: Verify guidance to look at DoD for actual status in old stories
if ! grep -iq "look.*dod\|dod.*section.*actual\|old.*stories.*dod\|check.*dod" "$CLAUDE_MD_PATH"; then
    echo -e "${RED}FAIL${NC}: CLAUDE.md does not guide to check DoD section for old stories"
    echo "Expected: guidance to look at Definition of Done for actual completion in old stories"
    exit 1
fi
echo -e "${GREEN}PASS${NC}: Guidance to check DoD section for old stories found"

echo ""
echo "==========================================="
echo -e "${GREEN}ALL AC#3 TESTS PASSED${NC}"
echo ""
exit 0
