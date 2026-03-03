#!/bin/bash
# Test: AC#6 - Zero Breaking Changes Validated Through Regression Testing
# Story: STORY-397
# Generated: 2026-02-13
# TDD Phase: RED (tests should FAIL before implementation)
#
# Validates zero breaking changes across all 17 agents, 17 skills, and
# 39 commands. Checks structural equivalence, interface stability, and
# cross-reference validity.

set -uo pipefail

# === Test Configuration ===
PASSED=0
FAILED=0
TOTAL=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
AGENTS_DIR="${PROJECT_ROOT}/src/claude/agents"
SKILLS_DIR="${PROJECT_ROOT}/src/claude/skills"
COMMANDS_DIR="${PROJECT_ROOT}/src/claude/commands"

# The 17 agents
AGENTS=(
    "architect-reviewer"
    "documentation-writer"
    "framework-analyst"
    "git-validator"
    "git-worktree-manager"
    "ideation-result-interpreter"
    "internet-sleuth"
    "observation-extractor"
    "qa-result-interpreter"
    "dev-result-interpreter"
    "session-miner"
    "sprint-planner"
    "stakeholder-analyst"
    "story-requirements-analyst"
    "technical-debt-analyzer"
    "ui-spec-formatter"
    "agent-generator"
)

# Skills
SKILLS=(
    "devforgeai-ideation"
    "devforgeai-brainstorming"
    "devforgeai-architecture"
    "devforgeai-orchestration"
    "devforgeai-story-creation"
    "devforgeai-ui-generator"
    "devforgeai-development"
    "devforgeai-qa"
    "devforgeai-release"
    "devforgeai-documentation"
    "devforgeai-feedback"
    "devforgeai-rca"
    "devforgeai-subagent-creation"
    "devforgeai-mcp-cli-converter"
    "claude-code-terminal-expert"
    "devforgeai-github-actions"
    "skill-creator"
)

# === Helper Functions ===
run_test() {
    local name="$1"
    local result="$2"
    ((TOTAL++))
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        ((PASSED++))
    else
        echo "  FAIL: $name"
        ((FAILED++))
    fi
}

# === Test Suite ===
echo "============================================================"
echo "  AC#6: Regression Validation (Zero Breaking Changes)"
echo "  Story: STORY-397 | Phase: RED"
echo "============================================================"
echo ""

# --- Test Category 1: Agent Regression Tests (17 tests) ---
echo "--- Category 1: Agent Regression (17 agents) ---"
for agent in "${AGENTS[@]}"; do
    FILE="${AGENTS_DIR}/${agent}.md"
    if [ -f "$FILE" ]; then
        # Regression check: YAML frontmatter name: field matches filename
        EXPECTED_NAME="$agent"
        ACTUAL_NAME=$(grep '^name:' "$FILE" | head -1 | sed 's/^name: *//; s/^"//; s/"$//')
        if [ "$ACTUAL_NAME" = "$EXPECTED_NAME" ]; then
            run_test "Agent name preserved: ${agent} (actual: ${ACTUAL_NAME})" 0
        else
            run_test "Agent name preserved: ${agent} (actual: ${ACTUAL_NAME})" 1
        fi

        # Regression check: tools: field still present
        if grep -q '^tools:' "$FILE" 2>/dev/null; then
            run_test "Agent tools: field preserved: ${agent}" 0
        else
            run_test "Agent tools: field preserved: ${agent}" 1
        fi

        # Regression check: model: field still present
        if grep -q '^model:' "$FILE" 2>/dev/null; then
            run_test "Agent model: field preserved: ${agent}" 0
        else
            run_test "Agent model: field preserved: ${agent}" 1
        fi

        # Regression check: H1 title still present
        if grep -q '^# ' "$FILE" 2>/dev/null; then
            run_test "Agent H1 title preserved: ${agent}" 0
        else
            run_test "Agent H1 title preserved: ${agent}" 1
        fi
    else
        run_test "Agent file exists: ${agent}" 1
    fi
done
echo ""

# --- Test Category 2: Skill Regression Tests (17 tests) ---
echo "--- Category 2: Skill Regression (17 skills) ---"
for skill in "${SKILLS[@]}"; do
    FILE="${SKILLS_DIR}/${skill}/SKILL.md"
    if [ -f "$FILE" ]; then
        # Regression check: YAML frontmatter preserved
        if head -1 "$FILE" | grep -q '^---$'; then
            run_test "Skill frontmatter preserved: ${skill}" 0
        else
            run_test "Skill frontmatter preserved: ${skill}" 1
        fi

        # Regression check: name: field matches expected
        if grep -q '^name:' "$FILE" 2>/dev/null; then
            run_test "Skill name: field preserved: ${skill}" 0
        else
            run_test "Skill name: field preserved: ${skill}" 1
        fi

        # Regression check: Purpose section still present
        if grep -q '^## Purpose' "$FILE" 2>/dev/null; then
            run_test "Skill Purpose section preserved: ${skill}" 0
        else
            run_test "Skill Purpose section preserved: ${skill}" 1
        fi

        # Regression check: File is non-empty (>10 lines)
        LINE_COUNT=$(wc -l < "$FILE")
        if [ "$LINE_COUNT" -gt 10 ] 2>/dev/null; then
            run_test "Skill has content (${LINE_COUNT} lines): ${skill}" 0
        else
            run_test "Skill has content (${LINE_COUNT} lines): ${skill}" 1
        fi
    else
        run_test "Skill file exists: ${skill}" 1
    fi
