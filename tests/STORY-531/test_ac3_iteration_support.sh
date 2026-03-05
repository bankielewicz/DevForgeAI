#!/bin/bash
# Test: AC#3 - Iteration and Refinement Support
# Story: STORY-531
# Generated: 2026-03-04

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

# Test 1: Iteration section exists with correct heading
grep -q "^## 4\. Iteration and Refinement Workflow$" "$REF_FILE" 2>/dev/null
run_test "Section '## 4. Iteration and Refinement Workflow' exists" $?

# Extract iteration section
ITER_SECTION=$(sed -n '/^## 4\. Iteration and Refinement Workflow$/,/^## [0-9]/p' "$REF_FILE" | head -n -1)

# Test 2: All 4 steps present with correct ### headers
echo "$ITER_SECTION" | grep -q "^### Step 1: Read"
run_test "Iteration has ### Step 1: Read" $?

echo "$ITER_SECTION" | grep -q "^### Step 2: Present"
run_test "Iteration has ### Step 2: Present" $?

echo "$ITER_SECTION" | grep -q "^### Step 3: Modify"
run_test "Iteration has ### Step 3: Modify" $?

echo "$ITER_SECTION" | grep -q "^### Step 4: Write"
run_test "Iteration has ### Step 4: Write" $?

# Test 3: Read step references Read(file_path= pattern for existing canvas
echo "$ITER_SECTION" | grep -q 'Read(file_path='
run_test "Read step uses Read(file_path= pattern" $?

# Test 4: Write step references Write(file_path= pattern for updated canvas
echo "$ITER_SECTION" | grep -q 'Write(file_path='
run_test "Write step uses Write(file_path= pattern" $?

# Test 5: AskUserQuestion is used for presenting iteration options
echo "$ITER_SECTION" | grep -q "AskUserQuestion"
run_test "Iteration workflow uses AskUserQuestion for options" $?

# Test 6: Options include keep/modify/clear-like choices
echo "$ITER_SECTION" | grep -qi "keep"
run_test "Iteration options include 'keep' choice" $?

echo "$ITER_SECTION" | grep -qi "modify"
run_test "Iteration options include 'modify' choice" $?

echo "$ITER_SECTION" | grep -qi "fresh\|clear"
run_test "Iteration options include 'fresh' or 'clear' choice" $?

# Test 7: Unchanged blocks preservation explicitly stated
echo "$ITER_SECTION" | grep -qi "unchanged blocks"
run_test "Iteration explicitly states unchanged blocks are preserved" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
