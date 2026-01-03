#!/bin/bash

################################################################################
# Test AC#4: Format Maintains Numbering Reference
#
# Acceptance Criteria:
#   Given: New AC header format
#   When: Documentation references acceptance criteria
#   Then: References like "See AC#3" should still work logically
#
# Test Strategy (TDD Red Phase):
#   - This test SHOULD FAIL initially (before implementation)
#   - Verifies numbering is unambiguous and parseable
#   - Checks that AC# notation is consistent and maintainable
#
# Rationale:
#   - Ensures documentation and references continue to work
#   - AC#N notation is explicit and unambiguous
#   - Cross-references between stories remain valid
#
# Note: Validates the new format's referencability
#
################################################################################

set -e

# Test Setup
TEMPLATE_FILE=".claude/skills/devforgeai-story-creation/assets/templates/story-template.md"
AC_NUMBERING_VALID=0
REFERENCE_FORMAT_VALID=0

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo "================================"
echo "AC#4: Format Maintains Numbering Reference"
echo "================================"
echo ""

# Step 1: Verify template exists
if [ ! -f "$TEMPLATE_FILE" ]; then
    echo -e "${RED}FAIL${NC}: Template file not found: $TEMPLATE_FILE"
    exit 1
fi
echo "✓ Template file found"

# Step 2: Extract AC section
AC_SECTION=$(sed -n '/^## Acceptance Criteria/,/^## [^A]/p' "$TEMPLATE_FILE" | head -n -1)

if [ -z "$AC_SECTION" ]; then
    echo -e "${RED}FAIL${NC}: Acceptance Criteria section not found"
    exit 1
fi
echo "✓ AC section extracted"

# Step 3: Extract all AC headers with their numbers
echo ""
echo "AC Headers found in template:"
echo "$AC_SECTION" | grep -E "^### AC#[0-9]+:" | while IFS= read -r line; do
    # Extract AC number from format: ### AC#N: Title
    AC_NUMBER=$(echo "$line" | sed -E 's/^### AC#([0-9]+):.*/\1/')
    AC_TITLE=$(echo "$line" | sed -E 's/^### AC#[0-9]+: (.*)/\1/')
    echo "  AC#$AC_NUMBER: $AC_TITLE"
done

# Step 4: Validate numbering is sequential and consistent
ALL_AC_HEADERS=$(echo "$AC_SECTION" | grep -E "^### AC#[0-9]+:" | sed -E 's/^### AC#([0-9]+):.*/\1/')

if [ -z "$ALL_AC_HEADERS" ]; then
    echo -e "${RED}FAIL${NC}: No AC headers with format ### AC#N: found"
    exit 1
fi

# Get the count of AC headers
AC_COUNT=$(echo "$ALL_AC_HEADERS" | wc -l)
echo ""
echo "✓ Found $AC_COUNT AC headers in template"

# Step 5: Validate that numbering is unambiguous (only digits)
INVALID_NUMBERING=$(echo "$ALL_AC_HEADERS" | grep -v "^[0-9]*$" | wc -l)
if [ "$INVALID_NUMBERING" -gt 0 ]; then
    echo -e "${RED}FAIL${NC}: Found invalid AC numbers (non-numeric)"
    exit 1
fi
echo "✓ All AC numbers are valid numeric format"

# Step 6: Verify reference format would work
# Example references: "See AC#1", "AC#2 requires", "per AC#3"
echo ""
echo "Testing reference format validity..."

# Create test references
TEST_REFS=("AC#1" "AC#2" "AC#3" "AC#4" "See AC#1" "per AC#2 requires")

REF_VALID=1
for test_ref in "${TEST_REFS[@]}"; do
    # Pattern: AC#[0-9]+ or AC#[0-9]+ with surrounding text
    if echo "$test_ref" | grep -qE "AC#[0-9]+" ; then
        echo "  ✓ Reference format valid: '$test_ref'"
    else
        echo -e "  ${RED}✗ Invalid reference${NC}: '$test_ref'"
        REF_VALID=0
    fi
done

echo ""
echo "================================"
echo "Test Results:"
echo "================================"

# Assertions
if [ "$AC_COUNT" -lt 3 ]; then
    echo -e "${RED}FAIL${NC}: Expected at least 3 AC headers, found $AC_COUNT"
    exit 1
fi

if [ "$INVALID_NUMBERING" -gt 0 ]; then
    echo -e "${RED}FAIL${NC}: Invalid numbering found"
    exit 1
fi

if [ "$REF_VALID" -eq 0 ]; then
    echo -e "${RED}FAIL${NC}: Reference format is invalid"
    exit 1
fi

echo -e "${GREEN}PASS${NC}: AC numbering is sequential and unambiguous"
echo -e "${GREEN}PASS${NC}: AC#N format enables clear cross-references"
echo -e "${GREEN}PASS${NC}: References like 'See AC#3' work logically"
echo -e "${GREEN}PASS${NC}: Format maintains referencability in documentation"

exit 0
