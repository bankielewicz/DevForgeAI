#!/bin/bash
# ============================================================================
# STORY-122 Edge Case Test 2: Large Binary Not Corrupted
# ============================================================================
#
# Given: A large binary file (1MB+)
# When: The file is committed and checked out
# Then: The file is unchanged (checksum matches)
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

# Create a 1MB binary file with random data
dd if=/dev/urandom of=large.zip bs=1024 count=1024 2>/dev/null

# Calculate checksum before
CHECKSUM_BEFORE=$(sha256sum large.zip | awk '{print $1}')

# Commit
git add large.zip
git commit -m "Add large binary" >/dev/null 2>&1

# Checkout fresh
rm large.zip
git checkout large.zip

# Calculate checksum after
CHECKSUM_AFTER=$(sha256sum large.zip | awk '{print $1}')

if [[ "$CHECKSUM_BEFORE" != "$CHECKSUM_AFTER" ]]; then
    echo "FAIL: Large binary corrupted (checksums differ)" >&2
    echo "  Before: $CHECKSUM_BEFORE" >&2
    echo "  After:  $CHECKSUM_AFTER" >&2
    exit 1
fi

echo "PASS: Large binary file unchanged"
exit 0
