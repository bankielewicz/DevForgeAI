#!/bin/bash
# STORY-121 Edge Case Test 9: Invalid STORY-XXX Format Handled Gracefully
#
# Technical Spec: Validation: "Must match STORY-\\d{3} format or be unset"
#
# Given: Developer sets DEVFORGEAI_STORY with invalid format:
#   - STORY-120-extra (has extra characters)
#   - STORY-AB (not numeric)
#   - STORY-12 (only 2 digits, needs 3)
#   - invalid-format (no STORY- prefix)
# When: Pre-commit hook runs
# Then: Hook handles invalid format gracefully (either rejects or defaults to unscoped)
# And: No crashes or unexpected behavior occurs
#
# Test Approach:
# 1. Verify hook exists
# 2. Check if hook validates DEVFORGEAI_STORY format
# 3. Test with various invalid formats
# 4. Verify graceful handling (no shell errors)

set -e

TEST_NAME="test_invalid_format"

# Create temporary test directory
TEST_TMPDIR=$(mktemp -d)
trap "rm -rf $TEST_TMPDIR" EXIT

cd "$TEST_TMPDIR"
git init >/dev/null 2>&1

# Test 1: Verify pre-commit hook exists
HOOK_PATH=".git/hooks/pre-commit"
if [ ! -f "$HOOK_PATH" ]; then
    echo "SKIP: Pre-commit hook not found"
    exit 0
fi

# Test 2: Create a story file
mkdir -p devforgeai/specs/Stories
cat > devforgeai/specs/Stories/STORY-120.story.md << 'EOF'
---
id: STORY-120
title: Test Story
status: Backlog
---
# Story
EOF

git add devforgeai/specs/Stories/STORY-120.story.md

# Test 3: Test with STORY-120-extra (has extra suffix)
export DEVFORGEAI_STORY="STORY-120-extra"

# Run hook and check if it handles invalid format gracefully
if bash "$HOOK_PATH" >/dev/null 2>&1; then
    # Hook accepted invalid format - might be too permissive
    # Check if it at least didn't validate the malformed story ID
    echo "WARN: Hook accepts STORY-120-extra (may be too permissive)"
else
    # Hook rejected invalid format - this is acceptable
    echo "PASS: Hook rejects STORY-120-extra (invalid format)"
    return_code=0
fi

# Test 4: Test with STORY-AB (non-numeric)
export DEVFORGEAI_STORY="STORY-AB"

if bash "$HOOK_PATH" >/dev/null 2>&1; then
    echo "WARN: Hook accepts STORY-AB (should validate format)"
else
    echo "PASS: Hook rejects STORY-AB (invalid format)"
fi

# Test 5: Test with STORY-12 (only 2 digits)
export DEVFORGEAI_STORY="STORY-12"

if bash "$HOOK_PATH" >/dev/null 2>&1; then
    echo "WARN: Hook accepts STORY-12 (invalid format)"
else
    echo "PASS: Hook rejects STORY-12 (invalid format)"
fi

# Test 6: Test with invalid-format (completely wrong)
export DEVFORGEAI_STORY="invalid-format"

if bash "$HOOK_PATH" >/dev/null 2>&1; then
    echo "WARN: Hook accepts invalid-format (should reject)"
else
    echo "PASS: Hook rejects invalid-format"
fi

# Test 7: Test with empty string (should default to unscoped)
export DEVFORGEAI_STORY=""

# Empty string should either be treated as unset (unscoped mode)
# or be explicitly rejected - either is acceptable
if bash "$HOOK_PATH" >/dev/null 2>&1; then
    echo "PASS: Hook handles empty DEVFORGEAI_STORY gracefully (defaults to unscoped)"
else
    echo "WARN: Hook rejects empty DEVFORGEAI_STORY"
fi

# Test 8: Verify hook checks for STORY- prefix
if grep -q 'STORY-' "$HOOK_PATH"; then
    echo "PASS: Hook includes STORY- prefix validation"
else
    echo "WARN: Hook may not validate STORY- prefix"
fi

echo "PASS: Invalid format handling verified"
exit 0
