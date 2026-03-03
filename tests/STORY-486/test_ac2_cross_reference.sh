#!/bin/bash
# Test: AC#2 - Cross-Reference to Session Template
# Story: STORY-486
# Generated: 2026-02-23
# TDD Phase: RED (tests expected to FAIL before implementation)

PASSED=0
FAILED=0
TARGET_FILE="src/claude/skills/implementing-stories/references/observation-capture.md"

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

echo "AC#2: Cross-Reference to Session Template"
echo "Target: $TARGET_FILE"
echo ""

# Arrange: verify target file exists
if [ ! -f "$TARGET_FILE" ]; then
    echo "  ERROR: Target file not found: $TARGET_FILE"
    exit 1
fi

# Test 1: Explicit cross-reference to batch-sibling-story-session-template.md exists
grep -q "batch-sibling-story-session-template" "$TARGET_FILE"
run_test "Explicit cross-reference to batch-sibling-story-session-template.md exists" $?

# Test 2: Cross-reference includes .md extension (full filename reference)
grep -q "batch-sibling-story-session-template\.md" "$TARGET_FILE"
run_test "Cross-reference includes full filename (batch-sibling-story-session-template.md)" $?

# Test 3: Cross-reference appears with usage context (not just a bare mention)
# Usage context: should appear alongside words indicating how/when to use it
grep -qi "batch-sibling-story-session-template" "$TARGET_FILE" && \
    grep -B5 -A5 "batch-sibling-story-session-template" "$TARGET_FILE" | grep -qi "use\|see\|refer\|template\|batch"
run_test "Cross-reference appears with usage context" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
