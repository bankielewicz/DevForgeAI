#!/bin/bash
# Test: AC#1 - create-epic.md meets lean orchestration targets
# Story: STORY-461
# Generated: 2026-02-21
# Expected state: FAIL against pre-refactoring file (444 lines, no Lean section)

PASS=0
FAIL=0
TARGET="/mnt/c/Projects/DevForgeAI2/src/claude/commands/create-epic.md"

run_test() {
    local name="$1"
    local result="$2"
    if [[ "$result" -eq 0 ]]; then
        echo "  PASS: $name"
        ((PASS++))
    else
        echo "  FAIL: $name"
        ((FAIL++))
    fi
}

echo "=== AC#1: create-epic.md Lean Orchestration Targets ==="

# --- File exists ---
[[ -f "$TARGET" ]]
run_test "create-epic.md file exists" $?

# --- Line count <=150 ---
LINE_COUNT=$(wc -l < "$TARGET")
echo "  INFO: Line count = $LINE_COUNT (target <=150)"
[[ "$LINE_COUNT" -le 150 ]]
run_test "Line count is <=150 (current: $LINE_COUNT)" $?

# --- Character count <=12000 ---
CHAR_COUNT=$(wc -c < "$TARGET")
echo "  INFO: Character count = $CHAR_COUNT (target <=12000)"
[[ "$CHAR_COUNT" -le 12000 ]]
run_test "Character count is <=12000 (current: $CHAR_COUNT)" $?

# --- Code blocks before Skill() <=4 ---
# Extract content before first Skill() call, count ``` occurrences, divide by 2
SKILL_LINE=$(grep -n "Skill(" "$TARGET" | head -1 | cut -d: -f1)
if [[ -z "$SKILL_LINE" ]]; then
    SKILL_LINE=99999
fi
BACKTICK_COUNT=$(head -n "$SKILL_LINE" "$TARGET" | grep -c '^```')
CODE_BLOCK_COUNT=$(( BACKTICK_COUNT / 2 ))
echo "  INFO: Code blocks before Skill() = $CODE_BLOCK_COUNT (target <=4)"
[[ "$CODE_BLOCK_COUNT" -le 4 ]]
run_test "Code blocks before Skill() are <=4 (current: $CODE_BLOCK_COUNT)" $?

# --- Contains Lean Orchestration Enforcement section ---
grep -q "Lean Orchestration Enforcement" "$TARGET"
run_test "Contains 'Lean Orchestration Enforcement' section" $?

# --- Zero forbidden patterns: Bash(command= ---
BASH_CMD_COUNT=$(grep -c "Bash(command=" "$TARGET" 2>/dev/null; true)
BASH_CMD_COUNT=$(echo "$BASH_CMD_COUNT" | tail -1 | tr -d '[:space:]')
echo "  INFO: Bash(command= occurrences = $BASH_CMD_COUNT (target 0)"
[[ "${BASH_CMD_COUNT:-0}" -eq 0 ]]
run_test "Zero 'Bash(command=' patterns (current: $BASH_CMD_COUNT)" $?

# --- Zero forbidden patterns: Task( ---
TASK_COUNT=$(grep -c "Task(" "$TARGET" 2>/dev/null; true)
TASK_COUNT=$(echo "$TASK_COUNT" | tail -1 | tr -d '[:space:]')
echo "  INFO: Task( occurrences = $TASK_COUNT (target 0)"
[[ "${TASK_COUNT:-0}" -eq 0 ]]
run_test "Zero 'Task(' patterns (current: $TASK_COUNT)" $?

# --- Zero forbidden patterns: FOR...in loops ---
FOR_LOOP_COUNT=$(grep -cE "^\s*FOR\s+\w+\s+in\s+" "$TARGET" 2>/dev/null; true)
FOR_LOOP_COUNT=$(echo "$FOR_LOOP_COUNT" | tail -1 | tr -d '[:space:]')
echo "  INFO: FOR...in loop occurrences = $FOR_LOOP_COUNT (target 0)"
[[ "${FOR_LOOP_COUNT:-0}" -eq 0 ]]
run_test "Zero FOR...in loop patterns (current: $FOR_LOOP_COUNT)" $?

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
[[ $FAIL -eq 0 ]] && exit 0 || exit 1
