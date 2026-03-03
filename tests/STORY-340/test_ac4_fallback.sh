#!/bin/bash
# Test AC#4: Graceful Fallback
# Verifies dev-result-interpreter.md contains fallback message for missing ai-analysis.json

set -e
TARGET_FILE=".claude/agents/dev-result-interpreter.md"

echo "AC#4: Verifying fallback message..."

# Test 1: Exact fallback message present
if ! grep -q 'No framework insights captured for this story' "$TARGET_FILE"; then
    echo "FAIL: Missing fallback message 'No framework insights captured for this story'"
    exit 1
fi

# Test 2: Conditional logic for file existence
if ! grep -qi 'IF.*not.*exist\|IF.*missing\|IF.*file.*not\|ELSE' "$TARGET_FILE"; then
    echo "FAIL: Missing conditional logic for file existence check"
    exit 1
fi

echo "PASS: AC#4 Graceful Fallback"
