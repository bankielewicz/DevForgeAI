#!/bin/bash
# Test: AC#2 - Anthropic Prompt Engineering Patterns Applied to All 17 Agents
# Story: STORY-397
# Generated: 2026-02-13
# TDD Phase: RED (tests should FAIL before implementation)
#
# Validates that all 17 remaining agents contain the 5 Anthropic prompt
# engineering patterns: CoT, structured output, examples, role anchoring,
# and DO/DO NOT constraint lists.

set -uo pipefail

# === Test Configuration ===
PASSED=0
FAILED=0
TOTAL=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
AGENTS_DIR="${PROJECT_ROOT}/src/claude/agents"

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
echo "  AC#2: Anthropic Prompt Engineering Patterns (17 Agents)"
echo "  Story: STORY-397 | Phase: RED"
echo "============================================================"
echo ""

# --- Pattern 1: Chain-of-thought reasoning in Workflow section ---
echo "--- Pattern 1: Chain-of-thought Reasoning ---"
for agent in "${AGENTS[@]}"; do
    FILE="${AGENTS_DIR}/${agent}.md"
    if [ -f "$FILE" ]; then
        # CoT indicators: explicit reasoning instructions within Workflow section
        # Look for phrases like "Reasoning:", "reason about", "think through",
        # "step-by-step", "*Reasoning:*", or numbered steps with reasoning
        WORKFLOW_SECTION=$(awk '/^## Workflow/{found=1; next} found && /^## [A-Z]/{exit} found{print}' "$FILE")
        COT_FOUND=1
        if echo "$WORKFLOW_SECTION" | grep -qiE '(\*?Reasoning:?\*?|reason about|think through|step.by.step|explicit.?reasoning)'; then
            COT_FOUND=0
        fi
        run_test "CoT reasoning in Workflow: ${agent}.md" $COT_FOUND
    else
        run_test "CoT reasoning in Workflow: ${agent}.md (file missing)" 1
    fi
done
echo ""

# --- Pattern 2: Structured output specification in Output Format section ---
echo "--- Pattern 2: Structured Output Specification ---"
for agent in "${AGENTS[@]}"; do
    FILE="${AGENTS_DIR}/${agent}.md"
    if [ -f "$FILE" ]; then
        # Check for Output Format section with structured format definition
        # Look for JSON schema, markdown template, code blocks, or structured report
        OUTPUT_SECTION=$(awk '/^## Output Format/{found=1; next} found && /^## [A-Z]/{exit} found{print}' "$FILE")
        STRUCTURED_FOUND=1
        if echo "$OUTPUT_SECTION" | grep -qE '(```|json|yaml|markdown|template|schema|format|structure)'; then
            STRUCTURED_FOUND=0
        fi
        run_test "Structured output in Output Format: ${agent}.md" $STRUCTURED_FOUND
    else
        run_test "Structured output in Output Format: ${agent}.md (file missing)" 1
    fi
done
echo ""

# --- Pattern 3: At least 1 worked example with Task() invocation ---
echo "--- Pattern 3: Worked Examples with Task() ---"
for agent in "${AGENTS[@]}"; do
    FILE="${AGENTS_DIR}/${agent}.md"
    if [ -f "$FILE" ]; then
        # Check for Examples section containing at least one Task() invocation
        EXAMPLES_SECTION=$(awk '/^## Examples/{found=1; next} found && /^## [A-Z]/{exit} found{print}' "$FILE")
        EXAMPLE_FOUND=1
        if echo "$EXAMPLES_SECTION" | grep -q 'Task('; then
            EXAMPLE_FOUND=0
        fi
        run_test "Worked example with Task() in Examples: ${agent}.md" $EXAMPLE_FOUND
    else
        run_test "Worked example with Task() in Examples: ${agent}.md (file missing)" 1
    fi
done
echo ""

# --- Pattern 4: Role/identity anchoring in Purpose section ---
echo "--- Pattern 4: Role/Identity Anchoring ---"
for agent in "${AGENTS[@]}"; do
    FILE="${AGENTS_DIR}/${agent}.md"
    if [ -f "$FILE" ]; then
        # Check Purpose section for identity statement
        # Look for "You are a", "expert", "specialist", "responsible for"
        PURPOSE_SECTION=$(awk '/^## Purpose/{found=1; next} found && /^## [A-Z]/{exit} found{print}' "$FILE")
        IDENTITY_FOUND=1
        if echo "$PURPOSE_SECTION" | grep -qiE '(You are a|expert|specialist|responsible for|identity|your role)'; then
            IDENTITY_FOUND=0
        fi
        run_test "Role/identity anchoring in Purpose: ${agent}.md" $IDENTITY_FOUND
    else
        run_test "Role/identity anchoring in Purpose: ${agent}.md (file missing)" 1
    fi
