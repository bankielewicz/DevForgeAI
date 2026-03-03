#!/bin/bash

# STORY-162 AC-3: User Visibility - Granular Progress
# Test that user sees granular progress (~15 items) instead of coarse progress (9 items)
#
# AC-3 Requirement:
# When user runs `/dev STORY-XXX`, user should see granular progress (~15 items)
# instead of coarse progress (9 items)
#
# This test SHOULD FAIL initially (Red phase - TDD)
# Implementation needed: Expand TodoWrite to ~15 items with clear descriptions

set -e

SKILL_FILE=".claude/skills/devforgeai-development/SKILL.md"

echo "TEST: AC-3 - User Visibility (Granular Progress)"
echo "==============================================="
echo ""

# Check if SKILL.md exists
if [ ! -f "$SKILL_FILE" ]; then
    echo "FAIL: $SKILL_FILE does not exist"
    exit 1
fi

# Extract TodoWrite array
TODOWRITE_CONTENT=$(sed -n '/^TodoWrite(/,/^)/p' "$SKILL_FILE")

echo "Verifying TodoWrite has granular items (not coarse 10-item tracker)..."
echo ""

# Check for specific granular items that indicate expansion
# Note: SKILL.md uses Phase 01-10 (1-indexed), story uses Phase 0-7 (0-indexed)
# Mapping: Story Phase 0 = SKILL Phase 01, Story Phase 1 = SKILL Phase 02, etc.
declare -a REQUIRED_ITEMS=(
    "Phase 01"
    "Phase 02"
    "Phase 02 Step 4"
    "Phase 03 Step 1-2"
    "Phase 03 Step 3"
    "Phase 04 Step 1-2"
    "Phase 04 Step 3"
    "Phase 04 Step 5"
    "Phase 05"
    "Phase 06"
    "DoD Update"
    "Phase 08"
    "Phase 09"
    "Phase 10"
)

FOUND_COUNT=0
for item in "${REQUIRED_ITEMS[@]}"; do
    if echo "$TODOWRITE_CONTENT" | grep -qi "$item"; then
        echo "  ✓ Found: $item"
        FOUND_COUNT=$((FOUND_COUNT + 1))
    else
        echo "  ✗ Missing: $item"
    fi
done

echo ""
echo "Found $FOUND_COUNT / ${#REQUIRED_ITEMS[@]} granular items"

# Verify activeForm descriptions are specific to each item
echo ""
echo "Checking for specific activeForm descriptions..."
echo ""

# Count unique activeForm descriptions
ACTIVEFORM_COUNT=$(echo "$TODOWRITE_CONTENT" | grep -o 'activeForm: "[^"]*"' | sort -u | wc -l)
echo "Unique activeForm descriptions: $ACTIVEFORM_COUNT"

if [ "$ACTIVEFORM_COUNT" -lt 12 ]; then
    echo "FAIL: Too few unique activeForm descriptions (expected ~14-15, got $ACTIVEFORM_COUNT)"
    exit 1
fi

# Each todo item should have different activeForm (no copy-paste)
TOTAL_ITEMS=$(echo "$TODOWRITE_CONTENT" | grep -c 'activeForm:' || true)
echo "Total items with activeForm: $TOTAL_ITEMS"

if [ "$FOUND_COUNT" -ge 12 ] && [ "$TOTAL_ITEMS" -ge 13 ]; then
    echo ""
    echo "PASS: User will see granular progress with ~$TOTAL_ITEMS items"
    exit 0
else
    echo ""
    echo "FAIL: Insufficient granular items for user visibility"
    echo "  Expected: ~15 items with 14+ unique activeForm descriptions"
    echo "  Found: $TOTAL_ITEMS items with $ACTIVEFORM_COUNT unique descriptions"
    exit 1
fi
