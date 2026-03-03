#!/bin/bash
# STORY-215 AC-2: Checklist Contains 5 Verification Points
# Tests that all 5 required verification points are present
# Expected: FAIL initially (file not yet modified)

# Note: Not using set -e to allow all tests to run even when some fail

CLAUDE_MD="/mnt/c/Projects/DevForgeAI2/CLAUDE.md"
TEST_NAME="AC-2: Checklist Contains 5 Verification Points"
PASS_COUNT=0
FAIL_COUNT=0

echo "=================================================="
echo "STORY-215 Test: $TEST_NAME"
echo "=================================================="

# Test 2.1: Verification Point 1 - "Skill contains phases?"
echo -n "Test 2.1: Verification point 'Skill contains phases?' exists... "
if grep -q "Skill contains phases?" "$CLAUDE_MD"; then
    echo "PASS"
    ((PASS_COUNT++))
else
    echo "FAIL - Missing verification point: 'Skill contains phases?'"
    ((FAIL_COUNT++))
fi

# Test 2.2: Verification Point 2 - "Phase 0 has reference loading?"
echo -n "Test 2.2: Verification point 'Phase 0 has reference loading?' exists... "
if grep -q "Phase 0 has reference loading?" "$CLAUDE_MD"; then
    echo "PASS"
    ((PASS_COUNT++))
else
    echo "FAIL - Missing verification point: 'Phase 0 has reference loading?'"
    ((FAIL_COUNT++))
fi

# Test 2.3: Verification Point 3 - "Phases 1-4 have pre-flight checks?"
echo -n "Test 2.3: Verification point 'Phases 1-4 have pre-flight checks?' exists... "
if grep -q "Phases 1-4 have pre-flight checks?" "$CLAUDE_MD"; then
    echo "PASS"
    ((PASS_COUNT++))
else
    echo "FAIL - Missing verification point: 'Phases 1-4 have pre-flight checks?'"
    ((FAIL_COUNT++))
fi

# Test 2.4: Verification Point 4 - "Skill says \"YOU execute\"?"
echo -n "Test 2.4: Verification point 'Skill says \"YOU execute\"?' exists... "
if grep -q 'Skill says "YOU execute"?' "$CLAUDE_MD"; then
    echo "PASS"
    ((PASS_COUNT++))
else
    echo "FAIL - Missing verification point: 'Skill says \"YOU execute\"?'"
    ((FAIL_COUNT++))
fi

# Test 2.5: Verification Point 5 - "Mode requested matches execution scope?"
echo -n "Test 2.5: Verification point 'Mode requested matches execution scope?' exists... "
if grep -q "Mode requested matches execution scope?" "$CLAUDE_MD"; then
    echo "PASS"
    ((PASS_COUNT++))
else
    echo "FAIL - Missing verification point: 'Mode requested matches execution scope?'"
    ((FAIL_COUNT++))
fi

# Test 2.6: Verify numbered list structure (1. through 5.)
echo -n "Test 2.6: Numbered list has 5 items... "
NUMBERED_ITEMS=$(grep -c "^[0-9]\. \*\*" "$CLAUDE_MD" 2>/dev/null || echo "0")
# We need at least 5 numbered items with bold formatting
if [ "$NUMBERED_ITEMS" -ge 5 ]; then
    echo "PASS (Found $NUMBERED_ITEMS numbered items)"
    ((PASS_COUNT++))
else
    echo "FAIL - Expected at least 5 numbered verification points, found $NUMBERED_ITEMS"
    ((FAIL_COUNT++))
fi

echo ""
echo "=================================================="
echo "Results: $PASS_COUNT passed, $FAIL_COUNT failed"
echo "=================================================="

if [ $FAIL_COUNT -gt 0 ]; then
    echo "AC-2 FAILED: Not all 5 verification points present in CLAUDE.md"
    exit 1
else
    echo "AC-2 PASSED: All 5 verification points present in CLAUDE.md"
    exit 0
fi