done
echo ""

# --- Pattern 5: Explicit DO/DO NOT constraint lists ---
echo "--- Pattern 5: DO/DO NOT Constraint Lists ---"
for agent in "${AGENTS[@]}"; do
    FILE="${AGENTS_DIR}/${agent}.md"
    if [ -f "$FILE" ]; then
        # Check Constraints and Boundaries section for DO/DO NOT lists
        CONSTRAINTS_SECTION=$(awk '/^## Constraints and Boundaries/{found=1; next} found && /^## [A-Z]/{exit} found{print}' "$FILE")
        DO_FOUND=1
        DONOT_FOUND=1
        if echo "$CONSTRAINTS_SECTION" | grep -qE '(\*\*DO:\*\*|\*\*DO\*\*|^DO:)'; then
            DO_FOUND=0
        fi
        if echo "$CONSTRAINTS_SECTION" | grep -qE '(\*\*DO NOT:\*\*|\*\*DO NOT\*\*|^DO NOT:|\*\*DON.T\*\*)'; then
            DONOT_FOUND=0
        fi
        # Both DO and DO NOT must be present
        BOTH_FOUND=$((DO_FOUND + DONOT_FOUND))
        if [ "$BOTH_FOUND" -eq 0 ]; then
            run_test "DO/DO NOT lists in Constraints: ${agent}.md" 0
        else
            run_test "DO/DO NOT lists in Constraints: ${agent}.md" 1
        fi
    else
        run_test "DO/DO NOT lists in Constraints: ${agent}.md (file missing)" 1
    fi
done
echo ""

# --- Pattern 6: All 5 patterns present in single agent (comprehensive check) ---
echo "--- Pattern 6: All 5 Patterns Present (Comprehensive) ---"
for agent in "${AGENTS[@]}"; do
    FILE="${AGENTS_DIR}/${agent}.md"
    if [ -f "$FILE" ]; then
        PATTERN_COUNT=0

        # 1. CoT in Workflow
        WORKFLOW=$(awk '/^## Workflow/{found=1; next} found && /^## [A-Z]/{exit} found{print}' "$FILE")
        if echo "$WORKFLOW" | grep -qiE '(\*?Reasoning:?\*?|reason about|think through|step.by.step)'; then
            ((PATTERN_COUNT++))
        fi

        # 2. Structured Output
        OUTPUT=$(awk '/^## Output Format/{found=1; next} found && /^## [A-Z]/{exit} found{print}' "$FILE")
        if echo "$OUTPUT" | grep -qE '(```|json|yaml|template|schema)'; then
            ((PATTERN_COUNT++))
        fi

        # 3. Task() example
        EXAMPLES=$(awk '/^## Examples/{found=1; next} found && /^## [A-Z]/{exit} found{print}' "$FILE")
        if echo "$EXAMPLES" | grep -q 'Task('; then
            ((PATTERN_COUNT++))
        fi

        # 4. Identity anchoring
        PURPOSE=$(awk '/^## Purpose/{found=1; next} found && /^## [A-Z]/{exit} found{print}' "$FILE")
        if echo "$PURPOSE" | grep -qiE '(You are a|expert|specialist|responsible for)'; then
            ((PATTERN_COUNT++))
        fi

        # 5. DO/DO NOT
        CONSTRAINTS=$(awk '/^## Constraints and Boundaries/{found=1; next} found && /^## [A-Z]/{exit} found{print}' "$FILE")
        if echo "$CONSTRAINTS" | grep -qE '(\*\*DO:\*\*|\*\*DO\*\*)' && echo "$CONSTRAINTS" | grep -qE '(\*\*DO NOT:\*\*|\*\*DO NOT\*\*)'; then
            ((PATTERN_COUNT++))
        fi

        if [ "$PATTERN_COUNT" -eq 5 ]; then
            run_test "All 5 Anthropic patterns (${PATTERN_COUNT}/5): ${agent}.md" 0
        else
            run_test "All 5 Anthropic patterns (${PATTERN_COUNT}/5): ${agent}.md" 1
        fi
    else
        run_test "All 5 Anthropic patterns: ${agent}.md (file missing)" 1
    fi
done
echo ""

# === Summary ===
echo "============================================================"
echo "  AC#2 Results: ${PASSED} passed, ${FAILED} failed (${TOTAL} total)"
echo "============================================================"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
