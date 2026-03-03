#!/bin/bash
# AC#2 Verification Script - STORY-454
# Command code blocks consolidated from 15 to 10 or fewer
# Run from project root: bash src/tests/results/STORY-454/test-ac2-code-block-consolidation.sh

CMD_FILE="src/claude/commands/ideate.md"
PASSED=0
FAILED=0

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        PASSED=$((PASSED + 1))
    else
        echo "  FAIL: $name"
        FAILED=$((FAILED + 1))
    fi
}

echo "=== AC#2: Command Code Blocks Consolidated from 15 to 10 or Fewer ==="
echo "Target: $CMD_FILE"
echo ""

# Find the line number of Skill(command="discovering-requirements")
skill_line=$(grep -n 'Skill(command="discovering-requirements")' "$CMD_FILE" | head -1 | cut -d: -f1)

if [ -z "$skill_line" ]; then
    echo "  FAIL: Could not find Skill() invocation line"
    exit 1
fi

echo "Skill() invocation at line: $skill_line"

# Count code block fence lines (```) before Skill() line
fence_count=$(head -n "$skill_line" "$CMD_FILE" | grep -c '^```')
block_count=$((fence_count / 2))

# Test 1: Total pre-Skill() code blocks <= 10
[ "$block_count" -le 10 ]
run_test "Total pre-Skill() code blocks <= 10 (actual: $block_count)" $?

# Test 2: AskUserQuestion is preserved in Phase 0
grep -q 'AskUserQuestion' "$CMD_FILE"
run_test "AskUserQuestion call preserved in command" $?

# Test 3: AskUserQuestion has 3 brainstorm options preserved
grep -A 20 'AskUserQuestion' "$CMD_FILE" | grep -q 'Yes - use most recent'
run_test "AskUserQuestion brainstorm option 'Yes - use most recent' preserved" $?

grep -A 20 'AskUserQuestion' "$CMD_FILE" | grep -q 'Yes - let me choose'
run_test "AskUserQuestion brainstorm option 'Yes - let me choose' preserved" $?

grep -A 20 'AskUserQuestion' "$CMD_FILE" | grep -q 'No - start fresh'
run_test "AskUserQuestion brainstorm option 'No - start fresh' preserved" $?

# Test 4: Phase 2.0 Glob detection still present
grep -q 'Glob(pattern="devforgeai/specs/context/\*.md")' "$CMD_FILE"
run_test "Phase 2.0 Glob context file detection preserved" $?

# Test 5: Phase 2.1 ideation-context XML markers still present
grep -q '<ideation-context>' "$CMD_FILE"
run_test "Phase 2.1 ideation-context XML markers preserved" $?

# Test 6: ideate.md line count <= 500
line_count=$(wc -l < "$CMD_FILE")
[ "$line_count" -le 500 ]
run_test "ideate.md line count <= 500 (actual: $line_count)" $?

echo ""
echo "=== Results: $PASSED passed, $FAILED failed ==="

if [ "$FAILED" -gt 0 ]; then
    exit 1
else
    exit 0
fi
