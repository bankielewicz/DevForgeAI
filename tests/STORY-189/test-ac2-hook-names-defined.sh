#!/bin/bash
# STORY-189 AC-2: Hook Names Defined
# Verifies post-qa-success.sh, post-qa-failure.sh, post-qa-warning.sh are defined

set -e

HOOKS_README=".claude/hooks/README.md"

echo "=== STORY-189 AC-2: Hook Names Defined ==="

FAILED=0

# Test 1: post-qa-success.sh
if grep -q "post-qa-success.sh" "$HOOKS_README"; then
    echo "PASS: post-qa-success.sh defined"
else
    echo "FAIL: post-qa-success.sh NOT defined"
    FAILED=1
fi

# Test 2: post-qa-failure.sh
if grep -q "post-qa-failure.sh" "$HOOKS_README"; then
    echo "PASS: post-qa-failure.sh defined"
else
    echo "FAIL: post-qa-failure.sh NOT defined"
    FAILED=1
fi

# Test 3: post-qa-warning.sh
if grep -q "post-qa-warning.sh" "$HOOKS_README"; then
    echo "PASS: post-qa-warning.sh defined"
else
    echo "FAIL: post-qa-warning.sh NOT defined"
    FAILED=1
fi

if [[ $FAILED -eq 1 ]]; then
    echo ""
    echo "RESULT: Some hook names are missing"
    exit 1
fi

echo ""
echo "RESULT: All 3 hook names defined"
exit 0
