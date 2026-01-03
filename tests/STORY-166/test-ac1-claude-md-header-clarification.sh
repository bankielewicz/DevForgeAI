#!/bin/bash
#
# STORY-166: AC#1 - CLAUDE.md Updated with AC Header Clarification
# Test validates that CLAUDE.md contains a section explaining AC header clarification
#
# AC#1 Requirements:
# - New subsection explaining AC headers are definitions, not trackers
# - Documentation explaining why AC headers are never marked complete
# - Documentation explaining where to look for actual completion status (DoD section)
#
# Expected: FAILS (RED state - documentation doesn't exist yet)

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

TEST_NAME="AC#1: CLAUDE.md Updated with AC Header Clarification"
CLAUDE_MD_PATH="CLAUDE.md"
EXPECTED_SECTION="Acceptance Criteria vs. Tracking Mechanisms"

echo "Running: $TEST_NAME"
echo "==========================================="
echo ""

# Test 1: CLAUDE.md file exists
if [ ! -f "$CLAUDE_MD_PATH" ]; then
    echo -e "${RED}FAIL${NC}: CLAUDE.md file not found at $CLAUDE_MD_PATH"
    exit 1
fi
echo -e "${GREEN}PASS${NC}: CLAUDE.md file exists"

# Test 2: Verify section about AC headers exists (case-insensitive search)
if ! grep -iq "acceptance criteria.*tracking\|ac.*headers.*definitions" "$CLAUDE_MD_PATH"; then
    echo -e "${RED}FAIL${NC}: CLAUDE.md does not contain section explaining AC headers vs tracking"
    echo "Expected section title containing: 'Acceptance Criteria' and 'Tracking Mechanisms'"
    exit 1
fi
echo -e "${GREEN}PASS${NC}: CLAUDE.md contains section about AC headers vs tracking mechanisms"

# Test 3: Verify documentation about AC headers being definitions, not trackers
if ! grep -iq "ac.*headers.*definitions\|definitions.*not.*trackers\|ac headers.*immutable" "$CLAUDE_MD_PATH"; then
    echo -e "${RED}FAIL${NC}: CLAUDE.md does not explain that AC headers are definitions, not trackers"
    echo "Expected content: AC headers are definitions (immutable), not progress trackers"
    exit 1
fi
echo -e "${GREEN}PASS${NC}: CLAUDE.md explains AC headers are definitions, not trackers"

# Test 4: Verify documentation about why AC headers are never marked complete
if ! grep -iq "never.*marked.*complete\|never meant to be checked\|marking.*complete.*incorrect" "$CLAUDE_MD_PATH"; then
    echo -e "${RED}FAIL${NC}: CLAUDE.md does not explain why AC headers are never marked complete"
    echo "Expected content: explanation of why marking AC headers complete is incorrect"
    exit 1
fi
echo -e "${GREEN}PASS${NC}: CLAUDE.md explains why AC headers are never marked complete"

# Test 5: Verify documentation about where to find actual completion status (DoD)
if ! grep -iq "definition of done\|dod.*section\|actual completion.*status\|look at dod" "$CLAUDE_MD_PATH"; then
    echo -e "${RED}FAIL${NC}: CLAUDE.md does not mention Definition of Done (DoD) as completion status"
    echo "Expected content: reference to DoD section for actual completion status"
    exit 1
fi
echo -e "${GREEN}PASS${NC}: CLAUDE.md references Definition of Done for actual completion status"

echo ""
echo "==========================================="
echo -e "${GREEN}ALL AC#1 TESTS PASSED${NC}"
echo ""
exit 0
