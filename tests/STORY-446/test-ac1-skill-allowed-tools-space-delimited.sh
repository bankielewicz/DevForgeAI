#!/bin/bash
# Test: AC#1 - SKILL.md allowed-tools Is Space-Delimited String
# Story: STORY-446
# Generated: 2026-02-18
# Expected: FAIL (TDD Red) - current file uses YAML array syntax

PASSED=0
FAILED=0
TARGET="/mnt/c/Projects/DevForgeAI2/src/claude/skills/discovering-requirements/SKILL.md"

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

echo "=== AC#1: SKILL.md allowed-tools Is Space-Delimited String ==="

# Extract frontmatter (between --- markers)
FRONTMATTER=$(awk '/^---$/{n++; if(n==2) exit} n==1{print}' "$TARGET")

# Test 1: allowed-tools should be a single-line quoted string, not YAML array
echo "$FRONTMATTER" | grep -qP '^allowed-tools:\s*"[^"]+"'
run_test "allowed-tools is a quoted space-delimited string" $?

# Test 2: No YAML array indicators (lines starting with "  - ")
ARRAY_LINES=$(echo "$FRONTMATTER" | grep -c '^\s*-\s\(Read\|Write\|Edit\|Glob\|Grep\|Bash\|Task\|AskUserQuestion\|WebFetch\)')
[ "$ARRAY_LINES" -eq 0 ]
run_test "No YAML array syntax for tool names" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
