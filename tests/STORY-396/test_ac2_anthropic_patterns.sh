#!/bin/bash
# Test: AC#2 - Anthropic Prompt Engineering Patterns Applied to All 9 Agents
# Story: STORY-396
# Generated: 2026-02-13
# TDD Phase: RED (tests should FAIL before migration)

# === Test Configuration ===
PASSED=0
FAILED=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"

AGENTS=(
    "backend-architect"
    "frontend-developer"
    "code-reviewer"
    "refactoring-specialist"
    "integration-tester"
    "api-designer"
    "deployment-engineer"
    "security-auditor"
    "code-analyzer"
)

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

echo "============================================"
echo "AC#2: Anthropic Prompt Engineering Patterns"
echo "Story: STORY-396"
echo "============================================"
echo ""

# --- Pattern 1: Chain-of-thought reasoning in Workflow section ---
echo "--- Pattern 1: Chain-of-thought reasoning ---"
for agent in "${AGENTS[@]}"; do
    AGENT_FILE="$PROJECT_ROOT/src/claude/agents/${agent}.md"
    if [ -f "$AGENT_FILE" ]; then
        if grep -qi "reasoning\|step-by-step\|chain.of.thought\|think through\|explicit reasoning" "$AGENT_FILE" 2>/dev/null; then
            run_test "${agent} has chain-of-thought reasoning" 0
        else
            run_test "${agent} has chain-of-thought reasoning" 1
        fi
    else
        run_test "${agent} has chain-of-thought reasoning (file missing)" 1
    fi
done
echo ""

# --- Pattern 2: Structured output specification in Output Format ---
echo "--- Pattern 2: Structured output specification ---"
for agent in "${AGENTS[@]}"; do
    AGENT_FILE="$PROJECT_ROOT/src/claude/agents/${agent}.md"
    if [ -f "$AGENT_FILE" ]; then
        if grep -q "^## Output Format" "$AGENT_FILE" 2>/dev/null; then
            run_test "${agent} has Output Format section" 0
        else
            run_test "${agent} has Output Format section" 1
        fi
    else
        run_test "${agent} has Output Format section (file missing)" 1
    fi
done
echo ""

# --- Pattern 3: Worked examples with Task() invocation ---
echo "--- Pattern 3: Worked examples with Task() ---"
for agent in "${AGENTS[@]}"; do
    AGENT_FILE="$PROJECT_ROOT/src/claude/agents/${agent}.md"
    if [ -f "$AGENT_FILE" ]; then
        if grep -q "Task(" "$AGENT_FILE" 2>/dev/null; then
            run_test "${agent} has worked example with Task()" 0
        else
            run_test "${agent} has worked example with Task()" 1
        fi
    else
        run_test "${agent} has worked example with Task() (file missing)" 1
    fi
done
echo ""

# --- Pattern 4: Role/identity anchoring in Purpose section ---
echo "--- Pattern 4: Role/identity anchoring ---"
for agent in "${AGENTS[@]}"; do
    AGENT_FILE="$PROJECT_ROOT/src/claude/agents/${agent}.md"
    if [ -f "$AGENT_FILE" ]; then
        if grep -qi "you are a\|identity.*statement\|role.*anchor" "$AGENT_FILE" 2>/dev/null; then
            run_test "${agent} has role/identity anchoring" 0
        else
            run_test "${agent} has role/identity anchoring" 1
        fi
    else
        run_test "${agent} has role/identity anchoring (file missing)" 1
    fi
done
echo ""

# --- Pattern 5: DO/DO NOT constraint lists in Constraints section ---
echo "--- Pattern 5: DO/DO NOT constraints ---"
for agent in "${AGENTS[@]}"; do
    AGENT_FILE="$PROJECT_ROOT/src/claude/agents/${agent}.md"
    if [ -f "$AGENT_FILE" ]; then
        HAS_DO=$(grep -c '^\*\*DO:\*\*\|^\*\*DO\*\*\|^DO:' "$AGENT_FILE" 2>/dev/null || echo 0)
        HAS_DONOT=$(grep -c '^\*\*DO NOT:\*\*\|^\*\*DO NOT\*\*\|^DO NOT:' "$AGENT_FILE" 2>/dev/null || echo 0)
        if [ "$HAS_DO" -gt 0 ] && [ "$HAS_DONOT" -gt 0 ]; then
            run_test "${agent} has DO/DO NOT constraint lists" 0
        else
            run_test "${agent} has DO/DO NOT constraint lists" 1
        fi
    else
        run_test "${agent} has DO/DO NOT constraint lists (file missing)" 1
    fi
done
echo ""

# === Summary ===
echo "============================================"
echo "AC#2 Results: $PASSED passed, $FAILED failed"
echo "============================================"
if [ "$FAILED" -eq 0 ]; then exit 0; else exit 1; fi
