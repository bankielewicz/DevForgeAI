#!/bin/bash

################################################################################
# Test AC#1: Template AC Header Format Updated
#
# Acceptance Criteria:
#   Given: `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md`
#   When: Review the Acceptance Criteria section
#   Then: AC headers should use format `### AC#1: {Title}` instead of `### 1. [ ] {Title}`
#
# Test Strategy (TDD Red Phase):
#   - This test SHOULD FAIL initially (before implementation)
#   - Verifies template file uses correct AC header format
#   - Checks for absence of old checkbox syntax
#
# Rationale:
#   - Templates define the standard AC format for all new stories
#   - Ensures consistency across framework and projects using DevForgeAI
#   - Prevents regression to old checkbox format
#
################################################################################

set -e

# Test Setup
TEMPLATE_FILE=".claude/skills/devforgeai-story-creation/assets/templates/story-template.md"
ACCEPTANCE_CRITERIA_SECTION=0
FOUND_CORRECT_FORMAT=0
FOUND_INCORRECT_FORMAT=0

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo "================================"
echo "AC#1: Template AC Header Format Updated"
echo "================================"
echo ""

# Step 1: Verify template file exists
if [ ! -f "$TEMPLATE_FILE" ]; then
    echo -e "${RED}FAIL${NC}: Template file not found: $TEMPLATE_FILE"
    exit 1
fi
echo "✓ Template file found: $TEMPLATE_FILE"

# Step 2: Extract Acceptance Criteria section (between "## Acceptance Criteria" and next "##")
ACCEPTANCE_CRITERIA_CONTENT=$(sed -n '/^## Acceptance Criteria/,/^## [^A]/p' "$TEMPLATE_FILE" | head -n -1)

if [ -z "$ACCEPTANCE_CRITERIA_CONTENT" ]; then
    echo -e "${RED}FAIL${NC}: Acceptance Criteria section not found in template"
    exit 1
fi
echo "✓ Acceptance Criteria section found"
echo ""

# Step 3: Check for correct format: ### AC#N: {Title}
# This pattern should match: ### AC#1: , ### AC#2: , etc.
CORRECT_PATTERN=$(echo "$ACCEPTANCE_CRITERIA_CONTENT" | grep -E "^### AC#[0-9]+:" | wc -l)
if [ "$CORRECT_PATTERN" -gt 0 ]; then
    FOUND_CORRECT_FORMAT=1
    echo "✓ Found $CORRECT_PATTERN correct AC headers with format: ### AC#N: {Title}"
fi

# Step 4: Check for INCORRECT format: ### N. [ ] {Title} (old checkbox syntax)
# This pattern should NOT exist
INCORRECT_PATTERN=$(echo "$ACCEPTANCE_CRITERIA_CONTENT" | grep -E "^### [0-9]+\. \[ \]" | wc -l)
if [ "$INCORRECT_PATTERN" -gt 0 ]; then
    FOUND_INCORRECT_FORMAT=$INCORRECT_PATTERN
    echo -e "${RED}✗ Found $INCORRECT_PATTERN incorrect AC headers with checkbox syntax: ### N. [ ] {Title}${NC}"
fi

# Step 5: Show examples of AC headers found
echo ""
echo "AC Headers found in template:"
echo "$ACCEPTANCE_CRITERIA_CONTENT" | grep -E "^###" | head -5

echo ""
echo "================================"
echo "Test Results:"
echo "================================"

# Assertions
if [ "$FOUND_CORRECT_FORMAT" -eq 0 ]; then
    echo -e "${RED}FAIL${NC}: No correct AC headers found (expected ### AC#N: format)"
    exit 1
fi

if [ "$FOUND_INCORRECT_FORMAT" -gt 0 ]; then
    echo -e "${RED}FAIL${NC}: Found $FOUND_INCORRECT_FORMAT incorrect checkbox-style AC headers"
    exit 1
fi

echo -e "${GREEN}PASS${NC}: Template AC headers use correct format (### AC#N: {Title})"
echo -e "${GREEN}PASS${NC}: No old checkbox syntax found (### N. [ ] {Title})"
exit 0
