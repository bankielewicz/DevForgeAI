#!/bin/bash
#
# STORY-166: AC#2 - Table Comparing Elements
# Test validates that CLAUDE.md includes a comparison table
#
# AC#2 Requirements:
# - Table showing Element, Purpose, Checkbox Behavior columns
# - Row for AC Headers with definition of what to test and never marked complete
# - Row for AC Checklist with track progress and marked during TDD
# - Row for Definition of Done with official record and marked in Phase 4.5-5 Bridge
#
# Expected: FAILS (RED state - table doesn't exist yet)

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

TEST_NAME="AC#2: Table Comparing Elements (AC Headers, Checklist, DoD)"
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

# Test 2: Verify table structure exists with pipe separators
if ! grep -q "| Element | Purpose | Checkbox Behavior |" "$CLAUDE_MD_PATH"; then
    echo -e "${RED}FAIL${NC}: CLAUDE.md does not contain comparison table with correct header"
    echo "Expected table header: | Element | Purpose | Checkbox Behavior |"
    exit 1
fi
echo -e "${GREEN}PASS${NC}: Comparison table header found"

# Test 3: Verify AC Headers row exists
if ! grep -iq "| *ac headers\|ac headers.*define what to test.*never marked" "$CLAUDE_MD_PATH"; then
    echo -e "${RED}FAIL${NC}: Table missing AC Headers row with correct content"
    echo "Expected: AC Headers | Define what to test | Never marked complete"
    exit 1
fi
echo -e "${GREEN}PASS${NC}: AC Headers row found in table"

# Test 4: Verify AC Checklist row exists
if ! grep -iq "| *ac.*checklist\|ac.*checklist.*track.*marked.*tdd" "$CLAUDE_MD_PATH"; then
    echo -e "${RED}FAIL${NC}: Table missing AC Checklist row with correct content"
    echo "Expected: AC Checklist | Track progress | Marked during TDD"
    exit 1
fi
echo -e "${GREEN}PASS${NC}: AC Checklist row found in table"

# Test 5: Verify Definition of Done row exists
if ! grep -iq "| *definition of done\|definition of done.*official.*record\|dod.*phase.*4\.5.*5.*bridge" "$CLAUDE_MD_PATH"; then
    echo -e "${RED}FAIL${NC}: Table missing Definition of Done row with correct content"
    echo "Expected: Definition of Done | Official record | Marked in Phase 4.5-5 Bridge"
    exit 1
fi
echo -e "${GREEN}PASS${NC}: Definition of Done row found in table"

# Test 6: Verify table uses pipe format (Markdown table)
# Count pipes in a line that should have the table - rough validation
TABLE_LINES=$(grep -c "| " "$CLAUDE_MD_PATH" || echo "0")
if [ "$TABLE_LINES" -lt 4 ]; then
    echo -e "${RED}FAIL${NC}: Table structure appears incomplete (fewer than 4 lines with pipes)"
    exit 1
fi
echo -e "${GREEN}PASS${NC}: Table structure validated"

echo ""
echo "==========================================="
echo -e "${GREEN}ALL AC#2 TESTS PASSED${NC}"
echo ""
exit 0
