#!/bin/bash
# Test: AC#3 - Iteration and Refinement Support
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

echo "=== AC#3: Iteration and Refinement Support ==="

# Test 1: Reference file exists
test -f "$REF_FILE"; run_test "Reference file exists" $?

# Test 2: Defines iteration workflow
grep -qiE "(iteration|refinement|refine)" "$REF_FILE" 2>/dev/null; run_test "Defines iteration/refinement workflow" $?

# Test 3: Workflow reads existing canvas
grep -qiE "(read existing|existing.*canvas|load.*canvas)" "$REF_FILE" 2>/dev/null; run_test "Workflow handles reading existing canvas" $?

# Test 4: Workflow presents current state
grep -qiE "(present|display|show.*current)" "$REF_FILE" 2>/dev/null; run_test "Workflow presents current canvas state" $?

# Test 5: Workflow supports modification
grep -qiE "(modify|update|edit|change)" "$REF_FILE" 2>/dev/null; run_test "Workflow supports canvas modification" $?

# Test 6: Workflow writes updated canvas
grep -qiE "(write|save|output|generate)" "$REF_FILE" 2>/dev/null; run_test "Workflow writes updated canvas" $?

# Test 7: Handles existing lean-canvas.md
grep -qi "lean-canvas.md" "$REF_FILE" 2>/dev/null; run_test "References lean-canvas.md file" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
