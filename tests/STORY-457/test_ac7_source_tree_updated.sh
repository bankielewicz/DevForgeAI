#!/usr/bin/env bash
# STORY-457 AC#7: source-tree.md updated for new artifacts
# Tests run against devforgeai/specs/context/ (shared context file)
set -euo pipefail

SOURCE_TREE="devforgeai/specs/context/source-tree.md"
PASS=0
FAIL=0

assert_true() {
    local desc="$1"; shift
    if "$@" >/dev/null 2>&1; then
        echo "  PASS: $desc"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: $desc"
        FAIL=$((FAIL + 1))
    fi
}

echo "=== AC#7: source-tree.md Updated ==="
echo ""

# Test 1: source-tree.md exists
echo "--- File Existence ---"
assert_true "source-tree.md exists" test -f "$SOURCE_TREE"

# Test 2: Skill entry added
echo "--- Skill Entry ---"
assert_true "Has validating-epic-coverage skill entry" grep -q 'validating-epic-coverage' "$SOURCE_TREE"

# Test 3: Subagent entry added
echo "--- Subagent Entry ---"
assert_true "Has epic-coverage-result-interpreter entry" grep -q 'epic-coverage-result-interpreter' "$SOURCE_TREE"

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
