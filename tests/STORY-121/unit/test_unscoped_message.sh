#!/bin/bash
# STORY-121 Unit Test 4: Hook Message Absent When Unset (Backward Compat)
#
# AC#3: Clear Console Message Shows Scoping Status (backward compatibility)
#
# Given: DEVFORGEAI_STORY is NOT set
# When: Pre-commit hook runs
# Then: Console shows NO scoping message (original behavior preserved)
#
# Test Approach:
# 1. Verify pre-commit hook exists
# 2. Check that "Scoped to:" message is ONLY in the if branch
# 3. Verify else branch does NOT contain the scoping message
# 4. Ensure backward compatibility (unscoped runs silently)

set -e

TEST_NAME="test_unscoped_message"
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

# Test 1: Verify hook has scoped message
if ! grep -q 'Scoped to:' "$HOOK_PATH"; then
    echo "FAIL: Hook does not contain 'Scoped to:' message (Test 3 may have failed)" >&2
    exit 1
fi

# Test 2: Verify "Scoped to:" message is ONLY in the if (scoped) branch
# Extract the if and else branches separately and verify message placement
IF_BLOCK=$(awk '/\[\s*-n\s*"\$DEVFORGEAI_STORY"/ {found=1} found && /else/ {exit} found {print}' "$HOOK_PATH")
ELSE_BLOCK=$(awk '/^else/ {found=1} found && /fi/ {exit} found {print}' "$HOOK_PATH")

# Verify message exists in if block
if ! echo "$IF_BLOCK" | grep -q 'Scoped to:'; then
    echo "FAIL: 'Scoped to:' message not found in scoped (if) branch" >&2
    exit 1
fi

# Verify message does NOT exist in else block
if echo "$ELSE_BLOCK" | grep -q 'Scoped to:'; then
    echo "FAIL: 'Scoped to:' message should NOT appear in unscoped (else) branch" >&2
    exit 1
fi

# Test 3: Verify else branch does not have echo statement for scoping
if echo "$ELSE_BLOCK" | grep -q 'Scoped'; then
    echo "FAIL: Else branch contains reference to scoping (should not)" >&2
    exit 1
fi

# Test 4: Verify conditional has proper if/else/fi structure
CONDITIONAL_COUNT=$(grep -c '^if \[' "$HOOK_PATH" || echo "0")
ELSE_COUNT=$(grep -c '^else' "$HOOK_PATH" || echo "0")
FI_COUNT=$(grep -c '^fi' "$HOOK_PATH" || echo "0")

if [ "$CONDITIONAL_COUNT" -lt 1 ] || [ "$ELSE_COUNT" -lt 1 ] || [ "$FI_COUNT" -lt 1 ]; then
    echo "FAIL: Hook missing proper if/else/fi structure" >&2
    exit 1
fi

echo "PASS: Unscoped mode runs without 'Scoped to:' message (backward compatible)"
exit 0
