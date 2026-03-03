#!/bin/bash
# Test: AC#3 - create-agent.md meets lean orchestration targets
# Story: STORY-461
# Generated: 2026-02-21
# Expected state: FAIL against pre-refactoring file (256 lines, no Lean section)

PASS=0
FAIL=0
TARGET="/mnt/c/Projects/DevForgeAI2/src/claude/commands/create-agent.md"

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

echo "=== AC#3: create-agent.md Lean Orchestration Targets ==="

# --- File exists ---
[[ -f "$TARGET" ]]
run_test "create-agent.md file exists" $?

# --- Line count <=100 ---
LINE_COUNT=$(wc -l < "$TARGET")
echo "  INFO: Line count = $LINE_COUNT (target <=100)"
[[ "$LINE_COUNT" -le 100 ]]
run_test "Line count is <=100 (current: $LINE_COUNT)" $?

# --- Code blocks before Skill() <=4 ---
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

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
[[ $FAIL -eq 0 ]] && exit 0 || exit 1
