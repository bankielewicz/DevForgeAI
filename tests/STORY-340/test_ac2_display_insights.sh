#!/bin/bash
# Test AC#2: Framework Insights Section Displayed
# Verifies dev-result-interpreter.md contains Framework Insights display template

set -e
TARGET_FILE=".claude/agents/dev-result-interpreter.md"

echo "AC#2: Verifying Framework Insights section..."

# Test 1: Framework Insights header present
if ! grep -q 'Framework Insights' "$TARGET_FILE"; then
    echo "FAIL: Missing 'Framework Insights' section header"
    exit 1
fi

# Test 2: Unicode box drawing characters for visual separation
if ! grep -q '━' "$TARGET_FILE"; then
    echo "FAIL: Missing Unicode box drawing characters"
    exit 1
fi

echo "PASS: AC#2 Framework Insights Section Displayed"
