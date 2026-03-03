#!/bin/bash
# Test: AC#2 - Adaptive Question Depth
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

echo "=== AC#2: Adaptive Question Depth ==="

# Test 1: Reference file exists
test -f "$REF_FILE"; run_test "Reference file exists" $?

# Test 2: Defines beginner experience level
grep -qi "beginner" "$REF_FILE" 2>/dev/null; run_test "Defines beginner experience level" $?

# Test 3: Defines intermediate experience level
grep -qi "intermediate" "$REF_FILE" 2>/dev/null; run_test "Defines intermediate experience level" $?

# Test 4: Defines advanced experience level
grep -qi "advanced" "$REF_FILE" 2>/dev/null; run_test "Defines advanced experience level" $?

# Test 5: Beginner has extended/more questions
grep -qi "beginner" "$REF_FILE" 2>/dev/null && grep -qiE "(extended|detailed|more questions|additional)" "$REF_FILE" 2>/dev/null; run_test "Beginner level has extended question depth" $?

# Test 6: Advanced questions are concise
grep -qi "advanced" "$REF_FILE" 2>/dev/null && grep -qiE "(concise|brief|minimal|streamlined)" "$REF_FILE" 2>/dev/null; run_test "Advanced level has concise questions" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
