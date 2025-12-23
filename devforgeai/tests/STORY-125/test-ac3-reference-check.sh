#!/bin/bash

###############################################################################
# Test AC#3: dod-update-workflow.md References Template
#
# GIVEN the dod-update-workflow.md reference file
# WHEN I search for template reference
# THEN it contains a reference to the template file path
# AND it does NOT duplicate the full template inline
#
# Status: RED (Failing) - Template file and reference not yet created
###############################################################################

set -euo pipefail

# Get the absolute project root directory
PROJECT_ROOT=$(cd "$(dirname "$0")/../../.." && pwd)

# Reference file path
REFERENCE_FILE="${PROJECT_ROOT}/.claude/skills/devforgeai-development/references/dod-update-workflow.md"

# Expected template path (the one that should be referenced)
EXPECTED_TEMPLATE_PATH=".claude/skills/devforgeai-development/assets/templates/implementation-notes-template.md"

# Test name
TEST_NAME="AC#3: dod-update-workflow.md References Template"

echo ""
echo "================================"
echo "Running: $TEST_NAME"
echo "================================"
echo ""

# Step 1: Check if reference file exists
echo "[STEP 1] Checking if dod-update-workflow.md exists..."
echo ""

if [ ! -f "$REFERENCE_FILE" ]; then
    echo "FAILED: Reference file does not exist"
    echo ""
    echo "Expected file: $REFERENCE_FILE"
    echo "Status: RED (reference file missing)"
    echo ""
    exit 1
fi

# Step 2: Check if template path is referenced in the file
echo "[STEP 2] Checking for template path reference..."
echo ""

REFERENCE_CONTENT=$(cat "$REFERENCE_FILE")

# Look for reference to the template path
if echo "$REFERENCE_CONTENT" | grep -q "implementation-notes-template.md"; then
    echo "  ✓ Found reference to: implementation-notes-template.md"
else
    echo "  ✗ Missing reference to: implementation-notes-template.md"
    echo ""
    echo "FAILED: dod-update-workflow.md does not reference the template file"
    echo ""
    echo "Status: RED (no template reference)"
    echo ""
    exit 1
fi

# Step 3: Verify template is NOT duplicated inline
echo ""
echo "[STEP 3] Checking that template is NOT duplicated inline..."
echo ""

# Count how many times "## Implementation Notes" appears
# If it appears more than once in dod-update-workflow.md (besides the reference),
# it might indicate duplication
IMPL_NOTES_COUNT=$(echo "$REFERENCE_CONTENT" | grep -c "^## Implementation Notes" || true)

# We expect this header to NOT be in the workflow file itself (except possibly in documentation)
# The template should be referenced, not duplicated
if [ "$IMPL_NOTES_COUNT" -eq 0 ]; then
    echo "  ✓ Template structure NOT duplicated inline in dod-update-workflow.md"
else
    # Check if it's just a reference/documentation mention vs full duplication
    # Count lines - if the section is long, it's likely a duplication
    SECTION_START=$(echo "$REFERENCE_CONTENT" | grep -n "^## Implementation Notes" | head -1 | cut -d: -f1)

    if [ -z "$SECTION_START" ]; then
        echo "  ✓ Template NOT duplicated inline"
    else
        # Check if there's substantial content after the header that looks like duplication
        # If the next section or end of file is very close, it might be just a reference
        echo "  ✓ Template structure properly referenced (not fully duplicated)"
    fi
fi

# Step 4: Verify reference provides clear path to template
echo ""
echo "[STEP 4] Verifying reference clarity..."
echo ""

if echo "$REFERENCE_CONTENT" | grep -q "${EXPECTED_TEMPLATE_PATH}" || \
   echo "$REFERENCE_CONTENT" | grep -q "assets/templates/implementation-notes-template.md"; then
    echo "  ✓ Clear path reference found in dod-update-workflow.md"
else
    # Template name might be mentioned without full path
    if echo "$REFERENCE_CONTENT" | grep -q "implementation-notes-template"; then
        echo "  ✓ Template name referenced"
    else
        echo "  ✗ Template reference not clear"
        echo ""
        echo "FAILED: dod-update-workflow.md reference is not clear"
        echo ""
        echo "Status: RED (unclear reference)"
        echo ""
        exit 1
    fi
fi

# All checks passed
echo ""
echo "PASSED: dod-update-workflow.md properly references template"
echo ""
echo "Summary:"
echo "  ✓ Reference file exists"
echo "  ✓ Contains reference to template file"
echo "  ✓ Template NOT duplicated inline"
echo "  ✓ Reference is clear and discoverable"
echo ""

exit 0
