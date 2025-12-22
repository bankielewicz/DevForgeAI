#!/bin/bash
# ============================================================================
# STORY-122 Unit Test 3: All Binary File Types Marked as Binary
# ============================================================================
#
# AC#4: Binary Files Marked as Binary
#
# Given: .gitattributes exists
# When: Binary file patterns are examined
# Then: All specified binary extensions have 'binary' attribute
# ============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
GITATTRIBUTES_PATH="$PROJECT_ROOT/.gitattributes"

# Check file exists
if [ ! -f "$GITATTRIBUTES_PATH" ]; then
    echo "FAIL: .gitattributes not found at $GITATTRIBUTES_PATH" >&2
    exit 1
fi

# Required binary file extensions from story specification
REQUIRED_BINARY_TYPES=(
    "*.png"
    "*.jpg"
    "*.jpeg"
    "*.gif"
    "*.ico"
    "*.pdf"
    "*.zip"
    "*.tar"
    "*.gz"
)

# Count failures
FAILURES=0

for pattern in "${REQUIRED_BINARY_TYPES[@]}"; do
    # Escape the * for grep
    escaped_pattern=$(echo "$pattern" | sed 's/\*/\\*/g')

    # Check if pattern exists with binary attribute
    if ! grep -E "^${escaped_pattern}[[:space:]].*binary" "$GITATTRIBUTES_PATH" >/dev/null 2>&1; then
        echo "FAIL: Pattern '$pattern' missing or doesn't have binary attribute" >&2
        ((FAILURES++))
    fi
done

if [ $FAILURES -gt 0 ]; then
    echo "FAIL: $FAILURES binary file patterns missing 'binary' attribute" >&2
    exit 1
fi

echo "PASS: All required binary file types marked as binary"
exit 0
