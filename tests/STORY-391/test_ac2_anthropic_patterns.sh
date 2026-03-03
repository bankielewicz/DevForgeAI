#!/usr/bin/env bash
# =============================================================================
# STORY-391 AC#2: Anthropic Prompt Engineering Patterns Applied
#
# Verifies the updated src/claude/agents/test-automator.md contains:
# 1. Chain-of-thought reasoning in Workflow section
# 2. Structured output in Output Format section
# 3. At least 2 worked examples in Examples section
# 4. Role/identity anchoring in Purpose section
# 5. Explicit DO/DO NOT constraint lists in Constraints and Boundaries section
#
# TDD Phase: RED (these tests must FAIL before implementation)
# =============================================================================

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
AGENT_FILE="${PROJECT_ROOT}/src/claude/agents/test-automator.md"

PASS_COUNT=0
FAIL_COUNT=0
TOTAL_TESTS=0

# --- Test Helper ---
run_test() {
    local test_name="$1"
    local test_result="$2"

    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    if [ "$test_result" -eq 0 ]; then
        PASS_COUNT=$((PASS_COUNT + 1))
        echo "  PASS: ${test_name}"
    else
        FAIL_COUNT=$((FAIL_COUNT + 1))
        echo "  FAIL: ${test_name}"
    fi
}

echo "================================================================"
echo "STORY-391 AC#2: Anthropic Prompt Engineering Patterns Tests"
echo "Target: ${AGENT_FILE}"
echo "================================================================"
echo ""

# --- Pre-check: File exists ---
if [ ! -f "$AGENT_FILE" ]; then
    echo "FATAL: Agent file not found at ${AGENT_FILE}"
    exit 1
fi

# =============================================================================
# Pattern 1: Chain-of-thought in Workflow section
# =============================================================================
echo "--- Pattern 1: Chain-of-thought in Workflow ---"

# Extract content between ## Workflow and the next ## heading
WORKFLOW_CONTENT=$(sed -n '/^## Workflow/,/^## [A-Z]/p' "$AGENT_FILE" | head -n -1)

# Chain-of-thought indicators: reasoning steps, think/analyze/determine language
COT_REASONING=$(echo "$WORKFLOW_CONTENT" | grep -ciE 'reason|think|analyze|determine|consider|evaluate|assess|decide|step.*reason|reasoning' || true)
run_test "Chain-of-thought: reasoning instruction phrases in Workflow (found: ${COT_REASONING})" "$( [ "$COT_REASONING" -ge 2 ] && echo 0 || echo 1 )"

# Explicit reasoning steps (numbered or bulleted with reasoning verbs)
COT_STEPS=$(echo "$WORKFLOW_CONTENT" | grep -cE '^\s*[0-9]+\.' || true)
run_test "Chain-of-thought: at least 3 numbered reasoning steps in Workflow (found: ${COT_STEPS})" "$( [ "$COT_STEPS" -ge 3 ] && echo 0 || echo 1 )"

# =============================================================================
# Pattern 2: Structured output in Output Format section
# =============================================================================
echo ""
echo "--- Pattern 2: Structured output in Output Format ---"

# Check Output Format section exists
HAS_OUTPUT_FORMAT=$(grep -c '^## Output Format' "$AGENT_FILE" || true)
run_test "Output Format section exists" "$( [ "$HAS_OUTPUT_FORMAT" -ge 1 ] && echo 0 || echo 1 )"

# Extract Output Format content
OUTPUT_FORMAT_CONTENT=$(sed -n '/^## Output Format/,/^## [A-Z]/p' "$AGENT_FILE" | head -n -1)

# Structured output indicators: code block with template, field names, format definition
HAS_CODE_BLOCK=$(echo "$OUTPUT_FORMAT_CONTENT" | grep -c '```' || true)
run_test "Output Format contains code block with template (found: ${HAS_CODE_BLOCK})" "$( [ "$HAS_CODE_BLOCK" -ge 2 ] && echo 0 || echo 1 )"

# Check for specific repeatable structure (field names, headers, or JSON/YAML/Markdown template)
HAS_STRUCTURED_FIELDS=$(echo "$OUTPUT_FORMAT_CONTENT" | grep -ciE 'status|format|section|field|template|structure' || true)
run_test "Output Format defines structured fields (found: ${HAS_STRUCTURED_FIELDS})" "$( [ "$HAS_STRUCTURED_FIELDS" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Pattern 3: At least 2 worked examples in Examples section
# =============================================================================
echo ""
echo "--- Pattern 3: Worked examples in Examples section ---"

# Check Examples section exists
HAS_EXAMPLES=$(grep -c '^## Examples' "$AGENT_FILE" || true)
run_test "Examples section exists" "$( [ "$HAS_EXAMPLES" -ge 1 ] && echo 0 || echo 1 )"

# Extract Examples content
EXAMPLES_CONTENT=$(sed -n '/^## Examples/,/^## [A-Z]/p' "$AGENT_FILE" | head -n -1)

# Count worked examples (### Example N: or similar heading patterns)
EXAMPLE_COUNT=$(echo "$EXAMPLES_CONTENT" | grep -cE '^### Example [0-9]' || true)
run_test "At least 2 worked examples present (found: ${EXAMPLE_COUNT})" "$( [ "$EXAMPLE_COUNT" -ge 2 ] && echo 0 || echo 1 )"

