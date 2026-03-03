#!/bin/bash
# ============================================================================
# STORY-122 Integration Test 4: Renormalization Works
# ============================================================================
#
# AC#5: Existing Files Can Be Renormalized
#
# Given: A repository with mixed line endings
# When: 'git add --renormalize .' is run
# Then: All files are normalized according to .gitattributes
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

# Create files with CRLF BEFORE adding .gitattributes
printf "line1\r\nline2\r\n" > file1.md
printf "line1\r\nline2\r\n" > file2.py
printf '#!/bin/bash\r\necho hello\r\n' > script.sh

git add .
git commit -m "Initial commit with CRLF" >/dev/null 2>&1

# Verify files have CRLF in index
CRLF_COUNT=$(git ls-files --eol | grep -c "i/crlf" || echo "0")
if [ "$CRLF_COUNT" -lt 3 ]; then
    echo "WARNING: Initial files may not have CRLF (got $CRLF_COUNT), test may be inconclusive" >&2
fi

# Now add .gitattributes
cp "$GITATTRIBUTES_PATH" .gitattributes
git add .gitattributes
git commit -m "Add .gitattributes" >/dev/null 2>&1

# Run renormalization
git add --renormalize .
git commit -m "Renormalize line endings" >/dev/null 2>&1 || true  # May be empty if already normalized

# Verify files now have LF in index
LF_COUNT=$(git ls-files --eol | grep -v "i/-" | grep -c "i/lf" || echo "0")
TOTAL_TEXT=$(git ls-files --eol | grep -v "i/-" | wc -l)

if [ "$LF_COUNT" -ne "$TOTAL_TEXT" ]; then
    echo "FAIL: Not all text files normalized to LF" >&2
    echo "  LF count: $LF_COUNT, Total text: $TOTAL_TEXT" >&2
    git ls-files --eol >&2
    exit 1
fi

echo "PASS: Renormalization converted all files to LF"
exit 0
