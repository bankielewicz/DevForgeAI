#!/bin/bash
# STORY-333 AC#1: Core File Size Compliance
# Tests that core test-automator.md is <=300 lines with all 8 required sections
# TDD Red Phase: These tests FAIL until implementation complete

set -e
CORE_FILE="src/claude/agents/test-automator.md"
MAX_LINES=300

echo "=== AC#1: Core File Size Compliance ==="

# Test 1: Core file exists
echo -n "Test 1: Core file exists... "
if [ ! -f "$CORE_FILE" ]; then
    echo "FAIL (file not found)"
    exit 1
fi
echo "PASS"

# Test 2: Core file <=300 lines
echo -n "Test 2: Line count <= $MAX_LINES... "
LINE_COUNT=$(wc -l < "$CORE_FILE")
if [ "$LINE_COUNT" -gt "$MAX_LINES" ]; then
    echo "FAIL (got $LINE_COUNT lines, max $MAX_LINES)"
    exit 1
fi
echo "PASS ($LINE_COUNT lines)"

# Test 3: Required section - YAML frontmatter
echo -n "Test 3: YAML frontmatter present... "
if ! grep -q "^---" "$CORE_FILE"; then
    echo "FAIL"
    exit 1
fi
echo "PASS"

# Test 4-11: Required sections (8 total)
REQUIRED_SECTIONS=(
    "## Purpose"
    "## When Invoked"
    "## .*Workflow"
    "## Success Criteria"
    "## Error Handling"
    "## Reference Loading"
    "## Observation Capture"
)

for i in "${!REQUIRED_SECTIONS[@]}"; do
    SECTION="${REQUIRED_SECTIONS[$i]}"
    TEST_NUM=$((i + 4))
    echo -n "Test $TEST_NUM: Section '$SECTION' exists... "
    if ! grep -qE "$SECTION" "$CORE_FILE"; then
        echo "FAIL"
        exit 1
    fi
    echo "PASS"
done

echo ""
echo "AC#1: All tests PASSED"
