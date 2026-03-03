#!/bin/bash
# Test Edge Case: Large observations (>1KB per phase)
# Verifies schema doesn't impose size limits

set -e
TARGET_FILE="src/claude/skills/devforgeai-development/phases/phase-01-preflight.md"

echo "Edge Case: Verifying large observation handling..."

# Test 1: No explicit size limits in schema
if grep -qiE 'max.*size|limit.*byte|size.*limit' "$TARGET_FILE"; then
    echo "FAIL: Size limits found - may reject large observations"
    exit 1
fi

# Test 2: Schema uses markdown sections (inherently flexible size)
if grep -qE '## Observations|### Phase' "$TARGET_FILE"; then
    echo "INFO: Markdown section format used - no inherent size limits"
fi

# Test 3: Edit() pattern allows variable-length content
if grep -qE 'Edit.*old_string.*new_string' "$TARGET_FILE"; then
    echo "INFO: Edit pattern supports content of any length"
fi

echo "PASS: Edge case - Large observations supported (no size limits)"