done
echo ""

# --- Test Category 3: Command Regression Tests (by category) ---
echo "--- Category 3: Command Regression (10 category tests) ---"

# Category 3.1: Planning commands
PLANNING_CMDS=("brainstorm" "ideate" "create-context" "create-epic" "create-sprint")
for cmd in "${PLANNING_CMDS[@]}"; do
    FILE="${COMMANDS_DIR}/${cmd}.md"
    if [ -f "$FILE" ]; then
        if grep -q '^description:' "$FILE" 2>/dev/null; then
            run_test "Planning cmd preserved: ${cmd}" 0
        else
            run_test "Planning cmd preserved: ${cmd}" 1
        fi
    else
        run_test "Planning cmd exists: ${cmd}" 1
    fi
done

# Category 3.2: Development commands
DEV_CMDS=("create-story" "create-ui" "dev")
for cmd in "${DEV_CMDS[@]}"; do
    FILE="${COMMANDS_DIR}/${cmd}.md"
    if [ -f "$FILE" ]; then
        if grep -q '^description:' "$FILE" 2>/dev/null; then
            run_test "Dev cmd preserved: ${cmd}" 0
        else
            run_test "Dev cmd preserved: ${cmd}" 1
        fi
    else
        run_test "Dev cmd exists: ${cmd}" 1
    fi
done

# Category 3.3: Validation commands
VAL_CMDS=("qa" "release" "orchestrate")
for cmd in "${VAL_CMDS[@]}"; do
    FILE="${COMMANDS_DIR}/${cmd}.md"
    if [ -f "$FILE" ]; then
        if grep -q '^description:' "$FILE" 2>/dev/null; then
            run_test "Validation cmd preserved: ${cmd}" 0
        else
            run_test "Validation cmd preserved: ${cmd}" 1
        fi
    else
        run_test "Validation cmd exists: ${cmd}" 1
    fi
done

# Category 3.4: Maintenance commands
MAINT_CMDS=("audit-deferrals" "rca" "audit-hooks" "audit-budget")
for cmd in "${MAINT_CMDS[@]}"; do
    FILE="${COMMANDS_DIR}/${cmd}.md"
    if [ -f "$FILE" ]; then
        if grep -q '^description:' "$FILE" 2>/dev/null; then
            run_test "Maintenance cmd preserved: ${cmd}" 0
        else
            run_test "Maintenance cmd preserved: ${cmd}" 1
        fi
    else
        run_test "Maintenance cmd exists: ${cmd}" 1
    fi
done

# Category 3.5: Feedback commands
FB_CMDS=("feedback-search" "feedback-config" "export-feedback" "import-feedback" "feedback-reindex")
for cmd in "${FB_CMDS[@]}"; do
    FILE="${COMMANDS_DIR}/${cmd}.md"
    if [ -f "$FILE" ]; then
        if grep -q '^description:' "$FILE" 2>/dev/null; then
            run_test "Feedback cmd preserved: ${cmd}" 0
        else
            run_test "Feedback cmd preserved: ${cmd}" 1
        fi
    else
        run_test "Feedback cmd exists: ${cmd}" 1
    fi
done
echo ""

# --- Test Category 4: Cross-Reference Validation ---
echo "--- Category 4: Cross-Reference Validation ---"

# Check that agent references in skills still point to valid files
for skill in "${SKILLS[@]}"; do
    FILE="${SKILLS_DIR}/${skill}/SKILL.md"
    if [ -f "$FILE" ]; then
        # Find references to agent files (subagent_type="...")
        AGENT_REFS=$(grep -oP 'subagent_type="([^"]+)"' "$FILE" 2>/dev/null | sed 's/subagent_type="//; s/"//' || true)
        for ref in $AGENT_REFS; do
            AGENT_FILE="${AGENTS_DIR}/${ref}.md"
            if [ -f "$AGENT_FILE" ]; then
                run_test "Cross-ref valid: ${skill} -> ${ref}" 0
            else
                run_test "Cross-ref valid: ${skill} -> ${ref} (BROKEN)" 1
            fi
        done
    fi
done
echo ""

# --- Test Category 5: Minimum test count validation ---
echo "--- Category 5: Test Suite Size ---"
REGRESSION_MIN=44
echo "  Required minimum tests: ${REGRESSION_MIN}"
echo "  Actual tests executed: ${TOTAL}"
if [ "$TOTAL" -ge "$REGRESSION_MIN" ] 2>/dev/null; then
    run_test "Regression suite has 44+ tests (actual: ${TOTAL})" 0
else
    run_test "Regression suite has 44+ tests (actual: ${TOTAL})" 1
fi
echo ""

# === Summary ===
echo "============================================================"
echo "  AC#6 Results: ${PASSED} passed, ${FAILED} failed (${TOTAL} total)"
echo "============================================================"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
