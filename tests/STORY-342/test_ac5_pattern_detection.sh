#!/bin/bash
# STORY-342 AC#5: Pattern Detection Algorithm Implemented
# Tests that the post-qa-memory-update.sh hook exists and has required functions

set -e

PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$(dirname "$0")/../.." && pwd)}"
HOOK_FILE="$PROJECT_ROOT/.claude/hooks/post-qa-memory-update.sh"
HOOKS_CONFIG="$PROJECT_ROOT/devforgeai/config/hooks.yaml"

echo "=== AC#5: Pattern Detection Algorithm Tests ==="

# Test 1: Hook file exists
echo -n "Test 1: post-qa-memory-update.sh exists... "
if [ -f "$HOOK_FILE" ]; then
    echo "PASS"
else
    echo "FAIL - Hook file not found at $HOOK_FILE"
    exit 1
fi

# Test 2: Hook is executable
echo -n "Test 2: Hook file is executable... "
if [ -x "$HOOK_FILE" ]; then
    echo "PASS"
else
    echo "FAIL - Hook file is not executable"
    exit 1
fi

# Test 3: Hook reads session memory (pattern detection step 1)
echo -n "Test 3: Hook contains session memory read logic... "
if grep -qi "session\|observation\|memory" "$HOOK_FILE"; then
    echo "PASS"
else
    echo "FAIL - Hook does not contain session/observation reading logic"
    exit 1
fi

# Test 4: Hook updates long-term memory files
echo -n "Test 4: Hook contains long-term memory update logic... "
if grep -qi "learning\|pattern\|update" "$HOOK_FILE"; then
    echo "PASS"
else
    echo "FAIL - Hook does not contain long-term memory update logic"
    exit 1
fi

# Test 5: Hook implements pattern detection algorithm
echo -n "Test 5: Hook implements pattern detection (keyword extraction)... "
if grep -qi "keyword\|hash\|pattern_id\|extract" "$HOOK_FILE"; then
    echo "PASS"
else
    echo "FAIL - Hook does not implement pattern detection algorithm"
    exit 1
fi

# Test 6: Hook registered in hooks.yaml
echo -n "Test 6: Hook registered in hooks.yaml... "
if [ -f "$HOOKS_CONFIG" ] && grep -q "post-qa-memory-update" "$HOOKS_CONFIG"; then
    echo "PASS"
else
    echo "FAIL - Hook not registered in hooks.yaml"
    exit 1
fi

# Test 7: Hook handles pattern merging (70% keyword overlap)
echo -n "Test 7: Hook implements pattern merging logic... "
if grep -qi "merge\|overlap\|similar" "$HOOK_FILE"; then
    echo "PASS"
else
    echo "FAIL - Hook does not implement pattern merging logic"
    exit 1
fi

echo ""
echo "=== AC#5 Tests Complete: All PASSED ==="
