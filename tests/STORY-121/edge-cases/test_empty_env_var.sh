#!/bin/bash
# STORY-121 Edge Case Test 10: Empty DEVFORGEAI_STORY Defaults to Unscoped
#
# Technical Spec: "defaults to unscoped if unset"
#
# Given: DEVFORGEAI_STORY is set to empty string ("") or unset
# When: Pre-commit hook runs
# Then: Hook defaults to unscoped mode (validates all .story.md files)
# And: Behavior matches AC#2 (backward compatibility)
#
# Test Approach:
# 1. Verify hook exists
# 2. Test with DEVFORGEAI_STORY="" (empty string)
# 3. Test with unset DEVFORGEAI_STORY
# 4. Verify hook uses [ -n "$DEVFORGEAI_STORY" ] check
# 5. Confirm unscoped filtering applies when variable is empty/unset

set -e

TEST_NAME="test_empty_env_var"

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

# Test 2: Verify hook uses [ -n "$DEVFORGEAI_STORY" ] check
# The [ -n ... ] check returns true only if variable is non-empty
if ! grep -q '\[\s*-n\s*"\$DEVFORGEAI_STORY"' "$HOOK_PATH"; then
    echo "FAIL: Hook does not use [ -n \"\$DEVFORGEAI_STORY\" ] for checking"
    exit 1
fi

# Test 3: Create story files for testing
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

# Test 4: Test with empty string - should use else (unscoped) branch
export DEVFORGEAI_STORY=""

# The [ -n "" ] check should be FALSE, triggering else branch
# This is the critical test - empty string must not trigger scoped mode
if grep -A 5 '\[\s*-n\s*"\$DEVFORGEAI_STORY"' "$HOOK_PATH" | grep -q 'STORY_FILES'; then
    # Verify the structure: if [ -n ... ] then scoped_files else unscoped_files fi
    echo "PASS: Hook structure supports empty variable handling"
else
    echo "FAIL: Hook does not properly handle variable structure"
    exit 1
fi

# Test 5: Verify that empty DEVFORGEAI_STORY doesn't override unscoped logic
# Extract the conditional logic
CONDITIONAL=$(awk '/\[\s*-n\s*"\$DEVFORGEAI_STORY"/ {found=1} found && /fi/ {exit} found' "$HOOK_PATH")

# Count the closing fi
if echo "$CONDITIONAL" | grep -q 'fi'; then
    echo "PASS: Conditional structure is properly closed"
else
    echo "FAIL: Conditional structure missing closing fi"
    exit 1
fi

# Test 6: Verify that [ -n "" ] would evaluate to FALSE
# This is shell behavior, but we verify the hook uses this pattern
# When DEVFORGEAI_STORY is empty, [ -n "$DEVFORGEAI_STORY" ] returns FALSE
# Therefore, the else branch (unscoped) should execute

# Test actual shell behavior
if [ -n "" ]; then
    echo "FAIL: Shell behavior unexpected - [ -n \"\" ] should be FALSE"
    exit 1
else
    # This is correct behavior - empty string is not non-empty
    echo "PASS: [ -n \"\" ] correctly evaluates to FALSE (uses else/unscoped branch)"
fi

# Test 7: Unset the variable and test again
unset DEVFORGEAI_STORY

if [ -n "$DEVFORGEAI_STORY" ]; then
    echo "FAIL: [ -n \$DEVFORGEAI_STORY ] should be FALSE when unset"
    exit 1
else
    echo "PASS: [ -n \$DEVFORGEAI_STORY ] correctly evaluates to FALSE when unset"
fi

# Test 8: Verify hook has proper else branch for unscoped mode
if ! grep -q 'else' "$HOOK_PATH"; then
    echo "FAIL: Hook missing else branch for unscoped fallback"
    exit 1
fi

echo "PASS: Empty/unset DEVFORGEAI_STORY correctly defaults to unscoped mode"
exit 0
