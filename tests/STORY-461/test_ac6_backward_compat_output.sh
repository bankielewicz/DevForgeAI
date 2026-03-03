#!/bin/bash
# Test: AC#6 - Backward compatibility - content preserved in commands OR reference files
# Story: STORY-461
# Generated: 2026-02-21
# Strategy: Search command file AND skill references directory for each term
# Expected state: PASS now (content in command), still PASS after refactor (content in references)

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

# Helper: search in command file OR skill references directory
search_command_or_refs() {
    local pattern="$1"
    local command_file="$2"
    local refs_dir="$3"

    if grep -q "$pattern" "$command_file" 2>/dev/null; then
        return 0
    fi
    if [[ -d "$refs_dir" ]] && grep -rq "$pattern" "$refs_dir" 2>/dev/null; then
        return 0
    fi
    return 1
}

echo "=== AC#6: Backward Compatibility - Content Preserved ==="

# --- create-epic: Schema Validation ---
CREATE_EPIC_CMD="/mnt/c/Projects/DevForgeAI2/src/claude/commands/create-epic.md"
CREATE_EPIC_REFS="/mnt/c/Projects/DevForgeAI2/src/claude/skills/designing-systems/references"
EPIC_SKILL="/mnt/c/Projects/DevForgeAI2/src/claude/skills/designing-systems/SKILL.md"

search_command_or_refs "Schema Validation" "$CREATE_EPIC_CMD" "$CREATE_EPIC_REFS"
[[ $? -eq 0 ]] || grep -q "Schema Validation" "$EPIC_SKILL" 2>/dev/null
run_test "create-epic: 'Schema Validation' preserved in command or references" $?

search_command_or_refs "Context Preservation" "$CREATE_EPIC_CMD" "$CREATE_EPIC_REFS"
[[ $? -eq 0 ]] || grep -q "Context Preservation" "$EPIC_SKILL" 2>/dev/null
run_test "create-epic: 'Context Preservation' preserved in command or references" $?

search_command_or_refs "Invalid Epic Name" "$CREATE_EPIC_CMD" "$CREATE_EPIC_REFS"
run_test "create-epic: 'Invalid Epic Name' preserved in command or references" $?

search_command_or_refs "Skill Invocation Failed" "$CREATE_EPIC_CMD" "$CREATE_EPIC_REFS"
run_test "create-epic: 'Skill Invocation Failed' preserved in command or references" $?

search_command_or_refs "Epic Validation Failed" "$CREATE_EPIC_CMD" "$CREATE_EPIC_REFS"
run_test "create-epic: 'Epic Validation Failed' preserved in command or references" $?

# --- rca: Framework-Aware Analysis ---
RCA_CMD="/mnt/c/Projects/DevForgeAI2/src/claude/commands/rca.md"
RCA_REFS="/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-rca/references"
RCA_SKILL="/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-rca/SKILL.md"

search_command_or_refs "Framework-Aware Analysis" "$RCA_CMD" "$RCA_REFS"
[[ $? -eq 0 ]] || grep -q "Framework-Aware Analysis" "$RCA_SKILL" 2>/dev/null
run_test "rca: 'Framework-Aware Analysis' preserved in command or references" $?

search_command_or_refs "Evidence-Based Recommendations" "$RCA_CMD" "$RCA_REFS"
[[ $? -eq 0 ]] || grep -q "Evidence-Based Recommendations" "$RCA_SKILL" 2>/dev/null
run_test "rca: 'Evidence-Based Recommendations' preserved in command or references" $?

search_command_or_refs "Example 1" "$RCA_CMD" "$RCA_REFS"
[[ $? -eq 0 ]] || grep -q "Example 1" "$RCA_SKILL" 2>/dev/null
run_test "rca: 'Example 1' preserved in command or references" $?

search_command_or_refs "Example 2" "$RCA_CMD" "$RCA_REFS"
[[ $? -eq 0 ]] || grep -q "Example 2" "$RCA_SKILL" 2>/dev/null
run_test "rca: 'Example 2' preserved in command or references" $?

