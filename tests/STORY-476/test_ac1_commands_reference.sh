#!/bin/bash
# Test: AC#1 - commands-reference.md Updated with /audit-alignment
# Story: STORY-476
# Generated: 2026-02-23

PASSED=0
FAILED=0
TARGET="src/claude/memory/commands-reference.md"

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

echo "=== AC#1: commands-reference.md Updated with /audit-alignment ==="

# Test 1: /audit-alignment entry exists
grep -q '/audit-alignment' "$TARGET"
run_test "/audit-alignment entry exists" $?

# Test 2: Entry is in Framework Maintenance section
grep -A 50 'Framework Maintenance' "$TARGET" | grep -q '/audit-alignment'
run_test "/audit-alignment in Framework Maintenance section" $?

# Test 3: Purpose description present
grep -A 10 '/audit-alignment' "$TARGET" | grep -qi 'purpose\|description'
run_test "Purpose description present" $?

# Test 4: Invokes alignment-auditor subagent mentioned
grep -A 20 '/audit-alignment' "$TARGET" | grep -q 'alignment-auditor'
run_test "Invokes alignment-auditor mentioned" $?

# Test 5: Workflow overview present
grep -A 30 '/audit-alignment' "$TARGET" | grep -qi 'workflow'
run_test "Workflow overview present" $?

# Test 6: Example usage present (at least 2 examples)
EXAMPLE_COUNT=$(grep -A 40 '/audit-alignment' "$TARGET" | grep -c '`/audit-alignment')
[ "$EXAMPLE_COUNT" -ge 2 ]
run_test "At least 2 example usages present (found: $EXAMPLE_COUNT)" $?

# Test 7: Output format documented
grep -A 40 '/audit-alignment' "$TARGET" | grep -qi 'output'
run_test "Output format documented" $?

# Test 8: Related commands section
grep -A 40 '/audit-alignment' "$TARGET" | grep -qi 'related'
run_test "Related commands referenced" $?

# Test 9: Command count is 40 in quick_index
grep -i 'quick.index' "$TARGET" | grep -q '40'
run_test "Command count 40 in quick_index" $?

# Test 10: Command count is 40 in overview
grep -i 'overview' "$TARGET" | grep -q '40'
run_test "Command count 40 in overview" $?

# Test 11: Command count is 40 in command_overview
grep -i 'command.overview' "$TARGET" | grep -q '40'
run_test "Command count 40 in command_overview" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
