#!/bin/bash
# Test: AC#4 - CLAUDE.md Subagent Registry Updated
# Story: STORY-476
# Generated: 2026-02-23

PASSED=0
FAILED=0
TARGET="CLAUDE.md"

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

echo "=== AC#4: CLAUDE.md Subagent Registry Updated ==="

# Test 1: alignment-auditor row exists in Subagent Registry (between BEGIN/END markers)
sed -n '/BEGIN SUBAGENT REGISTRY/,/END SUBAGENT REGISTRY/p' "$TARGET" | grep -q 'alignment-auditor'
run_test "alignment-auditor in Subagent Registry table" $?

# Test 2: Description present for alignment-auditor
sed -n '/BEGIN SUBAGENT REGISTRY/,/END SUBAGENT REGISTRY/p' "$TARGET" | grep 'alignment-auditor' | grep -q '|.*|.*|'
run_test "Description present in registry row" $?

# Test 3: Tools [Read, Glob, Grep] present
sed -n '/BEGIN SUBAGENT REGISTRY/,/END SUBAGENT REGISTRY/p' "$TARGET" | grep 'alignment-auditor' | grep -q 'Read' && \
sed -n '/BEGIN SUBAGENT REGISTRY/,/END SUBAGENT REGISTRY/p' "$TARGET" | grep 'alignment-auditor' | grep -q 'Glob' && \
sed -n '/BEGIN SUBAGENT REGISTRY/,/END SUBAGENT REGISTRY/p' "$TARGET" | grep 'alignment-auditor' | grep -q 'Grep'
run_test "Tools [Read, Glob, Grep] present" $?

# Test 4: alignment-auditor in Proactive Trigger Mapping table
grep -A 500 'Proactive Trigger Mapping' "$TARGET" | grep -q 'alignment-auditor'
run_test "alignment-auditor in Proactive Trigger Mapping" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