search_command_or_refs "Missing Argument" "$RCA_CMD" "$RCA_REFS"
[[ $? -eq 0 ]] || grep -q "Missing Argument" "$RCA_SKILL" 2>/dev/null
run_test "rca: 'Missing Argument' preserved in command or references" $?

search_command_or_refs "Invalid Severity" "$RCA_CMD" "$RCA_REFS"
[[ $? -eq 0 ]] || grep -q "Invalid Severity" "$RCA_SKILL" 2>/dev/null
run_test "rca: 'Invalid Severity' preserved in command or references" $?

search_command_or_refs "Skill Execution Failure" "$RCA_CMD" "$RCA_REFS"
[[ $? -eq 0 ]] || grep -q "Skill Execution Failure" "$RCA_SKILL" 2>/dev/null
run_test "rca: 'Skill Execution Failure' preserved in command or references" $?

search_command_or_refs "RCA Document Already Exists" "$RCA_CMD" "$RCA_REFS"
[[ $? -eq 0 ]] || grep -q "RCA Document Already Exists" "$RCA_SKILL" 2>/dev/null
run_test "rca: 'RCA Document Already Exists' preserved in command or references" $?

# --- create-agent: Error scenarios ---
CREATE_AGENT_CMD="/mnt/c/Projects/DevForgeAI2/src/claude/commands/create-agent.md"
CREATE_AGENT_REFS="/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-subagent-creation/references"
CREATE_AGENT_SKILL="/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-subagent-creation/SKILL.md"

search_command_or_refs "Invalid Name" "$CREATE_AGENT_CMD" "$CREATE_AGENT_REFS"
[[ $? -eq 0 ]] || grep -q "Invalid Name" "$CREATE_AGENT_SKILL" 2>/dev/null
run_test "create-agent: 'Invalid Name' preserved in command or references" $?

search_command_or_refs "Template Not Found" "$CREATE_AGENT_CMD" "$CREATE_AGENT_REFS"
[[ $? -eq 0 ]] || grep -q "Template Not Found" "$CREATE_AGENT_SKILL" 2>/dev/null
run_test "create-agent: 'Template Not Found' preserved in command or references" $?

search_command_or_refs "Invalid Domain" "$CREATE_AGENT_CMD" "$CREATE_AGENT_REFS"
[[ $? -eq 0 ]] || grep -q "Invalid Domain" "$CREATE_AGENT_SKILL" 2>/dev/null
run_test "create-agent: 'Invalid Domain' preserved in command or references" $?

search_command_or_refs "Spec File Missing" "$CREATE_AGENT_CMD" "$CREATE_AGENT_REFS"
[[ $? -eq 0 ]] || grep -q "Spec File Missing" "$CREATE_AGENT_SKILL" 2>/dev/null
run_test "create-agent: 'Spec File Missing' preserved in command or references" $?

search_command_or_refs "Generation Failed" "$CREATE_AGENT_CMD" "$CREATE_AGENT_REFS"
[[ $? -eq 0 ]] || grep -q "Generation Failed" "$CREATE_AGENT_SKILL" 2>/dev/null
run_test "create-agent: 'Generation Failed' preserved in command or references" $?

# --- document: template content preserved ---
DOC_CMD="/mnt/c/Projects/DevForgeAI2/src/claude/commands/document.md"
DOC_REFS="/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-documentation/references"
DOC_SKILL="/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-documentation/SKILL.md"

search_command_or_refs "template" "$DOC_CMD" "$DOC_REFS"
[[ $? -eq 0 ]] || grep -qi "template" "$DOC_SKILL" 2>/dev/null
run_test "document: 'template' content preserved in command or references" $?

# --- insights: help section content preserved ---
INSIGHTS_CMD="/mnt/c/Projects/DevForgeAI2/src/claude/commands/insights.md"
INSIGHTS_REFS="/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-insights/references"
INSIGHTS_SKILL="/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-insights/SKILL.md"

search_command_or_refs "help" "$INSIGHTS_CMD" "$INSIGHTS_REFS"
[[ $? -eq 0 ]] || grep -qi "help" "$INSIGHTS_SKILL" 2>/dev/null
run_test "insights: help section content preserved in command or references" $?

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
[[ $FAIL -eq 0 ]] && exit 0 || exit 1
