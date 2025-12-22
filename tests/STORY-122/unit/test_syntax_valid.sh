#!/bin/bash
# ============================================================================
# STORY-122 Unit Test 1: .gitattributes Syntax Validation
# ============================================================================
#
# AC#1: .gitattributes File Created at Project Root
#
# Given: .gitattributes is created
# When: Git parses the file
# Then: No syntax errors are reported
# ============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
GITATTRIBUTES_PATH="$PROJECT_ROOT/.gitattributes"

# Test 1: File exists at project root
if [ ! -f "$GITATTRIBUTES_PATH" ]; then
    echo "FAIL: .gitattributes does not exist at project root" >&2
    echo "      Expected: $GITATTRIBUTES_PATH" >&2
    exit 1
fi

# Test 2: File is not empty
if [ ! -s "$GITATTRIBUTES_PATH" ]; then
    echo "FAIL: .gitattributes is empty" >&2
    exit 1
fi

# Test 3: Git can parse the file without errors
cd "$PROJECT_ROOT"
ERROR_OUTPUT=$(git check-attr -a -- ".gitattributes" 2>&1) || {
    echo "FAIL: Git cannot parse .gitattributes: $ERROR_OUTPUT" >&2
    exit 1
}

# Test 4: File contains required global default
if ! grep -q '^\*[[:space:]]*text=auto[[:space:]]*eol=lf' "$GITATTRIBUTES_PATH" && \
   ! grep -q '^\*[[:space:]]text=auto[[:space:]]eol=lf' "$GITATTRIBUTES_PATH"; then
    echo "FAIL: Missing global default '* text=auto eol=lf'" >&2
    exit 1
fi

echo "PASS: .gitattributes syntax is valid"
exit 0
