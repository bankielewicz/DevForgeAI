#!/bin/bash
# STORY-189 AC-5: Parameters Documented
# Verifies STORY_ID passed as argument is documented

set -e

HOOKS_README=".claude/hooks/README.md"

echo "=== STORY-189 AC-5: STORY_ID Parameter Documented ==="

FAILED=0

# Test 1: Check for STORY_ID mention
if grep -q "STORY_ID" "$HOOKS_README" || grep -q "story.id" "$HOOKS_README" || grep -q "\$1" "$HOOKS_README"; then
    echo "PASS: STORY_ID or argument reference found"
else
    echo "FAIL: STORY_ID or argument reference NOT found"
    FAILED=1
fi

# Test 2: Check for argument passing documentation (e.g., $1, ${STORY_ID}, argument)
if grep -qi "argument\|parameter\|\$1\|\${" "$HOOKS_README"; then
    echo "PASS: Argument/parameter documentation found"
else
    echo "FAIL: No argument/parameter documentation found"
    FAILED=1
fi

if [[ $FAILED -eq 1 ]]; then
    echo ""
    echo "RESULT: Parameter documentation incomplete"
    exit 1
fi

echo ""
echo "RESULT: STORY_ID parameter documented"
exit 0
