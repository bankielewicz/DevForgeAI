#!/bin/bash
# STORY-121 Unit Test 3: Hook Shows "Scoped to: STORY-XX" Message When Set
#
# AC#3: Clear Console Message Shows Scoping Status
#
# Given: A developer commits with DEVFORGEAI_STORY=STORY-114
# When: Pre-commit hook runs
# Then: Console shows "Scoped to: STORY-114"
#
# Test Approach:
# 1. Verify pre-commit hook exists
# 2. Check that hook contains echo statement with "Scoped to:" message
# 3. Verify message includes variable substitution for story ID
# 4. Ensure message is in the scoped (if) branch only

set -e

TEST_NAME="test_scoped_message"
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

# Test 1: Verify hook contains "Scoped to:" message
if ! grep -q 'Scoped to:' "$HOOK_PATH"; then
    echo "FAIL: Hook does not contain 'Scoped to:' message text" >&2
    exit 1
fi

# Test 2: Verify message uses echo command
if ! grep -q 'echo.*Scoped to:' "$HOOK_PATH"; then
    echo "FAIL: Hook does not echo the 'Scoped to:' message" >&2
    exit 1
fi

# Test 3: Verify message includes DEVFORGEAI_STORY variable substitution
if ! grep -q 'echo.*Scoped to:.*\$DEVFORGEAI_STORY\|echo.*Scoped to:.*${DEVFORGEAI_STORY}' "$HOOK_PATH"; then
    echo "FAIL: Message does not substitute \$DEVFORGEAI_STORY variable in output" >&2
    exit 1
fi

# Test 4: Verify message is in the scoped (if -n) branch
# Extract the if block and verify it contains the scoped message
IF_BLOCK=$(awk '/\[\s*-n\s*"\$DEVFORGEAI_STORY"/ {found=1} found && /fi/ {exit} found {print}' "$HOOK_PATH")
if ! echo "$IF_BLOCK" | grep -q 'Scoped to:'; then
    echo "FAIL: 'Scoped to:' message not found in scoped (if) branch" >&2
    exit 1
fi

# Test 5: Verify message format contains story ID pattern
if ! grep 'Scoped to:' "$HOOK_PATH" | grep -q '\$DEVFORGEAI_STORY\|${DEVFORGEAI_STORY}'; then
    echo "FAIL: Message does not display the story ID in message output" >&2
    exit 1
fi

echo "PASS: Hook correctly displays 'Scoped to: STORY-XX' message when scoped"
exit 0
