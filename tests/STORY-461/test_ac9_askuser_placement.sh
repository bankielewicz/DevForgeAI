#!/bin/bash
# Test: AC#9 - No new AskUserQuestion added to skill SKILL.md files by this story
# Story: STORY-461
# Generated: 2026-02-21
# Baseline counts captured pre-refactoring:
#   devforgeai-story-creation/SKILL.md: 13
#   devforgeai-rca/SKILL.md: 5
#   devforgeai-subagent-creation/SKILL.md: 0
#   devforgeai-documentation/SKILL.md: 4
#   devforgeai-insights/SKILL.md: 2
# Expected state: PASS if counts do not increase beyond baseline

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

check_skill_askuser() {
    local skill_file="$1"
    local baseline="$2"
    local label="$3"

    if [[ ! -f "$skill_file" ]]; then
        echo "  WARN: $skill_file not found - skipping"
        return
    fi

    local current
    current=$(grep -c "AskUserQuestion" "$skill_file" 2>/dev/null; true)
    current=$(echo "$current" | tail -1 | tr -d '[:space:]')
    current="${current:-0}"
    echo "  INFO: $label AskUserQuestion count = $current (baseline <=  $baseline)"
    [[ "$current" -le "$baseline" ]]
    run_test "$label: AskUserQuestion count ($current) does not exceed baseline ($baseline)" $?
}

echo "=== AC#9: No New AskUserQuestion Added to SKILL.md Files ==="

SKILLS_BASE="/mnt/c/Projects/DevForgeAI2/src/claude/skills"

check_skill_askuser \
    "$SKILLS_BASE/devforgeai-story-creation/SKILL.md" \
    13 \
    "devforgeai-story-creation"

check_skill_askuser \
    "$SKILLS_BASE/devforgeai-rca/SKILL.md" \
    5 \
    "devforgeai-rca"

check_skill_askuser \
    "$SKILLS_BASE/devforgeai-subagent-creation/SKILL.md" \
    0 \
    "devforgeai-subagent-creation"

check_skill_askuser \
    "$SKILLS_BASE/devforgeai-documentation/SKILL.md" \
    4 \
    "devforgeai-documentation"

check_skill_askuser \
    "$SKILLS_BASE/devforgeai-insights/SKILL.md" \
    2 \
    "devforgeai-insights"

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
[[ $FAIL -eq 0 ]] && exit 0 || exit 1
