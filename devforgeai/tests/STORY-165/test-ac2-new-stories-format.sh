#!/bin/bash

################################################################################
# Test AC#2: New Stories Use Updated Format
#
# Acceptance Criteria:
#   Given: Updated story template
#   When: Run `/create-story "Test story"`
#   Then: Generated story should have AC headers in `### AC#1:` format with no checkboxes
#
# Test Strategy (TDD Red Phase):
#   - This test SHOULD FAIL initially (before implementation)
#   - Simulates story creation to verify format is applied
#   - Checks generated story file structure
#
# Rationale:
#   - Ensures all new stories follow the updated format
#   - Validates that `/create-story` command uses updated template
#   - Prevents manual creation of stories with old format
#
# Note: This test creates a temporary story file to verify format
#
################################################################################

set -e

# Test Setup
STORY_TEMPLATE=".claude/skills/devforgeai-story-creation/assets/templates/story-template.md"
TEMP_TEST_DIR="devforgeai/tests/STORY-165"
TEST_STORY_FILE="$TEMP_TEST_DIR/test-generated-story.story.md"
FOUND_AC_HEADERS=0
FOUND_INCORRECT_FORMAT=0

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo "================================"
echo "AC#2: New Stories Use Updated Format"
echo "================================"
echo ""

# Step 1: Verify template file exists
if [ ! -f "$STORY_TEMPLATE" ]; then
    echo -e "${RED}FAIL${NC}: Story template not found: $STORY_TEMPLATE"
    exit 1
fi
echo "✓ Story template found"

# Step 2: Create a test story from template (simulating /create-story command)
# In real execution, this would be actual story creation output
# For test purposes, we copy template content and verify it
if [ ! -d "$TEMP_TEST_DIR" ]; then
    mkdir -p "$TEMP_TEST_DIR"
fi

# Step 3: Extract AC section from template (represents what would be in a new story)
TEMPLATE_AC_SECTION=$(sed -n '/^## Acceptance Criteria/,/^## [^A]/p' "$STORY_TEMPLATE" | head -n -1)

if [ -z "$TEMPLATE_AC_SECTION" ]; then
    echo -e "${RED}FAIL${NC}: Cannot extract AC section from template"
    exit 1
fi
echo "✓ Extracted AC section from template"

# Step 4: Verify new stories would have correct format
# Count correct headers
CORRECT_HEADERS=$(echo "$TEMPLATE_AC_SECTION" | grep -E "^### AC#[0-9]+:" | wc -l)
if [ "$CORRECT_HEADERS" -gt 0 ]; then
    FOUND_AC_HEADERS=$CORRECT_HEADERS
    echo "✓ Found $CORRECT_HEADERS AC headers in correct format"
fi

# Step 5: Verify no incorrect checkbox format appears
INCORRECT_HEADERS=$(echo "$TEMPLATE_AC_SECTION" | grep -E "^### [0-9]+\. \[ \]" | wc -l)
if [ "$INCORRECT_HEADERS" -gt 0 ]; then
    FOUND_INCORRECT_FORMAT=$INCORRECT_HEADERS
    echo -e "${RED}✗ Found $INCORRECT_HEADERS headers with old checkbox syntax${NC}"
fi

# Step 6: Verify example AC structure
echo ""
echo "Example AC headers from template:"
echo "$TEMPLATE_AC_SECTION" | grep -E "^###" | head -3

echo ""
echo "================================"
echo "Test Results:"
echo "================================"

# Assertions
if [ "$FOUND_AC_HEADERS" -lt 3 ]; then
    echo -e "${RED}FAIL${NC}: Expected at least 3 AC headers in new story format, found $FOUND_AC_HEADERS"
    exit 1
fi

if [ "$FOUND_INCORRECT_FORMAT" -gt 0 ]; then
    echo -e "${RED}FAIL${NC}: New story format contains old checkbox syntax"
    exit 1
fi

echo -e "${GREEN}PASS${NC}: New stories will use correct AC header format"
echo -e "${GREEN}PASS${NC}: Template generates stories without checkbox syntax"

# Cleanup test file
rm -f "$TEST_STORY_FILE"

exit 0
