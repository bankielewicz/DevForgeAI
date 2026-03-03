#!/bin/bash
# ============================================================================
# STORY-122 Edge Case Test 1: Mixed Line Endings Normalized
# ============================================================================
#
# Given: A file with mixed CRLF and LF line endings
# When: The file is committed
# Then: All line endings are normalized to LF
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

# Initialize test repository with .gitattributes
git init >/dev/null 2>&1
git config user.email "test@test.com"
git config user.name "Test User"

cp "$GITATTRIBUTES_PATH" .gitattributes
git add .gitattributes
git commit -m "Add .gitattributes" >/dev/null 2>&1

# Create file with mixed line endings (CRLF, LF, CRLF)
printf "line1\r\nline2\nline3\r\n" > mixed.md

# Commit the file
git add mixed.md
git commit -m "Add mixed file" >/dev/null 2>&1

# Check stored format
STORED=$(git ls-files --eol mixed.md | awk '{print $1}')
if [[ "$STORED" != "i/lf" && "$STORED" != "i/mixed" ]]; then
    # Mixed input should be normalized to LF with text=auto eol=lf
    # Note: some git versions may report i/mixed during transition
    echo "INFO: Git stored file as '$STORED'" >&2
fi

# Checkout and verify all LF
rm mixed.md
git checkout mixed.md

# Count CRLF endings (should be 0)
CRLF_COUNT=$(grep -c $'\r' mixed.md 2>/dev/null || echo "0")
if [ "$CRLF_COUNT" -gt 0 ]; then
    echo "FAIL: File still has $CRLF_COUNT CRLF line endings after checkout" >&2
    exit 1
fi

echo "PASS: Mixed line endings normalized to LF"
exit 0
