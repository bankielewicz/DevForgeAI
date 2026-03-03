#!/bin/bash
# Test: AC#3 - Multi-Select Feature Presentation
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

echo "=== AC#3: Multi-Select Feature Presentation ==="

# Test 1: Step 0.3 section exists
grep -q "Step 0\.3" "$TARGET_FILE" 2>/dev/null
run_test "Step 0.3 section exists in story-discovery.md" $?

# Test 2: AskUserQuestion tool referenced
grep -q "AskUserQuestion" "$TARGET_FILE" 2>/dev/null
run_test "AskUserQuestion tool referenced" $?

# Test 3: multiSelect: true option documented
grep -qi "multiSelect.*true\|multi.select" "$TARGET_FILE" 2>/dev/null
run_test "multiSelect: true option documented" $?

# Test 4: Pre-selected features skip logic
grep -qi "pre.selected\|already.*selected\|skip.*selection" "$TARGET_FILE" 2>/dev/null
run_test "Pre-selected features skip logic documented" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
