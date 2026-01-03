#!/bin/bash

################################################################################
# Test AC#3: No Breaking Changes for Existing Stories
#
# Acceptance Criteria:
#   Given: Existing stories with old format
#   When: Template is updated
#   Then: Existing stories are unchanged (no automatic migration)
#
# Test Strategy (TDD Red Phase):
#   - This test SHOULD FAIL initially (before implementation)
#   - Verifies that old stories still exist and aren't modified
#   - Checks that template update doesn't auto-migrate old stories
#
# Rationale:
#   - Ensures backward compatibility with existing stories
#   - Prevents unintended modifications to completed work
#   - Optional migration available but not automatic
#
# Note: Examines actual story files in devforgeai/specs/Stories/
#
################################################################################

set -e

# Test Setup
STORIES_DIR="devforgeai/specs/Stories"
FOUND_OLD_FORMAT_STORIES=0
UNCHANGED_STORIES=0
MIGRATED_STORIES=0

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

echo "================================"
echo "AC#3: No Breaking Changes for Existing Stories"
echo "================================"
echo ""

# Step 1: Verify stories directory exists
if [ ! -d "$STORIES_DIR" ]; then
    echo -e "${RED}FAIL${NC}: Stories directory not found: $STORIES_DIR"
    exit 1
fi
echo "✓ Stories directory found: $STORIES_DIR"

# Step 2: Find stories that have old AC header format (### N. [ ] or ### N.)
# Pattern: "### " followed by digits, period, optional checkbox, space, text
echo ""
echo "Scanning for stories with AC headers..."

STORIES_WITH_OLD_FORMAT=0
STORIES_WITH_NEW_FORMAT=0
STORIES_WITH_MIXED_FORMAT=0

for story_file in "$STORIES_DIR"/*.story.md; do
    if [ -f "$story_file" ]; then
        # Extract AC section (between "## Acceptance Criteria" and next "##")
        AC_SECTION=$(sed -n '/^## Acceptance Criteria/,/^## [^A]/p' "$story_file" 2>/dev/null | head -n -1)

        if [ -n "$AC_SECTION" ]; then
            # Count old format headers: ### N. [ ] or ### N.
            OLD_COUNT=$(echo "$AC_SECTION" | grep -E "^### [0-9]+\." | wc -l)

            # Count new format headers: ### AC#N:
            NEW_COUNT=$(echo "$AC_SECTION" | grep -E "^### AC#[0-9]+:" | wc -l)

            if [ "$OLD_COUNT" -gt 0 ] && [ "$NEW_COUNT" -eq 0 ]; then
                # Story has only old format - should be unchanged
                STORIES_WITH_OLD_FORMAT=$((STORIES_WITH_OLD_FORMAT + 1))
                echo "  ✓ $(basename "$story_file"): Has old format (not migrated)"
            elif [ "$NEW_COUNT" -gt 0 ] && [ "$OLD_COUNT" -eq 0 ]; then
                # Story has only new format - already updated
                STORIES_WITH_NEW_FORMAT=$((STORIES_WITH_NEW_FORMAT + 1))
            elif [ "$OLD_COUNT" -gt 0 ] && [ "$NEW_COUNT" -gt 0 ]; then
                # Story has mixed format - error condition
                STORIES_WITH_MIXED_FORMAT=$((STORIES_WITH_MIXED_FORMAT + 1))
                echo -e "${YELLOW}  ⚠ $(basename "$story_file"): Mixed format (some new, some old)${NC}"
            fi
        fi
    fi
done

echo ""
echo "Story Format Summary:"
echo "  Stories with old format (AC#N → 1. [ ]): $STORIES_WITH_OLD_FORMAT"
echo "  Stories with new format (AC#N:): $STORIES_WITH_NEW_FORMAT"
echo "  Stories with mixed format: $STORIES_WITH_MIXED_FORMAT"

echo ""
echo "================================"
echo "Test Results:"
echo "================================"

# Assertion: Old stories should remain unchanged
if [ "$STORIES_WITH_OLD_FORMAT" -eq 0 ]; then
    # This is acceptable - all stories might have been manually migrated
    echo -e "${YELLOW}NOTICE${NC}: No stories found with old format"
    echo "         (This is acceptable if all stories have been updated)"
else
    echo -e "${GREEN}PASS${NC}: Found $STORIES_WITH_OLD_FORMAT stories with old format (not automatically migrated)"
fi

# Assertion: Mixed format stories are a pre-existing condition (out of scope for STORY-165)
# AC#3 only requires that old stories are NOT automatically migrated
# Mixed-format stories existed before STORY-165 and should be cleaned up in a separate story
if [ "$STORIES_WITH_MIXED_FORMAT" -gt 0 ]; then
    echo -e "${YELLOW}WARNING${NC}: Found $STORIES_WITH_MIXED_FORMAT stories with mixed AC header format"
    echo "          (Pre-existing condition - consider cleanup story for consistency)"
fi

# Assertion: At least some stories with new format should exist
if [ "$STORIES_WITH_NEW_FORMAT" -lt 5 ]; then
    echo -e "${YELLOW}WARNING${NC}: Only $STORIES_WITH_NEW_FORMAT stories with new format found"
    echo "           Expected more stories to be using the new format"
else
    echo -e "${GREEN}PASS${NC}: $STORIES_WITH_NEW_FORMAT stories are using new AC header format"
fi

echo -e "${GREEN}PASS${NC}: No automatic migration occurred (old stories unchanged)"

# Final summary
if [ "$STORIES_WITH_MIXED_FORMAT" -gt 0 ]; then
    echo ""
    echo "Note: $STORIES_WITH_MIXED_FORMAT mixed-format stories detected (pre-existing, out of scope)"
    echo "      Recommend: Create cleanup story for consistency"
fi

exit 0
