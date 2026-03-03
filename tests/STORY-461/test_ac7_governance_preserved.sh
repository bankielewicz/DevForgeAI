#!/bin/bash
# Test: AC#7 - Governance sections preserved in command or skill references
# Story: STORY-461
# Generated: 2026-02-21
# Expected state: PASS now (content still in command files), PASS after (moved to references)

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

echo "=== AC#7: Governance Sections Preserved ==="

CREATE_EPIC_CMD="/mnt/c/Projects/DevForgeAI2/src/claude/commands/create-epic.md"
EPIC_SKILL_DIR="/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-story-creation"

RCA_CMD="/mnt/c/Projects/DevForgeAI2/src/claude/commands/rca.md"
RCA_SKILL_DIR="/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-rca"

# --- STORY-301 reference: create-epic command or story-creation skill ---
STORY301_FOUND=0
grep -q "STORY-301" "$CREATE_EPIC_CMD" 2>/dev/null && STORY301_FOUND=1
grep -rq "STORY-301" "$EPIC_SKILL_DIR" 2>/dev/null && STORY301_FOUND=1
[[ "$STORY301_FOUND" -eq 1 ]]
run_test "STORY-301 reference preserved in create-epic command or skill (>=1 match)" $?

# --- STORY-299 reference: create-epic command or story-creation skill ---
STORY299_FOUND=0
grep -q "STORY-299" "$CREATE_EPIC_CMD" 2>/dev/null && STORY299_FOUND=1
grep -rq "STORY-299" "$EPIC_SKILL_DIR" 2>/dev/null && STORY299_FOUND=1
[[ "$STORY299_FOUND" -eq 1 ]]
run_test "STORY-299 reference preserved in create-epic command or skill (>=1 match)" $?

# --- Framework-Aware Analysis: rca command or skill ---
FW_FOUND=0
grep -q "Framework-Aware Analysis" "$RCA_CMD" 2>/dev/null && FW_FOUND=1
grep -rq "Framework-Aware Analysis" "$RCA_SKILL_DIR" 2>/dev/null && FW_FOUND=1
[[ "$FW_FOUND" -eq 1 ]]
run_test "'Framework-Aware Analysis' preserved in rca command or skill references" $?

# --- Evidence-Based: rca command or skill ---
EB_FOUND=0
grep -q "Evidence-Based" "$RCA_CMD" 2>/dev/null && EB_FOUND=1
grep -rq "Evidence-Based" "$RCA_SKILL_DIR" 2>/dev/null && EB_FOUND=1
[[ "$EB_FOUND" -eq 1 ]]
run_test "'Evidence-Based' preserved in rca command or skill references" $?

# --- Integration Pattern: rca command or skill ---
IP_FOUND=0
grep -qi "Integration Pattern" "$RCA_CMD" 2>/dev/null && IP_FOUND=1
grep -rqi "Integration Pattern" "$RCA_SKILL_DIR" 2>/dev/null && IP_FOUND=1
[[ "$IP_FOUND" -eq 1 ]]
run_test "'Integration Pattern' preserved in rca command or skill references" $?

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
[[ $FAIL -eq 0 ]] && exit 0 || exit 1
