#!/bin/bash
# STORY-121 Unit Test 1: Hook Filters Correctly When DEVFORGEAI_STORY Set
#
# AC#1: DEVFORGEAI_STORY Environment Variable Scopes Validation
#
# Given: A developer sets DEVFORGEAI_STORY=STORY-114
# When: They run git commit (triggering pre-commit hook)
# Then: Pre-commit hook validates only STORY-114 file (not all staged story files)
#
# Test Approach:
# 1. Verify pre-commit hook exists
# 2. Check that hook contains scoping logic (grep for DEVFORGEAI_STORY conditional)
# 3. Verify filtering logic uses story ID pattern in grep command
# 4. Ensure hook validates ONLY the scoped story

set -e

TEST_NAME="test_scoped_filtering"
HOOK_PATH=".git/hooks/pre-commit"

# Create temporary test directory
TEST_TMPDIR=$(mktemp -d)
trap "rm -rf $TEST_TMPDIR" EXIT

cd "$TEST_TMPDIR"
git init >/dev/null 2>&1

# Verify hook exists (should be created by install_hooks.sh)
if [ ! -f "$HOOK_PATH" ]; then
    echo "ERROR: Pre-commit hook not found at $HOOK_PATH" >&2
    exit 1
fi

# Test 1: Verify hook contains DEVFORGEAI_STORY environment variable check
if ! grep -q "DEVFORGEAI_STORY" "$HOOK_PATH"; then
    echo "FAIL: Hook does not check for DEVFORGEAI_STORY environment variable" >&2
    exit 1
fi

# Test 2: Verify hook has scoped filtering logic (conditional block)
if ! grep -q '\[\s*-n\s*"$DEVFORGEAI_STORY"' "$HOOK_PATH"; then
    echo "FAIL: Hook does not have [ -n \"\$DEVFORGEAI_STORY\" ] conditional check" >&2
    exit 1
fi

# Test 3: Verify scoped path uses grep to filter by story ID
if ! grep -q 'grep.*DEVFORGEAI_STORY' "$HOOK_PATH"; then
    echo "FAIL: Hook does not filter files by DEVFORGEAI_STORY in grep pattern" >&2
    exit 1
fi

# Test 4: Verify filtering uses sed or parameter expansion to build pattern
if ! grep -q '${DEVFORGEAI_STORY}' "$HOOK_PATH"; then
    echo "FAIL: Hook does not use \$DEVFORGEAI_STORY variable in filtering logic" >&2
    exit 1
fi

# Test 5: Verify scoped mode does NOT match all .story.md files
# The scoped grep should NOT have the general .story.md$ pattern
SCOPED_SECTION=$(awk '/\[\s*-n\s*"\$DEVFORGEAI_STORY"/ {found=1} found && /fi/ {exit} found' "$HOOK_PATH")
if echo "$SCOPED_SECTION" | grep -q '\.story\.md$'; then
    echo "FAIL: Scoped filtering section contains .story.md$ pattern (should only match specific story)" >&2
    exit 1
fi

echo "PASS: Hook correctly filters when DEVFORGEAI_STORY is set"
exit 0
