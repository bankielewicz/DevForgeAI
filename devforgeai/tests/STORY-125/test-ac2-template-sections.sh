#!/bin/bash

###############################################################################
# Test AC#2: Template Contains Required Sections
#
# GIVEN the implementation notes template file
# WHEN I read its contents
# THEN it contains:
# - ## Implementation Notes header
# - **Developer:** field
# - **Implemented:** field (date)
# - **Branch:** field
# - ### Definition of Done Status subsection
# - Completed item format: - [x] {item} - Completed: {evidence}
# - Deferred item format: - [ ] {item} - Deferred: {justification} (See: {STORY-XXX})
#
# Status: RED (Failing) - Template file does not exist yet
###############################################################################

set -euo pipefail

# Get the absolute project root directory
PROJECT_ROOT=$(cd "$(dirname "$0")/../../.." && pwd)

# Expected template path
TEMPLATE_PATH="${PROJECT_ROOT}/.claude/skills/devforgeai-development/assets/templates/implementation-notes-template.md"

# Test name
TEST_NAME="AC#2: Template Contains Required Sections"

echo ""
echo "================================"
echo "Running: $TEST_NAME"
echo "================================"
echo ""

# Step 1: Check if template file exists
echo "[STEP 1] Checking if template file exists..."
echo ""

if [ ! -f "$TEMPLATE_PATH" ]; then
    echo "FAILED: Template file does not exist"
    echo ""
    echo "Expected file: $TEMPLATE_PATH"
    echo "Status: RED (template not created)"
    echo ""
    exit 1
fi

# Array to track required sections and their presence
declare -A sections_found
sections_found["Implementation Notes header"]="no"
sections_found["Developer field"]="no"
sections_found["Implemented field"]="no"
sections_found["Branch field"]="no"
sections_found["Definition of Done Status subsection"]="no"
sections_found["Completed item format"]="no"
sections_found["Deferred item format"]="no"

# Read template content
TEMPLATE_CONTENT=$(cat "$TEMPLATE_PATH")

echo "[STEP 2] Checking for required sections..."
echo ""

# Check for ## Implementation Notes header
if echo "$TEMPLATE_CONTENT" | grep -q "^## Implementation Notes"; then
    sections_found["Implementation Notes header"]="yes"
    echo "  ✓ Found: ## Implementation Notes header"
else
    echo "  ✗ Missing: ## Implementation Notes header"
fi

# Check for **Developer:** field
if echo "$TEMPLATE_CONTENT" | grep -q "\*\*Developer:\*\*"; then
    sections_found["Developer field"]="yes"
    echo "  ✓ Found: **Developer:** field"
else
    echo "  ✗ Missing: **Developer:** field"
fi

# Check for **Implemented:** field
if echo "$TEMPLATE_CONTENT" | grep -q "\*\*Implemented:\*\*"; then
    sections_found["Implemented field"]="yes"
    echo "  ✓ Found: **Implemented:** field"
else
    echo "  ✗ Missing: **Implemented:** field"
fi

# Check for **Branch:** field
if echo "$TEMPLATE_CONTENT" | grep -q "\*\*Branch:\*\*"; then
    sections_found["Branch field"]="yes"
    echo "  ✓ Found: **Branch:** field"
else
    echo "  ✗ Missing: **Branch:** field"
fi

# Check for ### Definition of Done Status subsection
if echo "$TEMPLATE_CONTENT" | grep -q "^### Definition of Done"; then
    sections_found["Definition of Done Status subsection"]="yes"
    echo "  ✓ Found: ### Definition of Done Status subsection"
else
    echo "  ✗ Missing: ### Definition of Done Status subsection"
fi

# Check for completed item format: - [x] {item} - Completed: {evidence}
if echo "$TEMPLATE_CONTENT" | grep -q "\- \[x\].*Completed:"; then
    sections_found["Completed item format"]="yes"
    echo "  ✓ Found: Completed item format (- [x] {item} - Completed: {evidence})"
else
    echo "  ✗ Missing: Completed item format (- [x] {item} - Completed: {evidence})"
fi

# Check for deferred item format: - [ ] {item} - Deferred: {justification} (See: {STORY-XXX})
if echo "$TEMPLATE_CONTENT" | grep -q "\- \[ \].*Deferred:"; then
    sections_found["Deferred item format"]="yes"
    echo "  ✓ Found: Deferred item format (- [ ] {item} - Deferred: {justification})"
else
    echo "  ✗ Missing: Deferred item format (- [ ] {item} - Deferred: {justification})"
fi

echo ""
echo "[STEP 3] Validating all required sections present..."
echo ""

# Count missing sections
MISSING_COUNT=0
for section in "${!sections_found[@]}"; do
    if [ "${sections_found[$section]}" = "no" ]; then
        MISSING_COUNT=$((MISSING_COUNT + 1))
    fi
done

if [ "$MISSING_COUNT" -gt 0 ]; then
    echo "FAILED: $MISSING_COUNT required section(s) missing from template"
    echo ""
    echo "Status: RED (template incomplete)"
    echo ""
    exit 1
fi

# All checks passed
echo "PASSED: All required sections present in template"
echo ""
echo "Summary:"
echo "  ✓ ## Implementation Notes header"
echo "  ✓ **Developer:** field"
echo "  ✓ **Implemented:** field (date)"
echo "  ✓ **Branch:** field"
echo "  ✓ ### Definition of Done Status subsection"
echo "  ✓ Completed item format"
echo "  ✓ Deferred item format"
echo ""

exit 0
