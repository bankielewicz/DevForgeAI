#!/bin/bash
# ============================================================================
# STORY-122 Unit Test 4: Shell Scripts Explicitly Set to LF
# ============================================================================
#
# AC#3: Shell Scripts Explicitly Set to LF
#
# Given: .gitattributes exists
# When: *.sh pattern is examined
# Then: Shell scripts have explicit 'text eol=lf' (not just text=auto)
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

# Test 1: *.sh pattern exists
if ! grep -q '^\*\.sh[[:space:]]' "$GITATTRIBUTES_PATH"; then
    echo "FAIL: *.sh pattern not found in .gitattributes" >&2
    exit 1
fi

# Test 2: *.sh has explicit 'text' attribute (not relying on text=auto)
if ! grep -E '^\*\.sh[[:space:]].*text[[:space:]]' "$GITATTRIBUTES_PATH" >/dev/null 2>&1 && \
   ! grep -E '^\*\.sh[[:space:]]text[[:space:]]' "$GITATTRIBUTES_PATH" >/dev/null 2>&1; then
    echo "FAIL: *.sh does not have explicit 'text' attribute" >&2
    exit 1
fi

# Test 3: *.sh has eol=lf
if ! grep -E '^\*\.sh[[:space:]].*eol=lf' "$GITATTRIBUTES_PATH" >/dev/null 2>&1; then
    echo "FAIL: *.sh does not have eol=lf attribute" >&2
    exit 1
fi

echo "PASS: Shell scripts explicitly set to LF"
exit 0
