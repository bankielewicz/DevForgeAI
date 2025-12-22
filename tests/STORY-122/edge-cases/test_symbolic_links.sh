#!/bin/bash
# ============================================================================
# STORY-122 Edge Case Test 3: Symbolic Links Handled Correctly
# ============================================================================
#
# Given: A symbolic link to a text file
# When: Git processes the repository
# Then: The link is preserved, target file is normalized
# ============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
GITATTRIBUTES_PATH="$PROJECT_ROOT/.gitattributes"
TEST_TMPDIR=$(mktemp -d)
trap "rm -rf $TEST_TMPDIR" EXIT

# Check prerequisites
if [ ! -f "$GITATTRIBUTES_PATH" ]; then
    echo "SKIP: .gitattributes not found at project root" >&2
    exit 77
fi

cd "$TEST_TMPDIR"

# Initialize test repository
git init >/dev/null 2>&1
git config user.email "test@test.com"
git config user.name "Test User"

cp "$GITATTRIBUTES_PATH" .gitattributes
git add .gitattributes
git commit -m "Add .gitattributes" >/dev/null 2>&1

# Create a text file with CRLF
printf "content\r\n" > target.md

# Create symbolic link
ln -s target.md link.md

# Commit both
git add target.md link.md
git commit -m "Add file and symlink" >/dev/null 2>&1

# Clean and checkout fresh
rm -f target.md link.md
git checkout .

# Verify link is still a symlink
if [ ! -L link.md ]; then
    echo "FAIL: Symbolic link was not preserved" >&2
    exit 1
fi

# Verify target was normalized (no CRLF)
CRLF_COUNT=$(grep -c $'\r' target.md 2>/dev/null || echo "0")
if [ "$CRLF_COUNT" -gt 0 ]; then
    echo "FAIL: Target file still has CRLF" >&2
    exit 1
fi

# Verify link points to correct target
LINK_TARGET=$(readlink link.md)
if [[ "$LINK_TARGET" != "target.md" ]]; then
    echo "FAIL: Symbolic link target changed to '$LINK_TARGET'" >&2
    exit 1
fi

echo "PASS: Symbolic links handled correctly"
exit 0
