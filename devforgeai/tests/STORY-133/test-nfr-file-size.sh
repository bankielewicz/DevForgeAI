#!/bin/bash

# Test NFR#1: File Size Constraint
# Purpose: Verify subagent file size is ≤ 200 lines for token efficiency
# Expected: All checks pass (exit 0 on success, non-zero on failure)

STORY_ID="STORY-133"
AGENT_FILE=".claude/agents/ideation-result-interpreter.md"
TEST_RESULTS=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
MAX_LINES=200

# Change to project root
cd "$PROJECT_ROOT" || { echo "ERROR: Cannot cd to project root"; exit 1; }

echo "════════════════════════════════════════════════════════════════"
echo "Test NFR#1: File Size Constraint"
echo "Story: $STORY_ID"
echo "Testing: $AGENT_FILE"
echo "Max allowed lines: $MAX_LINES"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Test 1: File exists (prerequisite)
echo "TEST 1: File exists (prerequisite)"
if [ -f "$AGENT_FILE" ]; then
    echo "  ✓ PASS: File found"
else
    echo "  ✗ FAIL: File not found at $AGENT_FILE"
    echo "         Cannot proceed with remaining tests"
    exit 1
fi
echo ""

# Test 2: File has content (not empty)
echo "TEST 2: File has content (not empty)"
FILE_SIZE=$(stat -c%s "$AGENT_FILE" 2>/dev/null || stat -f%z "$AGENT_FILE" 2>/dev/null || du -b "$AGENT_FILE" | cut -f1)
if [ -n "$FILE_SIZE" ] && [ "$FILE_SIZE" -gt 0 ]; then
    echo "  ✓ PASS: File has content ($FILE_SIZE bytes)"
else
    echo "  ✗ FAIL: File is empty or cannot read size"
    TEST_RESULTS=1
fi
echo ""

# Test 3: Count total lines
echo "TEST 3: Count total lines in file"
LINE_COUNT=$(wc -l < "$AGENT_FILE")
echo "  Total lines: $LINE_COUNT"
echo ""

# Test 4: File size is within limits (≤ 200 lines)
echo "TEST 4: File size is within limits (≤ 200 lines)"
if [ "$LINE_COUNT" -le "$MAX_LINES" ]; then
    echo "  ✓ PASS: File size within limits"
    echo "         Lines: $LINE_COUNT / $MAX_LINES (usage: $(echo "scale=1; $LINE_COUNT * 100 / $MAX_LINES" | bc)%)"
else
    EXCESS=$((LINE_COUNT - MAX_LINES))
    PERCENTAGE=$(echo "scale=1; $EXCESS * 100 / $MAX_LINES" | bc)
    echo "  ✗ FAIL: File size exceeds limit"
    echo "         Lines: $LINE_COUNT / $MAX_LINES (+$EXCESS lines, +${PERCENTAGE}%)"
    TEST_RESULTS=1
fi
echo ""

# Test 5: Check for incomplete content (not truncated)
echo "TEST 5: Check for complete content (not truncated)"
LAST_LINES=$(tail -3 "$AGENT_FILE")
if echo "$LAST_LINES" | grep -q "Success Criteria\|---\|## \|# "; then
    echo "  ✓ PASS: File appears complete (ends with proper section)"
    echo "         Last lines:"
    echo "$LAST_LINES" | sed 's/^/            /'
elif [ -n "$LAST_LINES" ]; then
    # Check if it's reasonable content
    if echo "$LAST_LINES" | grep -qE "[a-zA-Z0-9]"; then
        echo "  ✓ PASS: File has content to the end"
    else
        echo "  ⚠ WARNING: File ends with unusual content"
    fi
else
    echo "  ✗ FAIL: File appears truncated or empty"
    TEST_RESULTS=1
fi
echo ""

# Test 6: Verify no garbage/encoding issues
echo "TEST 6: Verify file is valid UTF-8 (no encoding issues)"
if file "$AGENT_FILE" | grep -E "UTF-8|ASCII|text" | grep -q "."; then
    echo "  ✓ PASS: File is valid text format"
    FILE_TYPE=$(file "$AGENT_FILE" | cut -d: -f2 | xargs)
    echo "         Type: $FILE_TYPE"
else
    echo "  ⚠ WARNING: Could not determine file type"
fi
echo ""

# Test 7: Count non-empty lines (excluding blank lines and comments)
echo "TEST 7: Code/content density analysis"
CONTENT_LINES=$(grep -v "^[[:space:]]*$" "$AGENT_FILE" | grep -v "^[[:space:]]*#[^#]" | wc -l)
echo "  Total lines: $LINE_COUNT"
echo "  Content lines (non-blank, non-comment): $CONTENT_LINES"
echo "  Content density: $(echo "scale=1; $CONTENT_LINES * 100 / $LINE_COUNT" | bc)%"
echo ""

# Test 8: Check for markers indicating sections exist
echo "TEST 8: Verify key sections are present (structural sanity)"
SECTIONS_FOUND=0
[ $(grep -c "^# Purpose\|^## Purpose" "$AGENT_FILE") -gt 0 ] && ((SECTIONS_FOUND++)) && echo "  ✓ Purpose section found"
[ $(grep -c "^# When Invoked\|^## When Invoked" "$AGENT_FILE") -gt 0 ] && ((SECTIONS_FOUND++)) && echo "  ✓ When Invoked section found"
[ $(grep -c "^# Workflow\|^## Workflow" "$AGENT_FILE") -gt 0 ] && ((SECTIONS_FOUND++)) && echo "  ✓ Workflow section found"
[ $(grep -c "^# Templates\|^## Templates" "$AGENT_FILE") -gt 0 ] && ((SECTIONS_FOUND++)) && echo "  ✓ Templates section found"
[ $(grep -c "^# Error Handling\|^## Error Handling" "$AGENT_FILE") -gt 0 ] && ((SECTIONS_FOUND++)) && echo "  ✓ Error Handling section found"

if [ "$SECTIONS_FOUND" -ge 4 ]; then
    echo "  ✓ PASS: Key sections present ($SECTIONS_FOUND/5)"
else
    echo "  ⚠ WARNING: Some key sections may be missing ($SECTIONS_FOUND/5)"
fi
echo ""

# Test 9: Verify file is not too small (has actual content)
echo "TEST 9: File has sufficient content (not too small)"
MIN_REASONABLE_LINES=30
if [ "$LINE_COUNT" -ge "$MIN_REASONABLE_LINES" ]; then
    echo "  ✓ PASS: File has sufficient content"
    echo "         Minimum: $MIN_REASONABLE_LINES lines"
    echo "         Actual: $LINE_COUNT lines"
else
    echo "  ⚠ WARNING: File might be too small or incomplete"
    echo "         Minimum recommended: $MIN_REASONABLE_LINES lines"
    echo "         Actual: $LINE_COUNT lines"
fi
echo ""

# Summary
echo "════════════════════════════════════════════════════════════════"
echo "NFR#1 File Size Analysis:"
echo "  Lines: $LINE_COUNT / $MAX_LINES"
echo "  Limit: $(echo "scale=1; $LINE_COUNT * 100 / $MAX_LINES" | bc)% of max"
echo ""
if [ $TEST_RESULTS -eq 0 ]; then
    echo "✓ NFR Test Suite: ALL TESTS PASSED"
else
    echo "✗ NFR Test Suite: SOME TESTS FAILED"
fi
echo "════════════════════════════════════════════════════════════════"

exit $TEST_RESULTS
