#!/bin/bash
# ============================================================================
# STORY-122 Integration Test 3: Binary Files Unchanged After Commit
# ============================================================================
#
# AC#4: Binary Files Marked as Binary
#
# Given: A binary file (PNG) is committed
# When: Git processes the file
# Then: The binary content is unchanged (checksum matches)
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

# Create a simple PNG file (minimal valid PNG)
# PNG header: 89 50 4E 47 0D 0A 1A 0A followed by IHDR chunk
printf '\x89PNG\r\n\x1a\n' > test.png
# Add some binary data that would be corrupted if line-ending conversion happened
printf '\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde' >> test.png

# Calculate checksum before commit
CHECKSUM_BEFORE=$(sha256sum test.png | awk '{print $1}')

# Commit the binary
git add test.png
git commit -m "Add test binary" >/dev/null 2>&1

# Checkout fresh
rm test.png
git checkout test.png

# Calculate checksum after checkout
CHECKSUM_AFTER=$(sha256sum test.png | awk '{print $1}')

# Compare checksums
if [[ "$CHECKSUM_BEFORE" != "$CHECKSUM_AFTER" ]]; then
    echo "FAIL: Binary file corrupted (checksums differ)" >&2
    echo "  Before: $CHECKSUM_BEFORE" >&2
    echo "  After:  $CHECKSUM_AFTER" >&2
    exit 1
fi

echo "PASS: Binary file unchanged after commit"
exit 0
