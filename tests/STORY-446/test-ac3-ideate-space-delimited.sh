#!/bin/bash
# Test: AC#3 - ideate.md allowed-tools Is Space-Delimited
# Story: STORY-446
# Generated: 2026-02-18
# Expected: FAIL (TDD Red) - current file uses comma-delimited

PASSED=0
FAILED=0
TARGET="/mnt/c/Projects/DevForgeAI2/src/claude/commands/ideate.md"

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        ((PASSED++))
    else
        echo "  FAIL: $name"
        ((FAILED++))
    fi
}

echo "=== AC#3: ideate.md allowed-tools Is Space-Delimited ==="

FRONTMATTER=$(awk '/^---$/{n++; if(n==2) exit} n==1{print}' "$TARGET")

# Test 1: allowed-tools line contains no commas
TOOLS_LINE=$(echo "$FRONTMATTER" | grep '^allowed-tools:')
echo "$TOOLS_LINE" | grep -q ','
[ $? -ne 0 ]
run_test "No commas in allowed-tools value" $?

# Test 2: allowed-tools is a quoted space-delimited string
echo "$TOOLS_LINE" | grep -qP '^allowed-tools:\s*"[^"]+"'
run_test "allowed-tools is a quoted space-delimited string" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
