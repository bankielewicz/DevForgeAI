#!/bin/bash
# Test: AC#7 - Removed Epic Batch Workflow Steps 1-3 code blocks
# Story: STORY-408
# Generated: 2026-02-16

PASSED=0
FAILED=0
TARGET_FILE="src/claude/commands/create-story.md"

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

echo "=== AC#7: Removed Steps 1-3 code blocks ==="

# Test 1: No "Extract Features from Epic" section
grep -qi 'Extract Features from Epic' "$TARGET_FILE"
[ $? -ne 0 ]
run_test "No 'Extract Features from Epic' section found" $?

# Test 2: No "Multi-Select Features" section
grep -qi 'Multi-Select Features' "$TARGET_FILE"
[ $? -ne 0 ]
run_test "No 'Multi-Select Features' section found" $?

# Test 3: No "Batch Metadata Collection" section
grep -qi 'Batch Metadata Collection' "$TARGET_FILE"
[ $? -ne 0 ]
run_test "No 'Batch Metadata Collection' section found" $?

# Test 4: No multi-select AskUserQuestion code blocks (batch workflow artifact)
grep -qi 'multi-select' "$TARGET_FILE"
[ $? -ne 0 ]
run_test "No multi-select AskUserQuestion patterns found" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
