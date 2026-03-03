#!/bin/bash
# Test: AC#2 - subagents-reference.md Updated with alignment-auditor
# Story: STORY-476
# Generated: 2026-02-23

PASSED=0
FAILED=0
TARGET="src/claude/memory/subagents-reference.md"

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

echo "=== AC#2: subagents-reference.md Updated with alignment-auditor ==="

# Test 1: alignment-auditor row exists in Available Subagents table
grep -q 'alignment-auditor' "$TARGET"
run_test "alignment-auditor entry exists" $?

# Test 2: Entry is in alphabetical order (between agent-generator and anti-pattern-scanner)
# Extract table lines only (lines with | ** pattern) and verify ordering
BEFORE_LINE=$(grep -n '| \*\*agent-generator\*\*' "$TARGET" | head -1 | cut -d: -f1)
AFTER_LINE=$(grep -n '| \*\*anti-pattern-scanner\*\*' "$TARGET" | head -1 | cut -d: -f1)
AUDITOR_LINE=$(grep -n '| \*\*alignment-auditor\*\*' "$TARGET" | head -1 | cut -d: -f1)
if [ -n "$BEFORE_LINE" ] && [ -n "$AFTER_LINE" ] && [ -n "$AUDITOR_LINE" ]; then
    [ "$AUDITOR_LINE" -gt "$BEFORE_LINE" ] && [ "$AUDITOR_LINE" -lt "$AFTER_LINE" ]
    run_test "alignment-auditor in alphabetical order (between agent-generator and anti-pattern-scanner)" $?
else
    run_test "alignment-auditor in alphabetical order (between agent-generator and anti-pattern-scanner)" 1
fi

# Test 3: Model is haiku
grep 'alignment-auditor' "$TARGET" | grep -qi 'haiku'
run_test "Model is haiku" $?

# Test 4: Tools include Read, Glob, Grep
grep 'alignment-auditor' "$TARGET" | grep -q 'Read' && \
grep 'alignment-auditor' "$TARGET" | grep -q 'Glob' && \
grep 'alignment-auditor' "$TARGET" | grep -q 'Grep'
run_test "Tools include [Read, Glob, Grep]" $?

# Test 5: Proactive trigger mapping entry exists
grep -A 200 'Proactive Trigger' "$TARGET" | grep -q 'alignment-auditor'
run_test "Proactive trigger mapping entry exists" $?

# Test 6: Subagent count is 40 (not 39) in summary/count lines
# Look for lines that mention a total/count of subagents with the number 40
grep -i 'total\|count\|available' "$TARGET" | grep -q '\b40\b'
run_test "Subagent count updated to 40 in summary lines" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
