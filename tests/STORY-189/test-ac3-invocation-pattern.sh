#!/bin/bash
# STORY-189 AC-3: Invocation Pattern Documented
# Verifies Phase 4.2 invocation pattern is documented

set -e

HOOKS_README=".claude/hooks/README.md"

echo "=== STORY-189 AC-3: Invocation Pattern Documented ==="

FAILED=0

# Test 1: Check for Phase 4.2 reference OR invocation pattern keywords
if grep -qi "phase 4" "$HOOKS_README" || grep -qi "invocation" "$HOOKS_README"; then
    echo "PASS: Invocation/Phase reference found"
else
    echo "FAIL: No invocation pattern or Phase reference found"
    FAILED=1
fi

# Test 2: Check for code block with hook invocation example
if grep -q "post-qa-{status}" "$HOOKS_README" || grep -q "post-qa-success" "$HOOKS_README"; then
    echo "PASS: Hook invocation pattern example found"
else
    echo "FAIL: Hook invocation pattern example NOT found"
    FAILED=1
fi

# Test 3: Check for IF/exists pattern (conditional invocation)
if grep -q "IF exists" "$HOOKS_README" || grep -q "if.*exists" "$HOOKS_README" || grep -q "\-f.*post-qa" "$HOOKS_README"; then
    echo "PASS: Conditional invocation pattern found"
else
    echo "FAIL: Conditional invocation pattern NOT found (IF exists or -f check)"
    FAILED=1
fi

if [[ $FAILED -eq 1 ]]; then
    echo ""
    echo "RESULT: Invocation pattern documentation incomplete"
    exit 1
fi

echo ""
echo "RESULT: Invocation pattern fully documented"
exit 0
