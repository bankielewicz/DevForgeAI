#!/bin/bash
# Test: AC#1 - Skill invocation occurs within first 50 lines of command
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

echo "=== AC#1: Skill invocation within first 50 lines ==="

# Test 1: File exists
[ -f "$TARGET_FILE" ]
run_test "Target file exists" $?

# Test 2: Skill() call exists in file
grep -q 'Skill(command="devforgeai-story-creation")' "$TARGET_FILE"
run_test "Skill invocation call exists in file" $?

# Test 3: Find end of frontmatter (second --- line), then count non-blank lines to Skill() call
FRONTMATTER_END=$(grep -n '^---$' "$TARGET_FILE" | sed -n '2p' | cut -d: -f1)
if [ -z "$FRONTMATTER_END" ]; then
    run_test "Frontmatter end marker found" 1
else
    run_test "Frontmatter end marker found" 0

    # Extract lines after frontmatter, find first Skill() call position in non-blank lines
    SKILL_LINE=$(tail -n +"$((FRONTMATTER_END + 1))" "$TARGET_FILE" | grep -n 'Skill(command="devforgeai-story-creation")' | head -1 | cut -d: -f1)
    if [ -z "$SKILL_LINE" ]; then
        run_test "Skill() call found after frontmatter" 1
    else
        run_test "Skill() call found after frontmatter" 0

        # Count non-blank lines before Skill() call
        NON_BLANK_BEFORE=$(tail -n +"$((FRONTMATTER_END + 1))" "$TARGET_FILE" | head -n "$SKILL_LINE" | grep -c '[^ ]')
        echo "    INFO: Skill() at non-blank line $NON_BLANK_BEFORE after frontmatter"

        [ "$NON_BLANK_BEFORE" -le 50 ]
        run_test "Skill() call within first 50 non-blank lines (found at $NON_BLANK_BEFORE)" $?
    fi
fi

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
