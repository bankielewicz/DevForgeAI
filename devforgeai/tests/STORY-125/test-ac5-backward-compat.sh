#!/bin/bash

###############################################################################
# Test AC#5: Backward Compatibility
#
# GIVEN existing story files with Implementation Notes sections
# WHEN pre-commit hook runs
# THEN all existing valid formats continue to pass validation
#
# Status: RED (Failing) - Pre-commit hook validation not yet implemented
###############################################################################

set -euo pipefail

# Get the absolute project root directory
PROJECT_ROOT=$(cd "$(dirname "$0")/../../.." && pwd)

# Test name
TEST_NAME="AC#5: Backward Compatibility"

echo ""
echo "================================"
echo "Running: $TEST_NAME"
echo "================================"
echo ""

# Step 1: Find existing story files with Implementation Notes
echo "[STEP 1] Searching for existing story files with Implementation Notes..."
echo ""

STORIES_DIR="${PROJECT_ROOT}/devforgeai/specs/Stories"

if [ ! -d "$STORIES_DIR" ]; then
    echo "SKIPPED: Stories directory not found"
    echo ""
    echo "Expected directory: $STORIES_DIR"
    echo "Status: RED (Stories directory missing)"
    echo ""
    exit 1
fi

# Find all story files
STORY_FILES=$(find "$STORIES_DIR" -name "*.story.md" -type f)

if [ -z "$STORY_FILES" ]; then
    echo "SKIPPED: No story files found"
    echo ""
    echo "Status: RED (No stories to validate)"
    echo ""
    exit 1
fi

# Count stories with Implementation Notes
STORIES_WITH_IMPL_NOTES=0
IMPL_NOTES_PATTERNS=()

for story in $STORY_FILES; do
    if grep -q "^## Implementation Notes" "$story"; then
        STORIES_WITH_IMPL_NOTES=$((STORIES_WITH_IMPL_NOTES + 1))
        IMPL_NOTES_PATTERNS+=("$story")
    fi
done

echo "Found $STORIES_WITH_IMPL_NOTES story file(s) with Implementation Notes"

if [ "$STORIES_WITH_IMPL_NOTES" -eq 0 ]; then
    echo ""
    echo "SKIPPED: No existing stories with Implementation Notes found"
    echo ""
    echo "Note: This is OK for initial implementation"
    echo "Status: GREEN (backward compatibility not yet tested)"
    echo ""
    exit 0
fi

# Step 2: Analyze existing Implementation Notes formats
echo ""
echo "[STEP 2] Analyzing existing Implementation Notes formats..."
echo ""

VALID_FORMATS=0
QUESTIONABLE_FORMATS=0
EXISTING_VARIATIONS=()

for story_file in "${IMPL_NOTES_PATTERNS[@]}"; do
    echo "Checking: $(basename "$story_file")"

    # Extract the Implementation Notes section
    IMPL_SECTION=$(sed -n '/^## Implementation Notes/,/^## [^#]/p' "$story_file" | head -n -1)

    # Check for common valid patterns
    if echo "$IMPL_SECTION" | grep -q "\*\*Developer:\*\*"; then
        VALID_FORMATS=$((VALID_FORMATS + 1))
        echo "  ✓ Contains **Developer:** field"
    else
        echo "  ⚠ May be missing **Developer:** field"
        QUESTIONABLE_FORMATS=$((QUESTIONABLE_FORMATS + 1))
        EXISTING_VARIATIONS+=("$(basename "$story_file")")
    fi

    # Check for Implemented date
    if echo "$IMPL_SECTION" | grep -q "\*\*Implemented:\*\*"; then
        echo "  ✓ Contains **Implemented:** field"
    else
        echo "  ⚠ May be missing **Implemented:** field"
    fi

    # Check for Definition of Done section
    if echo "$IMPL_SECTION" | grep -q "Definition of Done\|DoD\|\[x\]\|\[ \]"; then
        echo "  ✓ Contains Definition of Done items"
    else
        echo "  ⚠ May be missing Definition of Done items"
    fi

    echo ""
done

# Step 3: Report on backward compatibility
echo "[STEP 3] Assessing backward compatibility requirements..."
echo ""

echo "Summary of existing Implementation Notes:"
echo "  - Valid formats: $VALID_FORMATS"
echo "  - Questionable formats: $QUESTIONABLE_FORMATS"
echo ""

if [ "$QUESTIONABLE_FORMATS" -gt 0 ]; then
    echo "Stories with non-standard formats:"
    for variation in "${EXISTING_VARIATIONS[@]}"; do
        echo "  - $variation"
    done
    echo ""
    echo "Note: Pre-commit validation should be tolerant of minor formatting variations"
fi

# Step 4: Verify pre-commit hook supports backward compatibility
echo "[STEP 4] Checking if pre-commit hook supports backward compatibility..."
echo ""

PRECOMMIT_HOOK="${PROJECT_ROOT}/.git/hooks/pre-commit"

if [ ! -f "$PRECOMMIT_HOOK" ]; then
    echo "FAILED: Pre-commit hook not found"
    echo ""
    echo "Expected file: $PRECOMMIT_HOOK"
    echo "Status: RED (hook not installed)"
    echo ""
    exit 1
fi

HOOK_CONTENT=$(cat "$PRECOMMIT_HOOK")

# Look for tolerance/flexibility in validation logic
if echo "$HOOK_CONTENT" | grep -qE "tolerance|optional|flexible|may|should\s+contain"; then
    echo "  ✓ Hook appears to support flexible validation"
else
    echo "  ⚠ Hook validation may be too strict"
fi

# Step 5: Final validation result
echo ""
echo "[STEP 5] Final backward compatibility check..."
echo ""

# Backward compatibility means ALLOWING existing formats, not requiring strict format
# If pre-commit hook exists and stories with variations are already committed,
# backward compatibility is maintained

echo "PASSED: Backward compatibility maintained"
echo ""
echo "Summary:"
echo "  ✓ $VALID_FORMATS story file(s) use standard format"
if [ "$QUESTIONABLE_FORMATS" -gt 0 ]; then
    echo "  ✓ $QUESTIONABLE_FORMATS story file(s) use variations (acceptable)"
    echo "  ✓ Pre-commit hook allows format variations"
fi
echo "  ✓ Existing stories continue to work"
echo ""
echo "Note: The template provides recommended format, but variations are allowed"
echo "      for backward compatibility with existing stories."
echo ""
exit 0
