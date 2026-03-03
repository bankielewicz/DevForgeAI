#!/bin/bash
# Test AC#3: Top 3 Items Per Category
# Verifies dev-result-interpreter.md limits display to 3 items per category

set -e
TARGET_FILE=".claude/agents/dev-result-interpreter.md"

echo "AC#3: Verifying 3-item limit per category..."

# Test 1: what_worked limited reference
if ! grep -qi 'what_worked.*3\|3.*what_worked\|top.*3\|max.*3\|limit.*3' "$TARGET_FILE"; then
    echo "FAIL: Missing 3-item limit for what_worked_well"
    exit 1
fi

# Test 2: areas_for_improvement limited reference
if ! grep -qi 'improvement.*3\|3.*improvement\|top.*3\|max.*3\|limit.*3' "$TARGET_FILE"; then
    echo "FAIL: Missing 3-item limit for areas_for_improvement"
    exit 1
fi

# Test 3: recommendations limited reference
if ! grep -qi 'recommendation.*3\|3.*recommendation\|top.*3\|max.*3\|limit.*3' "$TARGET_FILE"; then
    echo "FAIL: Missing 3-item limit for recommendations"
    exit 1
fi

echo "PASS: AC#3 Top 3 Items Per Category"
