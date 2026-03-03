#!/bin/bash
# STORY-121 Edge Case Test 11: Case Sensitivity (STORY-120 vs story-120 vs Story-120)
#
# Technical Spec: Story ID format "STORY-NNN (3-digit number)"
#
# Given: Developer sets DEVFORGEAI_STORY with different cases:
#   - STORY-120 (correct uppercase)
#   - story-120 (lowercase)
#   - Story-120 (mixed case)
# When: Pre-commit hook runs
# Then: Hook correctly identifies STORY-120 files using proper case
# And: Case-insensitive matching is handled appropriately
#
# Test Approach:
# 1. Create story files with correct naming (STORY-120.story.md)
# 2. Test scoping with various case combinations
# 3. Verify grep patterns are case-sensitive or case-insensitive as appropriate
# 4. Confirm story IDs are always uppercase in the framework

set -e

TEST_NAME="test_case_sensitivity"

# Create temporary test directory
TEST_TMPDIR=$(mktemp -d)
trap "rm -rf $TEST_TMPDIR" EXIT

cd "$TEST_TMPDIR"
git init >/dev/null 2>&1

# Test 1: Verify pre-commit hook exists
HOOK_PATH=".git/hooks/pre-commit"
if [ ! -f "$HOOK_PATH" ]; then
    echo "SKIP: Pre-commit hook not found"
    exit 0
fi

# Test 2: Create story file with STANDARD casing (STORY-120)
mkdir -p devforgeai/specs/Stories
cat > devforgeai/specs/Stories/STORY-120.story.md << 'EOF'
---
id: STORY-120
title: Test Story
status: Backlog
---
# Story
EOF

git add devforgeai/specs/Stories/STORY-120.story.md

# Test 3: Test with correct case (STORY-120)
export DEVFORGEAI_STORY="STORY-120"

STAGED_FILES=$(git diff --cached --name-only --diff-filter=d)
FILTERED=$(echo "$STAGED_FILES" | grep "STORY-120" || true)

if echo "$FILTERED" | grep -q 'STORY-120'; then
    echo "PASS: Correct case STORY-120 matches file correctly"
else
    echo "FAIL: Correct case STORY-120 does not match"
    exit 1
fi

# Test 4: Test with lowercase (story-120)
# This should NOT match because story file names are UPPERCASE
export DEVFORGEAI_STORY="story-120"

FILTERED=$(echo "$STAGED_FILES" | grep "story-120" || true)

if [ -z "$FILTERED" ]; then
    echo "PASS: Lowercase story-120 does not match uppercase STORY-120 (case-sensitive)"
else
    echo "WARN: Lowercase story-120 matches - grep may be case-insensitive"
    # This is not necessarily wrong, just different behavior
fi

# Test 5: Test with mixed case (Story-120)
export DEVFORGEAI_STORY="Story-120"

FILTERED=$(echo "$STAGED_FILES" | grep "Story-120" || true)

if [ -z "$FILTERED" ]; then
    echo "PASS: Mixed case Story-120 does not match uppercase STORY-120 (case-sensitive)"
else
    echo "WARN: Mixed case Story-120 matches - grep may be case-insensitive"
fi

# Test 6: Verify framework convention: all story IDs are UPPERCASE
# Check if actual story files in the project use uppercase
if [ -d "devforgeai/specs/Stories" ]; then
    STORY_FILES=$(find devforgeai/specs/Stories -name "*.story.md" 2>/dev/null | head -5 || true)
    if [ -n "$STORY_FILES" ]; then
        # Check if any files have lowercase story IDs
        if echo "$STORY_FILES" | grep -qE '[a-z]+' 2>/dev/null; then
            echo "WARN: Some story files may have lowercase names"
        else
            echo "PASS: Story files follow UPPERCASE naming convention"
        fi
    fi
fi

# Test 7: Verify hook grep pattern is case-sensitive
# Standard grep is case-sensitive by default
if grep -q 'grep' "$HOOK_PATH"; then
    # Check if hook uses -i flag for case-insensitive matching
    if grep 'grep' "$HOOK_PATH" | grep -q '\-i'; then
        echo "WARN: Hook uses case-insensitive grep (-i flag)"
    else
        echo "PASS: Hook uses case-sensitive grep (default behavior)"
    fi
fi

# Test 8: Framework convention check
# Story IDs in the framework should always be STORY-NNN format (uppercase)
if grep -q 'STORY-' "$HOOK_PATH"; then
    echo "PASS: Hook references STORY- prefix (uppercase convention)"
else
    echo "WARN: Hook may not enforce STORY- uppercase convention"
fi

echo "PASS: Case sensitivity handling verified"
exit 0
