#!/bin/bash
# ============================================================================
# STORY-122 Unit Test 2: All Text File Types Have eol=lf Rule
# ============================================================================
#
# AC#2: Text Files Auto-Normalize to LF on Commit
#
# Given: .gitattributes exists
# When: Text file patterns are examined
# Then: All specified text extensions have eol=lf attribute
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

# Required text file extensions from story specification
REQUIRED_TEXT_TYPES=(
    "*.sh"
    "*.py"
    "*.md"
    "*.json"
    "*.yaml"
    "*.yml"
    "*.ts"
    "*.tsx"
    "*.js"
    "*.jsx"
)

# Count failures
FAILURES=0

for pattern in "${REQUIRED_TEXT_TYPES[@]}"; do
    # Escape the * for grep
    escaped_pattern=$(echo "$pattern" | sed 's/\*/\\*/g')

    # Check if pattern exists with eol=lf
    if ! grep -E "^${escaped_pattern}[[:space:]].*eol=lf" "$GITATTRIBUTES_PATH" >/dev/null 2>&1; then
        echo "FAIL: Pattern '$pattern' missing or doesn't have eol=lf" >&2
        ((FAILURES++))
    fi
done

if [ $FAILURES -gt 0 ]; then
    echo "FAIL: $FAILURES text file patterns missing eol=lf" >&2
    exit 1
fi

echo "PASS: All required text file types have eol=lf"
exit 0
