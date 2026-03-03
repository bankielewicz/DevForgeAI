#!/bin/bash
# Test: AC#4 - Batch Metadata Collection
# Story: STORY-409
# Generated: 2026-02-16

PASSED=0
FAILED=0
TARGET_FILE="src/claude/skills/devforgeai-story-creation/references/story-discovery.md"

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

echo "=== AC#4: Batch Metadata Collection ==="

# Test 1: Step 0.4 section exists
grep -q "Step 0\.4" "$TARGET_FILE" 2>/dev/null
run_test "Step 0.4 section exists in story-discovery.md" $?

# Test 2: Sprint assignment question
grep -qi "sprint" "$TARGET_FILE" 2>/dev/null
run_test "Sprint assignment collection documented" $?

# Test 3: Priority question with valid values
grep -qE "Critical|High|Medium|Low" "$TARGET_FILE" 2>/dev/null
run_test "Priority values (Critical/High/Medium/Low) documented" $?

# Test 4: Story points with Fibonacci values
grep -qE "1.*2.*3.*5.*8.*13|Fibonacci|story.*points" "$TARGET_FILE" 2>/dev/null
run_test "Story points Fibonacci values documented" $?

# Test 5: Default values concept
grep -qi "default" "$TARGET_FILE" 2>/dev/null
run_test "Default metadata concept documented" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
