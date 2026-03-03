#!/bin/bash
# Test: AC#2 - Anthropic Prompt Engineering Patterns Applied to All 10 Agents
# Story: STORY-395
# Generated: 2026-02-13
# TDD Phase: RED (tests expected to FAIL before migration)
#
# Validates that each of the 10 agents contains the 5 Anthropic prompt
# engineering patterns: chain-of-thought, structured output, worked examples,
# role/identity anchoring, and DO/DO NOT constraints.

set -uo pipefail

# === Test Configuration ===
PASSED=0
FAILED=0
TOTAL=0
PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$(dirname "$0")/../.." && pwd)}"
AGENTS_DIR="$PROJECT_ROOT/src/claude/agents"

AGENTS=(
    "anti-pattern-scanner"
    "context-validator"
    "context-preservation-validator"
    "coverage-analyzer"
    "code-quality-auditor"
    "deferral-validator"
    "dependency-graph-analyzer"
    "file-overlap-detector"
    "pattern-compliance-auditor"
    "tech-stack-detector"
)

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

echo "=============================================="
echo "  AC#2: Anthropic Prompt Engineering Patterns"
echo "  Testing 10 agents x 5 patterns"
echo "=============================================="
echo ""

# --- Pattern 1: Chain-of-thought reasoning in Workflow section ---
echo "--- Pattern 1: Chain-of-Thought in Workflow ---"
for agent in "${AGENTS[@]}"; do
    AGENT_FILE="$AGENTS_DIR/${agent}.md"
    if [ ! -f "$AGENT_FILE" ]; then
        run_test "Chain-of-thought: ${agent} (file missing)" 1
        continue
    fi

    # Extract Workflow section and check for reasoning/step-by-step indicators
    WORKFLOW_CONTENT=$(sed -n '/^## Workflow/,/^## /p' "$AGENT_FILE" | head -n -1)
    if [ -z "$WORKFLOW_CONTENT" ]; then
        run_test "Chain-of-thought (Workflow section exists): ${agent}" 1
        continue
    fi

    # Check for explicit reasoning markers within Workflow section
    echo "$WORKFLOW_CONTENT" | grep -qiE "(Reasoning:|reasoning\b|step-by-step|explicit.*(reason|think)|think through)" && RC=0 || RC=1
    run_test "Chain-of-thought reasoning in Workflow: ${agent}" $RC
done
echo ""

# --- Pattern 2: Structured output in Output Format section ---
echo "--- Pattern 2: Structured Output in Output Format ---"
for agent in "${AGENTS[@]}"; do
    AGENT_FILE="$AGENTS_DIR/${agent}.md"
    if [ ! -f "$AGENT_FILE" ]; then
        run_test "Structured output: ${agent} (file missing)" 1
        continue
    fi

    # Check for Output Format section existence
    grep -q "^## Output Format" "$AGENT_FILE" && RC=0 || RC=1
    run_test "Output Format section exists: ${agent}" $RC

    # Extract Output Format section and check for structured format definition
    OUTPUT_CONTENT=$(sed -n '/^## Output Format/,/^## /p' "$AGENT_FILE" | head -n -1)
    if [ -z "$OUTPUT_CONTENT" ]; then
        run_test "Structured format defined: ${agent}" 1
        continue
    fi

    # Check for JSON schema, Markdown template, or structured report markers
    echo "$OUTPUT_CONTENT" | grep -qiE '(json|schema|template|structured|format|```)' && RC=0 || RC=1
    run_test "Structured format defined in Output Format: ${agent}" $RC
done
echo ""