# Verify examples contain Task() invocations
TASK_IN_EXAMPLES=$(echo "$EXAMPLES_CONTENT" | grep -c 'Task(' || true)
run_test "Examples contain Task() invocation patterns (found: ${TASK_IN_EXAMPLES})" "$( [ "$TASK_IN_EXAMPLES" -ge 2 ] && echo 0 || echo 1 )"

# Verify examples show expected behavior/output
EXPECTED_IN_EXAMPLES=$(echo "$EXAMPLES_CONTENT" | grep -ciE 'expected|behavior|output|result|produces|returns|generates' || true)
run_test "Examples describe expected behavior/output (found: ${EXPECTED_IN_EXAMPLES})" "$( [ "$EXPECTED_IN_EXAMPLES" -ge 2 ] && echo 0 || echo 1 )"

# =============================================================================
# Pattern 4: Role/identity anchoring in Purpose section
# =============================================================================
echo ""
echo "--- Pattern 4: Role/identity anchoring in Purpose ---"

# Extract Purpose content
PURPOSE_CONTENT=$(sed -n '/^## Purpose/,/^## [A-Z]/p' "$AGENT_FILE" | head -n -1)

# Check for "You are" identity anchoring
HAS_YOU_ARE=$(echo "$PURPOSE_CONTENT" | grep -c 'You are' || true)
run_test "Purpose contains 'You are' identity anchoring (found: ${HAS_YOU_ARE})" "$( [ "$HAS_YOU_ARE" -ge 1 ] && echo 0 || echo 1 )"

# Check for specialization/expertise language
HAS_SPECIALIZATION=$(echo "$PURPOSE_CONTENT" | grep -ciE 'specializ|expert|responsible for|focus' || true)
run_test "Purpose describes specialization/expertise (found: ${HAS_SPECIALIZATION})" "$( [ "$HAS_SPECIALIZATION" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Pattern 5: DO/DO NOT constraint lists in Constraints and Boundaries
# =============================================================================
echo ""
echo "--- Pattern 5: DO/DO NOT constraints ---"

# Check Constraints section exists
HAS_CONSTRAINTS=$(grep -c '^## Constraints and Boundaries' "$AGENT_FILE" || true)
run_test "Constraints and Boundaries section exists" "$( [ "$HAS_CONSTRAINTS" -ge 1 ] && echo 0 || echo 1 )"

# Extract Constraints content
CONSTRAINTS_CONTENT=$(sed -n '/^## Constraints and Boundaries/,/^## [A-Z]/p' "$AGENT_FILE" | head -n -1)

# Check for DO items (positive instructions)
DO_ITEMS=$(echo "$CONSTRAINTS_CONTENT" | grep -cE '^\s*-\s+DO\b' || true)
# Also check for "DO:" heading or bold DO
DO_HEADING=$(echo "$CONSTRAINTS_CONTENT" | grep -ciE '\*\*DO\b|^DO:' || true)
DO_TOTAL=$((DO_ITEMS + DO_HEADING))
run_test "Constraints contain DO list/items (found: ${DO_TOTAL})" "$( [ "$DO_TOTAL" -ge 1 ] && echo 0 || echo 1 )"

# Check for DO NOT items (prohibitions)
DO_NOT_ITEMS=$(echo "$CONSTRAINTS_CONTENT" | grep -cE 'DO NOT|NEVER|MUST NOT' || true)
run_test "Constraints contain DO NOT/NEVER items (found: ${DO_NOT_ITEMS})" "$( [ "$DO_NOT_ITEMS" -ge 1 ] && echo 0 || echo 1 )"

# Verify at least 3 constraint statements total (per canonical template)
CONSTRAINT_BULLETS=$(echo "$CONSTRAINTS_CONTENT" | grep -cE '^\s*-\s+' || true)
run_test "Constraints contain at least 3 constraint statements (found: ${CONSTRAINT_BULLETS})" "$( [ "$CONSTRAINT_BULLETS" -ge 3 ] && echo 0 || echo 1 )"

# =============================================================================
# Pattern Traceability: Each pattern traceable to specific section
# =============================================================================
echo ""
echo "--- Pattern Traceability ---"

# Verify each pattern exists within its expected section (not just anywhere in file)
# This ensures patterns are properly placed, not scattered

# Chain-of-thought MUST be in Workflow
COT_IN_WORKFLOW=$(echo "$WORKFLOW_CONTENT" | grep -ciE 'reason|think|analyze|determine' || true)
run_test "Chain-of-thought is within Workflow section (not elsewhere)" "$( [ "$COT_IN_WORKFLOW" -ge 1 ] && echo 0 || echo 1 )"

# Identity anchoring MUST be in Purpose
IDENTITY_IN_PURPOSE=$(echo "$PURPOSE_CONTENT" | grep -c 'You are' || true)
run_test "Identity anchoring is within Purpose section (not elsewhere)" "$( [ "$IDENTITY_IN_PURPOSE" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Summary
# =============================================================================
echo ""
echo "================================================================"
echo "AC#2 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed out of ${TOTAL_TESTS} tests"
echo "================================================================"

if [ "$FAIL_COUNT" -gt 0 ]; then
    exit 1
else
    exit 0
fi
