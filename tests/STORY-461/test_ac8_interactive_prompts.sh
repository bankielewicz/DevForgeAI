#!/bin/bash
# Test: AC#8 - AskUserQuestion prompts preserved with exact counts in refactored commands
# Story: STORY-461
# Generated: 2026-02-21
# Baseline counts (pre-refactor): create-epic=3, create-agent=9, rca=6, document=1, insights=1
# Expected state: FAIL after refactor if counts change; tests enforce exact baseline counts

PASS=0
FAIL=0

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

echo "=== AC#8: AskUserQuestion Prompts Preserved ==="

CREATE_EPIC_CMD="/mnt/c/Projects/DevForgeAI2/src/claude/commands/create-epic.md"
CREATE_AGENT_CMD="/mnt/c/Projects/DevForgeAI2/src/claude/commands/create-agent.md"
RCA_CMD="/mnt/c/Projects/DevForgeAI2/src/claude/commands/rca.md"
DOC_CMD="/mnt/c/Projects/DevForgeAI2/src/claude/commands/document.md"
INSIGHTS_CMD="/mnt/c/Projects/DevForgeAI2/src/claude/commands/insights.md"

# --- create-epic: exactly 3 AskUserQuestion references ---
EPIC_COUNT=$(grep -c "AskUserQuestion" "$CREATE_EPIC_CMD" 2>/dev/null || echo 0)
echo "  INFO: create-epic.md AskUserQuestion count = $EPIC_COUNT (expected 3)"
[[ "$EPIC_COUNT" -eq 3 ]]
run_test "create-epic.md has exactly 3 AskUserQuestion references (found: $EPIC_COUNT)" $?

# --- create-agent: exactly 9 AskUserQuestion references ---
AGENT_COUNT=$(grep -c "AskUserQuestion" "$CREATE_AGENT_CMD" 2>/dev/null || echo 0)
echo "  INFO: create-agent.md AskUserQuestion count = $AGENT_COUNT (expected 9)"
[[ "$AGENT_COUNT" -eq 9 ]]
run_test "create-agent.md has exactly 9 AskUserQuestion references (found: $AGENT_COUNT)" $?

# --- rca: exactly 6 AskUserQuestion references ---
RCA_COUNT=$(grep -c "AskUserQuestion" "$RCA_CMD" 2>/dev/null || echo 0)
echo "  INFO: rca.md AskUserQuestion count = $RCA_COUNT (expected 6)"
[[ "$RCA_COUNT" -eq 6 ]]
run_test "rca.md has exactly 6 AskUserQuestion references (found: $RCA_COUNT)" $?

# --- document: exactly 1 AskUserQuestion reference ---
DOC_COUNT=$(grep -c "AskUserQuestion" "$DOC_CMD" 2>/dev/null || echo 0)
echo "  INFO: document.md AskUserQuestion count = $DOC_COUNT (expected 1)"
[[ "$DOC_COUNT" -eq 1 ]]
run_test "document.md has exactly 1 AskUserQuestion reference (found: $DOC_COUNT)" $?

# --- insights: exactly 1 AskUserQuestion reference ---
INSIGHTS_COUNT=$(grep -c "AskUserQuestion" "$INSIGHTS_CMD" 2>/dev/null || echo 0)
echo "  INFO: insights.md AskUserQuestion count = $INSIGHTS_COUNT (expected 1)"
[[ "$INSIGHTS_COUNT" -eq 1 ]]
run_test "insights.md has exactly 1 AskUserQuestion reference (found: $INSIGHTS_COUNT)" $?

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
[[ $FAIL -eq 0 ]] && exit 0 || exit 1
