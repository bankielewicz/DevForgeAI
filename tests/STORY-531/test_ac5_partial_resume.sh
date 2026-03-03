#!/bin/bash
# Test: AC#5 - Partial Completion and Resume
# Story: STORY-531
# Generated: 2026-03-03

set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
REF_FILE="$PROJECT_ROOT/src/claude/skills/planning-business/references/lean-canvas-workflow.md"

PASSED=0
FAILED=0

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        PASSED=$((PASSED+1))
    else
        echo "  FAIL: $name"
        FAILED=$((FAILED+1))
    fi
}

echo "=== AC#5: Partial Completion and Resume ==="

# Test 1: Reference file exists
test -f "$REF_FILE"; run_test "Reference file exists" $?

# Test 2: Defines resume from incomplete blocks
grep -qiE "(resume|incomplete|partial.*completion|continue)" "$REF_FILE" 2>/dev/null; run_test "Defines resume from incomplete blocks" $?

# Test 3: Partial blocks preserved on re-invocation
grep -qiE "(preserv|retain|keep|maintain).*partial" "$REF_FILE" 2>/dev/null; run_test "Partial blocks preserved on re-invocation" $?

# Test 4: Identifies which blocks are complete vs incomplete
grep -qiE "(complete|incomplete|filled|empty|missing).*block" "$REF_FILE" 2>/dev/null; run_test "Identifies complete vs incomplete blocks" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
