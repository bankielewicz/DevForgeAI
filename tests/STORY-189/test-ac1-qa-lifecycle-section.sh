#!/bin/bash
# STORY-189 AC-1: Convention Documented
# Verifies .claude/hooks/README.md includes "QA Lifecycle Hooks" section

set -e

HOOKS_README=".claude/hooks/README.md"

echo "=== STORY-189 AC-1: QA Lifecycle Hooks Section Exists ==="

# Test 1: Check file exists
if [[ ! -f "$HOOKS_README" ]]; then
    echo "FAIL: $HOOKS_README does not exist"
    exit 1
fi

# Test 2: Check for "QA Lifecycle Hooks" section header
if grep -q "^## QA Lifecycle Hooks" "$HOOKS_README"; then
    echo "PASS: 'QA Lifecycle Hooks' section found"
    exit 0
else
    echo "FAIL: 'QA Lifecycle Hooks' section NOT found in $HOOKS_README"
    echo "Expected: A section header '## QA Lifecycle Hooks'"
    exit 1
fi
