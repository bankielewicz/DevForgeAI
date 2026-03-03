#!/bin/bash
# Test: AC#1 - Complete Lean Canvas Generation
# Story: STORY-531
# Generated: 2026-03-03

set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SKILL_FILE="$PROJECT_ROOT/src/claude/skills/planning-business/SKILL.md"
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

echo "=== AC#1: Complete Lean Canvas Generation ==="

# Test 1: SKILL.md exists
test -f "$SKILL_FILE"; run_test "SKILL.md exists at src/claude/skills/planning-business/SKILL.md" $?

# Test 2: Reference file exists
test -f "$REF_FILE"; run_test "lean-canvas-workflow.md exists in references/" $?

# Test 3: SKILL.md contains lean canvas phase definition
grep -qi "lean canvas" "$SKILL_FILE" 2>/dev/null; run_test "SKILL.md contains lean canvas phase definition" $?

# Test 4-12: Reference contains all 9 lean canvas blocks
for block in "Problem" "Customer Segments" "Unique Value Proposition" "Solution" "Channels" "Revenue Streams" "Cost Structure" "Key Metrics" "Unfair Advantage"; do
    grep -qi "$block" "$REF_FILE" 2>/dev/null; run_test "Reference contains block: $block" $?
done

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
