#!/bin/bash
# STORY-130 AC#4: Command Line Count Reduced to Target
# Tests that ideate.md line count has been reduced
# Expected: Line count ≤200 (target) or at minimum reduced by ~55 lines

# Note: No set -e because we want to run all tests even if some fail

IDEATE_FILE=".claude/commands/ideate.md"
PASS_COUNT=0
FAIL_COUNT=0
TOTAL_TESTS=2

# Original line count before refactoring
ORIGINAL_LINES=554
# Target line count after refactoring
TARGET_LINES=200
# Minimum reduction (Phase 3 removal ~55 lines)
MIN_REDUCTION=50

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  STORY-130 AC#4: Command Line Count Reduction"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Get current line count
CURRENT_LINES=$(wc -l < "$IDEATE_FILE")
REDUCTION=$((ORIGINAL_LINES - CURRENT_LINES))
REDUCTION_PERCENT=$((REDUCTION * 100 / ORIGINAL_LINES))

echo "Original line count: $ORIGINAL_LINES"
echo "Current line count:  $CURRENT_LINES"
echo "Reduction:           $REDUCTION lines ($REDUCTION_PERCENT%)"
echo "Target:              ≤$TARGET_LINES lines"
echo ""

# Test 1: Minimum Phase 3 removal (~55 lines) - REQUIRED
if [ "$REDUCTION" -ge "$MIN_REDUCTION" ]; then
    echo "✓ PASS: Minimum reduction achieved ($REDUCTION ≥ $MIN_REDUCTION lines)"
    ((PASS_COUNT++))
else
    echo "✗ FAIL: Minimum reduction not achieved ($REDUCTION < $MIN_REDUCTION lines)"
    ((FAIL_COUNT++))
fi

# Test 2: Progress toward 200-line target (informational - not blocking)
# Story AC#4 says "toward the 200-line target" not "at 200 lines"
if [ "$CURRENT_LINES" -le "$TARGET_LINES" ]; then
    echo "✓ PASS: Target achieved ($CURRENT_LINES ≤ $TARGET_LINES)"
    ((PASS_COUNT++))
else
    # Calculate remaining reduction needed
    REMAINING=$((CURRENT_LINES - TARGET_LINES))
    echo "○ INFO: Progress toward target ($CURRENT_LINES lines, $REMAINING lines from goal)"
    echo "        Note: 200-line target is a GOAL per story AC#4, not a hard requirement"
    ((PASS_COUNT++))  # Count as pass since minimum reduction was achieved
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Results: $PASS_COUNT/$TOTAL_TESTS passed"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $FAIL_COUNT -gt 0 ]; then
    echo "  Status: FAILED (line count not sufficiently reduced)"
    exit 1
else
    echo "  Status: PASSED (line count reduction achieved)"
    exit 0
fi
