#!/bin/bash
# ============================================================================
# STORY-122 Integration Test 1: CRLF Normalized on Commit
# ============================================================================
#
# AC#2: Text Files Auto-Normalize to LF on Commit
#
# Given: A text file with CRLF line endings
# When: The file is committed
# Then: Git stores the file with LF line endings
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

# Copy project's .gitattributes
cp "$GITATTRIBUTES_PATH" .gitattributes
git add .gitattributes
git commit -m "Add .gitattributes" >/dev/null 2>&1

# Create a file with explicit CRLF endings
printf "line1\r\nline2\r\nline3\r\n" > test.md

# Verify file has CRLF before commit (check for carriage return)
if ! grep -q $'\r' test.md 2>/dev/null; then
    echo "WARNING: Test file may not have CRLF (continuing anyway)" >&2
fi

# Commit the file
git add test.md
git commit -m "Add test file" >/dev/null 2>&1

# Check what git stores (should be LF)
STORED_ENDINGS=$(git ls-files --eol test.md | awk '{print $1}')
if [[ "$STORED_ENDINGS" != "i/lf" ]]; then
    echo "FAIL: Git stored file with '$STORED_ENDINGS' (expected i/lf)" >&2
    exit 1
fi

echo "PASS: CRLF normalized to LF on commit"
exit 0
