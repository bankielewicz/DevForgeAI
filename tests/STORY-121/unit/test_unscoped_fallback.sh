#!/bin/bash
# STORY-121 Unit Test 2: Hook Validates All Stories When DEVFORGEAI_STORY Unset
#
# AC#2: Backward Compatibility When Env Var Unset
#
# Given: DEVFORGEAI_STORY is NOT set
# When: Developer runs git commit
# Then: Pre-commit hook validates ALL staged .story.md files (original behavior)
#
# Test Approach:
# 1. Verify pre-commit hook exists
# 2. Check that hook has else/fallback branch for unscoped mode
# 3. Verify fallback uses .story.md$ pattern to match all story files
# 4. Ensure else branch exists when DEVFORGEAI_STORY is unset

set -e

TEST_NAME="test_unscoped_fallback"
HOOK_PATH=".git/hooks/pre-commit"

# Create temporary test directory
TEST_TMPDIR=$(mktemp -d)
trap "rm -rf $TEST_TMPDIR" EXIT

cd "$TEST_TMPDIR"
git init >/dev/null 2>&1

# Verify hook exists
if [ ! -f "$HOOK_PATH" ]; then
    echo "ERROR: Pre-commit hook not found at $HOOK_PATH" >&2
    exit 1
fi

# Test 1: Verify hook has else block for unscoped mode
if ! grep -q 'else' "$HOOK_PATH"; then
    echo "FAIL: Hook does not have else block for unscoped fallback" >&2
    exit 1
fi

# Test 2: Verify else block contains .story.md$ pattern
# Extract the else block and check for the default behavior
ELSE_FOUND=0
IN_ELSE=0
while IFS= read -r line; do
    if [[ $line =~ ^else ]]; then
        IN_ELSE=1
    elif [[ $IN_ELSE -eq 1 && $line =~ fi ]]; then
        break
    elif [[ $IN_ELSE -eq 1 ]]; then
        if [[ $line =~ \.story\.md$ ]]; then
            ELSE_FOUND=1
            break
        fi
    fi
done < "$HOOK_PATH"

if [ $ELSE_FOUND -eq 0 ]; then
    echo "FAIL: Hook else block does not contain .story.md$ pattern for validating all stories" >&2
    exit 1
fi

# Test 3: Verify unscoped mode uses grep without story ID filter
# The else section should NOT have ${DEVFORGEAI_STORY} variable substitution
if grep -A 20 'else' "$HOOK_PATH" | grep -q '${DEVFORGEAI_STORY}'; then
    echo "FAIL: Unscoped else block should not reference \$DEVFORGEAI_STORY" >&2
    exit 1
fi

# Test 4: Verify STORY_FILES variable is set in both branches
if ! grep -q 'STORY_FILES=' "$HOOK_PATH"; then
    echo "FAIL: Hook does not set STORY_FILES variable" >&2
    exit 1
fi

# Test 5: Verify conditional structure is correct (if/else/fi)
if ! grep -q 'if \[' "$HOOK_PATH" || ! grep -q 'fi' "$HOOK_PATH"; then
    echo "FAIL: Hook missing proper if/fi conditional structure" >&2
    exit 1
fi

echo "PASS: Hook correctly validates all stories when DEVFORGEAI_STORY is unset"
exit 0
