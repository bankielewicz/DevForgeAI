#!/bin/bash

###############################################################################
# Test AC#1: Template File Created
#
# GIVEN the DevForgeAI templates directory exists
# WHEN this story is implemented
# THEN a new file exists at .claude/skills/devforgeai-development/assets/templates/implementation-notes-template.md
# AND the file is 25 lines or fewer
#
# Status: RED (Failing) - Template file does not exist yet
###############################################################################

set -euo pipefail

# Get the absolute project root directory
PROJECT_ROOT=$(cd "$(dirname "$0")/../../.." && pwd)

# Expected template path
TEMPLATE_PATH="${PROJECT_ROOT}/.claude/skills/devforgeai-development/assets/templates/implementation-notes-template.md"

# Test name
TEST_NAME="AC#1: Template File Created"

echo ""
echo "================================"
echo "Running: $TEST_NAME"
echo "================================"
echo ""

# Step 1: Check if template file exists
echo "[STEP 1] Checking if template file exists at:"
echo "  $TEMPLATE_PATH"
echo ""

if [ ! -f "$TEMPLATE_PATH" ]; then
    echo "FAILED: Template file does not exist"
    echo ""
    echo "Expected file: $TEMPLATE_PATH"
    echo "Status: RED (as expected for TDD Red phase)"
    echo ""
    exit 1
fi

# Step 2: Count lines in template file
echo "[STEP 2] Counting lines in template file..."
echo ""

LINE_COUNT=$(wc -l < "$TEMPLATE_PATH")
echo "Line count: $LINE_COUNT"
echo ""

# Step 3: Verify line count is 25 or fewer
echo "[STEP 3] Verifying line count is 25 or fewer..."
echo ""

if [ "$LINE_COUNT" -gt 25 ]; then
    echo "FAILED: Template file exceeds 25 lines"
    echo ""
    echo "Expected: 25 lines or fewer"
    echo "Actual: $LINE_COUNT lines"
    echo "Status: RED (template too large)"
    echo ""
    exit 1
fi

# All checks passed
echo "PASSED: Template file exists and is $LINE_COUNT lines (25 line limit)"
echo ""
echo "Summary:"
echo "  ✓ Template file exists at correct path"
echo "  ✓ File is within 25 line limit"
echo ""

exit 0
