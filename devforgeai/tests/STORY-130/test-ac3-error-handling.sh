#!/bin/bash
# STORY-130 AC#3: Skill Validation Failure Halts Command with Clear Error
# Tests that skill validation failures are propagated with HALT pattern
# Expected: Error handling section mentions skill failure propagation

# Note: No set -e because we want to run all tests even if some fail

IDEATE_FILE=".claude/commands/ideate.md"
PASS_COUNT=0
FAIL_COUNT=0
TOTAL_TESTS=4

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  STORY-130 AC#3: Skill Validation Failure Handling"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test 1: Error handling section exists
if grep -q "## Error Handling" "$IDEATE_FILE" 2>/dev/null; then
    echo "✓ PASS: Error handling section exists"
    ((PASS_COUNT++))
else
    echo "✗ FAIL: Error handling section missing"
    ((FAIL_COUNT++))
fi

# Test 2: Skill validation failure mentioned
if grep -qi "skill.*validation.*fail\|validation.*fail.*skill\|Phase 6.4.*fail" "$IDEATE_FILE" 2>/dev/null; then
    echo "✓ PASS: Skill validation failure handling documented"
    ((PASS_COUNT++))
else
    echo "✗ FAIL: No skill validation failure handling documented"
    ((FAIL_COUNT++))
fi

# Test 3: HALT pattern present for failures
if grep -q "HALT" "$IDEATE_FILE" 2>/dev/null; then
    echo "✓ PASS: HALT pattern present"
    ((PASS_COUNT++))
else
    echo "✗ FAIL: HALT pattern not found"
    ((FAIL_COUNT++))
fi

# Test 4: Error propagation (skill error passed through without modification)
# Should mention passing skill errors to user without modification/suppression
if grep -qi "propagat\|pass.*through\|verbatim\|without.*modif" "$IDEATE_FILE" 2>/dev/null; then
    echo "✓ PASS: Error propagation documented"
    ((PASS_COUNT++))
else
    echo "✗ FAIL: Error propagation not documented"
    ((FAIL_COUNT++))
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Results: $PASS_COUNT/$TOTAL_TESTS passed"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $FAIL_COUNT -gt 0 ]; then
    echo "  Status: FAILED ($FAIL_COUNT error handling issues)"
    exit 1
else
    echo "  Status: PASSED (error handling properly configured)"
    exit 0
fi
