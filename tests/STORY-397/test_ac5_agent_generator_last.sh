#!/bin/bash
# Test: AC#5 - agent-generator Updated LAST with Template Enforcement
# Story: STORY-397
# Generated: 2026-02-13
# TDD Phase: RED (tests should FAIL before implementation)
#
# Validates that agent-generator.md is migrated after all 16 other agents,
# conforms to canonical template, includes template enforcement rules,
# and demonstrates self-consistency.

set -uo pipefail

# === Test Configuration ===
PASSED=0
FAILED=0
TOTAL=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
AGENTS_DIR="${PROJECT_ROOT}/src/claude/agents"

# The 16 agents that must be committed BEFORE agent-generator
OTHER_AGENTS=(
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
echo "  AC#5: agent-generator Updated Last"
echo "  Story: STORY-397 | Phase: RED"
echo "============================================================"
echo ""

# --- Test Group 1: agent-generator conforms to canonical template ---
echo "--- Test Group 1: agent-generator Template Conformance ---"
AG_FILE="${AGENTS_DIR}/agent-generator.md"
if [ -f "$AG_FILE" ]; then
    # Version 2.0.0
    if grep -q '^version: ["'"'"']2\.0\.0["'"'"']' "$AG_FILE" 2>/dev/null; then
        run_test "agent-generator version 2.0.0" 0
    else
        run_test "agent-generator version 2.0.0" 1
    fi

    # All 10 required sections
    REQUIRED_SECTIONS=(
        "## Purpose"
        "## When Invoked"
        "## Input/Output Specification"
        "## Constraints and Boundaries"
        "## Workflow"
        "## Success Criteria"
        "## Output Format"
        "## Examples"
    )
    for section in "${REQUIRED_SECTIONS[@]}"; do
        if grep -q "^${section}" "$AG_FILE" 2>/dev/null; then
            run_test "agent-generator has '${section}'" 0
        else
            run_test "agent-generator has '${section}'" 1
        fi
    done

    # YAML frontmatter completeness
    for field in "name:" "description:" "tools:" "model:" "version:"; do
        if grep -q "^${field}" "$AG_FILE" 2>/dev/null; then
            run_test "agent-generator frontmatter '${field}'" 0
        else
            run_test "agent-generator frontmatter '${field}'" 1
        fi
    done
else
    run_test "agent-generator.md exists" 1
fi
echo ""

# --- Test Group 2: agent-generator includes template enforcement rules ---
echo "--- Test Group 2: Template Enforcement in agent-generator ---"
if [ -f "$AG_FILE" ]; then
    # Check for template validation/enforcement language
    if grep -qiE '(template.?enforcement|template.?validation|canonical.?template|10 required sections|template.?compliance)' "$AG_FILE" 2>/dev/null; then
        run_test "Template enforcement language present" 0
    else
        run_test "Template enforcement language present" 1
    fi

    # Check for reference to the 10 required sections as validation rules
    if grep -qiE '(validate|enforce|check|verify).*(section|template|structure)' "$AG_FILE" 2>/dev/null; then
        run_test "Template validation rules documented" 0
    else
        run_test "Template validation rules documented" 1
    fi

    # Check agent-generator mentions version 2.0.0 as the template version
    if grep -qiE '(version.?2\.0\.0|template.?v2|canonical.?v2)' "$AG_FILE" 2>/dev/null; then
        run_test "Template version 2.0.0 referenced in enforcement" 0
    else
        run_test "Template version 2.0.0 referenced in enforcement" 1
    fi
else
    run_test "Template enforcement (file missing)" 1
    run_test "Template validation rules (file missing)" 1
    run_test "Template version reference (file missing)" 1
fi
echo ""

# --- Test Group 3: Self-consistency check ---
echo "--- Test Group 3: Self-Consistency (agent-generator follows its own template) ---"
if [ -f "$AG_FILE" ]; then
    # Verify agent-generator has all Anthropic patterns it should enforce
    # CoT in Workflow
    WORKFLOW=$(awk '/^## Workflow/{found=1; next} found && /^## [A-Z]/{exit} found{print}' "$AG_FILE")
    COT=1
    if echo "$WORKFLOW" | grep -qiE '(\*?Reasoning:?\*?|step.by.step|reason)'; then
        COT=0
    fi
    run_test "Self-consistency: CoT in own Workflow" $COT

    # DO/DO NOT in Constraints
    CONSTRAINTS=$(awk '/^## Constraints and Boundaries/{found=1; next} found && /^## [A-Z]/{exit} found{print}' "$AG_FILE")
    DO_DONOT=1
    if echo "$CONSTRAINTS" | grep -qE '(\*\*DO:\*\*|\*\*DO\*\*)' && echo "$CONSTRAINTS" | grep -qE '(\*\*DO NOT:\*\*|\*\*DO NOT\*\*)'; then
        DO_DONOT=0
    fi
    run_test "Self-consistency: DO/DO NOT in own Constraints" $DO_DONOT

    # Task() example in Examples
    EXAMPLES=$(awk '/^## Examples/{found=1; next} found && /^## [A-Z]/{exit} found{print}' "$AG_FILE")
    TASK_EX=1
    if echo "$EXAMPLES" | grep -q 'Task('; then
        TASK_EX=0
    fi
    run_test "Self-consistency: Task() in own Examples" $TASK_EX
else
    run_test "Self-consistency (file missing)" 1
fi
echo ""

# --- Test Group 4: Git commit ordering (agent-generator is LAST) ---
echo "--- Test Group 4: Commit Ordering Validation ---"
# Check git log for STORY-397 commits to verify agent-generator was last
# This test validates the commit order constraint from BR-001
cd "$PROJECT_ROOT"
STORY_COMMITS=$(git log --oneline --all --diff-filter=M -- "src/claude/agents/*.md" 2>/dev/null | head -20)

if [ -z "$STORY_COMMITS" ]; then
    # No STORY-397 migration commits yet - expected in RED phase
    run_test "Git commits exist for agent migrations (none found yet)" 1
else
    # Find the most recent commit touching agent-generator.md
    AG_LAST_COMMIT=$(git log --format="%H" -1 -- "src/claude/agents/agent-generator.md" 2>/dev/null)

    # Verify all 16 other agents were committed before agent-generator
    ALL_BEFORE=0
    for agent in "${OTHER_AGENTS[@]}"; do
        AGENT_LAST=$(git log --format="%H" -1 -- "src/claude/agents/${agent}.md" 2>/dev/null)
        if [ -n "$AGENT_LAST" ] && [ -n "$AG_LAST_COMMIT" ]; then
            # Check if agent commit is ancestor of (before) agent-generator commit
            if ! git merge-base --is-ancestor "$AGENT_LAST" "$AG_LAST_COMMIT" 2>/dev/null; then
                # Agent was committed AFTER agent-generator - violation
                if [ "$AGENT_LAST" != "$AG_LAST_COMMIT" ]; then
                    ALL_BEFORE=1
                fi
            fi
        fi
    done
    run_test "agent-generator committed after all 16 other agents" $ALL_BEFORE
fi
echo ""

# === Summary ===
echo "============================================================"
echo "  AC#5 Results: ${PASSED} passed, ${FAILED} failed (${TOTAL} total)"
echo "============================================================"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