# --- Pattern 3: Worked example in Examples section ---
echo "--- Pattern 3: Worked Example in Examples ---"
for agent in "${AGENTS[@]}"; do
    AGENT_FILE="$AGENTS_DIR/${agent}.md"
    if [ ! -f "$AGENT_FILE" ]; then
        run_test "Worked example: ${agent} (file missing)" 1
        continue
    fi

    # Check for Examples section existence
    grep -q "^## Examples" "$AGENT_FILE" && RC=0 || RC=1
    run_test "Examples section exists: ${agent}" $RC

    # Extract Examples section and check for Task() invocation pattern
    EXAMPLES_CONTENT=$(sed -n '/^## Examples/,/^## /p' "$AGENT_FILE" | head -n -1)
    if [ -z "$EXAMPLES_CONTENT" ]; then
        run_test "Task() pattern in Examples: ${agent}" 1
        continue
    fi

    # Check for Task() invocation pattern showing usage
    echo "$EXAMPLES_CONTENT" | grep -qE 'Task\(' && RC=0 || RC=1
    run_test "Task() invocation example: ${agent}" $RC
done
echo ""

# --- Pattern 4: Role/identity anchoring in Purpose section ---
echo "--- Pattern 4: Role/Identity Anchoring in Purpose ---"
for agent in "${AGENTS[@]}"; do
    AGENT_FILE="$AGENTS_DIR/${agent}.md"
    if [ ! -f "$AGENT_FILE" ]; then
        run_test "Identity anchoring: ${agent} (file missing)" 1
        continue
    fi

    # Check for Purpose section existence (exact canonical name)
    grep -q "^## Purpose$" "$AGENT_FILE" && RC=0 || RC=1
    run_test "Purpose section exists (canonical name): ${agent}" $RC

    # Extract Purpose section and check for identity statement
    PURPOSE_CONTENT=$(sed -n '/^## Purpose$/,/^## /p' "$AGENT_FILE" | head -n -1)
    if [ -z "$PURPOSE_CONTENT" ]; then
        run_test "Identity statement in Purpose: ${agent}" 1
        continue
    fi

    # Check for identity anchoring language
    echo "$PURPOSE_CONTENT" | grep -qiE '(You are|specialist|expert|responsible for|your role)' && RC=0 || RC=1
    run_test "Identity anchoring statement: ${agent}" $RC
done
echo ""

# --- Pattern 5: DO/DO NOT constraints in Constraints section ---
echo "--- Pattern 5: DO/DO NOT in Constraints and Boundaries ---"
for agent in "${AGENTS[@]}"; do
    AGENT_FILE="$AGENTS_DIR/${agent}.md"
    if [ ! -f "$AGENT_FILE" ]; then
        run_test "DO/DO NOT constraints: ${agent} (file missing)" 1
        continue
    fi

    # Check for Constraints and Boundaries section
    grep -q "^## Constraints and Boundaries" "$AGENT_FILE" && RC=0 || RC=1
    run_test "Constraints and Boundaries section exists: ${agent}" $RC

    # Extract section and check for DO/DO NOT pattern
    CONSTRAINTS_CONTENT=$(sed -n '/^## Constraints and Boundaries/,/^## /p' "$AGENT_FILE" | head -n -1)
    if [ -z "$CONSTRAINTS_CONTENT" ]; then
        run_test "DO list present: ${agent}" 1
        run_test "DO NOT list present: ${agent}" 1
        continue
    fi

    # Check for explicit DO list
    echo "$CONSTRAINTS_CONTENT" | grep -qE '\*\*DO[:]*\*\*|^DO:' && RC=0 || RC=1
    run_test "DO list present: ${agent}" $RC

    # Check for explicit DO NOT list
    echo "$CONSTRAINTS_CONTENT" | grep -qiE '\*\*DO NOT[:]*\*\*|^DO NOT:' && RC=0 || RC=1
    run_test "DO NOT list present: ${agent}" $RC
done
echo ""

# === Summary ===
echo "=============================================="
echo "  AC#2 Anthropic Patterns Results"
echo "=============================================="
echo "  Total:  $TOTAL"
echo "  Passed: $PASSED"
echo "  Failed: $FAILED"
echo "=============================================="

if [ "$FAILED" -eq 0 ]; then
    echo "  STATUS: ALL TESTS PASSED"
    exit 0
else
    echo "  STATUS: $FAILED TESTS FAILED"
    exit 1
fi
